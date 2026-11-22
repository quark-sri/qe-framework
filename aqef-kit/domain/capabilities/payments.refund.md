---
id: cap.payments.refund
type: capability
title: Refunds
tier: t1
relates_to: [entity.order, entity.refund, REF-001, REF-002, wf.refund, int.payment-gateway]
owner: <payments domain expert>
status: active
last_reviewed: 2026-11-22
source: [SPEC-142]
---

# Capability: payments.refund

## Purpose
Return money to a customer for all or part of a paid order.

## Why tier t1
Moves money. Errors cause financial loss or legal complaints.

## Entities
- [Order](../entities/order.md)
- [Refund](../entities/refund.md)

## Rules
- [REF-001 Refund window](../rules/REF-001-refund-window.md)
- [REF-002 Refund amount limit](../rules/REF-002-refund-amount-limit.md)

## Workflows
- [Refund flow](../workflows/refund-flow.md)

## Integrations
- [Payment gateway refund API](../integrations/payment-gateway.md)

## Key risks
- Double refund on retry (see defect patterns DP-03)
- Wrong rounding on partial refunds
- Refund approved above the agent limit
