# Roadmap

AQEF is a framework plus a starter kit. The framework is complete enough to pilot. The kit has these known gaps.

## Bots (deterministic)

Only the Quality Gatekeeper has a sample implementation. The others are contracts in [`aqef-kit/bots/README.md`](aqef-kit/bots/README.md).

- [ ] **Results Normalizer:** convert JUnit XML, Playwright JSON and pytest output to `schemas/test-result.schema.json`.
- [ ] **Traceability Bot:** parse `@req` tags from specs, feature files and test code; emit the matrix and the untagged list; fail on missing `@cap`, `@req`, `@level`.
- [ ] **Test Guard:** diff rules for deleted tests, new skips, removed assertions, weakened matchers and added retries. Or delegate to `qestack guard`.
- [ ] **Report Builder:** layer, capability, delta and test health views from normalized results.
- [ ] **Data Guard:** scan fixtures for real emails, card numbers and national IDs.

## Kit

- [ ] A worked end-to-end example: one spec (`SPEC-142`) taken through every phase, with the real output files.
- [ ] `AGENTS.md` entry point for coding agents other than Claude Code.
- [ ] Gatekeeper: T3 sample audit selection (`sample_audit_rate`) and per-state triage autonomy checks.
- [ ] Packaging as a Claude Code plugin, like qestack.
- [ ] Release workflow that builds `aqef-kit.zip` from the folder.

## Framework

- [ ] Calibrate the starting thresholds (mutation, seeded faults, confidence bars) on a pilot and publish the data.
- [ ] Define how the agent performance metrics (audit agreement, override rate) are collected and stored.
