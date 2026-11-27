---
sprint: <sprint id>
period: <YYYY-MM-DD> to <YYYY-MM-DD>
aqef_version: <x.y.z>
maturity_level: <1-4>
---

# Scorecard: <sprint id>

Count; do not estimate. Write "not measured" when the source does not exist yet.
To share it with the framework maintainers, copy only the numbers into the "Adopter scorecard" issue (AQEF-005).

| Metric | Formula | Source | Value | Last sprint |
| --- | --- | --- | --- | --- |
| Gate catch rate | Human gate reviews that found a real problem ÷ human gate reviews | Gate logs, "Real problem found" | | |
| Bot false-positive rate | Gatekeeper FAIL or Test Guard blocks that were not a real problem ÷ all such blocks | CI history; a block closed by a waiver or a config fix counts as not real | | |
| Escaped defects, by stage | Escape records opened this sprint, grouped by `should_have_caught` | `reports/escapes/` | | |
| QE time added to PR feedback | Median minutes of the QE steps in CI per PR | CI job times | | |
| Human gate response time | Median working hours from request to decision | Gate logs, "Wait" | | |
| Agent override rate | Agent results that a human changed ÷ agent results a human reviewed | Triage records (`human_state`), gate logs | | |
| Flake rate in gating suites | See the formula in `bots/README.md` | Flake Bot or CI reruns | | |

## Open escape records
| Record | Stage | Open since | Owner |
| --- | --- | --- | --- |

## Proposed changes (ranked)
| Change | Evidence | Owner |
| --- | --- | --- |
