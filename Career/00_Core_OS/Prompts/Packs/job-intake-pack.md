---
Last Update: 2026-04-22
Previous Update:
---

# Job Intake Pack

## 1. Purpose

Provide a **pre-configured intake workflow** for converting raw job postings (PDFs) into structured, validated opportunity records inside CareerOS.

This pack ensures:
- consistent extraction from job postings
- strict separation of raw facts vs interpretation
- zero hallucination during intake
- human validation before system promotion

This pack is the **entry point** into the Application Pipeline.

This pack defines constraints, structure, and orchestration expectations only.

Runtime behavior is governed by `Prompts/Runtime/*`. This file defines only domain-specific constraints and MUST NOT restate runtime halt, validation, routing, or context-loading mechanics.

It does NOT:
- Perform mode selection directly
- Perform source routing
- Perform context loading
- Execute tasks directly

---

## 2. Scope

Use this pack when:

- a new job posting is downloaded
- a PDF job description is added to `Career/INBOX/Job_Postings/`
- an opportunity needs to be structured before analysis

This pack MUST NOT:
- perform opportunity analysis
- make pursue/hold/pass decisions
- generate resumes or application artifacts

---

## 3. Execution Profile

### Mode

- Primary: `build`
- Secondary: `refine` (optional, for cleanup after extraction)

---

## 4. Inputs

### Required

- PDF job posting from:
  ```
  Career/INBOX/Job_Postings/
  ```

### Optional

- job posting URL
- notes from user

---

## 5. Output

### Primary Output

A populated job opportunity file using:

```
/00_Core_OS/Prompts/Templates/Artifacts/job-opportunity-template.md
```

### Output Location (Staging)

```
Career/INBOX/Job_Postings/<company>_<role>_<YYYY-MM-DD>.md
```

Output Rules:

- Output MUST align with `output-standards.md`
- All assumptions, gaps, and warnings MUST be explicitly surfaced
- Output MUST reflect context status (complete vs partial)
- No canonical sources may be modified during intake

---

## 6. Extraction Rules (CRITICAL)

### 6.1 Allowed Actions

- extract explicit facts from PDF
- normalize into structured fields
- organize content into template sections

### 6.2 Forbidden Actions

- DO NOT infer missing data
- DO NOT fabricate metrics or responsibilities
- DO NOT perform evaluation or judgment
- DO NOT classify fit or alignment

---

### 6.3 Separation of Layers

| Section | Rule |
|-------|------|
| Raw Source | direct extraction only |
| Structured Extraction | normalized facts only |
| Signal Analysis | allowed but must be clearly labeled as interpretation |

Additional Rules:

- All extracted content MUST be traceable to source text
- Ambiguous content MUST be preserved verbatim or marked as unclear
- Missing sections MUST be explicitly labeled as gaps

---

## 7. Context Handling

### Source Priority

1. PDF job posting (primary)
2. URL (if provided)
3. user notes (if provided)

### Ignore

- CareerOS canonical sources (`02-05`)
- existing resumes or applications

This is **intake only**, not analysis.

Additional Rules:

- Context MUST be limited strictly to intake sources
- No external or canonical enrichment is allowed at this stage
- Conflicts between inputs MUST be surfaced, not resolved silently

---

## 9. Review and Refinement Phase

This phase is REQUIRED before promotion.

### Human or AI Review

- validate extracted facts
- correct errors
- fill obvious missing structured fields
- remove noise

Rules:

- Refinement MUST NOT introduce new facts
- Corrections MUST be traceable to source material
- Any assumptions introduced during review MUST be labeled

---

### Update Status

```yaml
intake_status: reviewed
```

---

## 10. Confirmation Gate

Before promotion, confirm:

- extraction is accurate
- no hallucinated content
- key fields are populated
- company, role, and metadata are correct

Additional Rules:

- All context gaps MUST be explicitly acknowledged
- No ambiguous content remains unlabeled
- Output must be fully compliant with intake constraints

---

### Final Status

```yaml
intake_status: confirmed
```

---

## 11. Promotion to CareerOS

### Create Destination Folder

```
Career/06_Job_Opportunities/<company>_<role>_<YYYY-MM-DD>/
```

---

### Move Files

Move:

- staging `.md` file → rename to `job-opportunity.md`
- PDF → rename to `source-posting.pdf`

---

### Final Structure

```
Career/06_Job_Opportunities/<company>_<role>_<YYYY-MM-DD>/
  job-opportunity.md
  source-posting.pdf
```

Additional Rules:

- Promotion MUST NOT occur if validation fails
- All files MUST be traceable to original intake source

---

## 12. Post-Intake Trigger

Once promoted, this pack hands off to:

- Opportunity Analysis Pack
- Application Pipeline

---

## 16. Validation Hooks

- All extracted content is traceable to source
- No inferred or fabricated data is present
- All required fields are populated or marked `MISSING`
- All assumptions and ambiguities are explicitly labeled
- Output structure matches template exactly
- Intake status progression is correct

---

## 17. Summary

The Job Intake Pack:

- converts unstructured job postings into structured data
- enforces strict extraction discipline
- prevents early-stage hallucination or misinterpretation
- creates validated inputs for downstream analysis and pipelines

It ensures deterministic, traceable, and zero-hallucination intake aligned with CareerOS runtime constraints.
