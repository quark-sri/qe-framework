---
feature: <feature-id>
seed: <fixed integer>
date: <YYYY-MM-DD>
---

# Test data plan: <feature name>

## Data per scenario

| Scenario | Entity | State | Key values | Source (rule or entity file) | Builder or data set |
| --- | --- | --- | --- | --- | --- |
| S1 | Order | paid | total = 100.00 NZD | entities/order.md | `anOrder().paid()` |

## New builders

| Builder | Entity | Defaults | `with...` methods | Invariants enforced |
| --- | --- | --- | --- | --- |

## Isolation and cleanup
- Create: <per test / per class>
- Unique keys: <how, e.g. run-id prefix>
- Cleanup: <transaction rollback / API delete / container reset>

## Privacy check
- [ ] No real names, emails, phone numbers, card numbers or national IDs.
- [ ] Generators use reserved test domains and test card ranges.
