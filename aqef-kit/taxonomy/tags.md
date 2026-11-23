# Tag taxonomy

Tags connect specs, scenarios, tests, results and defects. Use the same tags at every level.
Gherkin tags flow into test code as annotations (JUnit `@Tag`, pytest markers, Playwright tags, NUnit categories).

## Required tags on every scenario and every automated test

| Tag | Format | Example | Rule |
| --- | --- | --- | --- |
| Capability | `@cap:<domain>.<capability>` | `@cap:payments.refund` | Must exist in `domain/capabilities/` |
| Requirement | `@req:<spec-id>-AC<n>` | `@req:SPEC-142-AC3` | One or more. Must exist in the spec. NFR tests may use `@nfr` instead |
| Level | `@level:<level>` | `@level:api` | One of: unit, component, contract, integration, api, ui |
| Risk | `@risk:<tier>` | `@risk:t1` | Inherits the capability tier unless raised |

## Optional tags

| Tag | Format | Example | Use |
| --- | --- | --- | --- |
| Suite | `@suite:<name>` | `@suite:smoke` | smoke, regression, nightly, release |
| Defect | `@defect:<id>` | `@defect:BUG-881` | Test proves a defect fix. Used by the delta report |
| NFR | `@nfr:<type>` | `@nfr:a11y` | security, perf, a11y, privacy, reliability. The test keeps its real `@level` |
| Quarantine | `@quarantine:<ticket>` | `@quarantine:FLAKY-12` | Test runs in a non-gating job only |
| Owner | `@owner:<team>` | `@owner:checkout` | Routes triage |
| Manual | `@manual` | `@manual` | Scenario that cannot be automated. Needs a reason in the plan |

## Rules

1. The Traceability Bot fails the build if a test has no `@cap` or `@level` tag, or has neither `@req` nor `@nfr`.
2. An agent must not add `@quarantine` to a T1 test without a human approval record.
3. When a defect is fixed, the fix PR adds `@defect:<id>` to the test that proves the fix.
4. Tag names use lower case. Values use the IDs from the source system.

## Mapping examples

```gherkin
@cap:payments.refund @req:SPEC-142-AC2 @level:api @risk:t1 @suite:regression
Scenario: Refund is rejected after the refund window
```

```java
@Tag("cap:payments.refund") @Tag("req:SPEC-142-AC2") @Tag("level:api") @Tag("risk:t1")
@Test void refundIsRejectedAfterRefundWindow() { ... }
```

```python
# pytest selects marker names only (pytest -m level_api). Tags with a fixed set of values
# (level, risk, suite) are marker names. Capability and requirement are marker arguments.
# Register the markers in pytest.ini.
@pytest.mark.cap("payments.refund")
@pytest.mark.req("SPEC-142-AC2")
@pytest.mark.level_api
@pytest.mark.risk_t1
def test_refund_rejected_after_window(): ...
```

```ts
test('refund is rejected after the refund window',
  { tag: ['@cap:payments.refund', '@req:SPEC-142-AC2', '@level:api', '@risk:t1'] },
  async ({ request }) => { /* ... */ });
```
