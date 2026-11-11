---
Last Update: 2026-11-11
Previous Update: 2026-11-05
---

# Resume Pack (Execution Pack Contract)

## 1. Purpose

Provide a **pre-configured execution pack** for generating and refining resumes using CareerOS.

This pack defines constraints, structure, and orchestration expectations only.

Runtime behavior is governed by `Prompts/Runtime/*`. This file defines only domain-specific constraints and MUST NOT restate runtime halt, validation, routing, or context-loading mechanics.

It does NOT:
- Perform mode selection directly
- Perform source routing
- Perform context loading
- Execute tasks directly

---

## 2. Pack Interface

### 2.1 Inputs (Required)

```yaml
request:
  target_role: <string>
  job_description: <text | file reference>
  track: <track-2 | track-3 | track-4 | track-5 | track-9> # resolved from opportunity analysis/record
  role_target: <resolved canonical role-target file reference>
```

### 2.2 Inputs (Optional)

```yaml
request:
  base_resume: <file reference>
  story_inventory: <file reference>
  portfolio_artifacts: <file reference>
  constraints:
    page_limit: <1 | 2>
    emphasis: <string>
```

### 2.3 Outputs

```yaml
artifact:
  type: Document
  destination: /06_Job_Opportunities/<company>_<role>_<YYYY-MM-DD>/
  naming:
    pattern: resume.md
```

---

## 3. Execution Profile

### Mode

- Primary: `build`
- Secondary (optional): `refine` (post-pass only)

### Workflow Pattern

**Canonical → Context → Output**

---

## 4. Routing Inputs (for source-routing.md)

The pack MUST provide normalized routing inputs:

```yaml
mode_selection:
  primary_mode: build
task:
  artifact_state: new | existing (if base_resume provided)
  output_type: Document
request:
  pipeline: resume
  intent: role-specific resume generation
```

Expected routing behavior:
- Canonical (`02_–05_`) as primary
  - includes the resolved track's role target file in `04_Career_Goals_and_Strategy/Role_Targets/` (track from `analysis.md` `## Track`, else `job-opportunity.md` frontmatter; mapping in `04_Career_Goals_and_Strategy/career-tracks.md`)
- Execution (`06_`) for job context
- Presentation (`01_`) optional as baseline

### Track Resolution and Positioning Rules

- Resolve exactly one employment track (`track-2`, `track-3`, `track-4`, `track-5`, or `track-9`) from `analysis.md` `## Track`; fall back to `job-opportunity.md` frontmatter only when the analysis track is absent or `MISSING`. An explicitly unsupported analysis value must be corrected before generation.
- If both sources contain valid, different tracks, use analysis only when it explicitly records reassignment, the prior track, and rationale. Otherwise surface the conflict and reconcile through `/analyze-opportunity` before generating or updating targeted materials; do not silently choose one.
- If neither source contains a valid track, resolve it through `/analyze-opportunity` using `04_Career_Goals_and_Strategy/career-tracks.md`. Missing or unsupported track values are blocking for targeted resume/cover-letter generation, not a reason to inherit a baseline's framing.
- Load the resolved track's role target using `04_Career_Goals_and_Strategy/career-tracks.md`. A missing role target is blocking.
- Reuse the resolved track throughout resume, cover letter, application notes, and application record; do not ask the user to restate an already resolved assignment.

- The role target's Positioning Statement and Resume Tailoring Focus govern headline, Executive Profile framing, and bullet emphasis.
- Prefer an optional matching track baseline registered in `01_Resume_and_Profiles/README.md`. If none exists, build from canonical evidence and the role target. A missing baseline is non-blocking.
- The master is a comprehensive content baseline; its current summary is not a default across tracks. A mismatched baseline may supply verified achievements, but its positioning must be rewritten for the resolved track.
- Do not blend another track's lead narrative. Shared achievements remain usable when they support the target mandate and retain their actual scope.
- `track-9` has no fixed headline: choose one functional frame per posting from canonical evidence at its actual scope, and record the frame and its canonical sources in `application-notes.md`. Requirements the posting names that are absent from canonical content are stated gaps or assumptions, never implied by wording.
- Track-specific framing MUST NOT alter canonical facts or turn partial evidence into claimed ownership (especially Track 4 benefits realization).
- Record the track, role-target path, optional baseline path (`NONE` if unused), and positioning rationale in runtime context and opportunity `application-notes.md`; keep these internal notes out of shared resume content.
- Content-only refinement preserves the resolved track. If a new track is requested, reconcile opportunity analysis first, then revisit headline, Executive Profile, and achievements together.

Rules:

- Canonical sources are authoritative
- Contextual sources MUST NOT override canonical truth
- Missing canonical grounding MUST be surfaced as a gap
- Conflicts between sources MUST be surfaced, not resolved silently

---

## 5. task (Strict Schema)

The pack MUST construct a valid `task` object:

