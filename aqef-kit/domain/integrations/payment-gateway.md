---
id: int.payment-gateway
type: integration
title: Payment gateway refund API
relates_to: [cap.payments.refund, entity.refund, wf.refund]
owner: <payments platform team>
status: active
last_reviewed: 2026-11-22
source: [SPEC-142]
---

# Integration: Payment gateway refund API

## Contract (example)

| Item | Value |
| --- | --- |
| Operation | `POST /refunds` |
| Request | `paymentId`, `amount`, `currency`, `idempotencyKey` |
| Success | `201` with `refundId`, `status: succeeded` |
| Duplicate key | `200` with the original refund (no second refund) |
| Errors | `402` declined, `409` amount exceeds captured, `5xx` gateway error (retry) |
| Timeout | 10 s; treat as unknown and retry with the same key |

## Rules for the system
- Send the same `idempotencyKey` on every retry (DP-03).
- Retry only on `5xx` and timeout. Maximum 3 attempts.
- Never retry on `402` or `409`. Mark the refund `failed` and alert support.

## How to test
- Contract tests (consumer side) for each response above. Tag `@level:contract`.
- Use the gateway sandbox or a service virtualization stub. Never call the live gateway from tests.
