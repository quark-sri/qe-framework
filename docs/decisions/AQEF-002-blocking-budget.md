---
id: AQEF-002
title: "Blocking budget: only facts block a merge, and the gate fails closed"
status: accepted
scope: permanent
date: 2026-11-22
supersedes: []
applies_to:
  - docs/AQEF.md
  - aqef-kit/.aqef/config.yaml
  - aqef-kit/bots/gatekeeper.py
  - aqef-kit/bots/README.md
  - aqef-kit/skills/aqef-converge/SKILL.md
  - aqef-kit/skills/aqef-implement-tests/SKILL.md
  - aqef-kit/gates/human-gates.md
retired_wording:
  - "T1 always; others on ESCALATE"
  - "panel review if ESCALATE"
---

# AQEF-002: Blocking budget

## Decision

The gatekeeper blocks a merge only on facts:

- a new product defect confirmed by triage
- a Test Guard violation
- secrets or real personal data in tests
- missing red-before-green evidence
- acceptance criteria coverage below the tier minimum
- a required metric that is missing

A missing required metric is a FAIL, never a PASS (the gate fails closed).

Every other finding is an escalation. Each tier's `on_escalate` setting routes it:

| Setting | Default tier | Effect |
| --- | --- | --- |
| `block` | T1 | ESCALATE: the merge waits for a human gate |
| `follow_up` | T2 | FOLLOW_UP: the merge goes ahead; CI opens a follow-up task for H3 |
| `comment` | T3 | PASS with advisories; a 10% audit sample gets a follow-up |

A tier whose `human_gates` lists H3 always waits for a human, whatever `on_escalate` says.

## Why

- QE must keep pace with coding agents. Blocking on opinions or uncalibrated thresholds would make QE the bottleneck.
- Facts that block stop real bugs and agent shortcuts.
- A gate that passes when a bot fails to report lets bugs through silently. This happened in v0.1: a metrics file with only the tier could PASS.

## Consequences

- T2 and T3 teams merge faster. Some escalations are reviewed after merge, so the follow-up tasks must be tracked.
- Teams can make a tier stricter by setting `on_escalate: block`.

## Revisit when

Scorecard data shows escapes that a blocking escalation would have caught, or follow-up tasks are left open for too long.

## History

- 2026-11-22: Accepted for v0.2.
