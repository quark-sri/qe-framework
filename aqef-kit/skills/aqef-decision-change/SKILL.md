---
name: aqef-decision-change
description: Adds, changes, supersedes or retires a project decision (D-nnn) and updates every file that depends on it, so the repo never contradicts itself. Use when the user changes a rule, a threshold, a gate or a principle, or says "change decision D-nnn", "new decision" or "we decided".
---

# Change a decision

Decisions live in one place: `paths.decisions` in `.aqef/config.yaml` (default `docs/decisions/`). Other files state the rule in one line and cite the ID. Change the decision file first, then the files that depend on it.

## Steps

1. **Find the decision.** Search the decisions folder for the topic. If none exists, copy `templates/decision.md` to `D-<next free number>-<slug>.md`. (In the AQEF framework repo itself, decisions use `AQEF-nnn`; `D-nnn` is for adopting projects.)
2. **Confirm the change with the user.** Restate the old rule and the new rule in one or two lines each. A decision is the owner's choice. Never change one on your own initiative.
3. **Edit the decision file first.**
   - Small change (wording, a detail): edit in place, update `date`, add a line to History.
   - Reversal or replacement: create a new decision with `supersedes: [D-old]`. Set the old one to `status: superseded`.
   - Move old phrases that must not come back into `retired_wording`.
4. **Find the impact.** Combine three lists, then remove duplicates:
   - The `applies_to` list of the decision (and of the old one, if superseded).
   - A search for the ID in the repo.
   - A search for the key words and numbers of the old rule. This finds copies that do not cite the ID yet.
5. **Show the plan.** For each file: the current line and the proposed line. Wait for approval.
6. **Edit the files.** In each file, state the rule in one line and cite the ID. Do not copy the reasoning. Remove copies that are not needed. Update `applies_to` to match the files that now cite the ID.
7. **Check.** Run the project check (in the AQEF repo: `python scripts/check_kit.py`). Fix every problem it reports.
8. **Record.** Add a line to `CHANGELOG.md` if the change affects users.

## Must not

- Edit dependent files before the decision file.
- Change a decision, or approve a waiver or an exception, in the owner's name.
- Leave a file that cites a superseded decision.
- Copy the full reasoning into other files.
