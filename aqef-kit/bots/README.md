# Bots (deterministic automation)

Bots do exact work. They do not use an LLM. Use your CI system, scripts or existing tools. Each bot has a fixed contract.

| Bot | Input | Output | Typical tools |
| --- | --- | --- | --- |
| Execution Bot | Tags or test list, environment | Raw results, artifacts | CI jobs, dev container, `commands` in config |
| Results Normalizer | Raw results (JUnit XML, Allure, Playwright JSON, pytest, k6, ZAP, axe) | `results/<run-id>.jsonl` per `schemas/test-result.schema.json` | Small parser script |
| Traceability Bot | Specs, feature files, test tags, results | Matrix: criterion → scenario → test → last result; untagged list | Tag parser |
| Mutation Bot | Changed files | Mutation score, survivors | PIT, Stryker, mutmut, Stryker.NET |
| Flake Bot | Test list, rerun count | Flake rate, quarantine list updates | CI rerun job |
| Test Guard | Diff between base and head | Violations: deleted test files, removed tests, removed assertions, new skips, added retries | `testguard.py` (sample here); `qestack guard` |
| Quality Gatekeeper | Metrics JSON, `.aqef/config.yaml` | PASS / FOLLOW_UP / FAIL / ESCALATE with reasons | `gatekeeper.py` (sample here) |
| Report Builder | Normalized results, previous run | Dashboard data: layer, capability, delta, health | Script + Allure / Grafana / ReportPortal / BI |

## Setup

Both sample bots need Python 3.10+ and two packages:

```
pip install -r bots/requirements.txt
```

## Quality Gatekeeper (`gatekeeper.py`)

```
python bots/gatekeeper.py --config .aqef/config.yaml --metrics metrics.json [--json]
```

| Decision | Exit code | Meaning | CI action |
| --- | --- | --- | --- |
| `PASS` | 0 | No blocking fact, no escalation that blocks | Merge. Post `advisories` as a comment |
| `FOLLOW_UP` | 0 | Escalation on a `follow_up` tier, or the PR is in the T3 audit sample | Merge. Open a task for each gate in `gates` |
| `FAIL` | 1 | A blocking fact (see the blocking budget in `docs/AQEF.md`) | Do not merge |
| `ESCALATE` | 2 | Escalation on a `block` tier, or the tier always needs H3 | Merge waits for the human gate |
| `ERROR` | 3 | Missing file, invalid YAML or JSON, or a schema violation | Fix the input. Never treat it as a pass |

Rules (framework decision AQEF-002):
- The metrics file must match `schemas/metrics.schema.json`. Bots in CI write it. Agents must not.
- Every metric in `gate.required_metrics` must be present. A missing one is a FAIL: a broken bot must not let bugs through.
- Missing `gate.advisory_metrics` give an advisory only.
- `nfr_results` maps each NFR type to `pass` or `fail`. A type that the tier requires but that has no result is an escalation.
- The T3 audit sample is picked from a hash of `feature`, so the same PR always gets the same answer.

## Test Guard (`testguard.py`)

```
python bots/testguard.py --base origin/main [--head HEAD] [--json]
```

It compares the base and head commits and checks each changed test file (`test_guard.include` in the config):

| Rule | Violation |
| --- | --- |
| `deleted_test_file` | A test file is deleted |
| `removed_tests` | Fewer test definitions than before |
| `removed_assertions` | Fewer assertions than before |
| `added_skip` | A skip, ignore, disable or focus marker is added |
| `added_retry` | A retry or rerun setting is added |

The patterns cover pytest, unittest, JUnit, TestNG, Kotlin, NUnit, xUnit, MSTest, Jest, Vitest, Mocha, Playwright, Cypress, Go and Gherkin. They count lines, so a moved or rewritten test is not a violation, but a test with fewer assertions is.

A planned removal needs a waiver in `.aqef/test-guard-waivers.yaml`:

```yaml
- path: tests/test_old_api.py
  rule: deleted_test_file
  reason: API v1 removed in SPEC-201
  approved_by: jane.doe
```

Waived violations do not fail the build. They go to the gatekeeper as `test_guard_waived`, and a human confirms them.

The Test Guard checks only that `approved_by` is filled in. Who approved is checked by your code host: copy `templates/CODEOWNERS.example` and turn on "Require review from Code Owners". Then every change to the waivers file waits for an owner's review, so an agent can propose a waiver but cannot approve it.

Exit codes: 0 clean or all waived, 1 violations, 3 bad input.

## Flake rate

The Flake Bot computes `flake_rate` for the gatekeeper:

```
flake_rate = flaky tests / tests run
```

A test is flaky when it both passes and fails on the same commit. Count the tests in the gating stages (`stages` with `gating: true`) over the last 14 days, plus the reruns of the new tests in this PR (`flake_reruns` per tier). The gatekeeper compares the result with `suite_rules.gating_flake_rate_max`.

## The other bots

The other bots are contracts: build them with your CI and tools.
