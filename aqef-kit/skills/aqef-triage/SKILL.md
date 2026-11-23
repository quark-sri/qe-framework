---
name: aqef-triage
description: AQEF phases 6–7. Triages every failed test after a regression run (dev container or deployed environment), takes allowed actions and queues the rest for human confirmation. Use after any run with failures. Run it in your coding agent session on the CI results; no API key is needed (AQEF-001).
---

# AQEF phases 6–7: Triage and fix

## How to run
CI publishes the normalized results and the failure list as build artifacts. The person on the triage rota downloads them (or reads them from the CI run) and runs this skill in their coding agent.

## Steps
1. Results Normalizer (in CI): convert raw results to `schemas/test-result.schema.json`.
2. Run `failure-triage` on all failures. It writes one record per cluster to `triage/<run-id>/`.
3. For each record, check `.aqef/config.yaml`:
   - Confidence ≥ the bar for the state, state not in `never_autonomous`, and (for T1) state not in `t1_requires_human` → run the action.
   - Else → add to the H5 queue (`triage/<run-id>/h5-queue.md`).
4. Actions:
   - `product_defect_new` → `defect-reporter`
   - `test_defect`, `test_data_issue` → `test-fixer`, then `test-review-panel` on the fix PR
   - `flaky` → Flake Bot quarantines with ticket and deadline
   - `environment` → ops ticket, rerun after recovery
   - `expected_change` → H5, then `scenario-designer` and `automation-engineer` update
5. After H5 decisions, write the human state back into each record (`human_state`). This feeds agent accuracy metrics.
6. Monthly: replay 20 past records with known outcomes. Update the triage agent accuracy and autonomy level.

## Outputs
Triage records, H5 queue, defect tickets, fix PRs, quarantine updates.
