# Bots (deterministic automation)

Bots do exact work. They do not use an LLM. Use your CI system, scripts or existing tools. Each bot has a fixed contract.

| Bot | Input | Output | Typical tools |
| --- | --- | --- | --- |
| Execution Bot | Tags or test list, environment | Raw results, artifacts | CI jobs, dev container, `commands` in config |
| Results Normalizer | Raw results (JUnit XML, Allure, Playwright JSON, pytest, k6, ZAP, axe) | `results/<run-id>.jsonl` per `schemas/test-result.schema.json` | Small parser script |
| Traceability Bot | Specs, feature files, test tags, results | Matrix: criterion → scenario → test → last result; untagged list | Tag parser |
| Mutation Bot | Changed files | Mutation score, survivors | PIT, Stryker, mutmut, Stryker.NET |
| Flake Bot | Test list, rerun count | Flake rate, quarantine list updates | CI rerun job |
| Test Guard | Diff of test files | Violations: deleted tests, new skips, removed assertions, weakened matchers, added retries | Diff rules script; `qestack guard` |
| Quality Gatekeeper | Metrics JSON, `.aqef/config.yaml` | pass / fail / escalate and reasons | `gatekeeper.py` (sample here) |
| Report Builder | Normalized results, previous run | Dashboard data: layer, capability, delta, health | Script + Allure / Grafana / ReportPortal / BI |

## Gatekeeper sample

`gatekeeper.py` reads `.aqef/config.yaml` and a metrics file. It prints the decision and exits with code 0 (pass), 1 (fail) or 2 (escalate).

```
python3 bots/gatekeeper.py --config .aqef/config.yaml --metrics bots/example-metrics.json
```

Needs Python 3.9+ and PyYAML. `nfr_results` in the metrics file maps each NFR type to `pass` or `fail`; a type that the tier requires but has no result escalates.

Only the gatekeeper has a sample implementation. The other bots are contracts: build them with your CI and tools.
