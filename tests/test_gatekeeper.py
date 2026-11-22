import json
import sys
from pathlib import Path

import pytest
import yaml

KIT = Path(__file__).resolve().parent.parent / "aqef-kit"
sys.path.insert(0, str(KIT / "bots"))
from gatekeeper import decide  # noqa: E402

CONFIG = yaml.safe_load((KIT / ".aqef" / "config.yaml").read_text(encoding="utf-8"))
EXAMPLE = json.loads((KIT / "bots" / "example-metrics.json").read_text(encoding="utf-8"))


def metrics(**overrides):
    m = dict(EXAMPLE)
    m.update(overrides)
    return m


def test_example_t2_passes():
    assert decide(CONFIG, metrics())[0] == "PASS"


def test_t3_ignores_mutation_thresholds():
    assert decide(CONFIG, metrics(tier="t3", mutation_score=0.1, seeded_fault_detection=0.1))[0] == "PASS"


def test_t1_always_needs_h3_even_when_all_pass():
    m = metrics(tier="t1", mutation_score=0.9, seeded_fault_detection=0.99,
                nfr_results={"security": "pass", "performance": "pass", "accessibility": "pass"})
    decision, reasons, code = decide(CONFIG, m)
    assert (decision, code) == ("ESCALATE", 2)
    assert reasons == ["tier t1 requires human gate H3"]


def test_t1_missing_nfr_escalates():
    m = metrics(tier="t1", mutation_score=0.9, seeded_fault_detection=0.99)
    _, reasons, _ = decide(CONFIG, m)
    assert any("NFR performance: no result" in r for r in reasons)


def test_failed_nfr_escalates():
    _, reasons, code = decide(CONFIG, metrics(nfr_results={"security": "fail"}))
    assert code == 2 and "NFR security: result is fail" in reasons


@pytest.mark.parametrize("override, reason", [
    ({"test_guard_violations": 1}, "test guard violations: 1"),
    ({"new_product_defects": 2}, "new product defects open: 2"),
    ({"red_before_green_all": False}, "red-before-green evidence missing for one or more tests"),
    ({"criteria_coverage": 0.9}, "criteria coverage: 0.90 is below 1.00"),
])
def test_hard_failures(override, reason):
    decision, reasons, code = decide(CONFIG, metrics(**override))
    assert (decision, code) == ("FAIL", 1)
    assert reason in reasons


def test_fail_wins_over_escalate():
    assert decide(CONFIG, metrics(test_guard_violations=1, panel_result="ESCALATE"))[0] == "FAIL"


@pytest.mark.parametrize("override", [
    {"mutation_score": 0.69},
    {"ui_share": 0.11},
    {"flake_rate": 0.02},
    {"panel_result": "ESCALATE"},
    {"test_quality_score": 79},
])
def test_threshold_misses_escalate(override):
    assert decide(CONFIG, metrics(**override))[0] == "ESCALATE"


def test_unknown_tier_fails_cleanly():
    decision, reasons, code = decide(CONFIG, metrics(tier="t9"))
    assert (decision, code) == ("FAIL", 1)
    assert "unknown or missing tier" in reasons[0]
