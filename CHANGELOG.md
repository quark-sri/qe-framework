# Changelog

All notable changes to AQEF. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [semantic versioning](https://semver.org/) as described in [`CONTRIBUTING.md`](CONTRIBUTING.md).

## [0.4.0] - Unreleased

Theme: the improvement loops, proven on a worked example.

### Added
- **Worked example** (`examples/spec-142/`): one T1 feature through every phase with real evidence: red and green runs, mutation, seeded faults, flake reruns, security scan, metrics, quality report and gate log. CI runs it as a regression test for the framework.
- `check_kit.py` checks the links in `examples/`.
- **`aqef-improve` skill**: each sprint, one escape record and one change per escaped defect, a gate effectiveness review and the scorecard.
- `templates/escape-record.md` and `templates/scorecard.md` (7 metrics with formulas and sources, the same as the opt-in adopter scorecard).

### Changed
- The gate log has fixed columns (`templates/gate-log.md`), including the wait time and whether the gate found a real problem, so the scorecard can count them.
- Maturity Level 4 and phase 8 use the `aqef-improve` skill.

## [0.3.0] - 2026-11-25

Theme: any team can start in a week, on any stack and any coding agent.

### Added
- **AQEF Core** (`docs/core.md`): the minimum rules and parts, 4 maturity levels with exit criteria, and the week-1 steps to Level 1.
- **Adopting AQEF** (`docs/adopting.md`): small teams (role pairs, no self-approval), existing codebases (characterization tests, tag as you touch, ratchet from baseline) and teams without formal specs (criteria from tickets, approved at H1).
- Kit `AGENTS.md`: one entry point for any coding agent (rules, skill per phase, where things are). Kit `CLAUDE.md` imports it for Claude Code.
- `stages` in the config: which commands run before the PR, on the PR, after merge, nightly and before release. `check_kit.py` checks that each stage runs only defined commands.
- Commented test commands for Java (JUnit 5 tags), Python (pytest) and Node (Vitest or Jest, Playwright) in the config.
- CODEOWNERS for `.aqef/` and `docs/decisions/`, and `templates/CODEOWNERS.example` for adopters. With "Require review from Code Owners", only an owner can approve a Test Guard waiver or a decision change.

### Changed
- Version numbers are 0.3.0 in the README and the config.
- The install step for `AGENTS.md` and `CLAUDE.md` can run again without duplicate content.
- `aqef-precheck` proposes waivers with an empty approver, so the Test Guard fails until an owner fills it in.
- The rollout plan in `docs/AQEF.md` follows the maturity levels, not a 15-week calendar.
- Gherkin is optional. Scenarios can be a table in `test-plan.md` that meets the scenario contract (ID, criteria, level, given, when, then with source). Optional `@scn` tag.
- `aqef-precheck` skill: the precheck stage, the Test Guard, and tag and red-before-green checks in the agent session before a PR.
- Defect severity scale (critical, high, medium, low) in `gates/human-gates.md`.
- Flake rate formula in `bots/README.md`.
- Level glossary in `taxonomy/tags.md`: one line per test level.
- pytest tag mapping: level, risk and suite are marker names (`level_api`), so `pytest -m` can select them.

## [0.2.0] - 2026-11-23

Theme: a fast, safe gate. QE blocks only on facts, never passes on missing data, and stops agents from weakening tests.

### Added
- **Blocking budget.** Only facts block a merge. Each tier's `on_escalate` routes other findings: `block` (T1), `follow_up` (T2) or `comment` (T3).
- Gatekeeper decision `FOLLOW_UP` (exit 0): merge, and open a follow-up task for the listed gate. Exit code 3 (`ERROR`) for bad input. `--json` output.
- Gatekeeper uses `escalate_gates` and `sample_audit_rate` (stable hash-based T3 audit sample).
- New blocking metrics: `data_guard_violations`. New escalation metric: `test_guard_waived`.
- **Test Guard bot** (`bots/testguard.py`): fails on deleted test files, removed tests, removed assertions, added skips and added retries. Covers 15 test frameworks. Waivers need a reason and an approver.
- `schemas/config.schema.json` and `schemas/metrics.schema.json`. Each config key records who enforces it (`x-aqef-enforced-by`).
- Example records in `schemas/examples/`, validated in CI.
- Agent permission contract in front matter: `kind`, `writes`, `commands`. `check_kit.py` checks it.
- `check_kit.py --root`, and tests that break a copy of the kit to prove each check works.
- **Decision registry** (`docs/decisions/`): one home per decision (`AQEF-001` session-first, `AQEF-002` blocking budget). Other files cite the ID. `check_kit.py` fails when a file states a decision without citing it, cites an unknown or superseded decision, or brings back retired wording.
- `aqef-decision-change` skill and `templates/decision.md`, so adopting teams can keep their own decisions (`D-nnn`) consistent the same way. `paths.decisions` in the config.
- Decisions AQEF-003 (AI-product track, narrow v1), AQEF-004 (speed budget) and AQEF-005 (opt-in adopter scorecards), with an "Adopter scorecard" issue template.
- `speed_budget` config section: PR time targets per tier, gate response targets, and `on_gate_timeout: backup_reviewer` (the only allowed value).
- `AGENTS.md` (and `CLAUDE.md`, which imports it) with instructions for coding agents working in this repo.
- `CHANGELOG.md`, `CONTRIBUTING.md`, `pytest.ini`, `aqef-kit/bots/requirements.txt`. README status table.

### Changed
- **Breaking:** `suite_rules.pr_feedback_minutes_max` is replaced by `speed_budget` (AQEF-004).
- **Breaking:** config key `version: 1` is now `config_version: 2`, plus `aqef_version`. New required sections `gate` and per-tier `on_escalate`.
- **Breaking:** the gatekeeper fails when a metric in `gate.required_metrics` is missing. Before, it treated a missing `new_product_defects`, `test_guard_violations`, `flake_rate` or `ui_share` as 0 and could PASS.
- **Breaking:** metrics files need `schema_version: 1` and `feature`.
- **Breaking:** test results no longer use `level: nfr`. NFR tests keep their real level and set `nfr`. A result needs `requirements` or `nfr`.
- T2 escalations no longer block the merge. H3 runs as a follow-up after merge. T3 escalations are comments.
- `test-review-panel`, `report-analyst`, `coverage-traceability-analyst` and `fault-seeder` no longer have the Bash tool. None of their steps needed it.
- Thresholds are labelled provisional in the config and the docs.
- The docs state that AQEF needs no AI API keys or tokens. Agents run in the team's coding agent session. CI runs only deterministic bots. Triage and reporting after CI are run by a person in their coding agent, on the CI artifacts.
- One term for the lifecycle: "phase" (was a mix of "stage" and "phase").

### Upgrade from 0.1
1. In `.aqef/config.yaml`: replace `version: 1` with `config_version: 2` and `aqef_version: "0.2.0"`. Add the `gate` and `test_guard` sections and `on_escalate` per tier (copy from the kit).
2. Make your CI bots write `schema_version: 1`, `feature` and every metric in `gate.required_metrics`.
3. Run `python bots/gatekeeper.py --metrics <file>`. Exit 3 lists every schema problem.

## [0.1.0] - 2026-11-22

### Added
- AQEF framework doc, 15 diagrams, starter kit (agents, skills, config, templates, gate checklists, tag taxonomy, KB example, schemas), sample gatekeeper, kit consistency check and CI.
