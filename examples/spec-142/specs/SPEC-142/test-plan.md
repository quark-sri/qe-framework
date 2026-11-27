---
feature: SPEC-142
tier: t1
features: []   # this example uses the Scenarios table, not Gherkin
date: 2026-11-27
---

# Test plan: Customer refunds

## Scope
- In scope: the refund decision (`request_refund`): window, amount, currency, delivery state, order status.
- Out of scope (with reason): the payment gateway call and retries (DP-03). This example has no gateway; a real feature needs an integration test with the same idempotency key.

## Scenarios

| ID | Criteria | Level | Given | When | Then (source) | Technique |
| --- | --- | --- | --- | --- | --- | --- |
| SPEC-142-S1 | AC1 | unit | Order 100.00, nothing refunded | Customer asks for 100.00 | Accepted; status `refunded` (REF-002) | Equivalence |
| SPEC-142-S2 | AC1 | unit | Order 100.00, nothing refunded | Customer asks for 40.00 | Accepted; status `partially_refunded` (REF-002) | Equivalence |
| SPEC-142-S3 | AC1, AC3 | unit | Order 100.00, 60.00 refunded | Customer asks for 40.00 | Accepted; status `refunded` (REF-002) | Boundary value |
| SPEC-142-S4 | AC2 | unit | Delivered 0 or 30 days ago | Customer asks | Accepted (REF-001) | Boundary value |
| SPEC-142-S5 | AC2 | unit | Delivered 31 days ago | Customer asks | Rejected: "Refund window has closed" (REF-001) | Boundary value |
| SPEC-142-S6 | AC2 | unit | Delivered 31 days ago | Support lead accepts with a reason | Accepted; the reason is kept (REF-001) | Decision table |
| SPEC-142-S7 | AC2 | unit | Delivered 31 days ago | Support lead accepts without a reason | Rejected: "Override needs a reason" (H1 answer F1) | Decision table |
| SPEC-142-S8 | AC2 | unit | Delivery date tomorrow | Customer asks | Rejected: "Delivery date is in the future" (REF-001, F2) | Invalid input |
| SPEC-142-S9 | AC3 | unit | Order 100.00, nothing refunded | Customer asks for 0.00 or -5.00; 0.01 | 0.00 and -5.00 rejected: "Amount must be greater than zero"; 0.01 accepted (REF-002) | Boundary value |
| SPEC-142-S10 | AC3 | unit | Order 100.00, 60.00 refunded | Customer asks for 40.01 | Rejected: "Amount exceeds refundable amount" (REF-002) | Boundary value |
| SPEC-142-S11 | AC3 | unit | Order 100.00 | Customer asks for 10.005 or 0.005 | Rejected: "Amount must have at most two decimals" (REF-002, DP-02) | Invalid input |
| SPEC-142-S12 | AC3 | unit | Order in EUR | Customer asks in USD | Rejected: "Currency does not match the order" (REF-002) | Invalid input |
| SPEC-142-S13 | AC4 | unit | Order not delivered | Customer asks | Rejected: "Order not delivered" (REF-001) | Equivalence |
| SPEC-142-S14 | NFR | unit | Any valid order | 10,000 decisions | Average below 1 ms (spec NFR) | Performance budget |

## Criteria coverage

| Criterion | Scenarios | Negative case? |
| --- | --- | --- |
| SPEC-142-AC1 | S1, S2, S3 | via AC3 scenarios |
| SPEC-142-AC2 | S4, S5, S6, S7, S8 | yes |
| SPEC-142-AC3 | S3, S9, S10, S11, S12 | yes |
| SPEC-142-AC4 | S13 | yes |

## Level matrix

All scenarios are `unit`: the decision is a pure function with no I/O. UI share: 0%.

## Hardening plan (t1)
- Mutation on: `src/refunds.py`
- Seeded faults focus: DP-01 (off-by-one), DP-02 (rounding), refundable amount
- Flake reruns: 10

## Plan review (test-plan-reviewer)
Not run in this example. The H2 reviewer read the plan directly.

## Gate H2
Applies: yes (t1). Decision: APPROVE — Reviewer: example-qe-engineer — Date: 2026-11-27
