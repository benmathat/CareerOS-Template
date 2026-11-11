---
Last Update: 2026-11-11
Previous Update: 2026-11-05
---

# Job Intake Pipeline

## 1. Purpose

Standardize the ingestion, extraction, validation, and normalization of job opportunity data into CareerOS.

This pipeline ensures:
- zero-hallucination intake
- structured opportunity artifacts
- traceable source grounding
- readiness for downstream evaluation (Opportunity Analysis)

This pipeline defines orchestration only. It does NOT execute logic directly.

Runtime behavior is governed by `Prompts/Runtime/*`. This file defines only workflow-specific constraints and MUST NOT restate runtime halt, validation, routing, or context-loading mechanics.

---

## 2. Scope

Applies to:
- job descriptions (PDF, URL, text)
- recruiter messages
- referral notes

Outputs:
- normalized `job-opportunity.md`
- intake status metadata

---

## 3. Stages

### Stage 1 — Source Acquisition

**Objective**
- Obtain raw job source

**Inputs**
- PDF / URL / raw text

**task**
- Validate source availability and readability

**Mode**
- `execute`

**Outputs**
- Source confirmed OR blocking error

**Rules**
- Must halt if no valid source

---

### Stage 2 — Content Extraction

**Objective**
- Extract structured content from source

**Inputs**
- Raw job source

**task**
- Parse into structured fields (title, company, responsibilities, requirements, compensation, location)

**Mode**
- `transform`

**Outputs**
- Structured extraction

**Rules**
- No inference
- All missing fields marked `MISSING`
- Ambiguous content preserved verbatim or labeled unclear

---

### Stage 3 — Normalization

**Objective**
- Convert extraction into CareerOS canonical format

**Inputs**
- Structured extraction

**task**
- Map to `job-opportunity.md` schema

**Mode**
- `transform`

**Outputs**
- Draft `job-opportunity.md`

**Rules**
- Structure MUST match template exactly
- No content modification beyond formatting

---

### Stage 3A — Track Selection

**Objective**
- Route the opportunity to exactly one career track

**Inputs**
- Draft `job-opportunity.md`
- User-stated track (optional)
- `career-tracks.md` and `Role_Targets/role-target-*.md` (routing references only)

**task**
- Apply the Opportunity Routing Rule: use the user-stated track if given, else run the Role Selection Tests (Tracks 2, 3, 4, 5, then `track-9` as fallback) against the posting's primary object of management

**Mode**
- `analyze`

**Outputs**
- `track` frontmatter value
- `### Track Selection` subsection (Track, Basis, Rationale, Secondary, Confidence)

**Rules**
- Exactly one track; secondary named in the rationale
- Rationale cites posting text, not canonical claims about the user
- No fit scoring or pursue/hold/pass
- Too thin to classify → `track: MISSING` plus a Context Gap
- Proposal only; the user confirms at review

---

### Stage 4 — Validation

**Objective**
- Ensure integrity and completeness

**Inputs**
- Draft opportunity file

**task**
- Validate schema, traceability, and completeness

**Mode**
- `analyze`

**Outputs**
- Validation report

**Rules**
- All fields present or marked `MISSING`
- All content traceable to source
- No unsupported claims

---

### Stage 5 — Refinement (Optional)

**Objective**
- Improve clarity and structure without altering meaning

**Inputs**
- Draft opportunity file
- Validation findings

**task**
- Clean formatting, remove duplication, improve readability

**Mode**
- `refine`

**Outputs**
- Refined `job-opportunity.md`

**Rules**
- No new facts introduced
- All changes traceable to source

---

### Stage 6 — Confirmation Gate

**Objective**
- Final verification before promotion

**Inputs**
- Final opportunity file

**task**
- Confirm readiness for system use

**Mode**
- `analyze`

**Outputs**
- Approved OR blocked

**Rules**
- Must halt if validation fails
- All gaps explicitly surfaced

---

### Stage 7 — Promotion

**Objective**
- Persist artifact into CareerOS

**Inputs**
- Approved opportunity file

**task**
- Save to canonical location

**Mode**
- `execute`

**Outputs**
- Stored file

**Destination**
- `Career/06_Job_Opportunities/`

**Rules**
- No write if validation failed
- Must preserve traceability to original source

---

## 4. Data Integrity Rules

- No inferred or fabricated data
- All missing data explicitly marked `MISSING`
- All content traceable to source
- Canonical sources MUST NOT be modified

---

## 5. Validation Hooks

- Source exists and is readable
- All fields populated or `MISSING`
- Content traceable to source
- No unsupported claims
- Structure matches schema
- Pipeline stage progression is valid
- `track` is a valid value with a cited rationale, or `MISSING` with a gap

---

## 6. Invocation

```text
Use Job Intake Pipeline

Source:
<job posting PDF | URL | text>
```

---

## 7. Summary

The Job Intake Pipeline ensures:

- deterministic ingestion of job data
- zero-hallucination extraction
- structured, reusable opportunity artifacts

It is the entry point for all opportunity data into CareerOS.