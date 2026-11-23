---
id: AQEF-001
title: "Session-first: agents run in the team's own coding-agent sessions"
status: accepted
scope: phase
date: 2026-11-23
supersedes: []
applies_to:
  - README.md
  - docs/AQEF.md
  - aqef-kit/agents/failure-triage.md
  - aqef-kit/agents/report-analyst.md
  - aqef-kit/skills/aqef-triage/SKILL.md
  - aqef-kit/skills/aqef-report/SKILL.md
retired_wording:
  - "after every post-deploy run"
  - "after every regression run"
  - "Failure Triage** agent runs on every failure"
---

# AQEF-001: Session-first

## Decision

In this phase, AQEF runs from the team's own coding-agent sessions (Claude Code, Codex, Cursor, Copilot) on their normal plans. No part of AQEF needs AI API keys or tokens.

- LLM agents and skills run in a person's coding-agent session.
- CI runs only deterministic bots. CI does not call an LLM.
- Work after CI (triage, reports) uses CI artifacts. A person runs the skill in their coding agent.
- Cost is measured as people's time and agent sessions, not tokens.
- Outputs (results, metrics, triage records, scorecards) are plain files, so a later phase can automate them without changes.

## Why

AI API billing is costly, and the target teams already pay for coding-agent plans. A framework that needs API access would add cost and exclude these teams.

## Consequences

- Triage and reporting after a CI run need a person to start them. This adds some delay, but no API cost.
- Unattended agents in CI are an optional extra for teams that already have them. No milestone in this phase depends on them.

## Revisit when

A later phase wants automated reporting, scheduled triage or new solutions, and the value justifies the API cost. Write a new decision that supersedes this one.

## History

- 2026-11-23: Accepted. First stated as a hard rule, then changed to a phase default the same day.
