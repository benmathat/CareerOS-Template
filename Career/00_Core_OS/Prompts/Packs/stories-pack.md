---
Last Update: 2026-05-05
Previous Update: 2026-04-24
---

# Stories Pack

## 1. Purpose

Provide domain-specific rules and quality gates for creating, refining, and adapting SOAR/STAR stories while preserving canonical truth and interview utility.

This pack defines constraints and expectations only. It does NOT define execution flow.

This pack defines constraints, structure, and orchestration expectations only.

Runtime behavior is governed by `Prompts/Runtime/*`. This file defines only domain-specific constraints and MUST NOT restate runtime halt, validation, routing, or context-loading mechanics.

It does NOT:
- Perform mode selection directly
- Perform source routing
- Perform context loading
- Execute tasks directly

---

## 2. Supported Task Types

- `CreateCanonicalStory`
- `RefineCanonicalStory`
- `GenerateApplicationVariant`
- `UpdateStoryInventory`

Each task type maps to Mode Layer behavior (typically `build` or `refine`).

**Task Rules:**

- Each task MUST be independently valid and executable
- Tasks MUST NOT contain execution logic
- Tasks MUST align with Mode and Output contracts

---

## 3. Source Routing Hints

Canonical:
- `Career/02_Work_Experience/Stories/`

Execution (tactical variants):
- `Career/07_Applications_and_Interviews/Interview_Prep/Stories/`

Inventory:
- `Career/07_Applications_and_Interviews/Interview_Prep/story-inventory.md`

Supporting evidence:
- `Career/02_Work_Experience/`

Rules:
- Canonical sources are authoritative
- Tactical sources are contextual and must not override canonical truth

Additional Rules:

- Missing canonical grounding MUST be surfaced as a gap
- Conflicts between sources MUST be surfaced, not resolved silently
- Supporting evidence MUST be traceable to source files

---

## 4. Constraints

- Canonical stories MUST remain neutral (no company/role targeting)
- Tactical variants MUST NOT overwrite canonical truth
- Metrics MUST be real or explicitly labeled as gaps
- Ownership MUST be clearly attributed (self vs team/delegated)
- No fabrication of events, scope, or outcomes

Additional Constraints:

- No unsupported claims may be introduced

---

## 5. Quality Gates

All outputs MUST pass the following:

1. Structure completeness
   - Includes Situation / Objective / Action / Result (or STAR/SOAR equivalent)

2. Evidence quality
   - Concrete details and quantified outcomes where available
   - Missing metrics explicitly labeled as "data gap to validate"

3. Ownership clarity
   - Clear distinction between personal contribution and team context

4. Interview utility
   - Includes "When to Use"
   - Includes competency alignment

5. Cross-file consistency
   - Claims align with source files in `02_Work_Experience`

Additional Requirements:

- Assumptions are explicitly labeled when present
- Context gaps reflect impact on story completeness
- Output aligns with context status (complete vs partial)

---

## 6. Naming and Placement Rules

- Canonical filenames MUST be neutral (no employer/application prefixes)
- Canonical stories are long-form and durable
- Tactical variants are purpose-built and contextual
- Canonical truth MUST NOT be moved into tactical files

---

## 7. Output Expectations

Defer to:
- `output-standards.md`

Additional requirements:
- Include "When to Use"
- Include competency alignment
- Preserve traceability to source context

Output Rules:

- Outputs MUST include required disclosures (assumptions, gaps, warnings)
- Outputs MUST align with `output-standards.md`
- Outputs MUST reflect context status (complete vs partial)

---

## 8. Task-Specific Guidance

### CreateCanonicalStory
- Long-form, durable
- Evidence-first
- No application-specific framing

- Surface any missing details as context gaps
- Do NOT infer metrics or outcomes without labeling

### RefineCanonicalStory
- Improve clarity, structure, and metrics
- Preserve original truth

- Do NOT introduce new facts
- All improvements MUST be traceable to original content

### GenerateApplicationVariant
- Compress and tailor for role/company
- Adapt framing only; do NOT change facts

- Preserve all facts and outcomes exactly
- Any assumptions for tailoring MUST be labeled

### UpdateStoryInventory
- Maintain mappings to canonical story files
- Ensure competency/question alignment is accurate

- Inventory MUST reflect canonical truth only
- No inferred mappings without explicit justification

---

## 9. Validation Hooks

- Structure completeness check
- Evidence quality check
- Ownership clarity check
- Cross-file consistency check
- Output compliance with `output-standards.md`

- All content is traceable to source or labeled assumptions
- No unsupported or fabricated claims are present
- Context gaps are surfaced where applicable

---

## 12. Summary

This pack provides domain-specific constraints and validation for story work.

It ensures deterministic, grounded, and interview-ready story outputs aligned with CareerOS runtime constraints.