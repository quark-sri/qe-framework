#!/usr/bin/env python3
"""AQEF Quality Gatekeeper.

Reads .aqef/config.yaml and a metrics JSON file for one feature or PR, and decides.

Blocking budget (framework decision AQEF-002): only facts block a merge. Everything else is an escalation,
and the tier's `on_escalate` setting decides whether an escalation blocks, opens a
follow-up task, or is only a comment.

Decisions and exit codes:
  PASS       0  merge; `advisories` may hold comments
  FOLLOW_UP  0  merge; CI opens a follow-up task for the gates in `gates`
  FAIL       1  do not merge
  ESCALATE   2  the merge waits for a human gate (listed in `gates`)
  ERROR      3  bad input: missing file, invalid YAML/JSON, schema violation

A missing required metric is a FAIL, never a PASS: a broken bot must not let bugs through.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

SCHEMAS = Path(__file__).resolve().parent.parent / "schemas"
MERGE_GATES = ("H3",)  # the human gate that sits in the merge path


class InputError(Exception):
    """The config or metrics file cannot be used."""


def in_audit_sample(feature, rate):
    """Pick a stable sample: the same feature ID always gives the same answer."""
    if not rate:
        return False
    bucket = int(hashlib.sha256(feature.encode("utf-8")).hexdigest()[:8], 16) / 0xFFFFFFFF
    return bucket < rate


def result(decision, code, metrics, reasons=(), advisories=(), gates=()):
    return {
        "decision": decision,
        "exit_code": code,
        "feature": metrics.get("feature"),
        "tier": metrics.get("tier"),
        "reasons": list(reasons),
        "advisories": list(advisories),
        "gates": list(gates),
    }


def decide(config, metrics):
    tier = metrics.get("tier")
    tiers = config.get("tiers", {})
    if tier not in tiers:
        return result("FAIL", 1, metrics, [f"unknown or missing tier: {tier!r}"])
    tier_cfg = tiers[tier]
    rules = config.get("suite_rules", {})
    gate_cfg = config.get("gate", {})
    fail, escalate, advise = [], [], []

    # Required metrics: missing means a bot did not report. That is a FAIL.
    missing = {name for name in gate_cfg.get("required_metrics", []) if metrics.get(name) is None}
    fail.extend(f"required metric missing: {name}" for name in sorted(missing))
    for name in gate_cfg.get("advisory_metrics", []):
        if metrics.get(name) is None:
            advise.append(f"{name}: not reported")

    def below(bucket, name, key, minimum):
        value = metrics.get(key)
        if minimum is None or key in missing:
            return
        if value is None:
            bucket.append(f"{name}: no value, minimum is {minimum:.2f}")
        elif value < minimum:
            bucket.append(f"{name}: {value:.2f} is below {minimum:.2f}")

    def count(key):
        return metrics.get(key) or 0

    # Facts: these block in every tier.
    if count("new_product_defects") > 0:
        fail.append(f"new product defects open: {metrics['new_product_defects']}")
    if count("test_guard_violations") > 0:
        fail.append(f"test guard violations: {metrics['test_guard_violations']}")
    if count("data_guard_violations") > 0:
        fail.append(f"secrets or personal data in tests: {metrics['data_guard_violations']}")
    if rules.get("red_before_green_required") and "red_before_green_all" not in missing \
            and metrics.get("red_before_green_all") is not True:
        fail.append("red-before-green evidence missing for one or more tests")
    below(fail, "criteria coverage", "criteria_coverage", tier_cfg.get("criteria_coverage_min"))

    # Escalations: a human decides. on_escalate routes them.
    below(escalate, "mutation score", "mutation_score", tier_cfg.get("mutation_score_min"))
    below(escalate, "seeded fault detection", "seeded_fault_detection", tier_cfg.get("seeded_fault_detection_min"))
    if metrics.get("ui_share") is not None and "ui_share_max" in rules and metrics["ui_share"] > rules["ui_share_max"]:
        escalate.append(f"UI share {metrics['ui_share']:.2f} is above {rules['ui_share_max']:.2f}")
    if metrics.get("flake_rate") is not None and "gating_flake_rate_max" in rules \
            and metrics["flake_rate"] > rules["gating_flake_rate_max"]:
        escalate.append(f"flake rate {metrics['flake_rate']:.3f} is above {rules['gating_flake_rate_max']:.3f}")
    nfr_results = metrics.get("nfr_results") or {}
    for nfr in tier_cfg.get("nfr_required") or []:
        outcome = nfr_results.get(nfr)
        if outcome is None:
            escalate.append(f"NFR {nfr}: no result, tier {tier} requires it")
        elif outcome != "pass":
            escalate.append(f"NFR {nfr}: result is {outcome}")
    if metrics.get("panel_result") == "ESCALATE":
        escalate.append("review panel result is ESCALATE")
    score_min = config.get("review_panel", {}).get("accept_score_min")
    if score_min is not None and metrics.get("test_quality_score") is not None \
            and metrics["test_quality_score"] < score_min:
        escalate.append(f"test quality score {metrics['test_quality_score']} is below {score_min}")
    if count("test_guard_waived") > 0:
        escalate.append(f"test guard violations waived: {metrics['test_guard_waived']}; a human confirms the waivers")

    if fail:
        return result("FAIL", 1, metrics, fail, advise)

    always = [g for g in tier_cfg.get("human_gates", []) if g in MERGE_GATES]
    on_escalate = tier_cfg.get("on_escalate", "block")
    if escalate:
        gates = always or [g for g in tier_cfg.get("escalate_gates", MERGE_GATES) if g in MERGE_GATES] or list(MERGE_GATES)
        if always or on_escalate == "block":
            return result("ESCALATE", 2, metrics, escalate, advise, gates)
        if on_escalate == "follow_up":
            return result("FOLLOW_UP", 0, metrics, escalate, advise, gates)
        advise.extend(escalate)  # on_escalate == "comment"

    if always:
        return result("ESCALATE", 2, metrics, [f"tier {tier} requires human gate {', '.join(always)}"], advise, always)
    if in_audit_sample(str(metrics.get("feature", "")), tier_cfg.get("sample_audit_rate")):
        gates = [g for g in tier_cfg.get("escalate_gates", MERGE_GATES) if g in MERGE_GATES] or list(MERGE_GATES)
        return result("FOLLOW_UP", 0, metrics, [f"selected for the tier {tier} audit sample"], advise, gates)
    return result("PASS", 0, metrics, [], advise)


def load(path, parser):
    try:
        with open(path, encoding="utf-8") as f:
            return parser(f)
    except OSError as exc:
        raise InputError(f"cannot read {path}: {exc.strerror}") from exc
    except ValueError as exc:  # json.JSONDecodeError and yaml.YAMLError both describe the problem
        raise InputError(f"cannot parse {path}: {exc}") from exc


def validate(data, schema_name, label, schemas_dir):
    try:
        from jsonschema import Draft202012Validator
    except ImportError as exc:
        raise InputError("jsonschema is not installed: pip install pyyaml jsonschema") from exc
    schema = json.loads((schemas_dir / schema_name).read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(data), key=lambda e: list(e.absolute_path))
    if errors:
        details = "; ".join(f"{'/'.join(map(str, e.absolute_path)) or '(root)'}: {e.message}" for e in errors[:5])
        raise InputError(f"{label} does not match {schema_name}: {details}")


def run(config_path, metrics_path, schemas_dir=SCHEMAS):
    try:
        import yaml
    except ImportError as exc:
        raise InputError("PyYAML is not installed: pip install pyyaml jsonschema") from exc

    def parse_yaml(f):
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as exc:
            raise ValueError(str(exc)) from exc

    config = load(config_path, parse_yaml)
    metrics = load(metrics_path, json.load)
    validate(config, "config.schema.json", str(config_path), schemas_dir)
    validate(metrics, "metrics.schema.json", str(metrics_path), schemas_dir)
    return decide(config, metrics)


def render(res):
    lines = [f"AQEF gate: {res['decision']} (tier {res['tier']}, feature {res['feature']})"]
    lines += [f"  - {r}" for r in res["reasons"]]
    lines += [f"  advisory: {a}" for a in res["advisories"]]
    if res["gates"]:
        lines.append(f"  human gate: {', '.join(res['gates'])}")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="AQEF Quality Gatekeeper")
    parser.add_argument("--config", default=".aqef/config.yaml")
    parser.add_argument("--metrics", required=True)
    parser.add_argument("--json", action="store_true", help="print the decision as JSON")
    args = parser.parse_args(argv)

    try:
        res = run(args.config, args.metrics)
    except InputError as exc:
        res = {"decision": "ERROR", "exit_code": 3, "reasons": [str(exc)]}
        print(json.dumps(res) if args.json else f"AQEF gate: ERROR\n  - {exc}")
        return 3
    print(json.dumps(res, indent=2) if args.json else render(res))
    return res["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
