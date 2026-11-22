---
name: aqef-converge
description: AQEF phase 5. Runs the affected regression in the dev container, triages failures, checks that spec, code and tests agree, and applies the automatic merge gate. Use before a feature PR is merged.
---

# AQEF phase 5: Converge

## Steps
1. Execution Bot selects the regression set:
   - T1 feature: full regression.
   - T2 and T3: test impact analysis (changed files and touched capabilities) plus smoke.
2. Run the set in the dev container. Results Normalizer writes normalized results.
3. For each failure, run `failure-triage` (use skill `aqef-triage`). A `product_defect_new` blocks the merge.
4. Convergence check:
   - Each acceptance criterion → implemented code task done → tests exist → tests green.
   - No orphan tests, no untagged tests.
   - Spec, KB and tests use the same rule values.
5. Gatekeeper bot: compare all metrics with `.aqef/config.yaml`. Post the PR summary (template section "PR summary" in `quality-report.md`).

## Exit criteria (automatic merge gate)
- No open new product defect from this change.
- All thresholds pass for the tier.
- Traceability complete.
