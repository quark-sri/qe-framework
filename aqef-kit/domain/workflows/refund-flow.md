---
id: wf.refund
type: workflow
title: Refund flow
relates_to: [cap.payments.refund, entity.order, entity.refund, REF-001, REF-002, int.payment-gateway]
owner: <payments domain expert>
status: active
last_reviewed: 2026-11-22
source: [SPEC-142]
---

# Workflow: Refund flow

## States of a refund
`requested → approved → sent_to_gateway → completed`
`requested → rejected`
`sent_to_gateway → failed → sent_to_gateway` (retry, max 3)

## Transitions

| From | Event | To | Who | Rule |
| --- | --- | --- | --- | --- |
| — | request | requested | Customer, Support | REF-001 |
| requested | approve | approved | Support agent (≤ limit), Support lead | roles.md |
| requested | reject | rejected | Support | |
| approved | submit | sent_to_gateway | System | |
| sent_to_gateway | gateway ok | completed | System | Update order.refundedAmount (REF-002) |
| sent_to_gateway | gateway error | failed | System | |
| failed | retry | sent_to_gateway | System | Idempotency key required (DP-03) |

## Invalid transitions to test
- completed → approve
- rejected → submit
- requested → completed (skips approval)
