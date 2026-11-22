---
name: aqef-design-tests
description: AQEF phases 2 and 3. Designs Gherkin scenarios, assigns test levels and owners, designs synthetic test data, reviews the plan and adds test tasks to the task list. Use after gate H1 is approved.
---

# AQEF phases 2–3: Design tests

## Steps
1. Run `scenario-designer`. Output: `features/<capability>/<feature>.feature`.
2. Run `test-strategist`. Output: `@level` tags and the level matrix in `specs/<feature>/test-plan.md`.
3. Run `nfr-test-designer` for scenarios tagged `@nfr`.
4. Run `test-data-designer`. Output: `specs/<feature>/test-data-plan.md`.
5. Run `test-plan-reviewer` in a fresh context. Output: Plan review section with ACCEPT or ESCALATE.
6. If ESCALATE: send findings back to the agent that owns each item (steps 1–4). Repeat at most 2 times.
7. Apply gate H2 rules from `.aqef/config.yaml` (T1 always; T2 on ESCALATE; T3 on sample). Wait for the decision if H2 applies.
8. **Tasks (phase 3):** add test tasks to the feature task list.
   - Unit scenarios → tasks for the dev coding agent, placed before or with the code task.
   - Other levels → tasks for the Automation Engineer.
   - Each task lists its scenario IDs and tags.
9. Run the Traceability Bot to seed the matrix. Gate: every criterion has at least one planned scenario.

## Outputs
Feature files, `test-plan.md`, `test-data-plan.md`, updated task list, traceability matrix.
