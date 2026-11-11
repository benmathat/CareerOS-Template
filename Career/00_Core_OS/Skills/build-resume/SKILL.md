---
name: build-resume
description: Generate a tailored resume for a confirmed opportunity from canonical evidence.
argument-hint: "<opportunity folder>"
---

# /build-resume

## Purpose
Generate a tailored resume for a confirmed opportunity using CareerOS canonical evidence and the Resume Pack.

## Use When
- A confirmed opportunity record exists
- Opportunity analysis is complete
- You want to generate or update a role-tailored resume

## Required Inputs
- `/06_Job_Opportunities/<company>_<role>_<date>/job-opportunity.md`
- `/06_Job_Opportunities/<company>_<role>_<date>/analysis.md`

## Optional Inputs
- Existing `resume.md` in the opportunity folder (baseline to refine)
- Reusable presentation baselines in `/01_Resume_and_Profiles/` (master, templates, shareable)
- Story inventory
- Portfolio artifacts
- Page limit override

## Validation
Before execution, verify:
- `job-opportunity.md` exists
- `analysis.md` exists and contains `## Resume Keyword Map`
- `intake_status: confirmed`
- for opportunities added on or after 2026-11-03, `discussion.md` exists with `discussion_status: closed` (run `/discuss-opportunity` otherwise)
- Opportunity recommendation is `pursue` or explicit user override is provided
- Exactly one valid employment track and governing role target resolve under the Resume Pack's Track Resolution and Positioning Rules; unresolved conflicts are blocking

If validation fails:
- STOP execution
- return missing requirements

## Instructions
1. Use `Career/00_Core_OS/Prompts/Packs/resume-pack.md` as the governing workflow.
2. Use the confirmed opportunity record as the role-truth source.
3. Use the opportunity analysis as the positioning and prioritization source. When `discussion.md` exists, apply its `## Keyword Map Deltas` on top of the analysis map and follow its `## Resume and Cover Letter Strategy`; where the two differ, `discussion.md` governs. Do not claim anything the discussion recorded as `gap`, `accepted-risk` or `[declined]` beyond the wording it records.
4. Use canonical sources in `02_`–`05_` as the source of experience, skills, goals, and constraints.
5. Resolve the career track under the Resume Pack's Track Resolution and Positioning Rules:
   - use `analysis.md` `## Track`, falling back to opportunity frontmatter only when its analysis track is absent or `MISSING`; correct unsupported values before generation
   - accept a differing analysis track only with explicit reassignment, prior track, and rationale; otherwise reconcile before generation
   - if no valid track exists, resolve through `/analyze-opportunity`; do not position from a baseline or analysis alone
   - load the governing role target from the mapping in `Career/04_Career_Goals_and_Strategy/career-tracks.md`
   - apply its Positioning Statement and Resume Tailoring Focus to headline, Executive Profile, and achievements
   - reuse the resolved assignment; no repeated user track selection is needed
6. Use `/01_Resume_and_Profiles/` only as optional presentation input. Prefer a reviewed baseline for the resolved track; if none exists, use canonical evidence and the role target. The master's summary does not govern track positioning. Do not write opportunity-tailored resumes there.
7. Build a role-tailored resume that:
   - aligns to the role priorities identified in `analysis.md`
   - follows the resolved track's positioning and does not blend in the other track's framing
   - uses quantified achievements where available
   - opens each experience entry with a 1–2 sentence role description
   - states an accomplishment in every bullet (intervention plus result); where canonical evidence shows only a responsibility, ask the user for the missing outcome and record it canonically instead of publishing a responsibility statement
   - renders experience as keyword-labeled bullets (`- **<Label>:** evidence`) driven by `analysis.md`'s `## Resume Keyword Map`, per the Resume Pack; if the map is absent, stop and ask for it via `/analyze-opportunity` rather than inventing one
   - does not overstate domain or functional fit
   - preserves canonical truth
8. Apply Resume Pack task and output contract requirements.
8a. Before saving, run the prose edit pass in `Career/05_Personal_Profile/writing-style.md` (draft, `scripts/careeros lint`, fresh-context critique, apply only claim-preserving rewrites, re-lint). Prose rewrites never change facts, figures, dates, specific terms or causal verbs.
9. If an existing resume is provided:
   - treat it as a baseline only
   - do not allow it to override canonical truth
