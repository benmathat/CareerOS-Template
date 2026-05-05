---
Last Update: 2026-05-05
Previous Update: 2026-04-22
---

# Mode Selection (Runtime Contract)

## 1. Purpose

Deterministically select the correct **primary mode** (and optional secondary mode) based on `task` intent, artifact state, transformation intent, and required output.

This file governs **mode routing at runtime** and MUST:
- Produce a single primary mode
- Minimize ambiguity
- Avoid conversational loops

This layer MUST NOT introduce task logic or override System/Mode contracts.

---

## 2. Inputs (Required for Selection)

Mode selection MUST be based on a normalized `task` object (constructed if needed):

### Required Inputs

- `task.objective`
- `task.artifact_state`: `new` | `existing` | `none`
- Urgency: `speed` | `balanced` | `depth`
- `task.output_type`: `Document` | `Framework` | `Template` | `Checklist` | `Analysis`
- `task.transformation_intent`: `none` | `format_change` | `structure_change` | `audience_adaptation` | `artifact_conversion`

### Optional Inputs

- Workflow hints (e.g., interview prep, application, networking)
- Target artifact (path or type)

### Input Rules

- If any required field is missing, it MUST be inferred or marked as an assumption
- Inference MUST be minimal and recorded in `assumptions`
- Mode selection MUST NOT modify the task intent or output type

---

## 3. Decision Table (Primary Mode)

| `task.objective` Pattern | `task.artifact_state` | `task.output_type` | Primary Mode |
|---|---|---|---|
| Create a complete artifact | new/none | Document/Template/Checklist | build |
| Evaluate quality/fit/risk | existing/any | Analysis | analyze |
| Improve an existing artifact | existing | any (same as input) | refine |
| Convert an existing artifact into a different structure/format while preserving meaning | existing | Document/Template/Checklist | transform |
| Produce immediate, usable output | any | Document/Checklist/Template | execute |
| Design systems/frameworks/workflows | any | Framework/Document | architect |

Tie-breakers (when multiple rows match):
1. If `task.output_type` = Analysis → **analyze**
2. If `task.artifact_state` = existing AND `task.objective` includes "improve" → **refine**
3. If `task.artifact_state` = existing AND `task.transformation_intent` is not `none` → **transform**
4. If Urgency = speed → **execute**
5. If scope is system-level → **architect**
6. Otherwise → **build**

---

## 4. Selection Rules

- EXACTLY ONE primary mode MUST be selected
- Prefer the **narrowest mode** that satisfies the objective
- Do NOT blend modes implicitly

Secondary mode rules:
- OPTIONAL and MUST be explicit
- Allowed only for ordered workflows (e.g., `analyze → refine`, `build → refine`)
- Secondary mode MUST NOT contradict primary mode constraints

### Sufficiency Rule

The selected primary mode MUST be sufficient to complete the task without relying on implicit secondary modes.

---

## 5. Ambiguity Handling

Ambiguity MUST be resolved without conversation when possible.

### Non-Blocking Ambiguity

- Select the most constrained valid mode
- Record assumption in rationale

### Blocking Ambiguity

- Ask ONE decision-critical question
- Provide a fallback selection using best-supported assumption

Default fallback (last resort only): **analyze**

### Determinism Enforcement

When multiple valid modes exist:

- Prefer narrower scope over broader
- Prefer modes aligned with `task.output_type`
- Prefer modes that minimize downstream context requirements

Tie-breakers MUST be consistent and documented in `rationale`.

---

## 6. Escalation Logic (Deterministic)

If `task.output_type` = Analysis
  -> analyze

Else if `task.artifact_state` = existing AND `task.objective` contains improve/refine
  -> refine

Else if `task.artifact_state` = existing AND `task.transformation_intent` is not none
  -> transform

Else if `task.objective` contains convert/transform/adapt/translate/reformat/repurpose AND meaning must be preserved
  -> transform

Else if Urgency = speed AND output must be immediately usable
  -> execute

Else if `task.objective` involves system/workflow/framework design
  -> architect

Else
  -> build

If escalation logic conflicts with Decision Table, Decision Table takes precedence and the override MUST be recorded in `assumptions`.

---

## 7. Validation Checks

Before returning selection, the system MUST verify:

- Primary mode aligns with `task.output_type`
- Primary mode does not violate Mode constraints
- Artifact State is compatible with selected mode
- Transform mode is selected when transformation intent exists and meaning preservation is required
- Exactly one primary mode is selected
- Secondary mode (if present) is ordered and non-conflicting

If validation fails:

- Recompute selection
- If still invalid, set `status: invalid` and `blocking: true`
- Do NOT return an invalid mode without flags

---

## 8. Output Contract

```yaml
mode_selection:
  status: valid|partial|invalid
  blocking: true|false
  primary_mode: build|analyze|refine|transform|execute|architect
  secondary_mode:
  rationale:
  assumptions:
  confidence: high|medium|low
```

### Output Rules

- `mode_selection.status` MUST always be present
- `mode_selection.blocking` MUST be `true` only when mode cannot be safely determined
- `mode_selection.confidence` MUST reflect ambiguity level
- `mode_selection.rationale` MUST tie directly to objective and key inputs
- `mode_selection.assumptions` MUST be present if any inference occurred

## Failure Handling

### Missing Required Inputs

- Infer minimally if possible
- If inference is not reliable:
  - Set `mode_selection.status: invalid`
  - Set `mode_selection.blocking: true`

### Ambiguous Mode Selection

- Select most constrained valid mode
- Record ambiguity in `assumptions`
- Reduce `confidence` to `medium` or `low`

### Conflicting Signals

- Prioritize in order:
  1. `task.output_type`
  2. `task.objective`
  3. `task.artifact_state`
  4. `task.urgency`
- Record override in `assumptions`

### No Valid Mode

- Set `mode_selection.status: invalid`
- Set `mode_selection.blocking: true`

---

## 9. Summary

This runtime layer ensures:

- Deterministic mode selection
- Clear separation of responsibilities
- Compatibility with `task` and output contracts
- Proper distinction between build, refine, transform, execute, analyze, and architect behavior
