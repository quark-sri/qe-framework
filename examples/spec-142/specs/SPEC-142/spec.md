---
id: SPEC-142
title: Customer refunds
capability: payments.refund
---

# SPEC-142: Customer refunds

A customer can ask for a refund on a delivered order. A support lead can accept a late refund with a reason.

Dates are calendar dates in UTC. Amounts are decimal numbers in the order currency.

## Acceptance criteria

- **SPEC-142-AC1** An accepted refund adds the amount to the refunded total. The order becomes `refunded` when the refunded total equals the order total, and `partially_refunded` when it is lower.
- **SPEC-142-AC2** A customer can ask for a refund from day 0 to day 30 after delivery (rule REF-001). After day 30 the refund is rejected with "Refund window has closed". A support lead can accept a late refund only with a reason; without one, it is rejected with "Override needs a reason". A delivery date in the future is rejected with "Delivery date is in the future". (F1 and F2, approved at H1.)
- **SPEC-142-AC3** The amount is at least 0.01, has at most two decimals, uses the order currency and is not more than the refundable amount (rule REF-002). Other amounts are rejected with the message from REF-002.
- **SPEC-142-AC4** A refund for an order that is not delivered is rejected with "Order not delivered".

## Non-functional

- Performance: one refund decision takes less than 1 ms on average.
- Security: no high or medium findings from static analysis.
- Accessibility: not applicable. This change has no user interface (approved at H1).