```yaml
task:
  objective: Create a role-tailored resume aligned to the target role.
  scope:
    in_scope:
      - Resume content aligned to role priorities
      - Quantified achievements where available
      - Internal resume-positioning provenance in opportunity application notes
    out_of_scope:
      - Cover letter generation
      - Portfolio site changes
  inputs:
    required:
      - Work experience (canonical)
      - Skills (canonical)
      - Job description (execution)
      - Resolved employment track and governing role target
    optional:
      - Base resume
      - Story inventory
      - Portfolio artifacts
  constraints:
    hard:
      - Page limit: 3 pages unless the user sets a different limit
    soft:
      - Prefer concise, high-signal bullets
      - Avoid generic phrasing
  success_criteria:
    - Aligns to top role priorities
    - Uses quantified impact where available
    - No filler content
    - Headline, Executive Profile, and bullets reflect one resolved track
  output_type: Document
```

task Rules:

- `task` MUST be complete and independently executable
- `task` MUST NOT contain execution logic
- All assumptions used to fill gaps MUST be explicitly labeled

---

## 6. Output Contract (Document)

The assembler MUST enforce Document structure:

Required sections:
- Title
- Sections
- Subsections

Header and profile (three levels):
- Identity: name, then a role line in caps, `<TARGET ROLE TITLE> | <TRACK FOCUS AREA>`, using the posting's title wording and the role target's positioning area (e.g. `HEAD OF PRODUCT | PRODUCT STRATEGY & DEVELOPMENT`). It states the role pursued, not a title previously held, and goes in `## Headline`. The contact line follows.
- Profile: `## Executive Profile`, a short paragraph (about three sentences) with three layers: strategic (product strategy and organizational development), operational (establishing functions, leading cross-functional execution), and technical (staying hands-on). Do not state total years of experience ("20+ years"); lead with scope and outcomes (age-signal rule, `work-preferences.md` Resume Presentation: Age Signals). No metrics, and no industry-specific positioning (such as hosting or cybersecurity) unless the posting's industry is itself the target; those details belong in the experience entries.
- Value: the labeled experience bullets. Do not restate them in a highlights or skills block.

Keyword-labeled experience (required when `analysis.md` has a `## Resume Keyword Map`):
- Each Professional Experience entry starts with a 1–2 sentence plain description of the role (employer context, mandate, scope) directly under the dates line, drawn from the role's canonical Context/Details; then the keyword-labeled bullets. The description carries no label and does not repeat the bullets' metrics.
- Every employer renders in one model: employer name; `Location | overall tenure` only for multi-position employers; then `Position Title | Position dates`, a brief role description, and selected accomplishments. Single-position employers omit the location/tenure line.
- Multiple consecutive positions at one employer are written as separate entries (own dates, description, bullets); the renderer groups them under a single employer heading. Do not repeat employer context in each description, and do not split one label across both positions of the same employer.
- Every Professional Experience bullet is `- **<Label>:** <one sentence of evidence>`, with the metric inline where one exists.
- Labels are capability names from the Capability Label Vocabulary below, selected through the Keyword Map. They describe the candidate's capability in standing terms, not the posting's wording rewritten in the past tense. The sentence must trace to the role's canonical file and may not exceed its scope. Tailor the selection and prioritization of accomplishments, not their underlying language; posting keywords may appear inside the sentence only where they are the honest description of what was done.
- 3–5 labeled bullets for recent/most relevant roles, 1–2 for older roles. A given label is bold-labeled in at most 2 roles. Order within a role: must-have, then core duty, then nice-to-have.
- Skip any theme marked `GAP`; never stretch evidence to cover it. Surface skipped themes in the run's context gaps.
- Summary and Core Skills are replaced by `## Executive Profile` (paragraph only). `## Core Capabilities` (about six capabilities, two-column intent; renders as one list today) is optional and omitted by default; include it only for larger or process-heavy employers, never for a small founding team. It must not repeat bullet text; capability names come from the Keyword Map.
- Accomplishment rule: every bullet states what the user did and what changed because of it (a measurable result, a decision made, a process or framework now in use). A bullet that only describes a responsibility ("Owned...", "Connected...", "Managed...") fails. If the canonical records do not establish the change, do not publish the bullet as written: ask the user for the intervention and result (what was introduced, changed, improved or stopped), record the answer in the role's canonical file, then use it.
- Significance rule: express business impact consistently. Besides the intervention and the change, each bullet says why the change mattered, in terms of scope (teams, products or customers affected), risk avoided, a decision it enabled, or time and cost. More metrics are not the goal; explain what changed and why it was consequential. Process and governance work (operating models, intake, compliance) must name its scope and what it made possible. If the canonical records do not establish the significance, ask the user.
- Three layers rule: separate each accomplishment into outcome (what was delivered or changed), capability (what expertise made it possible), and implementation (methods and technologies). Lead with outcome and capability. Name tools, languages, or frameworks only when the posting makes them a specific qualification, and then at most one or two; otherwise keep them in canonical supporting evidence.
- Capability Label Vocabulary (extend only with standing capability names, never posting phrases): Product strategy and roadmap; Packaging and pricing; Product operating model; Product function establishment; Product organization development; Portfolio prioritization; Backlog and portfolio management; Engineering partnership; Customer research; User experience design; AI-enabled product development; Hands-on product development; Early-stage product development; Privacy and compliance; Release and quality management; Platform and ecosystem development.
- Emphasis rule: bold only the accomplishment label and, selectively, the single most significant numerical result in the bullet. Do not bold technology names, frameworks, policies, concepts, or role descriptions.
- The Keyword Map itself is internal; record it in `application-notes.md`, not the resume.

