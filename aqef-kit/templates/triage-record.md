---
run_id: <run-id>
cluster_id: <cluster-id>
env: <dev-container | test | staging | prod>
build: <build>
tests: [<test-id>, ...]
capability: <cap>
tier: <t1|t2|t3>
state: <product_defect_new | known_defect | regression_of_fixed_defect | test_defect | expected_change | test_data_issue | environment | flaky | needs_investigation>
confidence: <0.0-1.0>
action: <action taken or proposed>
acted_autonomously: <true|false>
human_state: <filled after H5, else empty>
defect_id: <id or empty>
---

# Triage: <short title>

## Failure
- Error signature:
- Failing step:
- First failed run:
- Tests in cluster: <n>

## Evidence
| Check | Result |
| --- | --- |
| Rerun in clean container | pass / fail |
| Environment health | ok / degraded (detail) |
| Product code changed since last green | yes (commits) / no |
| Test code changed | yes / no |
| Test data changed | yes / no |
| Spec or KB changed | yes (link) / no |
| Matches open defect | id / none |
| History (last 20 runs) | e.g. 18 pass, 2 fail |

## Reasoning
For the chosen state:
Against the chosen state:

## Action
- Taken / proposed:
- Links (ticket, PR):

## H5 (if needed)
Decision: CONFIRM / CHANGE STATE to ___ — Reviewer: — Date:
