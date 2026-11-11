---
Last Update: 2026-05-05
Previous Update: 2026-04-22
---

# Context Loader (Runtime Contract)

## 1. Purpose

Define a deterministic method for selecting, compressing, and formatting context before prompt assembly.

This component converts **routing outputs** into **execution-ready context blocks**.

It MUST:
- Enforce minimal viable context
- Preserve canonical vs contextual boundaries
- Produce structured, normalized context
- Prevent hallucination through strict grounding

It MUST NOT:
- Introduce new facts
- Infer missing information without labeling
- Expand beyond routed source set

---

## 2. Inputs

The loader operates on normalized runtime inputs.

### Required Inputs

- `routing_output` (from `source-routing.md`)
  - `required`
  - `optional`
  - `excluded`
  - `output_destination`
  - `routing_reason`
- `task`
  - `objective`
  - `constraints`
  - `inputs`
  - `output_type`
  - `durability_class`
- `mode`
  - selected mode contract
  - mode-specific context requirements

### Optional Inputs

- `explicit_sources`
  - user-provided files, paths, links, or pasted content
- `prior_context`
  - already-loaded context from the current session
- `artifact_target`
  - file or destination being created, updated, or analyzed

### Input Rules

- Explicit user-provided inputs have highest priority.
- `routing_output` defines the maximum allowed source set.
- The loader MUST NOT retrieve sources outside the routed set unless the user explicitly provides them.
- The loader MUST NOT mutate task intent, mode selection, or source routing decisions.

---

## 3. Dependencies

- `source-routing.md` → defines allowed, optional, and excluded source sets
- `mode-selection.md` → ensures mode compatibility and mode-specific context requirements
- `prompt-assembler.md` → consumes formatted context and blocking/gap flags
- `execution-flow.md` → determines whether execution may continue, pause, or halt
- `interaction-model.md` → handles user-facing clarification when blocking gaps exist
- `output-standards.md` → defines downstream output expectations
- `career-index.md` → high-signal file discovery

---

## 4. Load Sequence (Deterministic)

1. Normalize explicit task inputs into temporary context blocks
2. Load `explicit_sources` if provided
3. Load `routing_output.required`
4. Validate whether required context satisfies the task and selected mode
5. Evaluate `routing_output.optional` only if gaps remain
6. Exclude any `routing_output.excluded`
7. Apply tier classification rules
8. Apply conflict resolution rules
9. Compress all selected sources into normalized blocks
10. Validate output contract before handoff

The loader MUST NOT:
- Skip required sources
- Load optional sources preemptively
- Load excluded sources under any condition

The loader MUST explicitly record whether context is:

- `complete`
- `partial_non_blocking`
- `partial_blocking`

This status MUST be passed to `prompt-assembler.md` and `execution-flow.md`.

---

## 5. Context Tiers

The loader MUST classify every loaded source into one tier:

1. `canonical_context`
   - Durable truth sources
   - Usually from `/02_`, `/03_`, `/04_`, `/05_`

2. `contextual_context`
   - Opportunity-, application-, interview-, networking-, or workflow-specific sources
   - Usually from `/06_`, `/07_`, `/08_`, `/09_`

3. `supporting_context`
   - Optional reference material, research, coaching notes, or compliance context
   - Usually from `/09_`, `/10_`, `/11_`

Presentation artifacts MUST NOT be promoted to canonical context.

---

## 6. Source Selection Rules

- Always include explicit task inputs first
- Load required sources fully before considering optional sources
- Add optional sources ONLY if they resolve gaps or improve task alignment
- Respect domain boundaries defined in routing layer

Limits:
- Default: 3–5 files per domain
- Expand ONLY when required to satisfy `task` constraints

---

## 7. Context Extraction Rules

For each selected source, extract ONLY high-signal elements:

### Required Extraction

- Facts (verifiable statements)
- Metrics (quantified data)
- Constraints (explicit limits)
- Decisions (previously made and relevant)
- Gaps (missing or incomplete information)

### Optional Extraction

- Supporting examples (only if directly relevant)

### Remove

- Narrative repetition
- Stale or irrelevant details
- Duplicate claims from weaker sources
- Presentation-only phrasing

---

## 8. Context Compression Rules

Context MUST be:

- Structured
- Minimal
- Non-redundant

Compression priorities:

1. Specificity over breadth
2. Quantified over qualitative
3. Recent over stale (when applicable)
4. Canonical over contextual

### Blocking Rules

The loader MUST return `context_block.status: partial_blocking` when any of the following are true:

- Required canonical context is missing for a task that creates, updates, or modifies a durable artifact.
- Required routed sources cannot be loaded.
- The selected mode requires evidence that is unavailable.
- A material source conflict cannot be resolved deterministically.
- Compliance-sensitive output would be produced without required compliance context.

