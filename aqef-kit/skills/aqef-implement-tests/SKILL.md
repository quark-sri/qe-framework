---
name: aqef-implement-tests
description: AQEF phase 4. Implements automated tests from the approved plan, proves red-before-green, closes coverage gaps, hardens the tests and runs the review panel. Use during the implement phase of each task or feature.
---

# AQEF phase 4: Implement tests

## Steps
1. Dev coding agents write unit tests with the code (TDD) for `@level:unit` scenarios.
2. Run `automation-engineer` once per level (component, contract, integration, api, ui). Each instance works only on its level.
3. Each instance proves red-before-green and records evidence in `specs/<feature>/runs/`.
4. Execution Bot: run all new tests in the dev container.
5. Traceability Bot: update the matrix.
6. Run `coverage-traceability-analyst`. Output: `gaps.md`.
7. Loop: send open gaps to the owner agent. Repeat steps 2–6 until no T1 or T2 gap is open, or a human accepts it. Limit: 3 loops, then escalate.
8. Hardening (per tier):
   - Mutation Bot on changed code.
   - `fault-seeder`, then Execution Bot applies each fault.
   - Flake Bot reruns new tests (`flake_reruns` from config).
   - Test Guard (`bots/testguard.py`) checks the diff for deleted, skipped, retried or weakened tests.
9. Run `test-review-panel` in a fresh context. Output: `quality-report.md` with ACCEPT or ESCALATE.
10. Gatekeeper bot compares metrics with thresholds.
11. Apply gate H3 rules (AQEF-002): T1 always, before merge; T2 on escalation and T3 on sample, as a follow-up after merge.

## Exit criteria
- Quality report is ACCEPT, or H3 approves the exceptions.
- All new tests are green in the dev container.
