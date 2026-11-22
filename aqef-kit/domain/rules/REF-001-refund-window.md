---
id: REF-001
type: rule
title: Refund window
relates_to: [cap.payments.refund, entity.order, entity.refund, wf.refund]
owner: <payments domain expert>
status: active
last_reviewed: 2026-11-22
source: [SPEC-142-AC2]
---

# Rule REF-001: Refund window

## Statement
A customer can request a refund up to 30 days after delivery. Day 0 is the delivery date (UTC). A support lead can override the window.

## Examples

| Days since delivery | Requested by | Result |
| --- | --- | --- |
| 0 | Customer | Accepted |
| 30 | Customer | Accepted |
| 31 | Customer | Rejected: "Refund window has closed" |
| 31 | Support lead | Accepted (override, reason required) |
| Not delivered | Customer | Rejected: "Order not delivered" |

## Boundary values
- Lower: 0 days (accepted)
- Upper: 30 days (accepted), 31 days (rejected)
- Time zone: delivery at 23:59 UTC on day 0 counts as day 0.

## Invalid inputs
- Delivery date in the future → reject as data error.

## Related risks
- Off-by-one at day 30/31 (defect pattern DP-01).
