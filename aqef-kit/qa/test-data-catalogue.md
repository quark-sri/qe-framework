# Test data catalogue

Agents reuse these builders and data sets before they create new ones. Add each new builder here in the same PR.

## Builders

| Builder | Entity | Location | Key methods | Invariants it enforces |
| --- | --- | --- | --- | --- |
| `anOrder()` | Order | `<path>` | `withTotal`, `paid`, `delivered(daysAgo)`, `withRefunded` | refundedAmount ≤ total |
| `aCustomer()` | Customer | `<path>` | `withRole`, `withTier` | unique email in test domain |

## Named data sets

| Name | Purpose | Seed | Used by |
| --- | --- | --- | --- |
| `refund-window-boundaries` | Orders delivered 0, 30, 31 days ago | 4201 | REF-001 scenarios |

## Generators
- Emails: `<run-id>-<n>@example.test`
- Cards: payment gateway test card ranges only
- Seed: from `test-data-plan.md` of each feature
