---
run_id: <run-id>
env: <env>
build: <build>
previous_run: <run-id>
date: <YYYY-MM-DD>
---

# Release report: <release or build>

## 1. Verdict proposal
**<GO | NO-GO | GO WITH EXCEPTIONS>** — <one sentence why>

## Run summary
| Total | Passed | Failed | Skipped | Quarantined | Duration |
| --- | --- | --- | --- | --- | --- |

## Results by layer
| Level | Tests | Passed | Failed | Pass rate | Duration |
| --- | --- | --- | --- | --- | --- |
| unit | | | | | |
| component | | | | | |
| contract | | | | | |
| integration | | | | | |
| api | | | | | |
| ui | | | | | |
| nfr | | | | | |

## Results by capability
| Capability | Tier | Tests | Failed | Pass rate | Open defects | Status |
| --- | --- | --- | --- | --- | --- | --- |
| payments.refund | t1 | | | | | green / amber / red |

## 2. New failures (passed last run, fail now)
| Test | Capability | Triage state | Action | Link |
| --- | --- | --- | --- | --- |

## 3. Defect fixes verified
| Defect | Test(s) | Result |
| --- | --- | --- |

## Still failing
| Test | Since run | Triage state | Link |
| --- | --- | --- | --- |

## Fixed (failed last run, pass now)
| Test | Reason |
| --- | --- |

## 4. Capability risks (top 3)
1.

## 5. Test health
- Flake rate (gating):
- Quarantined tests (oldest):
- Mutation trend:
- Slowest suites:

## NFR
| Type | Result | Budget | Pass |
| --- | --- | --- | --- |

## Gate H4
Decision: GO / NO-GO / GO WITH EXCEPTIONS — Reviewer: — Date:
Exceptions:
