# Agents

Each file defines one LLM agent. The front matter follows the Claude Code subagent format (`name`, `description`, `tools`). Other agent tools can load the body as instructions.

| Agent | Phase | Writes |
| --- | --- | --- |
| spec-critic | 1 | `spec-review.md` |
| risk-analyst | 1 | Risk section of `spec-review.md` |
| domain-curator | 0, 1, 8 | KB pull request |
| scenario-designer | 2 | `.feature` files |
| test-strategist | 2 | Levels and level matrix |
| test-data-designer | 2 | `test-data-plan.md` |
| test-plan-reviewer | 2 | Plan review section |
| nfr-test-designer | 2, 4 | NFR scenarios and scripts |
| automation-engineer | 4 | Test code and run log |
| fault-seeder | 4 | Private fault patches, detection rate |
| coverage-traceability-analyst | 4, 5 | `gaps.md` |
| test-review-panel | 4 | `quality-report.md` |
| failure-triage | 5, 7 | Triage records |
| test-fixer | 7 | Test fix PR |
| defect-reporter | 7 | Defect ticket |
| report-analyst | 8 | `release-report.md` |

## Separation of duties

- Designer, writer and judge are different agents with separate context windows.
- Scenario Designer and Automation Engineer must not read private implementation code.
- Fault Seeder output is hidden from writer agents.
- Review agents are read-only.

## Common rules for all agents

1. Read `domain/INDEX.md` first. Then read only the files you need.
2. Write output to the fixed path, with the fixed template.
3. Cite evidence for every decision: file and line, criterion ID, rule ID, run ID or log line.
4. Give a confidence value (0 to 1) for every decision.
5. Stop and escalate when the spec and the KB disagree.
