import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

KIT = Path(__file__).resolve().parent.parent / "aqef-kit"
sys.path.insert(0, str(KIT / "bots"))
from gatekeeper import decide, in_audit_sample  # noqa: E402

CONFIG = yaml.safe_load((KIT / ".aqef" / "config.yaml").read_text(encoding="utf-8"))
EXAMPLE = json.loads((KIT / "bots" / "example-metrics.json").read_text(encoding="utf-8"))
T1_GREEN = {"tier": "t1", "mutation_score": 0.9, "seeded_fault_detection": 0.99,
            "nfr_results": {"security": "pass", "performance": "pass", "accessibility": "pass"}}


def metrics(**overrides):
    m = copy.deepcopy(EXAMPLE)
    m.update(overrides)
    return m


def without(*keys, **overrides):
    m = metrics(**overrides)
    for key in keys:
        m.pop(key)
    return m


def config(**tier_overrides):
    """Live config with overrides on tier t2 (keeps tests independent of shipped defaults)."""
    c = copy.deepcopy(CONFIG)
    c["tiers"]["t2"].update(tier_overrides)
    return c


# --- Decisions ---------------------------------------------------------------

def test_example_t2_passes():
    res = decide(CONFIG, metrics())
    assert (res["decision"], res["exit_code"]) == ("PASS", 0)
    assert res["reasons"] == [] and res["advisories"] == []


def test_t1_always_needs_h3_even_when_all_pass():
    res = decide(CONFIG, metrics(**T1_GREEN))
    assert (res["decision"], res["exit_code"]) == ("ESCALATE", 2)
    assert res["reasons"] == ["tier t1 requires human gate H3"]
    assert res["gates"] == ["H3"]


def test_t1_escalation_blocks_and_lists_the_reason():
    res = decide(CONFIG, metrics(**{**T1_GREEN, "mutation_score": 0.5}))
    assert (res["decision"], res["exit_code"]) == ("ESCALATE", 2)
    assert "mutation score: 0.50 is below 0.80" in res["reasons"]


def test_t2_escalation_is_a_non_blocking_follow_up():
    res = decide(CONFIG, metrics(mutation_score=0.5))
    assert (res["decision"], res["exit_code"]) == ("FOLLOW_UP", 0)
    assert res["gates"] == ["H3"]
    assert "mutation score: 0.50 is below 0.70" in res["reasons"]


def test_t3_escalation_is_only_a_comment():
    res = decide(CONFIG, metrics(tier="t3", feature="NOT-SAMPLED-1", panel_result="ESCALATE"))
    assert (res["decision"], res["exit_code"]) == ("PASS", 0)
    assert "review panel result is ESCALATE" in res["advisories"]


def test_on_escalate_block_makes_t2_wait_for_a_human():
    res = decide(config(on_escalate="block"), metrics(mutation_score=0.5))
    assert (res["decision"], res["exit_code"]) == ("ESCALATE", 2)


def test_always_required_h3_blocks_even_if_on_escalate_is_relaxed():
    c = config(human_gates=["H1", "H3", "H4"], on_escalate="follow_up")
    res = decide(c, metrics(mutation_score=0.5))
    assert (res["decision"], res["exit_code"]) == ("ESCALATE", 2)
    assert res["gates"] == ["H3"]


def test_t3_ignores_mutation_thresholds():
    res = decide(CONFIG, metrics(tier="t3", feature="NOT-SAMPLED-1", mutation_score=0.1, seeded_fault_detection=0.1))
    assert res["decision"] == "PASS" and res["advisories"] == []


# --- Fail closed: missing data never passes ----------------------------------

@pytest.mark.parametrize("key", CONFIG["gate"]["required_metrics"])
def test_missing_required_metric_fails(key):
    res = decide(CONFIG, without(key))
    assert (res["decision"], res["exit_code"]) == ("FAIL", 1)
    assert f"required metric missing: {key}" in res["reasons"]


def test_only_tier_reported_fails_on_every_required_metric():
    res = decide(CONFIG, {"schema_version": 1, "feature": "X", "tier": "t3"})
    assert res["decision"] == "FAIL"
    assert len(res["reasons"]) == len(CONFIG["gate"]["required_metrics"])


@pytest.mark.parametrize("key", CONFIG["gate"]["advisory_metrics"])
def test_missing_advisory_metric_is_reported_but_does_not_block(key):
    res = decide(CONFIG, without(key))
    assert res["decision"] == "PASS"
    assert f"{key}: not reported" in res["advisories"]


def test_missing_mutation_score_escalates_where_the_tier_requires_it():
    res = decide(CONFIG, without("mutation_score"))
    assert res["decision"] == "FOLLOW_UP"
    assert "mutation score: no value, minimum is 0.70" in res["reasons"]


# --- Facts that block ---------------------------------------------------------

@pytest.mark.parametrize("override, reason", [
    ({"test_guard_violations": 1}, "test guard violations: 1"),
    ({"new_product_defects": 2}, "new product defects open: 2"),
    ({"data_guard_violations": 1}, "secrets or personal data in tests: 1"),
    ({"red_before_green_all": False}, "red-before-green evidence missing for one or more tests"),
    ({"criteria_coverage": 0.9}, "criteria coverage: 0.90 is below 1.00"),
])
@pytest.mark.parametrize("tier", ["t1", "t2", "t3"])
def test_facts_fail_in_every_tier(override, reason, tier):
    if tier == "t3" and "criteria_coverage" in override:
        override = {"criteria_coverage": 0.9}
        reason = "criteria coverage: 0.90 is below 0.95"
    res = decide(CONFIG, metrics(tier=tier, **override))
    assert (res["decision"], res["exit_code"]) == ("FAIL", 1)
    assert reason in res["reasons"]


