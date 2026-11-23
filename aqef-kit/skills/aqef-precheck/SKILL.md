---
name: aqef-precheck
description: Fast AQEF checks in the coding-agent session before a PR is opened. Runs the precheck stage, the Test Guard, and the tag and red-before-green checks, so CI finds fewer problems. Use when a task is done and before you open or update a PR.
---

# AQEF precheck

Catch problems in the session, where a fix takes minutes, not in CI. Keep it fast: run only what is listed here.

## Steps
1. Run each command in `stages.precheck.runs` from `.aqef/config.yaml`. Use the command strings from `commands`. Fix failures before you go on.
2. Run the Test Guard against the base branch: `python bots/testguard.py --base origin/<base-branch>`.
   - If it reports a violation, restore the test. If the removal is planned, add an entry to `.aqef/test-guard-waivers.yaml` with `approved_by: <owner to approve>` and tell the user. Never fill in an approver yourself.
3. Check the tags of each new or changed test (`taxonomy/tags.md`):
   - It has `@cap`, `@level`, and `@req` or `@nfr`.
   - The `@cap` exists in `domain/capabilities/`. The `@req` exists in the spec.
4. Check that each new test has red-before-green evidence in `specs/<feature>/runs/`.
5. Report the result in the session. Do not write a metrics file.

## Output

```
AQEF precheck: READY | NOT READY
- <each problem, with the file and the fix>
```

Open the PR only when the result is READY, or when the user accepts each open problem.
