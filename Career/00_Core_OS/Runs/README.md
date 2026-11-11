# Runtime IO Runs

This directory stores one runtime emission file per command run. The command conformance gate validates each file, and the files form an audit history of what was run, with what inputs, and whether the gate passed.

## Purpose

- Hold the structured runtime objects for a command run (`request` through `execution_trace`)
- Provide a deterministic artifact for validation and audit
- Block final writes when conformance fails

## File Convention

- One file per run, never overwritten:
  - `Career/00_Core_OS/Runs/<YYYY-MM-DD>_<command-name>_<slug>.runtime-io.yaml`
- `<command-name>` is the command without the leading slash (`build-resume`, `intake-job`, ...).
- `<slug>` identifies the target (company/role or topic), lowercase with underscores.
- Create the file with the scaffolder instead of writing it by hand:
  - `scripts/careeros new-run <command-name> <slug> [--target <opportunity-folder>] [--file <artifact>]`
  - It prefills everything derivable (command, pack, pipeline, mode, output type, task id, destination class/path/filename) and sets every judgment field to `TODO`. Fill each `TODO` with grounded content; the gate fails while any remain.
  - `scripts/careeros run-path <command-name> <slug>` prints just the path.
- Examples:
  - `2026-10-07_build-resume_hp_transformation_portfolio_and_governance_manager.runtime-io.yaml`
  - `2026-10-07_log-activity_hp_inc_application_submitted.runtime-io.yaml`
- The document shape is defined in `Prompts/Runtime/runtime-io-schema.md` (section 5.11); the scaffold follows it.

## Validation

Before finalizing artifact writes, run:

`scripts/run_command_gate.sh "Career/00_Core_OS/Runs/<YYYY-MM-DD>_<command-name>_<slug>.runtime-io.yaml"`

The gate validates YAML structure and runtime contract conformance. Non-zero exit means stop and fix the runtime file before continuing. The pre-commit hook re-runs the gate on any staged run file and rejects new run files that don't follow the naming convention.
