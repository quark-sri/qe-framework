# Quality engineering (AQEF)

This repository uses AQEF for quality engineering. Follow these instructions when you write code or tests.

## Before you start a feature

- Read `.aqef/config.yaml`. Find the risk tier of the capability you change (`domain/capabilities/`).
- Use the AQEF skill for the phase. Skills are in `.claude/skills/` (Claude Code) or `skills/` (other agents):

| When | Skill |
| --- | --- |
| A spec is new or changed | `aqef-spec-review` |
| The spec is approved (H1) | `aqef-design-tests` |
| You implement a task | `aqef-implement-tests` |
| Before a PR is merged | `aqef-converge` |
| A test fails after deploy | `aqef-triage` |

## Rules

- **The spec is the oracle.** Expected results come from the acceptance criteria and `domain/`. When you design tests, do not read the implementation. If the expected result is not known, ask.
- **Do not review your own work.** Run review agents in a fresh session.
- **Do not delete, skip or weaken a test** to get a green build. The Test Guard blocks it in CI.
- **Tag every test** with `@cap`, `@req` (or `@nfr`) and `@level`. See `taxonomy/tags.md`.
- **Prove red before green.** Each new test must fail on the broken or missing behaviour first. Record the evidence in `specs/<feature>/runs/`.
- **Do not write gate metrics.** Bots write the metrics file. You read it.
- **Do not approve anything for a human.** This includes waivers, gate decisions, quarantine of a T1 test and changes to `.aqef/`. Write a proposal and ask.
- **Run tests with the commands in `.aqef/config.yaml`.** Do not invent other commands.

## Where things are

| Path | Contents |
| --- | --- |
| `.aqef/config.yaml` | Tiers, thresholds, test commands |
| `domain/` | Business rules. Start at `domain/INDEX.md` |
| `taxonomy/tags.md` | Tag rules |
| `qa/test-architecture.md` | How tests are written in this repo |
| `gates/human-gates.md` | What humans check at each gate |
| `templates/` | Output templates |
