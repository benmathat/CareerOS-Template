---
name: build-application
description: Build a complete application package for a confirmed, analyzed opportunity.
argument-hint: "<opportunity folder>"
---

# /build-application

## Purpose
Build a complete application package for a confirmed, analyzed opportunity using the CareerOS Application Pack.

## Use When
- A confirmed opportunity record exists
- Opportunity analysis is complete
- The opportunity recommendation is `pursue`, or the user explicitly overrides
- You need application-ready materials and an execution record

## Required Inputs
- `/06_Job_Opportunities/<company>_<role>_<date>/job-opportunity.md`
- `/06_Job_Opportunities/<company>_<role>_<date>/analysis.md`

## Optional Inputs
- Existing opportunity-folder artifacts (`resume.md`, `cover-letter.md`, notes/record/next-steps)
- Reusable presentation baselines in `/01_Resume_and_Profiles/` (master, templates, shareable)
- Recruiter or contact notes
- Application questions or required short-form responses
- Submission constraints or deadline

## Validation
Before execution, verify:
- `job-opportunity.md` exists
- `analysis.md` exists
- for opportunities added on or after 2026-11-03, `discussion.md` exists with `discussion_status: closed` (run `/discuss-opportunity` otherwise)
- `intake_status: confirmed`
- analysis includes exactly one recommendation: `pursue`, `consider`, or `pass`
- recommendation is `pursue`, or explicit user override is provided
- Exactly one valid employment track and governing role target resolve under the Resume Pack's Track Resolution and Positioning Rules; unresolved conflicts are blocking

If validation fails:
- STOP execution
- return missing requirements
- do not create application artifacts

## Instructions
1. Use `Career/00_Core_OS/Prompts/Packs/application-pack.md` as the governing workflow.
2. Use the confirmed opportunity record as the role-truth source.
3. Use the opportunity analysis as the decision, positioning, and risk source. When `discussion.md` exists, follow its `## Resume and Cover Letter Strategy` (including the cover-letter angle and how accepted gaps are handled) and apply its Keyword Map Deltas; where the two differ, `discussion.md` governs. Motivation statements come from the user's own words recorded there.
   - resolve and validate the track under the Resume Pack's Track Resolution and Positioning Rules; reconcile missing/unsupported tracks or unresolved conflicts through `/analyze-opportunity` before generating targeted materials
   - carry the same resolved track and role target through resume, cover letter, and application notes/record; accept a different analysis track only with explicit reassignment and rationale
   - record track, role target, baseline path (`NONE` if unused), and positioning rationale internally; keep track labels/provenance out of submitted resume and cover letter
4. Use canonical sources in `02_`–`05_` only for grounded career evidence.
5. Use `/01_Resume_and_Profiles/` only for optional reusable presentation baselines. Prefer a reviewed matching track baseline; when none exists, use canonical evidence and the role target. Validate any existing resume or cover letter against the resolved track before reuse; rework mismatched framing under the existing artifact-update rules. Do not write opportunity-tailored materials there.
6. Build the application package with the required outputs:
   - tailored resume reference or generated resume if missing and requested
   - cover letter or supporting note if needed
   - application notes
   - next-step checklist
   - application execution record
6a. Before saving a resume or cover letter, run the prose edit pass in `Career/05_Personal_Profile/writing-style.md` on each (draft, `scripts/careeros lint`, fresh-context critique, apply only claim-preserving rewrites, re-lint). Prose rewrites never change facts, figures, dates, specific terms or causal verbs. Style warnings are non-blocking; fix each or keep it deliberately.
7. Do not overwrite existing resume, cover letter, or application files silently.
8. If an artifact already exists:
   - ask whether to update, version, or leave unchanged
9. Save all opportunity-scoped artifacts to the opportunity folder:
   `/06_Job_Opportunities/<company>_<role>_<YYYY-MM-DD>/`
10. Use fixed generic filenames in that folder:
    - `resume.md`
    - `cover-letter.md`
    - `application-notes.md`
    - `next-steps.md`
    - `application-record.md`
