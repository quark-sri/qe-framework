# Contributing to AQEF

## Run the checks

```bash
pip install -r requirements-dev.txt
python scripts/check_kit.py
pytest -q
```

CI runs the same checks, and the Test Guard runs on every pull request. A pull request must not delete, skip or weaken a test unless it adds a waiver with a reason.

## What kind of change is it?

| Change | Process | Version bump |
| --- | --- | --- |
| Typo, wording, broken link, new example | Pull request | Patch |
| New optional agent, skill, template, config key with a default, bot | Pull request with a CHANGELOG entry | Minor |
| Change to a principle (P1–P12), a blocking rule, a required config key, a schema field, or a bot exit code | RFC issue first, then a pull request | Major (minor while the version is 0.x) |

## Decisions

Framework decisions live in `docs/decisions/` (`AQEF-nnn`). To change one, follow the `aqef-decision-change` skill: change the decision file first, then the files that cite it. Changing a decision with `scope: permanent` needs an RFC.

## RFC process

1. Open an issue titled `RFC: <short title>`. State the problem, the evidence (data, escaped defects, adopter feedback), the proposal and what it costs adopters.
2. Wait at least 7 days for comments.
3. The maintainer accepts or rejects it in the issue, with the reason.
4. The pull request links the RFC and adds an upgrade note to `CHANGELOG.md`.

## Rules for kit changes

- Keep the framework tool-agnostic and stack-agnostic. Examples are fine. Hard requirements on one tool are not.
- A new config key needs an entry in `schemas/config.schema.json` with `x-aqef-enforced-by`.
- A new agent needs `kind`, `writes` and (with Bash) `commands` in its front matter, and an autonomy level in `.aqef/config.yaml`.
- A change to a bot needs tests, including the failure paths.
- Write in plain, short sentences.
