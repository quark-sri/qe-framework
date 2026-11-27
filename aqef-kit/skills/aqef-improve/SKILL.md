---
name: aqef-improve
description: AQEF improvement loop for the team's process. Each sprint it turns escaped defects into one recorded change each, reviews how well each gate and bot works, and fills the sprint scorecard. Use at the end of each sprint or before a retrospective. Runs in your coding agent session; no API key is needed (AQEF-001).
---

# AQEF: Improve the process

Each sprint, the process learns from what it missed and what it cost (AQEF-006). Agents propose changes. Humans approve them through the normal gates.

## Inputs
- The defects found after release in this sprint (an export or a list from the defect tracker)
- `reports/escapes/` (earlier escape records)
- The gate logs `specs/*/gates.md` for this sprint
- `.aqef/config.yaml`

## Steps
1. **Escape review.** For each defect found after release that has no record, write `reports/escapes/ESC-<nnn>.md` from `templates/escape-record.md`. Propose `should_have_caught`, `miss_reason` and one change. The QE lead confirms the record.
2. **Make the change.** Each record gets one change through the normal path: a test (with `@defect:<id>`), a KB rule (run `domain-curator`, gate H6), a defect pattern, an agent instruction, a threshold or a gate check. Propose threshold and gate changes; do not edit `.aqef/` yourself.
3. **Open records.** List each record from earlier sprints that is still `open`. A record open for more than one sprint goes to the QE lead.
4. **Gate effectiveness.** From the gate logs, count for each gate: reviews, reviews that found a real problem, and the median wait in working hours. Compare the wait with `speed_budget`.
   - A gate that found no real problem in the last 3 months and has a cost: propose to relax it (for example, from always to a sample).
   - A stage named in `should_have_caught` by 2 or more escapes in a quarter: propose to make it stronger.
   - Never propose to relax a blocking fact (AQEF-002) or the T1 test review (H3).
5. **Scorecard.** Fill `templates/scorecard.md` and save it as `reports/scorecards/<sprint>.md`. Use the formulas in the template. Count; do not estimate. If a number is not available, write "not measured".
6. **Report.** Post one ranked list of proposed changes to the team. Each item has its evidence and an owner.

## Output
- Escape records in `reports/escapes/`
- `reports/scorecards/<sprint>.md`
- A ranked list of proposed changes

## Must not
- Close an escape record without a merged change.
- Change thresholds, tiers or gates in `.aqef/` without a human approval.
- Put names, customer data or ticket text in a scorecard that leaves the team (AQEF-005).
