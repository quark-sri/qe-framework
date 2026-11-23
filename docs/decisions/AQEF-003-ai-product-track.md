---
id: AQEF-003
title: "AI-product track is in scope for this phase, with a narrow first version"
status: accepted
scope: phase
date: 2026-11-23
supersedes: []
applies_to:
  - README.md
  - ROADMAP.md
retired_wording: []
---

# AQEF-003: AI-product track, narrow first version

## Decision

AQEF covers teams that **build AI-powered products** (LLM features, RAG, agents), not only teams that build software with AI coding agents. The first version covers only what catches bugs at pull request time:

1. **Eval sets as tests.** Golden and adversarial cases, versioned with the prompt.
2. **Statistical pass rule.** N runs per case, a pass rate against a threshold, and a `model_variance` triage state, so a stochastic miss is not treated as flaky.
3. **Graders.** Deterministic checks first. LLM-as-judge second, with the judge model pinned and spot-checked against human labels.
4. **Regression trigger.** A change to a prompt, a model version or a retrieval index runs the eval suite.
5. **Safety set.** Prompt-injection and data-leak cases are required for features that take user input.

Deferred to a later version: drift monitoring in production, a dedicated red-team agent, bias and fairness suites, RAG split metrics.

The model calls in an eval suite belong to the team's product and use the product's own model access. AQEF itself adds no API use (AQEF-001). AQEF's own agents get eval sets too; a maintainer runs them as a skill in their coding agent.

## Why

- All five reviews (2026-11-22) found that teams building AI products get no guidance today. Half of the target audience was not served.
- The framework's own improvement loop needs evals to test AQEF's agents.
- The deferred items need production data or specialist effort, and they do not stop bugs at merge time.

## Consequences

- New kit assets in milestone v0.5: `eval-designer` agent, `aqef-eval` skill, an `eval` level, an `eval` object in the result schema, `@nfr:ai-safety`, eval thresholds per tier.
- Until v0.5 ships, the README states that the track is planned.

## Revisit when

The first version is used on a real AI feature, or teams ask for the deferred items.

## History

- 2026-11-23: Accepted (owner decision D1 from the review).
