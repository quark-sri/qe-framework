# Instructions for coding agents in this repository

This repo holds AQEF, a quality engineering framework, and its starter kit (`aqef-kit/`). Read `README.md` for the layout.
`aqef-kit/AGENTS.md` is the file that adopters copy into their repos. When you change the kit itself, follow this file.

## Check your work

```bash
pip install -r requirements-dev.txt
python scripts/check_kit.py
pytest -q
```

Both must pass before you finish a change.

## Decisions

- Each framework decision has one home: `docs/decisions/AQEF-nnn-*.md`. Other files state the rule in one line and cite the ID. Do not copy the reasoning into other files.
- To add, change, supersede or retire a decision, follow `aqef-kit/skills/aqef-decision-change/SKILL.md`. Change the decision file first, then the files in its `applies_to` list.
- A decision is the owner's choice. Propose changes; never make them on your own initiative.
- `scripts/check_kit.py` fails when a file states a decision without citing it, cites an unknown or superseded decision, or brings back retired wording.

## Rules

- Session-first (AQEF-001): do not design anything that needs AI API keys or tokens in this phase.
- Never approve a waiver, an exception or a gate decision in the owner's name. Write the entry with a placeholder and ask the owner to approve it.
- Do not delete, skip or weaken a test. The Test Guard runs in CI.
- `.ai/` holds local review notes and plans. It is not committed. Do not reference it from committed files.
- Write docs in short, plain sentences.
