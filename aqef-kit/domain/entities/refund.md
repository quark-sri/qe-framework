---
id: entity.refund
type: entity
title: Refund
relates_to: [cap.payments.refund, entity.order, REF-001, REF-002, wf.refund, int.payment-gateway]
owner: <payments domain expert>
status: active
last_reviewed: 2026-11-22
source: [SPEC-142]
---

# Entity: Refund

## Attributes

| Attribute | Type | Valid values | Notes |
| --- | --- | --- | --- |
| id | string | `REF-` + 8 digits | Unique |
| orderId | string | existing order in status paid, shipped, delivered or partially_refunded | See [Order](order.md) |
| amount | decimal(10,2) | 0.01 – refundable amount of the order | Rule [REF-002](../rules/REF-002-refund-amount-limit.md) |
| currency | ISO 4217 | same as the order | |
| status | enum | requested, approved, rejected, sent_to_gateway, failed, completed | See [Refund flow](../workflows/refund-flow.md) |
| requestedBy | string | customer or support user | See [roles](../roles.md) |
| approvedBy | string | null until approved | Support agent (≤ limit) or support lead |
| reason | string | 1 – 500 characters | Required for a window override (REF-001) |
| idempotencyKey | string | UUID | Same key on every gateway retry (DP-03) |
| attempts | integer | 0 – 3 | Gateway submissions |

## Invariants
- `amount` ≤ refundable amount of the order at the time of approval.
- `currency` equals the order currency.
- `approvedBy` is set if and only if status is approved or later.
- `idempotencyKey` never changes after the first gateway submission.
- `attempts` ≤ 3.

## Builder hint
`aRefund().forOrder(order).withAmount("25.00").requestedBy(customer).build()`
