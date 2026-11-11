---
Last Update: 2026-11-05
Previous Update: 2026-11-03
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

- `/04_Career_Goals_and_Strategy/` — always include `career-tracks.md` and the role target file for the resolved track
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
- track definitions (`/04_Career_Goals_and_Strategy/career-tracks.md`) and the resolved track's role target file

### Track Resolution

1. If `job-opportunity.md` frontmatter has `track: track-2`, `track: track-3`, `track: track-4`, `track: track-5`, or `track: track-9`, use it. If analysis finds the Role Selection Test for a different track passes, state that in `## Track` as a challenge for the user to resolve; do not switch tracks silently.
2. If `track` is `MISSING` or absent, assign exactly one track using the Opportunity Routing Rule in `career-tracks.md`, and state the rationale in the `## Track` output section.
3. `track-9` is a fallback: assign it only when no Track 2, 3, 4, or 5 Role Selection Test passes, and cite the workspace source of the relevance or interest (see the Track 9 role target Entry Test).
4. If the posting spans both tracks, select the track whose positioning should lead and name the other as secondary in the rationale.
5. Do not modify `job-opportunity.md`; the assigned track is recorded in `analysis.md`.

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
- match against the resolved track's role target (must-haves, deal-breakers, and evidence map)

---

### 8.2 Career Alignment

- alignment with long-term trajectory
- positioning impact
- contribution to the resolved track's goal
- Track 1 implications (outside-work policy, network value inside the target-customer ICP) per `career-tracks.md`

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

## Track
- Track: track-2 | track-3 | track-4 | track-5 | track-9
- Source: job-opportunity frontmatter | assigned in this analysis
- Rationale (required when assigned)
- Role target: <path to role target file>

## ATS Keywords

## Resume Keyword Map

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

### Resume Keyword Map Rules

- Produce `## Resume Keyword Map` immediately after `## ATS Keywords` when
  the recommendation is `pursue` or `consider` (omit for `pass`). It is the
  input `/build-resume` uses to choose and label experience bullets.
- 6–10 themes, ranked. Each theme is one bullet block:
  - `Capability label:` the candidate's capability in standing,
    posting-independent terms, taken from the Capability Label Vocabulary
    in `resume-pack.md` (never the posting's sentence rewritten in the
    past tense)
  - `Tier:` `must-have` (posting says required or repeats it) | `core duty` |
    `nice-to-have`
  - `Posting phrases:` verbatim phrases from the posting that evidence the theme
  - `Evidence:` the best-supported role in `02_Work_Experience/Roles/`
    (file name) and the canonical fact/metric that supports it, or
    `GAP` when no canonical evidence exists
- Evidence search is not limited to `02_Work_Experience/Roles/`. For every
  theme also search `02_Work_Experience/Projects/`, `02_Work_Experience/Stories/`
  and `03_Skills_and_Portfolio/skills-inventory.md`, and the resolved role
  target's Evidence Anchors. Current-day work lives in Projects (recent independent or portfolio work); a theme whose only evidence is
  older or narrower than a Project record must name that Project or explain
  why it does not apply. Record it as `GAP` only after this search.
- Tailor the selection and ordering of themes, not the language of the
  candidate's experience. Posting wording belongs in `Posting phrases`
  (and, where honest, inside the bullet sentence), not in the label. If
  the evidence does not support the theme's scope, record `GAP` or a
  narrower capability and carry the gap into `## Context Gaps`.
- `## ATS Keywords` stays a flat, verbatim list (scripts read it); the map
  is separate and interpretive.

### ATS Keywords Rules

- Extract likely ATS-screened keywords as a flat bullet list: required
  skills, tools, certifications, domain/industry terms, and job-title
  variants — pulled verbatim from Section 1 (Raw Source) and Section 2
  (Structured Extraction) of `job-opportunity.md`.
- Bullets MUST be exact phrases from the posting, not paraphrased,
  reordered into different wording, or invented — this section is
  grounded extraction, not interpretation.
- Produce this section regardless of the pursue/consider/pass
  recommendation (it's cheap, objective extraction, unlike Positioning
  Strategy which depends on a pursue/consider decision).
- This section is the input `scripts/generate-resume-docx.sh --ats-keywords`
  and `scripts/generate-cover-letter-docx.sh --ats-keywords` read to
  populate a generated resume or cover letter's Keywords file property —
  see `Career/01_Resume_and_Profiles/Templates/README.md`.

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

- run `/discuss-opportunity` (see section 14)
- then trigger Resume Pack
- then trigger Application Pipeline

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

## 14. Discussion and Reconciliation Phase

After `analysis.md`, `/discuss-opportunity` (orchestrated by `Pipelines/opportunity-fit-pipeline.md`) weighs the user's own fit thesis and risks against canonical evidence and records the outcome in `discussion.md`.

Rules:

- The user's position is elicited before the analysis verdict is shown
- Each user claim is checked against canonical content and the resolved track's role target, with a file citation
- Claims without canonical evidence are `gap` (not assumptions) until the user supplies evidence or owner attestation
- Strengths, gaps and risks in `analysis.md` that the user did not raise are also put to the user
- `analysis.md` is not rewritten; `discussion.md` carries Keyword Map deltas and the positioning strategy, and governs where the two differ
- True new facts reach canonical `02_`–`05_` only through per-item user-approved edits
- Hand-off to `/build-resume` and `/build-application` requires `discussion_status: closed` for opportunities added on or after 2026-11-03

---

## 16. Summary

The Opportunity Analysis Pack:

- operates on validated structured opportunity data
- enforces consistent evaluation across opportunities
- produces explicit scoring and recommendations
- prevents premature execution on weak opportunities

It ensures deterministic, grounded, and decision-ready evaluation aligned with CareerOS runtime constraints.
