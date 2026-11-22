---
id: roles
type: role
title: Roles and permissions
owner: <domain lead>
last_reviewed: 2026-11-22
---

# Roles and permissions

| Role | Can request refund | Can approve refund | Approval limit |
| --- | --- | --- | --- |
| Customer | Own orders only | No | — |
| Support agent | Any order | Yes | ≤ 500.00 per refund |
| Support lead | Any order | Yes | No limit |
| Guest | No | No | — |

Negative cases to test for each capability: guest access, other customer's order, approval above limit.
