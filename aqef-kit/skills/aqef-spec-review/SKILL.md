---
name: aqef-spec-review
description: AQEF phase 1. Makes a feature spec testable, sets the risk tier and proposes knowledge base updates before planning. Use after a spec is written or changed.
---

# AQEF phase 1: Spec review

## Steps
1. Run the `spec-critic` agent on `specs/<feature>/spec.md`.
2. Run the `risk-analyst` agent. It adds the tier and the risk table to `spec-review.md`.
3. Run the `domain-curator` agent in "detect" mode. It lists new terms and rules and opens a KB PR if needed.
4. Post a summary for gate H1: number of findings by severity, open questions, proposed tier.
5. Stop. Wait for the H1 decision. Record it in `specs/<feature>/gates.md`.

## Exit criteria
- H1 decision is APPROVE.
- Every acceptance criterion has an ID.
- The tier is set.

## Outputs
`specs/<feature>/spec-review.md`, KB PR (optional), `gates.md` entry.
