"""Tests for SPEC-142. Scenarios: specs/SPEC-142/test-plan.md. Expected values: REF-001, REF-002."""
import time
from datetime import date, timedelta
from decimal import Decimal

import pytest

from refunds import Order, RefundRejected, request_refund

pytestmark = [pytest.mark.cap("payments.refund"), pytest.mark.level_unit, pytest.mark.risk_t1]

TODAY = date(2026, 11, 27)
D = Decimal


def order(total="100.00", refunded="0.00", currency="EUR", days_ago=5):
    delivered = None if days_ago is None else TODAY - timedelta(days=days_ago)
    return Order(total=D(total), refunded=D(refunded), currency=currency, delivered_on=delivered)


def ask(o, amount, currency="EUR", **kw):
    return request_refund(o, D(amount), currency, TODAY, **kw)


def rejected(o, amount, message, **kw):
    with pytest.raises(RefundRejected) as err:
        ask(o, amount, **kw)
    assert str(err.value) == message


# --- AC1: refunded total and status -------------------------------------------

@pytest.mark.req("SPEC-142-AC1")
def test_full_refund_marks_the_order_refunded():  # S1
    d = ask(order(), "100.00")
    assert (d.refunded_total, d.status) == (D("100.00"), "refunded")


@pytest.mark.req("SPEC-142-AC1")
def test_partial_refund_marks_the_order_partially_refunded():  # S2
    d = ask(order(), "40.00")
    assert (d.refunded_total, d.status) == (D("40.00"), "partially_refunded")


@pytest.mark.req("SPEC-142-AC1", "SPEC-142-AC3")
def test_refunding_the_rest_marks_the_order_refunded():  # S3
    d = ask(order(refunded="60.00"), "40.00")
    assert (d.refunded_total, d.status) == (D("100.00"), "refunded")


# --- AC2: refund window (REF-001) ----------------------------------------------

@pytest.mark.req("SPEC-142-AC2")
@pytest.mark.parametrize("days", [0, 30])
def test_customer_refund_inside_the_window_is_accepted(days):  # S4
    assert ask(order(days_ago=days), "10.00").status == "partially_refunded"


@pytest.mark.req("SPEC-142-AC2")
def test_customer_refund_on_day_31_is_rejected():  # S5
    rejected(order(days_ago=31), "10.00", "Refund window has closed")


@pytest.mark.req("SPEC-142-AC2")
def test_support_lead_can_accept_a_late_refund_with_a_reason():  # S6
    d = ask(order(days_ago=31), "10.00", role="support_lead", reason="Courier lost the return label")
    assert d.reason == "Courier lost the return label"
    assert d.refunded_total == D("10.00")


@pytest.mark.req("SPEC-142-AC2")
@pytest.mark.parametrize("reason", [None, "", "   "])
def test_support_lead_override_without_a_reason_is_rejected(reason):  # S7
    rejected(order(days_ago=31), "10.00", "Override needs a reason", role="support_lead", reason=reason)


@pytest.mark.req("SPEC-142-AC2")
def test_delivery_date_in_the_future_is_rejected():  # S8
    rejected(order(days_ago=-1), "10.00", "Delivery date is in the future")


# --- AC3: amount limits (REF-002) ----------------------------------------------

@pytest.mark.req("SPEC-142-AC3")
@pytest.mark.parametrize("amount", ["0.00", "-5.00"])
def test_zero_or_negative_amount_is_rejected(amount):  # S9
    rejected(order(), amount, "Amount must be greater than zero")


@pytest.mark.req("SPEC-142-AC3")
def test_smallest_amount_is_accepted():  # S9
    assert ask(order(), "0.01").refunded_total == D("0.01")


@pytest.mark.req("SPEC-142-AC3")
def test_amount_above_the_refundable_amount_is_rejected():  # S10
    rejected(order(refunded="60.00"), "40.01", "Amount exceeds refundable amount")


@pytest.mark.req("SPEC-142-AC3")
@pytest.mark.parametrize("amount", ["10.005", "0.005"])
def test_amount_with_three_decimals_is_rejected(amount):  # S11
    rejected(order(), amount, "Amount must have at most two decimals")


@pytest.mark.req("SPEC-142-AC3")
def test_amount_in_another_currency_is_rejected():  # S12
    rejected(order(), "10.00", "Currency does not match the order", currency="USD")


# --- AC4: delivery state ---------------------------------------------------------

@pytest.mark.req("SPEC-142-AC4")
def test_refund_for_an_order_not_delivered_is_rejected():  # S13
    rejected(order(days_ago=None), "10.00", "Order not delivered")


# --- NFR: performance ------------------------------------------------------------

@pytest.mark.nfr("perf")
def test_decision_takes_less_than_1_ms_on_average():  # S14
    o, runs = order(), 10_000
    start = time.perf_counter()
    for _ in range(runs):
        request_refund(o, D("10.00"), "EUR", TODAY)
    assert (time.perf_counter() - start) / runs < 0.001
