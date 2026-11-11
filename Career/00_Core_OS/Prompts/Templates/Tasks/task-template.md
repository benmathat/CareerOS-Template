---
Last Update: 2026-05-05
Previous Update: 2026-04-24
---

# Canonical task template

## Purpose

Define the single canonical task schema for all CareerOS executions.

All task definitions MUST use this structure.
Mode-specific behavior is allowed only inside `mode_details`.

---

## Rules

- This template defines structure only (no execution logic)
- All top-level fields MUST be present
- Unknown values MUST be set to `MISSING`
- Assumptions and context gaps MUST be explicit
- `mode_details` is the only mode-specific extension block

---

## Canonical Schema

```yaml
task:
  id: <string | MISSING>
  name: <string | MISSING>
  objective: <string | MISSING>
  mode_intent: <build | analyze | refine | execute | architect | transform | MISSING>
  artifact_state: <new | existing | none | MISSING>
  output_type: <Document | Framework | Template | Checklist | Analysis | MISSING>
  urgency: <speed | balanced | depth | MISSING>
  transformation_intent: <none | structure_only | format_only | audience_adaptation | MISSING>
  inputs:
    required:
      - <item | MISSING>
    optional:
      - <item | NONE>
  sources:
    required:
      - <path or source reference | MISSING>
    optional:
      - <path or source reference | NONE>
    excluded:
      - <path or source reference | NONE>
  constraints:
    hard:
      - <constraint | MISSING>
    soft:
      - <constraint | NONE>
  scope:
    in_scope:
      - <item | MISSING>
    out_of_scope:
      - <item | MISSING>
  assumptions:
    - assumption: <string | NONE>
      reason: <string | MISSING>
      risk: <low | medium | high | MISSING>
      must_label_in_output: <true | false | MISSING>
  context_gaps:
    - missing_information: <string | NONE>
      why_needed: <string | MISSING>
      blocking: <true | false | MISSING>
      suggested_source: <string | MISSING>
      suggested_user_action: <string | MISSING>
  success_criteria:
    - <testable success criterion | MISSING>
  destination: <logical output path | MISSING>
  mode_details:
    <mode-specific fields only>
```

---

## Validation Checklist

- [ ] All canonical top-level fields are present
- [ ] `mode_intent` is valid and explicit
- [ ] `output_type` is valid and explicit
- [ ] `scope.in_scope` and `scope.out_of_scope` are both present
- [ ] Hard constraints are defined
- [ ] Success criteria are testable
- [ ] Assumptions and context gaps are explicit when present
- [ ] `mode_details` contains only mode-specific extensions
- [ ] No execution logic appears in the task object
