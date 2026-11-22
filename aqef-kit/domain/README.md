# Domain knowledge base (KB)

The KB is a small ontology in plain markdown. Each file is one concept. Front matter links concepts. Agents read it with progressive disclosure: `INDEX.md` first, then only linked files.

The files here show a worked example: a refund capability of an online shop. Replace it with your domain.

## Folder layout

```
domain/
  INDEX.md                  # map: capabilities, tiers, entry files (< 150 lines)
  glossary.md               # one line per term
  roles.md                  # personas and permissions
  capabilities/<cap>.md     # one per capability
  entities/<entity>.md      # data contract: attributes, ranges, states, invariants
  rules/<RULE-ID>.md        # one business rule with examples and boundaries
  workflows/<flow>.md       # state machines and sequences
  integrations/<system>.md  # external contracts
  risks/defect-patterns.md  # known failure patterns and escapes
```

## Front matter (all files)

```yaml
id: <unique id>                 # e.g. REF-001, entity.order, cap.payments.refund
type: capability | entity | rule | workflow | integration | role | risk
title: <short title>
relates_to: [<ids>]             # links in both directions
owner: <person or team>         # domain expert who approves changes
status: active | draft | retired
last_reviewed: <YYYY-MM-DD>
source: [<spec or defect ids>]
```

## Writing rules

- Short sentences. One fact per line.
- Rules always have an examples table and boundary values.
- Use the glossary terms. Do not invent synonyms.
- Never put real customer data in examples.
- Retire, do not delete. Set `status: retired` with a reason.
