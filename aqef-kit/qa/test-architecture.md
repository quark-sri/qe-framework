# Test architecture contract

The Automation Engineer reads this file before it writes any test. The Test Review Panel checks code against it.
Fill every `<...>` for your stack. Keep it short and exact.

## Levels and tools

| Level | Framework | Location | Runs in | Max time per test |
| --- | --- | --- | --- | --- |
| unit | <JUnit 5 / pytest / Vitest> | `<src/test/unit>` | PR | 100 ms |
| component | <...> | `<...>` | PR | 1 s |
| contract | <Pact / Spring Cloud Contract> | `<...>` | PR | 1 s |
| integration | <Testcontainers> | `<...>` | PR | 5 s |
| api | <REST Assured / Playwright request / pytest + httpx> | `<...>` | PR, post-deploy | 5 s |
| ui | <Playwright / Cypress / Appium> | `<...>` | PR (smoke), post-deploy | 30 s |
| nfr | <axe, k6, ZAP, Semgrep> | `<...>` | See config | — |

## Patterns
- BDD binding: <Cucumber / pytest-bdd / playwright-bdd / none — tests name the scenario ID>
- UI: <page object or screenshot-free screen object>; locators by role and accessible name first, then test IDs. No XPath by position.
- API: one typed client per service in `<path>`. No raw URLs in tests.
- Data: builders in `<path>`; catalogue in `qa/test-data-catalogue.md`.
- Clock: inject `<Clock>`; tests set a fixed time.
- Waits: wait for a condition. Never `sleep`.
- Assertions: <AssertJ / expect>; one behaviour per test; message states the business rule.

## Naming
- Test name = scenario title in the language's style: `refundIsRejectedAfterRefundWindow`.
- File per feature: `<capability>/<feature>.<level>.<ext>`.

## Tags
Follow `taxonomy/tags.md`. Tags are mandatory: `cap`, `req`, `level`, `risk`.

## Environments
| Env | Base URL variable | Data reset | Who can run destructive tests |
| --- | --- | --- | --- |
| dev container | `BASE_URL` | per run | all |
| test | | nightly | all |
| staging | | per release | QE only |
| prod | | never | smoke read-only only |

## CI stages
1. PR: unit, component, contract, integration, api (impacted), ui smoke, SAST.
2. Merge: full affected regression in dev container.
3. Post-deploy (each env): smoke, regression, DAST baseline, a11y, perf smoke.
4. Nightly: full regression, mutation (T1), flake detection.

## Forbidden
- Shared mutable test data.
- Retries that hide failures in gating suites (max 0 in PR; quarantine instead).
- Tests that depend on run order.
- Secrets in test code.
