---
id: ESC-<nnn>
defect: <defect id>
capability: <cap>
tier: <t1|t2|t3>
found_in: <production | staging | release test | customer report>
found_on: <YYYY-MM-DD>
should_have_caught: <phase 1 spec review | phase 2 test design | phase 4 tests | mutation or seeded faults | Test Guard | gatekeeper | H1 | H2 | H3 | H4 | triage>
miss_reason: <no criterion | no scenario | wrong level | weak assertion | rule missing in KB | threshold too low | gate skipped | flaky test hid it | agent instruction gap | other>
change: <link to the merged PR, issue or KB change>
change_type: <test | KB rule | defect pattern | agent instruction | threshold | gate check | spec template>
status: <open | changed | verified>
---

# Escape ESC-<nnn>: <short title>

## What happened
- Impact: <who was affected and how>
- Severity: <critical | high | medium | low> (scale in `gates/human-gates.md`)

## Why the stage missed it
<One or two sentences. Name the stage in `should_have_caught` and the reason in `miss_reason`.>

## The one change
<The change that makes the same kind of defect fail before merge next time. One change per record. If more is needed, open more records.>

## Verified
- [ ] A test tagged `@defect:<id>` fails on the old build and passes on the fix.
- [ ] The change is merged. `status` is `changed`, then `verified` after the next release.