Pack-specific section schema:
- Header (Name + Contact)
- Executive Profile (replaces Summary + Core Skills; Core Capabilities optional)
- Professional Experience
- Education (if applicable)

Quality requirements:
- High signal density
- Role alignment
- Quantified achievements where available
- No fluff or repetition

Additional Rules:

- All claims MUST be grounded in context or explicitly labeled assumptions
- Metrics MUST be real or explicitly marked as gaps
- Output MUST align with `output-standards.md`
- Output MUST reflect context status (complete vs partial)

---

## 8. Refine Pass (Optional)

Trigger conditions:
- User request
- Validation improvements desired (clarity, concision)

Refine task (delta-focused):

```yaml
task:
  objective: Improve clarity, concision, and impact of the existing resume.
  scope:
    in_scope:
      - Bullet clarity
      - Redundancy removal
    out_of_scope:
      - Structural redesign
  inputs:
    required:
      - Generated resume
  constraints:
    hard:
      - Preserve content accuracy
    soft:
      - Increase signal density
  success_criteria:
    - Clearer bullets
    - Reduced redundancy
  output_type: Document
```

Rules:

- Refinement MUST preserve the resolved track and role-target positioning
- Refinement MUST NOT introduce new facts
- All improvements MUST be traceable to original content
- Assumptions MUST be explicitly labeled if introduced

---

## 9. Output Routing

Destination:
- `/06_Job_Opportunities/<company>_<role>_<YYYY-MM-DD>/resume.md`

Rules:
- Do not overwrite canonical sources
- Treat opportunity-tailored resumes as execution artifacts scoped to the opportunity folder
- Reusable baselines (master, templates, shareable) remain under `/01_Resume_and_Profiles/`

Additional Rules:

- Outputs MUST NOT modify canonical sources
- Outputs MUST be traceable to source context
- No artifacts may be written if validation fails

Note: this pack produces the markdown resume only. A shareable, formatted
copy (DOCX/PDF) for actual submission is a separate, deterministic step —
`scripts/generate-resume-docx.sh <path-to-resume.md>` — and is the primary
method for that conversion; when the input is opportunity-folder `resume.md`,
the script defaults to a long opportunity-named DOCX/PDF in the same folder.
It is not part of this pack's runtime contract.
See `Career/01_Resume_and_Profiles/Templates/README.md`.

---

## 10. Validation Gates (Pack-Level)

Before finalization:
- [ ] Exactly one valid employment track resolved; conflicting assignments explicitly reconciled
- [ ] Governing role target loaded; any baseline checked for track and evidence freshness
- [ ] Headline, Executive Profile, and achievements follow that track without overstating scope
- [ ] Track provenance recorded internally and excluded from shareable resume content
- [ ] Each bullet says what changed and why it mattered (scope, risk, decision enabled, time or cost), including process and governance bullets
- [ ] Bullets lead with outcome and capability; implementation detail (tools, languages) appears only when the posting makes it a specific qualification
- [ ] Every experience bullet states an intervention and its result; any responsibility-only bullet was resolved by asking the user
- [ ] Every experience entry opens with a 1–2 sentence role description; every experience bullet carries a Capability Label Vocabulary label chosen through the Keyword Map (when a map exists); no `GAP` theme claimed; no label in more than 2 roles
- [ ] Prose edit pass run per `Career/05_Personal_Profile/writing-style.md`; remaining `careeros lint` warnings fixed or deliberately kept (non-blocking)
- [ ] Meets page constraint
- [ ] Matches Document structure
- [ ] Claims traceable to context or labeled assumptions
- [ ] No canonical vs presentation boundary violations

- [ ] Assumptions are explicitly labeled when present
- [ ] Context gaps are surfaced where applicable
- [ ] No unsupported claims exist
- [ ] Output aligns with context status (complete vs partial)

---

## 12. Example Invocation (Normalized)

```yaml
request:
  target_role: Transformation Portfolio and Governance Manager
  track: track-4
  role_target: /04_Career_Goals_and_Strategy/Role_Targets/role-target-portfolio-transformation-governance.md
  job_description: <file>
  base_resume: <optional file>

runtime:
  primary_mode: build
  output_type: Document
  workflow_type: resume
```

---

## 13. Summary

The Resume Pack:

- Provides a deterministic interface to the runtime
- Encodes task, routing inputs, and output contract
- Produces consistent, high-quality resume artifacts

It ensures deterministic, grounded, and role-aligned resume generation aligned with CareerOS runtime constraints.