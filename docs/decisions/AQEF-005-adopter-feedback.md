---
id: AQEF-005
title: "Adopter feedback: opt-in, manual scorecards; no automatic data collection"
status: accepted
scope: phase
date: 2026-11-23
supersedes: []
applies_to:
  - CONTRIBUTING.md
  - .github/ISSUE_TEMPLATE/adopter-scorecard.md
retired_wording: []
---

# AQEF-005: Adopter feedback

## Decision

AQEF collects no data automatically. Teams that want to help improve the framework share a scorecard by hand:

1. The team fills in a scorecard each sprint, or the kit generates one when that tool exists. It has aggregate numbers only: gate catch rate, false-positive rate, escape rate by stage, QE time on the PR, agent override rate.
2. The team pastes it into the "Adopter scorecard" issue template. No code, no ticket text, no names.
3. Each quarter, the maintainer reviews the scorecards and proposes changes to the defaults through the RFC process.

## Why

- Enterprises and regulated teams reject tools that send data out. Automatic collection would block adoption in the teams that need QE most.
- There is no infrastructure or privacy policy for collection.
- A few good scorecards are worth more than a lot of noisy data at this stage.
- Opt-in automation is easy to add later. Removing collection once teams depend on it is hard.

## Consequences

- Default changes depend on adopters choosing to share. The maintainer may need to ask pilot teams directly.

## Revisit when

Adoption grows and adopters ask for an automated opt-in.

## History

- 2026-11-23: Accepted (owner decision D3 from the review).
