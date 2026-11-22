---
id: risks.defect-patterns
type: risk
title: Known defect patterns
owner: <QE lead>
status: active
last_reviewed: 2026-11-22
---

# Known defect patterns

Agents use these patterns for scenario design, fault seeding and triage. Add a pattern after each escaped defect.

| ID | Pattern | Where seen | Test idea | Source |
| --- | --- | --- | --- | --- |
| DP-01 | Off-by-one at date boundaries | REF-001 window | Boundary scenarios at day N and N+1, time zone edge | BUG-412 |
| DP-02 | Rounding on partial amounts | Partial refunds | Amounts with 3+ decimals, split totals | BUG-455 |
| DP-03 | Double action on retry | Gateway retries | Retry with same idempotency key; assert one refund | BUG-881 (escape) |
| DP-04 | Missing permission check on new endpoint | Support APIs | Each role × each new endpoint | BUG-503 |
