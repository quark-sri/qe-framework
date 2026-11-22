---
name: aqef-report
description: AQEF phase 8. Builds the layer, capability, delta, traceability and test health reports, writes the narrative and prepares gate H4. Use after every regression run in a deployed environment and before each release.
---

# AQEF phase 8: Report

## Steps
1. Report Builder bot reads normalized results for this run and the previous run in the same environment.
2. Build views:
   - Run summary
   - Layer report (unit, component, contract, integration, api, ui, nfr)
   - Capability heat map (pass rate and open defects per `@cap`, coloured by tier)
   - Delta: new failures, fixed, still failing, verified defect fixes
   - Traceability report
   - Triage report
   - Test health (flake rate, quarantine age, mutation trend, slowest tests)
   - Agent performance (decisions, audit agreement, override rate, autonomy level)
3. Run `report-analyst`. Output: `reports/<run-id>/release-report.md`.
4. For a release: post the report for gate H4. Record the decision.
5. Run `domain-curator` on escapes and on triage records with `expected_change` or `product_defect_new`.

## Outputs
Dashboard data (JSON), `release-report.md`, H4 decision, KB PR.
