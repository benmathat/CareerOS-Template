---
name: analyze-opportunity
description: Evaluate a confirmed opportunity record and produce a decision-ready analysis.
argument-hint: "<opportunity folder or job-opportunity.md path>"
---

# /analyze-opportunity

## Purpose
Evaluate a confirmed structured opportunity record and produce a decision-ready analysis.

## Use When
- `job-opportunity.md` exists
- `intake_status: confirmed`
- You need a pursue / consider / pass recommendation

## Required Inputs
- `/06_Job_Opportunities/<company>_<role>_<date>/job-opportunity.md`

## Validation
Before execution, verify:

- `intake_status: confirmed`
- Required sections exist:
  - Raw Source
  - Structured Extraction

If validation fails:
- STOP execution
- return missing requirements

## Instructions
1. Use `Career/00_Core_OS/Prompts/Packs/opportunity-analysis-pack.md` as the governing workflow.
2. Do not read raw PDFs directly unless the opportunity record is incomplete and the user explicitly asks.
3. Use canonical sources in `02_`–`05_` for evaluation. Search `02_Work_Experience/Projects/` and `03_Skills_and_Portfolio/skills-inventory.md` as well as `Roles/` for every theme, including recent independent or portfolio work; do not mark a theme `GAP` before that search.
4. Resolve the career track per the Opportunity Analysis Pack's Track Resolution rules:
   - use `track` from `job-opportunity.md` frontmatter when set
   - otherwise assign exactly one track (`track-2`, `track-3`, `track-4`, `track-5`, or `track-9`) using `Career/04_Career_Goals_and_Strategy/career-tracks.md`, with rationale
   - load the resolved track's role target file and evaluate Role Fit and Career Alignment against it
   - record the result in the `## Track` section of `analysis.md`
5. Score the opportunity using all required dimensions:
   - Role Fit
   - Career Alignment
   - Compensation
   - Company Context
   - Risk
   - Opportunity Value
   - All dimensions MUST be scored (1–5)
6. Extract likely ATS keywords verbatim from the job posting (Raw Source /
   Structured Extraction sections of `job-opportunity.md`): required
   skills, tools, certifications, domain terms, job-title variants. Do not
   paraphrase or invent — see the Opportunity Analysis Pack's ATS Keywords
   Rules. Produce this regardless of the recommendation.
   Then, for `pursue`/`consider`, add `## Resume Keyword Map` per the Opportunity Analysis Pack's Resume Keyword Map Rules (ranked themes with a capability label from the resume pack's vocabulary, tier, verbatim posting phrases, evidence role or `GAP`).
7. Produce the analysis artifact in the required structure defined in the Opportunity Analysis Pack.
   - All required sections MUST be present
8. Produce exactly ONE recommendation:
   - pursue
   - consider
   - pass
9. Save output to the same folder as the input file:
   `/06_Job_Opportunities/<opportunity-folder>/analysis.md`

## Must NOT
- create, edit, move, or delete anything other than `analysis.md` in the same opportunity folder (not `job-opportunity.md`, resumes, or application files)
- change `track`, `status`, or `intake_status` in `job-opportunity.md`; a track is recorded in `analysis.md` only
- generate resumes, cover letters, or application artifacts
- read raw PDFs unless the record is incomplete and the user asks
- edit `02_`–`05_` canonical sections, the tracker, or the work search log
- commit, push, or stage anything unless the user asks

## Failure Handling
- If required context is missing:
  - do not infer
  - explicitly list missing context

## Output
- `analysis.md`
- pursue / consider / pass recommendation

## Runtime IO Emission (Required)

Start the run file with `scripts/careeros new-run analyze-opportunity <slug> --target <opportunity-folder>`. It prefills the derivable fields; replace every `TODO` with grounded content before running the gate (the gate fails while any remain).
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
- `scripts/run_command_gate.sh "Career/00_Core_OS/Runs/<YYYY-MM-DD>_analyze-opportunity_<slug>.runtime-io.yaml"`
- Happy path example: runtime file `Career/00_Core_OS/Runs/<YYYY-MM-DD>_analyze-opportunity_<slug>.runtime-io.yaml` -> run `scripts/run_command_gate.sh "Career/00_Core_OS/Runs/<YYYY-MM-DD>_analyze-opportunity_<slug>.runtime-io.yaml"`

Fail/stop rules:

- If any required gate check fails, STOP finalization.
- Set `validation_result.passed: false`.
- Set `artifact_destination.write_allowed: false`.
- Populate `execution_trace.halted_at` and `execution_trace.reason`.
- Do not write or update artifacts until gate status is `pass`.