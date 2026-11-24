# Adopting AQEF

Start with [AQEF Core](core.md). This page tells you how to adapt it when your team is small, when you have an existing codebase, or when you have no formal specs. You can need more than one section.

## Small team (2 to 5 people, no QE lead)

- One person can hold several roles. Write who holds each gate role in the gate log (`specs/<feature>/gates.md`).
- **Nobody approves their own work.** The person who wrote a spec does not approve it at H1 alone. The person who wrote a test, or who ran the agent that wrote it, does not approve it at H3.
- Use the [lite path](AQEF.md#lite-path-and-full-path): H1 and H4 always, other gates as follow-ups.
- Pair the roles like this:

| Role | Can also be |
| --- | --- |
| Product owner (H1) | Tech lead |
| QE lead (H1, H4) | A developer who did not write the change |
| QE engineer (H3, H5) | Any developer who did not write the tests |
| Release owner (H4) | Tech lead |

If you work alone, nobody can review your work independently. Run `test-review-panel` in a fresh session as the second review and record it. This is weaker than a human review. Do not ship T1 changes without a second person.

## Existing codebase

- **Turn on the Test Guard on day one.** It checks only the tests that a PR changes, so old tests do not block new work.
- **Tag the tests that you touch.** Do not tag the whole suite at once. When you have time, tag the T1 capabilities first.
- **Record current behaviour before you change it.** Before an agent changes T1 or T2 code that has no tests, write characterization tests. Put the current behaviour in `specs/BASELINE-<capability>/spec.md` as acceptance criteria, and tag the tests with those IDs. At H1, a human confirms that each behaviour is correct or marks it as a known defect.
- **Gate new work, not old gaps.** The gatekeeper measures each feature and the changed code, not the whole codebase. Old gaps do not block a merge.
- **Ratchet.** Measure your baseline in the first month. Set the thresholds at the baseline, then raise them. Never lower a threshold to pass a PR.
- **Quarantine old flaky tests.** Each one gets a ticket and runs in a non-gating job. A T1 test needs a human approval to go into quarantine.

## No formal specs

- **Acceptance criteria can come from the ticket.** Write them as a numbered list with IDs: `PROJ-123-AC1`, `PROJ-123-AC2`.
- **Copy the criteria into the repo** as `specs/PROJ-123/spec.md`. Agents and bots then read them without access to your ticket system.
- **If a ticket has no criteria,** copy the ticket text into `spec.md` and run the `aqef-spec-review` skill. The Spec Critic proposes criteria in `spec-review.md`. A human approves them at H1 and adds them to `spec.md`.
- **Tests cite the criteria:** `@req:PROJ-123-AC2`.
- The test design agents never invent an expected result. If the ticket does not say what must happen, they ask.
