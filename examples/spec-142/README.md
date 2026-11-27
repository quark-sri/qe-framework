# Worked example: SPEC-142 Customer refunds

This folder shows one T1 feature taken through every AQEF phase. It is laid out like a project that uses the kit. The domain rules come from the kit's knowledge base: [REF-001](../../aqef-kit/domain/rules/REF-001-refund-window.md) and [REF-002](../../aqef-kit/domain/rules/REF-002-refund-amount-limit.md).

A coding agent produced it in one session. All reviewers are fictional roles. CI runs the tests and the gatekeeper on it, so it is also a regression test for the framework.

## Run it

```bash
cd examples/spec-142
python -m pytest -q                          # 20 tests
python ../../aqef-kit/bots/gatekeeper.py --config ../../aqef-kit/.aqef/config.yaml --metrics specs/SPEC-142/metrics.json
```

The gatekeeper returns ESCALATE (exit 2). That is correct: T1 work always waits for gate H3.

## The phases

| Phase | Output | What happened |
| --- | --- | --- |
| 1 Specify | [spec.md](specs/SPEC-142/spec.md), [spec-review.md](specs/SPEC-142/spec-review.md) | The review found two missing rules (F1, F2). H1 approved them, and they were added to AC2. H1 also marked accessibility not applicable: there is no user interface (F4) |
| 2–3 Plan | [test-plan.md](specs/SPEC-142/test-plan.md) | 14 scenarios in a table (no Gherkin), all at unit level. H2 approved |
| 4 Implement | [tests](tests/test_refunds.py), [code](src/refunds.py), [runs/](specs/SPEC-142/runs/) | 20 tests failed against a stub, then passed. One gap was found while writing the code: 0.005 got the wrong message. A test was added and red and green were run again |
| 4 Harden | [runs/](specs/SPEC-142/runs/) | Mutation 0.97 (68/70, 2 equivalent survivors). Seeded faults 14/14. 10 reruns, no flakes. Security scan clean |
| 5 Converge | [metrics.json](specs/SPEC-142/metrics.json), [quality-report.md](specs/SPEC-142/quality-report.md) | Gatekeeper: ESCALATE to H3, only because T1 always needs it. Accessibility shows as an advisory. H3 accepted with one recorded gap |
| 8 Report | [gates.md](specs/SPEC-142/gates.md) | Gate log with wait times and whether each gate found a real problem |

In your project, bots in CI write `metrics.json`. In this example it was written by hand from the files in `runs/`.

## What the example taught the framework

- **No user interface, no accessibility test.** T1 required an accessibility result for every change, so a change with no user interface always escalated. Now H1 can mark an NFR as not applicable with a reason (`nfr_not_applicable`). The gatekeeper shows it as an advisory.
- **Mutation testing found an invented rule.** The first code version dropped the override reason for refunds inside the window. No criterion asks for that. The rule was removed instead of being tested. The spec is the oracle.
- **Seeded faults come from the defect patterns.** DP-01 and DP-02 in the knowledge base gave the most useful faults.