The loader MAY return `context_block.status: partial_non_blocking` with gaps when:

- Missing context is useful but not required.
- The task can be completed safely from canonical context alone.
- The output can be explicitly labeled as draft, provisional, or assumption-based.

If contextual context is missing, execution may continue only if the task can be completed from canonical context alone and the output clearly identifies remaining gaps.

---

## 9. Output Contract

The loader MUST return a normalized context block:

```yaml
context_block:
  status: complete|partial_non_blocking|partial_blocking
  task_alignment:
    objective:
    mode:
    output_type:
    durability_class:
  canonical_context:
    - path:
      source_type:
      key_facts:
      key_metrics:
      constraints:
      decisions:
      freshness:
      relevance_to_task:
  contextual_context:
    - path:
      source_type:
      key_facts:
      key_metrics:
      constraints:
      decisions:
      freshness:
      relevance_to_task:
  supporting_context:
    - path:
      source_type:
      key_facts:
      constraints:
      freshness:
      relevance_to_task:
  context_gaps:
    - missing_information:
      why_needed:
      blocking: true|false
      suggested_source:
      suggested_user_action:
  conflicts:
    - conflict:
      sources:
      resolution:
      materiality: low|medium|high
  assumptions:
    - assumption:
      reason:
      risk:
      must_label_in_output: true|false
  warnings:
    - type:
      description:
  handoff:
    prompt_assembler_ready: true|false
    execution_may_continue: true|false
    required_user_clarification:
```

Rules:

- `context_block.status` MUST always be present.
- `task_alignment` MUST always be present.
- `handoff` MUST always be present.
- Every source MUST include `relevance_to_task`.
- Empty context tier sections MUST be omitted, not filled with placeholders.
- `context_gaps` MUST be explicit and actionable.
- `conflicts` MUST appear when materially relevant source disagreement exists.
- `assumptions` MUST only appear if inference was required.
- Any assumption that affects user-facing output MUST set `must_label_in_output: true`.

---

## 10. Context Gap Handling

If required information is missing:

- Add an entry to `context_gaps`
- Identify the minimal file, source, or user input needed
- Mark whether the gap is blocking
- Set `status` to `partial_blocking` or `partial_non_blocking`
- Do NOT infer or fabricate missing data

If gaps are blocking:

- Set `handoff.prompt_assembler_ready: false`
- Set `handoff.execution_may_continue: false`
- Populate `handoff.required_user_clarification`

If gaps are non-blocking:

- Set `handoff.prompt_assembler_ready: true`
- Set `handoff.execution_may_continue: true`
- Require downstream output to label uncertainty, limitation, or missing context when relevant

---

## 11. Conflict Resolution

When sources conflict:

1. Canonical overrides contextual
2. More specific overrides general
3. More recent overrides older (if time-sensitive)
4. Quantified overrides qualitative

Conflicts MUST be:
- surfaced
- not silently resolved if materially impactful

Conflict records MUST include:

- source paths
- conflicting claims
- selected resolution rule
- materiality level
- downstream warning if the conflict affects output quality

---

## 12. Failure Handling

### Missing Required Source

- Record source in `context_gaps`
- Set `context_block.status: partial_blocking`
- Halt downstream assembly through `handoff`

### Missing Optional Source

- Record source only if relevant to task quality
- Set `context_block.status: partial_non_blocking` only when gaps are material
- Continue with available context

### Excluded Source Requested

- Do NOT load the source
- Add warning explaining exclusion
- Continue only if required context remains sufficient

### Over-Budget Context

- Trim using:
  - relevance to task
  - specificity
  - quantified evidence
  - canonical priority
  - recency when time-sensitive

### Insufficient Context

- Do NOT expand arbitrarily
- Return minimal viable context plus explicit gaps
- Mark status as `partial_blocking` or `partial_non_blocking`

### Source Conflict

- Apply conflict resolution rules
- Record unresolved material conflicts
- Block execution if the conflict prevents grounded output

---

## 13. Validation Checks

- All required sources are included or explicitly recorded as missing
- No excluded sources are present
- Optional sources are included only when justified
- Context is minimal, not exhaustive
- All entries are grounded in actual sources
- Canonical, contextual, and supporting tiers are correctly separated
- Context gaps are actionable
- Material conflicts are recorded
- Blocking status is correctly set
- Handoff flags are consistent with status
- Output structure matches contract

---

## 14. Summary

This layer ensures:

- Deterministic context selection
- Minimal and high-signal inputs
- Strict grounding in CareerOS truth
- Clean handoff to prompt assembly

It is the grounding and completeness control point before prompt assembly and execution. It does not decide whether to ask the user questions, perform task work, or format final output; it only determines whether the assembled context is sufficient, insufficient-but-usable, or insufficient-and-blocking.
