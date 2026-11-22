---
feature: <feature-id>
tier: <t1|t2|t3>
result: ACCEPT | ESCALATE
test_quality_score: <0-100>
date: <YYYY-MM-DD>
panel_provider: aqef | qestack
---

# Quality report: <feature name>

## Result
**<ACCEPT | ESCALATE>** — Test Quality Score <n>/100

Escalation reasons:
1.

## Gate metrics

| Metric | Value | Threshold (tier) | Pass |
| --- | --- | --- | --- |
| Criteria with passing test | | 100% | |
| Red-before-green evidence | n/n tests | all | |
| Mutation score (changed code) | | | |
| Seeded faults detected | | | |
| Flake reruns passed | | all | |
| Test Guard (no weakened tests) | clean / violations | clean | |
| UI share | | ≤ 10% | |

## Findings (ranked)

| ID | Severity | Persona | File:line | Finding | Suggested fix | Confidence |
| --- | --- | --- | --- | --- | --- | --- |

## Accepted gaps
| Gap | Reason | Approver |
| --- | --- | --- |

## PR summary (posted by the Gatekeeper)
- Result:
- New tests: <n> (unit <n>, api <n>, ui <n> ...)
- Thresholds: <all pass | list failures>
- Human gate needed: <none | H3>

## Gate H3
Applies: yes / no. Decision: ACCEPT / REWORK TESTS — Reviewer: — Date:
