---
name: close-opportunity
description: Close an opportunity, archiving its folder, marking it closed, and updating the Closed Searches README and the application tracker.
argument-hint: "<folder in Career/06_Job_Opportunities/> <pass|withdrawn|rejected|no_response> <your reason>"
---

# /close-opportunity

## Purpose
Close a job opportunity the same way every time. The mechanical work is done by `scripts/careeros close`, not improvised, so every closed search ends with identical artifacts.

## Use When
- You decide to pass on an opportunity (`pass`)
- You withdraw an application or stop pursuing it (`withdrawn`)
- An employer rejects or closes the role (`rejected`)
- You were never rejected, but no response has come and none is expected (`no_response`); `scripts/careeros lapsed` lists candidates, and you decide

## Required Inputs
- Opportunity folder: `Career/06_Job_Opportunities/<company>_<role>_<YYYY-MM-DD>/`
- Outcome: `pass`, `withdrawn`, `rejected`, or `no_response`
- **Reason, supplied by the user.** Never invent, infer, or paraphrase beyond the user's words. If the user has not given a reason, ask for one (one question) and stop. A pack recommendation or analysis score is not a reason.

## Optional Inputs
- Would reapply: `Yes`, `Maybe`, `No`, `Unclear` (default `Unclear`; never guess)

## Validation
Before execution, verify with `scripts/careeros close ... --dry-run`:
- folder exists in `06_Job_Opportunities/` and has `job-opportunity.md` with `company` and `role`
- `intake_status` is not `draft`, and `status` is not already `closed`
- destination `99_Archive/Closed_Searches/<folder>/` does not exist
- at most one Active tracker row matches the role (zero or one)

If validation fails:
- STOP execution
- report the blocked checks verbatim
- do not move or edit anything

## Instructions
1. Confirm the three required inputs came from the user in this conversation.
2. Run the dry run and show the user its output, which lists every edit:
   `scripts/careeros close <folder> --outcome <outcome> --reason "<user reason>" [--would-reapply <v>] --dry-run`
3. Emit the runtime objects and run the conformance gate (see below).
4. If the gate passes, run the same command without `--dry-run`. It will:
   - set `status: closed`, `closed_date`, `close_outcome`, `close_reason` in `job-opportunity.md`; for `pass` it also sets `decision: pass`, `decision_date`, `decision_source: user_confirmed`
   - move the folder to `Career/99_Archive/Closed_Searches/`
   - add a row at the top of the table in `Closed_Searches/README.md`
   - remove the matching Active row from the application tracker (if any) and add a row to its Closed Applications table, recording the removed row's ID
   - rotate tracker `Last Update` / `Previous Update`
5. Set `artifact_destination` to `/99_Archive/Closed_Searches/<folder>/` with filename `job-opportunity.md`, class `reflection`.

## Must NOT
- invent or reword the close reason, or fill `Would reapply` by guessing
- analyze the opportunity, generate resumes or application documents, or change `track`
- delete any file in the opportunity folder (everything moves with it)
- edit any other opportunity, `02_`–`05_` canonical sections, or the work search log (use `/log-activity` for that)
- commit, push, or stage anything unless the user asks

## Failure Handling
- Active row ambiguity (more than one match): stop; suggest `/sync-application-tracker`.
- Destination exists: stop; do not merge or overwrite.

## Output
- Closed folder under `Career/99_Archive/Closed_Searches/`
- One new row each in the Closed_Searches README and the tracker's Closed Applications table
- A run file in `Career/00_Core_OS/Runs/` (`scripts/careeros run-path close-opportunity <slug>`)

## Next Step
Review `git diff`, then commit if satisfied.

## Runtime IO Emission (Required)

Start the run file with `scripts/careeros new-run close-opportunity <slug> --target <opportunity-folder>`. It prefills the derivable fields; replace every `TODO` with grounded content before running the gate (the gate fails while any remain).
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
- `scripts/run_command_gate.sh "Career/00_Core_OS/Runs/<YYYY-MM-DD>_close-opportunity_<slug>.runtime-io.yaml"`
- Happy path example: runtime file `Career/00_Core_OS/Runs/<YYYY-MM-DD>_close-opportunity_<slug>.runtime-io.yaml` -> run `scripts/run_command_gate.sh "Career/00_Core_OS/Runs/<YYYY-MM-DD>_close-opportunity_<slug>.runtime-io.yaml"`

Fail/stop rules:

- If any required gate check fails, STOP finalization.
- Set `validation_result.passed: false`.
- Set `artifact_destination.write_allowed: false`.
- Populate `execution_trace.halted_at` and `execution_trace.reason`.
- Do not write or update artifacts until gate status is `pass`.