---
name: aqef-kb-curate
description: AQEF phase 0 and learning loop. Builds or updates the markdown domain knowledge base that agents read with progressive disclosure. Use at project start, when a spec adds domain concepts, and after escapes.
---

# AQEF: Curate the domain knowledge base

## Start a new KB (phase 0)
1. Create `domain/INDEX.md` from the example. List capabilities with their default tier and one-line purpose.
2. Create `domain/glossary.md`. One line per term.
3. For the top 5 capabilities (by risk), create capability, entity, rule and workflow files.
4. Ask a domain expert to review (gate H6).

## Update the KB (any phase)
1. Run the `domain-curator` agent with the source (spec, triage record or defect).
2. Review the PR at gate H6.

## Progressive disclosure rules for all agents
1. Read `domain/INDEX.md` (always small).
2. Follow links to the capability file for the `@cap` in scope.
3. From the capability file, open only the entity, rule and workflow files the task needs.
4. Never load the whole `domain/` folder.

## File format
See `domain/README.md`.
