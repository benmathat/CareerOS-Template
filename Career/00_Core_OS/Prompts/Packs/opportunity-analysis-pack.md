---
Last Update: 2026-04-22
Previous Update: 2026-04-22
---

# Opportunity Analysis Pack

## 1. Purpose

Provide a **pre-configured prompt execution pack** for evaluating structured job opportunities using CareerOS.

This pack operates on **validated opportunity records** (not raw job postings) and produces a deterministic, decision-ready evaluation.

This pack enables:
- structured decision-making
- explicit tradeoff analysis
- consistent comparison across opportunities
- clear pursue / hold / pass outcomes

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

- a job opportunity has completed **Job Intake Pack**
- the opportunity file is marked:
  ```yaml
  intake_status: confirmed
  ```
- a decision is required

This pack MUST:
- operate on structured opportunity files
- use canonical career data for evaluation

This pack MUST NOT:
- ingest raw PDFs
- perform extraction tasks
- generate application artifacts

---

## 3. Execution Profile

### Mode

- Primary: `analyze`
- Secondary: `architect` (for positioning strategy only)
- Optional: `build` (only for explicitly requested follow-on outputs)

---

### Workflow Pattern

**Structured Context → Evaluate → Score → Decide → Position**

1. Load structured opportunity file
2. Load career goals and constraints
3. Load canonical experience and skills
4. Evaluate across defined dimensions
5. Score opportunity
6. Produce recommendation
7. (Optional) define positioning strategy

---

---

## 4. Required Input Contract

### Required Input File

```
/06_Job_Opportunities/<company>_<role>_<date>/job-opportunity.md
```

### Required Fields in Input

The opportunity file MUST contain:

- Section 1: Raw Source
- Section 2: Structured Extraction
- Section 3: Signal Analysis (if available)
- Metadata:
  ```yaml
  intake_status: confirmed
  ```

If missing:
- STOP execution
- return required missing sections

---

## 5. Source Routing

### Contextual Sources

- `/06_Job_Opportunities/` (primary input)
- `/09_Research_and_Market_Intelligence/`

### Canonical Sources

- `/04_Career_Goals_and_Strategy/`
- `/02_Work_Experience/`
- `/03_Skills_and_Portfolio/`
- `/05_Personal_Profile/`

### Optional Sources

- `/07_Applications_and_Interviews/`

Rules:
- opportunity file is the **single source of role truth**
- canonical sources define **evaluation baseline**

Rules:

- Opportunity file is authoritative for role definition
- Canonical sources define evaluation baseline
- Contextual sources MUST NOT override canonical truth
- Missing canonical grounding MUST be surfaced as a gap
- Conflicts between sources MUST be surfaced, not resolved silently

---

## 6. Context Assembly Rules

### Required

- structured opportunity file
- career goals and constraints

### Optional

- compensation data
- company research
- prior application notes

### Context Budget

- max 3–5 files per domain
- prioritize structured data
- avoid re-reading raw PDFs

Additional Rules:

- Required inputs MUST be sufficient to support evaluation
- Missing required inputs MUST be surfaced as context gaps
- Assumptions MUST be explicitly labeled when used

---

## 7. Context Compression

Extract only decision-relevant data:

- role requirements
- leadership scope
- systems / domain expectations
- compensation signals
- alignment factors
- explicit and implicit risks

Remove:
- redundant narrative
- marketing language
- duplicated content

Additional Rules:

- Compression MUST preserve all decision-critical information
- No meaningful risk or signal may be removed without justification
- Context gaps MUST be surfaced if compression reveals missing detail

---

## 8. Evaluation Dimensions (STRICT)

Each dimension MUST be evaluated explicitly.

### 8.1 Role Fit

- alignment with experience
- leadership scope match
- domain familiarity

---

### 8.2 Career Alignment

- alignment with long-term trajectory
- positioning impact

---

### 8.3 Compensation & Economics

- salary vs expectations
- upside potential

---

### 8.4 Company & Market Context

- company stability
- industry relevance
- strategic value

---

### 8.5 Risk Assessment

- domain mismatch
- execution ambiguity
- credibility gaps

---

### 8.6 Opportunity Value

- learning potential
- network expansion
- future optionality

---

Evaluation Rules:

- All evaluations MUST be grounded in context or explicitly labeled assumptions
- No dimension may be skipped
- Gaps in evaluation MUST be explicitly identified

---

## 9. Decision Scoring (REQUIRED)

Assign a score (1–5) for each dimension:

- Role Fit
- Career Alignment
- Compensation
- Company Context
- Risk (inverse: lower risk = higher score)
- Opportunity Value

---

### Weighted Model

Default weighting:

- Career Alignment → HIGH
- Role Fit → HIGH
- Risk → HIGH
- Compensation → MEDIUM
- Opportunity Value → MEDIUM

---

### Output

Produce:

```yaml
scores:
  role_fit:
  career_alignment:
  compensation:
  company_context:
  risk:
  opportunity_value:

weighted_summary:

overall_recommendation:
```

---

Scoring Rules:

- Scores MUST be justified with supporting evidence
- Assumptions affecting scores MUST be explicitly labeled
- Missing data MUST be reflected in scoring rationale

---

## 10. Output Contract

### Required Structure

```markdown
# Opportunity Analysis

## Summary

## Role Fit
- Strengths
- Gaps

## Career Alignment
- Short-term
- Long-term

## Compensation

## Company Context

## Risks

## Opportunity Value

## Scoring

## Overall Assessment

## Recommendation
- pursue | consider | pass

## Positioning Strategy (if pursue or consider)
```

---

Output Rules:

- Outputs MUST align with `output-standards.md`
- Outputs MUST include required disclosures (assumptions, gaps, warnings)
- Outputs MUST reflect context status (complete vs partial)

---

## 11. Disqualifiers (HARD RULES)

Immediately return `pass` if:

- violates non-negotiables in `/05_Personal_Profile/`
- compensation below minimum threshold
- fundamentally misaligned with trajectory

---

Additional Rules:

- Disqualifier triggers MUST be explicitly stated
- Any ambiguity in disqualification MUST be surfaced as a gap

---

## 12. Follow-On Actions

Only if recommendation = pursue:

- trigger Resume Pack
- trigger Application Pipeline

If consider:

- define required missing information

If pass:

- record rationale only

---

Rules:

- Follow-on actions MUST NOT execute automatically
- All follow-on actions MUST be explicitly triggered by runtime or user

---

## 13. Output Routing

Save results to:

```
/06_Job_Opportunities/<opportunity-folder>/analysis.md
```

---

Additional Rules:

- Outputs MUST NOT modify canonical sources
- Outputs MUST be traceable to source context
- No artifacts may be written if validation fails

---

## 16. Summary

The Opportunity Analysis Pack:

- operates on validated structured opportunity data
- enforces consistent evaluation across opportunities
- produces explicit scoring and recommendations
- prevents premature execution on weak opportunities

It ensures deterministic, grounded, and decision-ready evaluation aligned with CareerOS runtime constraints.
