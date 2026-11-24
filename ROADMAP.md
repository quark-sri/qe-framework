# Roadmap

AQEF is a framework plus a starter kit. The framework is complete enough to pilot. The kit has these known gaps.

## Bots (deterministic)

The Quality Gatekeeper and the Test Guard have sample implementations. The others are contracts in [`aqef-kit/bots/README.md`](aqef-kit/bots/README.md).

- [ ] **Results Normalizer:** convert JUnit XML, Playwright JSON and pytest output to `schemas/test-result.schema.json`.
- [ ] **Traceability Bot:** parse `@req` tags from specs, feature files and test code; emit the matrix and the untagged list; fail on missing `@cap`, `@req`, `@level`.
- [x] **Test Guard:** diff rules for deleted tests, removed tests, removed assertions, new skips and added retries (v0.2). Weakened matchers (for example `toEqual` to `toBeDefined`) are not detected yet.
- [ ] **Report Builder:** layer, capability, delta and test health views from normalized results.
- [ ] **Data Guard:** scan fixtures for real emails, card numbers and national IDs.

## Kit

- [ ] A worked end-to-end example: one spec (`SPEC-142`) taken through every phase, with the real output files.
- [x] `AGENTS.md` entry point for any coding agent (v0.3).
- [x] Day-one core: AQEF Core page, maturity levels, adoption guide, stages, stack examples, optional Gherkin, `aqef-precheck` skill (v0.3).
- [ ] Test impact selection with a nightly full run as the safety net, and a "missed by selection" metric.
- [x] Gatekeeper: T3 sample audit selection (`sample_audit_rate`) (v0.2).
- [ ] Gatekeeper: per-state triage autonomy checks.
- [x] **Waiver approval by code owners (v0.3).** CODEOWNERS owns `.aqef/` and `docs/decisions/`. With the code host's "Require review from Code Owners" setting, an agent can propose a waiver but only an owner can approve it. No extra bot code.
- [ ] Packaging as a Claude Code plugin, like qestack.
- [ ] Release workflow that builds `aqef-kit.zip` from the folder.

## AI-product track (AQEF-003, milestone v0.5)

For teams whose product calls a model. The first version covers what catches bugs at PR time:

- [ ] Eval sets as tests (golden and adversarial), versioned with the prompt.
- [ ] Statistical pass rule over N runs, and a `model_variance` triage state.
- [ ] Graders: deterministic first, then LLM-as-judge with a pinned judge model.
- [ ] Regression trigger on prompt, model or retrieval-index changes.
- [ ] Required prompt-injection and data-leak safety set.
- [ ] Kit: `eval-designer` agent, `aqef-eval` skill, `eval` level and result fields, `@nfr:ai-safety`.

Later: production drift monitoring, red-team agent, bias and fairness suites, RAG split metrics.

## Framework

- [ ] Calibrate the starting thresholds (mutation, seeded faults, confidence bars) on a pilot and publish the data.
- [ ] Define how the agent performance metrics (audit agreement, override rate) are collected and stored.