10. Use a default page limit of 3 pages unless the user explicitly sets a different limit.
11. Save output to the opportunity folder as `resume.md`:
    `/06_Job_Opportunities/<company>_<role>_<YYYY-MM-DD>/resume.md`
    Record track, role-target path, baseline path (`NONE` if unused), and positioning rationale in runtime context and sibling `application-notes.md`. Update only the resume-positioning notes; preserve existing application notes. Do not insert internal track labels or provenance into the submitted resume.
12. If requested, or if output quality needs improvement, run a refine pass focused on:
    - clarity
    - concision
    - signal density
    - role alignment and preservation of the resolved track; reconcile analysis before a requested track change

## Must NOT
- write `resume.md` anywhere except the opportunity folder, or write a tailored resume into `01_Resume_and_Profiles/`
- touch any file in the opportunity folder other than `resume.md` and the resume-positioning notes in `application-notes.md`; preserve all other notes
- write a cover letter, `application-record.md`, `next-steps.md`, or any tracker or log entry (see `/build-application`, `/log-activity`)
- generate DOCX/PDF files (that is the optional follow-on script step)
- put internal track labels, provenance, or `MISSING`/`TODO` markers into the submitted resume
- invent employers, titles, dates, or metrics, or edit `02_`–`05_` canonical sections
- commit, push, or stage anything unless the user asks

## Failure Handling
- If canonical evidence is weak:
  - use strongest grounded evidence available
  - explicitly surface evidence gaps
  - do not fabricate fit
- If role alignment is too weak for a credible resume:
  - stop and note that positioning is insufficient without overclaiming

## Output
- Tailored resume at `/06_Job_Opportunities/<company>_<role>_<date>/resume.md`
- Internal resume-positioning provenance in sibling `application-notes.md` (preserve other notes)
- Resume MUST:
  - satisfy Document structure
  - reflect role-specific positioning
  - remain truth-aligned
  - avoid filler and generic phrasing
  - follow `Career/05_Personal_Profile/writing-style.md` (register, no spoken-word affect or slogans, verb-led sentences, figures that say what they measure); `careeros lint` style warnings are non-blocking but each is fixed or deliberately kept

Optional follow-on (not part of this command's runtime contract): once the
markdown resume is finalized, `scripts/generate-resume-docx.sh <path-to-resume.md>`
is the primary method for producing a shareable, formatted DOCX/PDF copy —
deterministically, from `Career/01_Resume_and_Profiles/Templates/resume-template.docx`,
with page-fit checking. When the input is opportunity-folder `resume.md`, the
script defaults the shareable basename to
`resume_<INITIALS>-<company-role>-<YYYY-MM>` in the same folder (terse, standard abbreviations; see `Career/01_Resume_and_Profiles/Templates/README.md`, Shareable file names). Prefer it over
manually retyping content into a template. See that template folder's README.

## Runtime IO Emission (Required)

Start the run file with `scripts/careeros new-run build-resume <slug> --target <opportunity-folder>`. It prefills the derivable fields; replace every `TODO` with grounded content before running the gate (the gate fails while any remain).
Before finalizing, explicitly emit runtime objects defined in:

- `Career/00_Core_OS/Prompts/Runtime/runtime-io-schema.md`

Required object order:

1. `request`
2. `task`
3. `mode_selection`
4. `routing_output`
5. `context_block`
6. `prompt_object`
7. `output`
8. `validation_result`
9. `artifact_destination`
10. `execution_trace`

Rules:

- Do not skip objects.
- Preserve upstream objects if halted.
- Set `execution_trace.halted_at` and `execution_trace.reason` on failure.
- Do not write artifacts when `validation_result.passed` is `false`.

The run file skeleton comes from `scripts/careeros new-run`; its shape is defined in `Prompts/Runtime/runtime-io-schema.md`. Do not hand-write the YAML from scratch.

## Deterministic Conformance Gate (Required)
At end of command run, execute:

- `Career/00_Core_OS/Prompts/Runtime/command-conformance-gate.md`
- `scripts/run_command_gate.sh "Career/00_Core_OS/Runs/<YYYY-MM-DD>_build-resume_<slug>.runtime-io.yaml"`
- Happy path example: runtime file `Career/00_Core_OS/Runs/<YYYY-MM-DD>_build-resume_<slug>.runtime-io.yaml` -> run `scripts/run_command_gate.sh "Career/00_Core_OS/Runs/<YYYY-MM-DD>_build-resume_<slug>.runtime-io.yaml"`

Fail/stop rules:

- If any required gate check fails, STOP finalization.
- Set `validation_result.passed: false`.
- Set `artifact_destination.write_allowed: false`.
- Populate `execution_trace.halted_at` and `execution_trace.reason`.
- Do not write or update artifacts until gate status is `pass`.