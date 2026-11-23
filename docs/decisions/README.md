# Decisions

Each important decision has one home: a file in this folder. Other files state the rule in one line and cite the decision ID (for example `AQEF-001`). They do not copy the reasoning.

This keeps the repo consistent. When a decision changes, you change its file first. The `applies_to` list and a search for the ID show every file to update. `scripts/check_kit.py` fails CI when the files and the decision disagree.

To change a decision, use the `aqef-decision-change` skill in your coding agent.

These are the framework's own decisions, numbered `AQEF-nnn`. A team that adopts the kit keeps its own decisions in its repo, numbered `D-nnn`, with the same skill and template. The two series never clash.

## Index

| ID | Title | Scope | Status |
| --- | --- | --- | --- |
| [AQEF-001](AQEF-001-session-first.md) | Session-first: agents run in the team's own coding-agent sessions | This phase | Accepted |
| [AQEF-002](AQEF-002-blocking-budget.md) | Blocking budget: only facts block a merge, and the gate fails closed | Permanent | Accepted |

## File format

Copy [`aqef-kit/templates/decision.md`](../../aqef-kit/templates/decision.md). Front matter:

| Key | Meaning |
| --- | --- |
| `id` | `AQEF-` and three digits in this repo. Adopter projects use `D-` and three digits. Matches the start of the file name |
| `title` | One line |
| `status` | `proposed`, `accepted`, `superseded` or `retired` |
| `scope` | `phase` (a default for the current phase, revisit later) or `permanent` |
| `date` | Date of the last change, `YYYY-MM-DD` |
| `supersedes` | IDs this decision replaces |
| `applies_to` | Files that state this rule. Each must cite the ID |
| `retired_wording` | Old phrases that must not come back anywhere in the repo |

## What the check enforces

1. Each decision file has the required keys, and its ID is unique.
2. Each file in `applies_to` exists and cites the ID.
3. Each `AQEF-nnn` cited anywhere exists.
4. No file cites a `superseded` or `retired` decision, except other decision files.
5. No file contains a phrase from `retired_wording`, except decision files and `CHANGELOG.md`.
