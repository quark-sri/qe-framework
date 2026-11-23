# AQEF Core

This page is the minimum that a team must do to use AQEF. Everything else in the [framework doc](AQEF.md) is optional. Add an optional part when your data shows that you need it.

## The rules

1. **The spec is the oracle.** Tests come from acceptance criteria. The agent that designs a test does not read the implementation.
2. **No agent grades its own work.** The agent or person that writes a test does not review it.
3. **Tests are protected.** Nobody deletes, skips or weakens a test to get a green build. The Test Guard checks every PR.
4. **Only facts block.** A merge waits only for a fact: a confirmed defect, a weakened test, missing evidence or a missing metric. Other findings become a follow-up or a comment ([AQEF-002](decisions/AQEF-002-blocking-budget.md)).
5. **Humans own intent and risk.** Humans approve requirements (H1) and releases (H4). T1 changes wait for a human test review (H3).
6. **Agents run in your coding-agent sessions.** No AI API keys are needed ([AQEF-001](decisions/AQEF-001-session-first.md)).
7. **Every escaped defect changes something.** It adds a test, a rule in the knowledge base or an agent instruction.

## The parts you need

| Part | What it does |
| --- | --- |
| Risk tiers | T1 (money, safety, security, privacy, legal), T2 (core journeys), T3 (the rest). The tier sets how much proof a change needs |
| Tags | Every test has `@cap`, `@req` (or `@nfr`) and `@level`. See [the tag taxonomy](../aqef-kit/taxonomy/tags.md) |
| 4 agents | `scenario-designer`, `automation-engineer`, `test-review-panel`, `failure-triage` |
| 2 bots | Test Guard (blocks weakened tests) and Quality Gatekeeper (applies the thresholds) |
| 3 human gates | H1 requirements, H3 test review (T1 always), H4 release. See [the gate checklists](../aqef-kit/gates/human-gates.md) |
| Config | [`.aqef/config.yaml`](../aqef-kit/.aqef/config.yaml): tiers, thresholds, test commands |

## Maturity levels

Each level adds proof. Move up one level when you meet the exit criteria of your current level. Each level takes one sprint or more.

| Level | You add | Exit criteria |
| --- | --- | --- |
| 1 Protected | Tags, tiers, Test Guard in CI, red-before-green for new tests, H1 and H4 | See the checklist below |
| 2 Gated | The gatekeeper runs in CI on every PR. CI produces the required metrics. H3 for T1 | Every PR in one sprint has a gatekeeper decision. No required metric is missing |
| 3 Measured | Mutation and seeded faults on T1 and T2, flake reruns, triage agent at L1, reports by capability | A baseline for each metric. Thresholds tuned to the baseline |
| 4 Improving | Agents promoted on evidence, escape reviews each sprint, a scorecard each sprint | Every escaped defect produces a recorded change within one sprint |

## Week 1: reach Level 1

| Day | Do this |
| --- | --- |
| 1 | Copy the kit (see the [README](../README.md#quick-start)). Add the Test Guard to CI. Protect `.aqef/` with CODEOWNERS |
| 2 | List your top 5 capabilities. Give each one a risk tier |
| 3 | Set the test commands for your stack in `.aqef/config.yaml` |
| 4–5 | Take one small feature through the 4 agents. Tag its tests. Record red-before-green evidence. Hold H1 and H4 |

### Level 1 checklist

- [ ] The Test Guard runs on every PR and blocks on a violation.
- [ ] Waivers need an approval from a code owner.
- [ ] The top 5 capabilities have a risk tier.
- [ ] Every new test has `@cap`, `@req` (or `@nfr`) and `@level`.
- [ ] Every new test has red-before-green evidence.
- [ ] One feature went through H1 and H4 with a written decision.
- [ ] The person or agent that wrote a test did not approve it.
