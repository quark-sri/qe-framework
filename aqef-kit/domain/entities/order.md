---
id: entity.order
type: entity
title: Order
relates_to: [cap.payments.refund, entity.refund, wf.refund]
owner: <orders domain expert>
status: active
last_reviewed: 2026-11-22
source: [SPEC-101]
---

# Entity: Order

## Attributes

| Attribute | Type | Valid values | Notes |
| --- | --- | --- | --- |
| id | string | `ORD-` + 8 digits | Unique |
| customerId | string | existing customer | |
| total | decimal(10,2) | 0.01 – 99,999.99 | Currency of the order |
| currency | ISO 4217 | NZD, AUD, USD | |
| status | enum | created, paid, shipped, delivered, cancelled, refunded, partially_refunded | See states |
| deliveredAt | timestamp | null until delivered | UTC |
| refundedAmount | decimal(10,2) | 0.00 – total | Sum of approved refunds |

## States
`created → paid → shipped → delivered`. `paid|shipped|delivered → partially_refunded → refunded`. `created|paid → cancelled`.

## Invariants
- `refundedAmount` ≤ `total`.
- `status = refunded` if and only if `refundedAmount = total`.
- `deliveredAt` is set if and only if status is delivered or later.

## Builder hint
`anOrder().withTotal("100.00").delivered(daysAgo(10)).build()`
