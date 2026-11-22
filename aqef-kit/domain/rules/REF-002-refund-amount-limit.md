---
id: REF-002
type: rule
title: Refund amount limit
relates_to: [cap.payments.refund, entity.order, entity.refund, wf.refund]
owner: <payments domain expert>
status: active
last_reviewed: 2026-11-22
source: [SPEC-142-AC3]
---

# Rule REF-002: Refund amount limit

## Statement
A refund amount must be at least 0.01 and must not exceed the refundable amount.
Refundable amount = order total − refunded amount. Amounts have two decimals. The system does not round input; it rejects more than two decimals.

## Examples

| Order total | Already refunded | Requested | Result |
| --- | --- | --- | --- |
| 100.00 | 0.00 | 100.00 | Accepted; order becomes refunded |
| 100.00 | 0.00 | 40.00 | Accepted; order becomes partially_refunded |
| 100.00 | 60.00 | 40.00 | Accepted; order becomes refunded |
| 100.00 | 60.00 | 40.01 | Rejected: "Amount exceeds refundable amount" |
| 100.00 | 0.00 | 0.00 | Rejected: "Amount must be greater than zero" |
| 100.00 | 0.00 | 10.005 | Rejected: "Amount must have at most two decimals" |

## Boundary values
- Lower: 0.00 (rejected), 0.01 (accepted)
- Upper: refundable amount (accepted), refundable amount + 0.01 (rejected)

## Invalid inputs
- Negative amount → reject.
- Currency different from the order → reject.

## Related risks
- Rounding on partial amounts (DP-02).
- Two refunds approved at the same time that together exceed the refundable amount. Test concurrent approval.
