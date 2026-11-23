---
id: AQEF-004
title: "Speed budget: targets for QE time and gate response, never auto-approve"
status: accepted
scope: phase
date: 2026-11-23
supersedes: []
applies_to:
  - docs/AQEF.md
  - aqef-kit/.aqef/config.yaml
  - aqef-kit/schemas/config.schema.json
  - aqef-kit/gates/human-gates.md
retired_wording:
  - "≤ 15 min for the gating suite"
  - "pr_feedback_minutes_max"
---

# AQEF-004: Speed budget

## Decision

| Item | Default target | When the target is missed |
| --- | --- | --- |
| QE time added to PR feedback, T2 and T3 | 10 minutes | Reported. The improvement loop moves the slowest checks after merge or makes them faster. The build does not fail |
| QE time added to PR feedback, T1 | 20 minutes | Same. T1 runs more checks before merge by design |
| Response for gates in the merge path (H3, H5) | 4 working hours | The review goes to a named backup reviewer |
| Response for H1 and H2 | 1 working day (8 working hours) | The review goes to a named backup reviewer |
| H4 release gate | The team's release cadence | Not timed |

A late gate is **never auto-approved**.

The values live in `speed_budget` in `.aqef/config.yaml`. They are targets that drive improvement, not gates that fail the build.

## Why

- Failing a build because QE was slow punishes the developer for a QE problem. Measuring the time and fixing it in the improvement loop is the right response.
- Auto-approval on timeout would turn a speed rule into a hole in the bug filter.
- T2 and T3 escalations do not block a merge (AQEF-002), so the 4-hour target matters mainly for T1 and for triage below the confidence bar.

## Consequences

- Teams need a named backup reviewer for each gate.
- A bot must measure QE time on the PR and gate wait times. Until it exists, people report them.

## Revisit when

Scorecard data shows that the targets are always missed or always met by a wide margin.

## History

- 2026-11-23: Accepted (owner decision D2 from the review). Replaces the single `pr_feedback_minutes_max: 15` setting.
