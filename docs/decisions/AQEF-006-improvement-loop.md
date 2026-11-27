---
id: AQEF-006
title: "Improvement loop: one change per escaped defect, gates reviewed on evidence"
status: proposed
scope: phase
date: 2026-11-27
supersedes: []
applies_to:
  - aqef-kit/skills/aqef-improve/SKILL.md
  - docs/core.md
  - docs/AQEF.md
retired_wording: []
---

# AQEF-006: Improvement loop

## Decision

1. Every escaped defect gets an escape record and one change within one sprint. A record closes only when the change is merged.
2. Each sprint, the team reviews each gate and bot check on evidence: reviews, real problems found, wait time.
   - A gate or check that found no real problem in 3 months and has a cost is proposed for relaxing, for example from always to a sample.
   - A stage that 2 or more escapes in a quarter name as `should_have_caught` is proposed for strengthening.
3. These are proposals. A human decides. The review never relaxes the blocking facts (AQEF-002) or the T1 test review (H3). Changing those needs a decision change.
4. In this phase, the `aqef-improve` skill counts the numbers in the coding-agent session. A scorecard bot is added when pilot data shows that counting by hand is a burden or gives wrong numbers.

## Why

- Owner constraint: the process must improve itself continuously. Without a rule, escapes are discussed and forgotten.
- One change per record keeps the loop small and checkable.
- Gates that catch nothing cost time on every change. Removing them on evidence keeps QE at agent pace. Removing them on opinion would weaken the bug filter, so the blocking facts and T1 H3 are excluded.
- Principle P4 says bots produce facts. A bot needs data in a fixed format first. The gate log columns and escape records create that data; the bot can follow.

## Consequences

- Teams keep a gate log with fixed columns and escape records in `reports/escapes/`.
- The QE lead confirms each escape record and owns open ones after one sprint.
- Counting by an agent can be wrong. The scorecard says "not measured" rather than guess.

## Revisit when

- Pilot data shows the 3-month and 2-escape values are too slow or too noisy.
- Manual counting takes more than 30 minutes a sprint or gives a wrong number: build the scorecard bot.

## History

- 2026-11-27: Proposed (v0.4 plan). Waiting for the owner's decision.
