# AQEF Starter Kit — Agentic Quality Engineering Framework

This kit adds quality engineering to an AI-agent SDLC (spec-driven development and similar).
It is tool-agnostic. It works with Claude Code, Codex, Cursor, Copilot and other agents that read markdown instructions.

Read the [framework doc](../docs/AQEF.md) first. This kit is the working part of it.

## What is in the kit

| Folder | Contents |
| --- | --- |
| `AGENTS.md`, `CLAUDE.md` | Instructions for coding agents in your repo: rules and the skill for each phase |
| `.aqef/config.yaml` | Risk tiers, gate thresholds, autonomy levels, triage confidence bars |
| `agents/` | One definition per LLM agent: role, inputs, outputs, must-not rules |
| `skills/` | One skill per phase. Each skill runs agents and bots in order |
| `bots/` | Contracts for deterministic bots, and sample `gatekeeper.py` and `testguard.py` |
| `templates/` | Output templates that agents must fill |
| `gates/human-gates.md` | Checklists for human gates H1 to H6 |
| `taxonomy/tags.md` | Tag rules for specs, features, tests, results and defects |
| `domain/` | Knowledge base skeleton with a worked example (refunds) |
| `qa/test-architecture.md` | Test architecture contract template |
| `schemas/` | JSON schemas for the config, gate metrics, normalized test results and triage records, with example records |

## How to install

1. Copy the kit into the root of your repo.
2. Edit `.aqef/config.yaml`. Set your tiers, thresholds and tool commands. Install the bot dependencies: `pip install -r bots/requirements.txt`.
3. Fill `qa/test-architecture.md` for your stack.
4. Replace the example in `domain/` with your own capabilities. Start with the top 5.
5. Install the agents and skills for your coding agent:
   - Claude Code: copy `agents/*.md` to `.claude/agents/` and `skills/*` to `.claude/skills/`.
   - Other agents: copy `agents/` and `skills/` to the root of your repo.
   - All agents: append `AGENTS.md` to your `AGENTS.md`. For Claude Code, add the line `@AGENTS.md` to `CLAUDE.md` (the kit's `CLAUDE.md` holds only that line).
6. Map the AQEF phases to your SDLC commands (table below).

## Phase mapping

| AQEF phase | Spec Kit | Kiro | BMAD (approx.) | Skill to run |
| --- | --- | --- | --- | --- |
| 1 Specify | `/specify`, `/clarify` | Requirements | Analyst / PM | `aqef-spec-review` |
| 2 Plan | `/plan` | Design | Architect | `aqef-design-tests` |
| 3 Tasks | `/tasks` | Tasks | Scrum Master | `aqef-design-tests` (task step) |
| 4 Implement | `/implement` | Task execution | Dev | `aqef-implement-tests` |
| 4–5 Before the PR | — | — | Dev | `aqef-precheck` |
| 5 Converge | `/analyze`, PR | Review | QA | `aqef-converge` |
| 6–7 Deploy, triage | CI/CD | CI/CD | — | `aqef-triage` |
| 8 Report | — | — | — | `aqef-report` |
| 0, 8 Learn | — | Steering files | — | `aqef-kb-curate` |

Command names differ by tool version. Check your tool and adjust.

## Output locations (per feature)

```
specs/<feature>/
  spec-review.md
  test-plan.md
  test-data-plan.md
  quality-report.md
features/<capability>/<feature>.feature
triage/<run-id>/<cluster-id>.md
reports/<run-id>/release-report.md
```

## Using qestack

[qestack](https://github.com/quark-sri/qestack) can supply the test review panel, the fault seeder and the gated proof steps (`/qe-prove`, `/qe-harden`).
If you use it, point `review_panel.provider` in `.aqef/config.yaml` to `qestack`. AQEF then adds the knowledge base, test level assignment, triage and capability reporting around it.

## Rules that never change

- Test design agents must not read the implementation.
- No agent reviews its own output.
- No agent deletes, skips or weakens a test to get a green build.
- A T1 failure never leaves the gating suite without a human decision.
