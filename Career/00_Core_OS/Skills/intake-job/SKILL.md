---
name: intake-job
description: Ingest a raw job posting (PDF, URL, or text) into a draft staging file in Career/INBOX/Job_Postings/. Never promotes or commits.
argument-hint: "<PDF path | URL> [track-2|track-3|track-4|track-5|track-9 to override selection] [work type]"
---

# /intake-job

## Purpose
Process a raw job-posting source (PDF, URL, or text) through the Job Intake Pipeline to produce a structured staging opportunity file.

## Use When
- A new PDF job posting has been downloaded
- The opportunity has not yet been structured
- Job Intake Pack should be run
- A job source (PDF, URL, or text) needs to be ingested into CareerOS

## Required Inputs
- A job source in `Career/INBOX/Job_Postings/` (PDF preferred), OR
- A URL or raw text of the job posting

## Optional Inputs
- Career track (`track-2`, `track-3`, `track-4`, `track-5`, or `track-9`) if the user states it; it overrides intake selection. Otherwise intake selects one — see `Career/04_Career_Goals_and_Strategy/career-tracks.md`

## Validation
Before execution, verify:
- A readable source exists (PDF, URL, or text)
- The source is the intended target

If validation fails:
- STOP execution
- request correct input

## Instructions
1. Invoke the Job Intake Pipeline:
   - `Career/00_Core_OS/Prompts/Pipelines/job-intake-pipeline.md`

2. Use the artifact template:
   - `Career/00_Core_OS/Prompts/Templates/Artifacts/job-opportunity-template.md`

3. Ensure the pipeline produces a staging file in:
   - `Career/INBOX/Job_Postings/`

4. Enforce filename normalization (applied during pipeline normalization stage):
   - `<company>_<role>_<YYYY-MM-DD>.md`

5. Ensure metadata fields are populated:
   - source_pdf (or source reference)
   - source_platform (if known)
   - date_downloaded
   - intake_status = draft (the command never sets `reviewed` or `confirmed`; only the user does, after review)
   - track = user-stated value, otherwise the track selected in step 6; `MISSING` only when selection is blocked (see step 6)

6. Select the career track (Pipeline Stage 3A, after normalization):
   - read only `career-tracks.md` (Opportunity Routing Rule and routing heuristics) and the five employment `Role_Targets/role-target-*.md` files, and only to classify the posting
   - apply the Role Selection Tests in order: Track 2, Track 3, Track 4, Track 5; choose `track-9` only when none passes and relevance can be traced to workspace content (see the Track 9 Entry Test)
   - if the user stated a track, record it and write `Basis: user-stated`; do not re-select
   - assign exactly one track; when the posting spans tracks, pick the track whose positioning should lead and name the other as secondary
   - write the result to frontmatter `track` and to the `### Track Selection` subsection of Signal Analysis: `Track`, `Basis` (`user-stated` | `intake-selected`), `Rationale` (cite posting text), `Secondary`, `Confidence` (high | medium | low)
   - if the posting is too thin to classify (low confidence between two or more tracks, or a missing description), set `track: MISSING`, state why under Context Gaps, and leave the decision to `/analyze-opportunity`
   - the selection is a draft proposal: the user confirms or overrides it during review, before `/promote-opportunity`

7. Ensure outputs comply with:
   - `job-intake-pack.md`
   - `output-standards.md`

8. DO NOT:
   - bypass the pipeline
   - perform manual extraction outside pipeline stages
   - infer missing facts (track selection is the one sanctioned classification, and it cites the posting)
   - perform opportunity analysis
   - create, move, or copy anything into `Career/06_Job_Opportunities/` (that is `/promote-opportunity`, and only after the user reviews the draft)
   - move, rename, or delete the source PDF
   - commit, unless the user explicitly asks in the same request

9. Ensure all missing required fields are set to `MISSING`

10. Ensure all context gaps are surfaced explicitly in the output

## Failure Handling
- Follow pipeline failure handling:
  - halt on blocking conditions
  - surface context gaps
  - request minimal required inputs

- Do NOT perform recovery logic outside the pipeline

## Output
- Staging opportunity file in `Career/INBOX/Job_Postings/`
- Output MUST be produced via the Job Intake Pipeline
- File MUST include:
  - metadata
  - Raw Source
  - Structured Extraction
  - no empty required fields

## Runtime IO Emission (Required)

Start the run file with `scripts/careeros new-run intake-job <slug>`. It prefills the derivable fields; replace every `TODO` with grounded content before running the gate (the gate fails while any remain).
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
- `scripts/run_command_gate.sh "Career/00_Core_OS/Runs/<YYYY-MM-DD>_intake-job_<slug>.runtime-io.yaml"`
- Happy path example: runtime file `Career/00_Core_OS/Runs/<YYYY-MM-DD>_intake-job_<slug>.runtime-io.yaml` -> run `scripts/run_command_gate.sh "Career/00_Core_OS/Runs/<YYYY-MM-DD>_intake-job_<slug>.runtime-io.yaml"`

Fail/stop rules:

- If any required gate check fails, STOP finalization.
- Set `validation_result.passed: false`.
- Set `artifact_destination.write_allowed: false`.
- Populate `execution_trace.halted_at` and `execution_trace.reason`.
- Do not write or update artifacts until gate status is `pass`.