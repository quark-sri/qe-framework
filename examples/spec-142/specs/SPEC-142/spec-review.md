---
feature: SPEC-142
spec: specs/SPEC-142/spec.md
reviewed_by: spec-critic
date: 2026-11-27
---

# Spec review: Customer refunds

## Summary
- Findings: 1 high, 1 medium, 1 low
- Proposed tier: t1 (moves money; capability `payments.refund` is T1)
- Open questions: 2, answered at H1

## Acceptance criteria

| ID | Criterion (as written) | Testable? | Proposed rewrite |
| --- | --- | --- | --- |
| SPEC-142-AC1 | Refunded total and order status | yes | — |
| SPEC-142-AC2 | Refund window, support lead override | yes, after F1 | Add: a support lead override without a reason is rejected with "Override needs a reason" |
| SPEC-142-AC3 | Amount limits | yes | — |
| SPEC-142-AC4 | Order not delivered | yes | — |

## Findings

| ID | Severity | Type | Finding | Evidence | Confidence |
| --- | --- | --- | --- | --- | --- |
| F1 | high | missing behaviour | The spec does not say what happens when a support lead gives no reason | AC2, REF-001 | 0.9 |
| F2 | medium | missing behaviour | REF-001 rejects a delivery date in the future as a data error. The spec does not say this | REF-001 "Invalid inputs" | 0.8 |
| F3 | low | NFR gap | The performance budget is an average. A p95 budget is better for an API | NFR section | 0.6 |

## Questions for the product owner
1. What message does a support lead get without a reason? Answer at H1: "Override needs a reason".
2. Is a delivery date in the future in scope? Answer at H1: yes, reject with "Delivery date is in the future".

## Risk
- Tier: t1. Reason: moves money.

| Risk | Impact (1–3) | Likelihood (1–3) | Score | Test idea |
| --- | --- | --- | --- | --- |
| Off-by-one at day 30/31 (DP-01) | 3 | 2 | 6 | Boundary tests at day 30 and 31 |
| Rounding on partial amounts (DP-02) | 3 | 2 | 6 | Three decimals rejected; partial refunds add up exactly |
| Refund above the refundable amount | 3 | 2 | 6 | Refundable + 0.01 rejected after a partial refund |

## KB changes proposed
- None. REF-001 and REF-002 cover the rules.

## Gate H1
Decision: APPROVE with F1 and F2 answered — Reviewer: example-product-owner — Date: 2026-11-27
