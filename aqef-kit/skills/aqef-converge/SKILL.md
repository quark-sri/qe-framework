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
5. Test Guard: `python bots/testguard.py --base <base-branch> --json`. Put `test_guard_violations` and `test_guard_waived` in the metrics file.
6. Gatekeeper bot: `python bots/gatekeeper.py --metrics <metrics.json> --json`. Bots write the metrics file; agents must not. Act on the decision (AQEF-002):
   - `PASS`: merge. Post any advisories as a PR comment.
   - `FOLLOW_UP`: merge. Open a follow-up task for each gate in `gates`, with the reasons.
   - `FAIL`: do not merge. Fix the listed facts.
   - `ESCALATE`: the merge waits for the human gate in `gates`.
   - `ERROR`: a bot or file is broken. Fix the input; never treat it as a pass.
7. Post the PR summary (template section "PR summary" in `quality-report.md`).

## Exit criteria (automatic merge gate)
- Gatekeeper decision is `PASS` or `FOLLOW_UP`, or a human approved the `ESCALATE` gate.
- Traceability complete.