11. Shareable DOCX/PDF copies (via `scripts/generate-*-docx.sh`) use the terse `resume_<INITIALS>-<company-role>-<YYYY-MM>` and `cover-letter_<INITIALS>-<company-role>-<YYYY-MM>` names in the same folder (see `Career/01_Resume_and_Profiles/Templates/README.md`, Shareable file names); they are not written by this command.
12. Preserve truth boundaries:
    - do not fabricate qualifications
    - do not overstate domain or role fit (meet this by not claiming it, not by disclaiming it: submitted materials never announce or apologize for gaps; those go in `application-notes.md` and context gaps. See `writing-style.md` rule 14)
    - do not let presentation artifacts override canonical evidence
13. Update the application record with:
    - company
    - role
    - resolved track, governing role target, baseline used, and positioning rationale
    - status
    - linked opportunity
    - linked analysis
    - linked artifacts
    - next action
14. Do not write `Career/07_Applications_and_Interviews/Applications/application-tracker.md`. Fill the structured fields of `application-record.md` (company, role, status, linked artifacts, next action) completely so `/sync-application-tracker` can create or refresh the tracker row from it, and recommend that command as the next step.
15. Do not record a submission. If the user says the application has been submitted, direct them to `/log-activity`, which records the submission in `application-record.md` and updates the tracker.

## Compliance Hook
If the application is actually submitted or an external application-related action occurs:

→ Recommend: `/log-activity`

Purpose:
- document the application submission or external action as a work search activity
- link evidence such as confirmation emails or submission screenshots
- connect the compliance entry to the application record

Do NOT recommend `/log-activity` merely because internal artifacts were created.

## Must NOT
- create artifacts outside the opportunity folder, or any file beyond the five fixed filenames listed above
- overwrite an existing artifact without the user's choice to update, version, or leave it
- write to `01_Resume_and_Profiles/`, the work search log, or the tracker (use `/log-activity` and `/sync-application-tracker`)
- change `track`, `status`, or the analysis recommendation
- mark anything submitted or sent; submission is the user's action, recorded later via `/log-activity`
- commit, push, or stage anything unless the user asks

## Failure Handling
- If role alignment is too weak for credible application materials:
  - stop and state the positioning risk
  - do not create misleading artifacts
- If required application information is missing:
  - list missing inputs
  - create only non-submission artifacts if useful and explicitly allowed
- If submission evidence is unavailable:
  - allow application record update
  - mark evidence as `MISSING` if logging later

## Output
- Application package artifacts in `/06_Job_Opportunities/<company>_<role>_<date>/`
- Application execution record as `application-record.md` in that folder
- Tracker not modified; `/sync-application-tracker` creates or refreshes the row from `application-record.md`
- No canonical source files modified

## Next Step
After application materials are complete:
- generate shareable, formatted copies of the resume and cover letter for
  submission: `scripts/generate-resume-docx.sh <path-to-resume.md>` and
  `scripts/generate-cover-letter-docx.sh <path-to-cover-letter.md>`
  (deterministic markdown → DOCX/PDF; defaults to long opportunity-named
  outputs beside opportunity-folder `resume.md` / `cover-letter.md` —
  see `Career/01_Resume_and_Profiles/Templates/README.md`). Not
  part of this command's runtime contract.
- run `/sync-application-tracker` so the tracker row reflects the new application record
- submit externally if ready
- run `/log-activity` after the real-world submission or other qualifying action; it records the submission in `application-record.md` and updates the tracker

## Runtime IO Emission (Required)

Start the run file with `scripts/careeros new-run build-application <slug> --target <opportunity-folder>`. It prefills the derivable fields; replace every `TODO` with grounded content before running the gate (the gate fails while any remain).
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
- `scripts/run_command_gate.sh "Career/00_Core_OS/Runs/<YYYY-MM-DD>_build-application_<slug>.runtime-io.yaml"`
- Happy path example: runtime file `Career/00_Core_OS/Runs/<YYYY-MM-DD>_build-application_<slug>.runtime-io.yaml` -> run `scripts/run_command_gate.sh "Career/00_Core_OS/Runs/<YYYY-MM-DD>_build-application_<slug>.runtime-io.yaml"`

Fail/stop rules:

- If any required gate check fails, STOP finalization.
- Set `validation_result.passed: false`.
- Set `artifact_destination.write_allowed: false`.
- Populate `execution_trace.halted_at` and `execution_trace.reason`.
- Do not write or update artifacts until gate status is `pass`.