def test_fail_wins_over_escalate():
    assert decide(CONFIG, metrics(test_guard_violations=1, panel_result="ESCALATE"))["decision"] == "FAIL"


def test_waived_test_guard_violations_need_a_human():
    res = decide(CONFIG, metrics(test_guard_waived=2))
    assert res["decision"] == "FOLLOW_UP"
    assert any("waived: 2" in r for r in res["reasons"])


def test_unknown_tier_fails_cleanly():
    res = decide(CONFIG, metrics(tier="t9"))
    assert (res["decision"], res["exit_code"]) == ("FAIL", 1)
    assert "unknown or missing tier" in res["reasons"][0]


# --- Thresholds: equal passes, just past escalates ----------------------------

@pytest.mark.parametrize("override, decision", [
    ({"mutation_score": 0.70}, "PASS"),
    ({"mutation_score": 0.69}, "FOLLOW_UP"),
    ({"seeded_fault_detection": 0.90}, "PASS"),
    ({"seeded_fault_detection": 0.89}, "FOLLOW_UP"),
    ({"ui_share": 0.10}, "PASS"),
    ({"ui_share": 0.11}, "FOLLOW_UP"),
    ({"flake_rate": 0.01}, "PASS"),
    ({"flake_rate": 0.011}, "FOLLOW_UP"),
    ({"test_quality_score": 80}, "PASS"),
    ({"test_quality_score": 79}, "FOLLOW_UP"),
    ({"criteria_coverage": 1.0}, "PASS"),
    ({"criteria_coverage": 0.99}, "FAIL"),
])
def test_threshold_boundaries(override, decision):
    assert decide(CONFIG, metrics(**override))["decision"] == decision


def test_nfr_missing_or_failed_escalates():
    res = decide(CONFIG, metrics(nfr_results={"security": "fail"}))
    assert "NFR security: result is fail" in res["reasons"]
    res = decide(CONFIG, metrics(nfr_results={}))
    assert "NFR security: no result, tier t2 requires it" in res["reasons"]


# --- T3 audit sample ------------------------------------------------------------

def test_audit_sample_is_stable_and_respects_the_rate():
    features = [f"SPEC-{n}" for n in range(2000)]
    picked = [f for f in features if in_audit_sample(f, 0.10)]
    assert 0.07 < len(picked) / len(features) < 0.13
    assert picked == [f for f in features if in_audit_sample(f, 0.10)]
    assert not any(in_audit_sample(f, 0) for f in features[:50])
    assert all(in_audit_sample(f, 1.0) for f in features[:50])


def test_sampled_t3_feature_gets_a_follow_up_audit():
    sampled = next(f"SPEC-{n}" for n in range(1000) if in_audit_sample(f"SPEC-{n}", 0.10))
    res = decide(CONFIG, metrics(tier="t3", feature=sampled))
    assert (res["decision"], res["exit_code"]) == ("FOLLOW_UP", 0)
    assert res["gates"] == ["H3"]


# --- CLI ----------------------------------------------------------------------

def cli(tmp_path, data, *extra, config_path=None):
    metrics_path = tmp_path / "metrics.json"
    metrics_path.write_text(data if isinstance(data, str) else json.dumps(data), encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(KIT / "bots" / "gatekeeper.py"),
         "--config", str(config_path or KIT / ".aqef" / "config.yaml"), "--metrics", str(metrics_path), *extra],
        capture_output=True, text=True)


@pytest.mark.parametrize("data, code", [
    (metrics(), 0),
    (metrics(mutation_score=0.5), 0),
    (metrics(test_guard_violations=1), 1),
    (metrics(**T1_GREEN), 2),
])
def test_cli_exit_codes(tmp_path, data, code):
    assert cli(tmp_path, data).returncode == code


def test_cli_json_output(tmp_path):
    proc = cli(tmp_path, metrics(mutation_score=0.5), "--json")
    out = json.loads(proc.stdout)
    assert out["decision"] == "FOLLOW_UP" and out["gates"] == ["H3"]


@pytest.mark.parametrize("data", [
    "{not json",
    json.dumps(metrics(criteria_coverage="1.0")),
    json.dumps(metrics(mutaton_score=0.9)),
    json.dumps(without("schema_version")),
])
def test_cli_bad_metrics_is_an_input_error(tmp_path, data):
    proc = cli(tmp_path, data)
    assert proc.returncode == 3, proc.stdout
    assert "ERROR" in proc.stdout


def test_cli_unknown_config_version_is_an_input_error(tmp_path):
    bad = copy.deepcopy(CONFIG)
    bad["config_version"] = 1
    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump(bad), encoding="utf-8")
    proc = cli(tmp_path, metrics(), config_path=path)
    assert proc.returncode == 3 and "config_version" in proc.stdout


def test_cli_missing_file_is_an_input_error(tmp_path):
    proc = subprocess.run([sys.executable, str(KIT / "bots" / "gatekeeper.py"),
                           "--config", str(KIT / ".aqef" / "config.yaml"), "--metrics", str(tmp_path / "none.json")],
                          capture_output=True, text=True)
    assert proc.returncode == 3 and "cannot read" in proc.stdout
