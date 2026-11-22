#!/usr/bin/env python3
"""AQEF Quality Gatekeeper (sample).

Reads .aqef/config.yaml and a metrics JSON file for one feature or PR.
Prints a decision and the reasons.
Exit codes: 0 = pass, 1 = fail, 2 = escalate (human gate needed).
"""
import argparse
import json
import sys

import yaml


def check_min(reasons, name, value, minimum):
    if minimum is None:
        return
    if value is None:
        reasons.append(f"{name}: no value, minimum is {minimum}")
    elif value < minimum:
        reasons.append(f"{name}: {value:.2f} is below {minimum:.2f}")


def decide(config, metrics):
    tier = metrics.get("tier")
    if tier not in config.get("tiers", {}):
        return "FAIL", [f"unknown or missing tier: {tier!r}"], 1
    tier_cfg = config["tiers"][tier]
    rules = config.get("suite_rules", {})
    fail, escalate = [], []

    # Hard failures: the change must not merge.
    if metrics.get("new_product_defects", 0) > 0:
        fail.append(f"new product defects open: {metrics['new_product_defects']}")
    if metrics.get("test_guard_violations", 0) > 0:
        fail.append(f"test guard violations: {metrics['test_guard_violations']}")
    if rules.get("red_before_green_required") and not metrics.get("red_before_green_all", False):
        fail.append("red-before-green evidence missing for one or more tests")
    check_min(fail, "criteria coverage", metrics.get("criteria_coverage"), tier_cfg.get("criteria_coverage_min"))

    # Threshold misses: a human decides.
    check_min(escalate, "mutation score", metrics.get("mutation_score"), tier_cfg.get("mutation_score_min"))
    check_min(escalate, "seeded fault detection", metrics.get("seeded_fault_detection"), tier_cfg.get("seeded_fault_detection_min"))
    if metrics.get("ui_share", 0) > rules.get("ui_share_max", 1):
        escalate.append(f"UI share {metrics['ui_share']:.2f} is above {rules['ui_share_max']:.2f}")
    if metrics.get("flake_rate", 0) > rules.get("gating_flake_rate_max", 1):
        escalate.append(f"flake rate {metrics['flake_rate']:.3f} is above {rules['gating_flake_rate_max']:.3f}")
    nfr_results = metrics.get("nfr_results", {})
    for nfr in tier_cfg.get("nfr_required") or []:
        result = nfr_results.get(nfr)
        if result is None:
            escalate.append(f"NFR {nfr}: no result, tier {tier} requires it")
        elif result != "pass":
            escalate.append(f"NFR {nfr}: result is {result}")
    if metrics.get("panel_result") == "ESCALATE":
        escalate.append("review panel result is ESCALATE")
    score_min = config.get("review_panel", {}).get("accept_score_min")
    if score_min is not None and metrics.get("test_quality_score") is not None:
        if metrics["test_quality_score"] < score_min:
            escalate.append(f"test quality score {metrics['test_quality_score']} is below {score_min}")

    # Tier rule: T1 always needs H3, even when all checks pass.
    always_h3 = "H3" in tier_cfg.get("human_gates", [])

    if fail:
        return "FAIL", fail, 1
    if escalate:
        return "ESCALATE", escalate, 2
    if always_h3:
        return "ESCALATE", [f"tier {tier} requires human gate H3"], 2
    return "PASS", [], 0


def main():
    parser = argparse.ArgumentParser(description="AQEF Quality Gatekeeper")
    parser.add_argument("--config", default=".aqef/config.yaml")
    parser.add_argument("--metrics", required=True)
    args = parser.parse_args()

    with open(args.config, encoding="utf-8") as f:
        config = yaml.safe_load(f)
    with open(args.metrics, encoding="utf-8") as f:
        metrics = json.load(f)

    decision, reasons, code = decide(config, metrics)
    print(f"AQEF gate: {decision} (tier {metrics.get('tier')})")
    for reason in reasons:
        print(f"  - {reason}")
    sys.exit(code)


if __name__ == "__main__":
    main()
