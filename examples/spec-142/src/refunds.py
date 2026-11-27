"""Refund decision for SPEC-142 (rules REF-001 and REF-002)."""
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional

WINDOW_DAYS = 30
CENT = Decimal("0.01")


class RefundRejected(Exception):
    pass


@dataclass(frozen=True)
class Order:
    total: Decimal
    refunded: Decimal
    currency: str
    delivered_on: Optional[date]


@dataclass(frozen=True)
class Decision:
    refunded_total: Decimal
    status: str  # refunded | partially_refunded
    reason: Optional[str] = None


def request_refund(order, amount, currency, today, role="customer", reason=None):
    """Accept a refund and return the new order state, or raise RefundRejected."""
    if order.delivered_on is None:
        raise RefundRejected("Order not delivered")
    if order.delivered_on > today:
        raise RefundRejected("Delivery date is in the future")
    if currency != order.currency:
        raise RefundRejected("Currency does not match the order")
    if amount != amount.quantize(CENT):
        raise RefundRejected("Amount must have at most two decimals")
    if amount <= 0:
        raise RefundRejected("Amount must be greater than zero")

    late = (today - order.delivered_on).days > WINDOW_DAYS
    if late and role != "support_lead":
        raise RefundRejected("Refund window has closed")
    if late and not (reason or "").strip():
        raise RefundRejected("Override needs a reason")

    if amount > order.total - order.refunded:
        raise RefundRejected("Amount exceeds refundable amount")

    refunded_total = order.refunded + amount
    status = "refunded" if refunded_total == order.total else "partially_refunded"
    return Decision(refunded_total, status, reason)
