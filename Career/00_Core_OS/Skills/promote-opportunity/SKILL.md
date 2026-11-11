---
name: promote-opportunity
description: Promote a reviewed staged opportunity from the inbox into Career/06_Job_Opportunities/.
argument-hint: "<staged .md in Career/INBOX/Job_Postings/>"
---

# /promote-opportunity

## Purpose
Promote a reviewed job opportunity from `Career/INBOX/Job_Postings/` into the durable CareerOS opportunity structure.

## Use When
- A staged opportunity markdown file has been created by `/intake-job`
- The staged file has been reviewed for extraction accuracy
- The opportunity is ready to become a durable CareerOS record

## Required Inputs
- Staged opportunity file:
  `Career/INBOX/Job_Postings/<company>_<role>_<YYYY-MM-DD>.md`
- Source PDF:
  `Career/INBOX/Job_Postings/<source-file>.pdf`
  (not needed when the full-text-capture exception below applies)

## Full-Text-Capture Exception (no PDF)
A source PDF is waived only when the posting is wholly captured in another format. All of these must hold:
- staged frontmatter has `source: url` or `source: text`, and `source_pdf: MISSING`
- for `source: url`, `posting_url` is populated
- the Raw Source section is a verbatim extraction of the whole posting: description, responsibilities, requirements and compensation, with no part of the posting unreadable, truncated, image-only or behind a login
- the staged file's Context Gaps do not list a missing or unreadable part of the posting itself (gaps about facts the posting does not state are fine)

If any condition is doubtful, the PDF is required: stop and ask for it. The user's instruction to promote does not by itself establish the exception.

## Validation
Before execution, verify:
- staged markdown file exists
- source PDF exists, or the full-text-capture exception above holds
- staged file includes `intake_status: reviewed` or `intake_status: confirmed`
- staged file includes required sections:
  - Raw Source
  - Structured Extraction
- required metadata fields are present:
  - company
  - role
  - date_added or date_downloaded
  - source_pdf (a filename, or `MISSING` under the exception)

If validation fails:
- STOP execution
- return missing requirements
- do not move files

## Instructions
1. Use the staged opportunity file as the source of truth for folder naming.
2. Normalize the destination folder name using the same filename normalization rules from `/intake-job`:
   - lowercase
   - replace spaces with underscores
   - remove punctuation and special characters
   - remove common company suffixes only when clearly redundant
   - use normalized role title
   - use date in `YYYY-MM-DD` format
3. Create destination folder:
   `Career/06_Job_Opportunities/<company>_<role>_<YYYY-MM-DD>/`
4. Move the staged markdown file into the destination folder and rename it:
   `job-opportunity.md`
5. Move the source PDF into the destination folder and rename it:
   `source-posting.pdf`
   (skip under the full-text-capture exception; no placeholder file is created)
6. Update `job-opportunity.md` metadata:
   - set `intake_status: confirmed`
   - set or update `promoted_date`
   - update `source_pdf: source-posting.pdf`; under the exception leave `source_pdf: MISSING` and `posting_file: MISSING` and keep the staged assumption that records the capture format
   - set `status: intake` unless another valid lifecycle status is already present
   - preserve `track` as staged; if absent, add `track: MISSING` (do not infer)
7. Ensure all internal references point to the local promoted files.
8. Do not perform opportunity analysis.
9. Do not assign pursue / consider / pass.
10. Do not generate resume, cover letter, or application artifacts.

## Destination Structure
Final structure MUST be:

```text
Career/06_Job_Opportunities/<company>_<role>_<YYYY-MM-DD>/
  job-opportunity.md
  source-posting.pdf      # omitted under the full-text-capture exception
```

## Must NOT
- promote a draft the user has not reviewed; never set `intake_status` to anything but `confirmed`, and only for a staged file the user pointed to
- infer or assign `track` (preserve as staged, else `MISSING`)
- create files in the destination folder other than `job-opportunity.md` and `source-posting.pdf`
- leave a copy of the staged file or PDF behind in `Career/INBOX/`, or promote more than one opportunity per run
- touch the tracker, the work search log, or any other opportunity
- commit, push, or stage anything unless the user asks

## Failure Handling
- If destination folder already exists:
  - do not overwrite files silently
  - ask whether to merge, replace, or create a versioned folder
- If PDF cannot be matched confidently, or is absent and the full-text-capture exception does not clearly hold:
  - stop and ask for the correct source PDF
- If metadata is incomplete:
  - mark missing fields explicitly
  - do not promote until required fields are corrected

## Output
- Confirmed opportunity folder in `Career/06_Job_Opportunities/`
- Promoted `job-opportunity.md`
- Promoted `source-posting.pdf` (absent under the full-text-capture exception)
- No analysis artifacts created

## Next Step
After successful promotion, suggest running:

```text
/analyze-opportunity
```

## Runtime IO Emission (Required)

Start the run file with `scripts/careeros new-run promote-opportunity <slug> --target <opportunity-folder>`. It prefills the derivable fields; replace every `TODO` with grounded content before running the gate (the gate fails while any remain).
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
- `scripts/run_command_gate.sh "Career/00_Core_OS/Runs/<YYYY-MM-DD>_promote-opportunity_<slug>.runtime-io.yaml"`
- Happy path example: runtime file `Career/00_Core_OS/Runs/<YYYY-MM-DD>_promote-opportunity_<slug>.runtime-io.yaml` -> run `scripts/run_command_gate.sh "Career/00_Core_OS/Runs/<YYYY-MM-DD>_promote-opportunity_<slug>.runtime-io.yaml"`

Fail/stop rules:

- If any required gate check fails, STOP finalization.
- Set `validation_result.passed: false`.
- Set `artifact_destination.write_allowed: false`.
- Populate `execution_trace.halted_at` and `execution_trace.reason`.
- Do not write or update artifacts until gate status is `pass`.