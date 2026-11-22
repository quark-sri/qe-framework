---
feature: <feature-id>
tier: <t1|t2|t3>
features: [features/<capability>/<feature>.feature]
date: <YYYY-MM-DD>
---

# Test plan: <feature name>

## Scope
- In scope:
- Out of scope (with reason):

## Criteria coverage

| Criterion | Scenarios | Negative case? |
| --- | --- | --- |
| SPEC-000-AC1 | S1, S2 | yes |

## Level matrix

| Scenario | Title | Level | Owner | Reason for level | NFR | Est. run time |
| --- | --- | --- | --- | --- | --- | --- |
| S1 | | unit | dev agent | Pure calculation | — | < 1 s |
| S2 | | api | QE agent | Needs full refund flow | security | 2 s |

## Pyramid check

| Level | Count | Share | Limit |
| --- | --- | --- | --- |
| unit | | | — |
| component | | | — |
| contract | | | — |
| integration | | | — |
| api | | | — |
| ui | | | ≤ 10% |

## Hardening plan (by tier)
- Mutation on: <packages or modules>
- Seeded faults focus: <risks>
- Flake reruns: <n>

## Manual or exploratory items
| Item | Reason it is not automated | Owner |
| --- | --- | --- |

## Plan review (test-plan-reviewer)
Result: ACCEPT / ESCALATE

| ID | Lens | Severity | Scenario | Finding | Evidence | Suggested fix | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Gate H2
Applies: yes / no (rule). Decision: APPROVE / REVISE PLAN — Reviewer: — Date:
