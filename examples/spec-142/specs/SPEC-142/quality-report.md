---
feature: SPEC-142
tier: t1
result: ESCALATE
date: 2026-11-27
panel_provider: aqef
---

# Quality report: Customer refunds

## Result
**ESCALATE.** T1 work always waits for H3. The gatekeeper also escalates one item:

1. NFR accessibility: no result, tier t1 requires it. This change has no user interface. See finding E1.

## Gate metrics

| Metric | Value | Threshold (t1) | Pass | Evidence |
| --- | --- | --- | --- | --- |
| Criteria with passing test | 4/4 | 100% | yes | `test-plan.md`, `runs/2-green.txt` |
| Red-before-green evidence | 20/20 tests | all | yes | `runs/1-red.txt`, `runs/2-green.txt` |
| Mutation score (changed code) | 0.97 (68/70) | ≥ 0.80 | yes | `runs/5-mutation.txt` |
| Seeded faults detected | 1.00 (14/14) | ≥ 0.95 | yes | `runs/4-seeded-faults.txt` |
| Flake reruns passed | 10/10 | all | yes | `runs/3-flake-reruns.txt` |
| Test Guard (no weakened tests) | clean | clean | yes | CI |
| UI share | 0% | ≤ 10% | yes | `test-plan.md` |
| NFR security | pass | required | yes | `runs/6-security-bandit.txt` |
| NFR performance | pass | required | yes | test S14 |
| NFR accessibility | no result | required | no | E1 |

## Findings (ranked)

| ID | Severity | Persona | File:line | Finding | Suggested fix | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| E1 | medium | framework | `.aqef/config.yaml` `nfr_required` | T1 requires an accessibility result for every change, also for a change with no user interface. Each such change escalates | Let a human record "not applicable" with a reason, or require an NFR only when the change touches that surface | 0.9 |
| E2 | low | test review | `tests/test_refunds.py` S14 | The performance test measures an average on the build machine. A slow CI machine can fail it | Keep the budget generous, or run it outside the gating stage | 0.7 |

The review panel did not run in this example. The H3 reviewer read the tests directly.

## Accepted gaps
| Gap | Reason | Approver |
| --- | --- | --- |
| No accessibility result | No user interface in this change | example-qe-engineer (H3) |
| No gateway retry test (DP-03) | Out of scope: no gateway in this example | example-qe-engineer (H3) |

## PR summary (posted by the Gatekeeper)
- Result: ESCALATE (H3)
- New tests: 20 (unit 20)
- Thresholds: all pass, except NFR accessibility has no result
- Human gate needed: H3

## Gate H3
Applies: yes (t1). Decision: ACCEPT with the gaps above — Reviewer: example-qe-engineer — Date: 2026-11-27
