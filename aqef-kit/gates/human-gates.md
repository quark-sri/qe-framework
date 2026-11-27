# Human quality gates

Each gate gets a ranked agent report with evidence. The reviewer must not need to read everything.
A gate blocks the merge only when the tier says so (`on_escalate` in `.aqef/config.yaml`). Otherwise it runs as a follow-up after merge, so QE does not slow down the agents (AQEF-002).
Response targets (AQEF-004, `speed_budget` in the config): H3 and H5 within 4 working hours, H1 and H2 within 1 working day. A late gate goes to a named backup reviewer. It is never auto-approved.
Record each decision in the gate log of the feature (`specs/<feature>/gates.md`, from `templates/gate-log.md`): gate, date, reviewer, decision, wait in working hours, whether it found a real problem, notes.

| Gate | Phase | When | Who |
| --- | --- | --- | --- |
| H1 Requirement review | 1 Specify | Always | Product owner, QE lead |
| H2 Test plan review | 2 Plan | T1 always; T2 on ESCALATE; T3 10% sample | QE engineer, domain expert |
| H3 Test review after implementation | 4 Implement | T1 always, before merge; T2 on escalation and T3 on a 10% sample, as a follow-up after merge | QE engineer |
| H4 Release readiness | 8 Report | Always | Release owner, QE lead |
| H5 Triage confirmation | 7 Triage | Confidence below the bar, or a never-autonomous state | QE engineer on triage rota |
| H6 Knowledge base change | Any | Every KB PR | Domain expert |

## Defect severity

Agents and humans use one scale for product defects.

| Severity | Meaning |
| --- | --- |
| critical | A T1 capability is broken, data is lost, or security or privacy is breached. No workaround |
| high | A core journey (T2) is broken, or a T1 capability works only with a workaround |
| medium | A feature gives a wrong result, and a workaround exists |
| low | Cosmetic or text problem. The result is correct |

A confirmed new product defect blocks the merge at every severity (AQEF-002). Severity sets the release decision (H4) and the order of work.

---

## H1 Requirement review

Input: `specs/<feature>/spec-review.md`

- [ ] Every acceptance criterion has an ID and one testable outcome.
- [ ] No vague words remain ("fast", "easy", "secure") without a measure.
- [ ] Negative and error behaviour is stated (what must not happen).
- [ ] Conflicts with domain rules are resolved or recorded.
- [ ] NFR budgets are stated where needed (latency, accessibility level, security controls). An NFR marked not applicable has a reason that you agree with.
- [ ] Risk tier is correct. A T1 tier is never lowered without the QE lead.
- [ ] Open questions from the Spec Critic are answered.

Decision: APPROVE / CHANGE SPEC

## H2 Test plan review

Input: `test-plan.md`, `.feature` files, plan panel findings

- [ ] Each acceptance criterion maps to at least one scenario, including a negative one.
- [ ] Expected results agree with the domain KB rules. Spot-check 3 high-risk scenarios.
- [ ] Boundary values come from the KB rule files, not from guesses.
- [ ] Each scenario has the lowest level that can prove it. UI scenarios have a reason.
- [ ] Test data plan uses synthetic data only.
- [ ] All panel findings of severity high are closed or accepted with a reason.

Decision: APPROVE / REVISE PLAN

## H3 Test review after implementation

Input: `quality-report.md`

- [ ] Gate result is ACCEPT, or each ESCALATE reason is understood.
- [ ] Red-before-green evidence exists for each new test.
- [ ] Mutation score and seeded-fault detection meet the tier thresholds.
- [ ] No test was weakened, skipped or deleted (Test Guard report is clean).
- [ ] Panel findings of severity high are fixed.
- [ ] Spot-check 2 tests: the assertion checks the business outcome, not only a status code.

Decision: ACCEPT / REWORK TESTS

## H4 Release readiness

Input: `reports/<run-id>/release-report.md`

- [ ] No open new product defect of severity critical or high in the release scope.
- [ ] All T1 capabilities are green or have an approved exception.
- [ ] Defect fixes in scope are verified (tests tagged `@defect:` pass).
- [ ] No T1 test is in quarantine without an approved record.
- [ ] NFR results are within budget.
- [ ] The capability heat map shows no red area without an owner and a plan.

Decision: GO / NO-GO / GO WITH EXCEPTIONS (list them)

## H5 Triage confirmation

Input: `triage/<run-id>/<cluster-id>.md`

- [ ] The evidence supports the proposed state (logs, rerun result, diff).
- [ ] For "expected change": the spec or KB change is approved and linked.
- [ ] For "flaky" on T1: there is a fix ticket and a deadline.
- [ ] For "product defect": no duplicate exists.

Decision: CONFIRM / CHANGE STATE (record the correct state; this trains the agent)

## H6 Knowledge base change

Input: Domain Curator PR

- [ ] The change has a source (spec ID, defect ID or expert note).
- [ ] Rules have examples and boundary values.
- [ ] Links (`relates_to`) are correct and the index is updated.
- [ ] Tests that depend on the changed rule are listed for update.

Decision: MERGE / REVISE
