---
Last Update: 2026-11-05
Previous Update: 2026-11-03
---

# Load Manifest (Per-Command Reads)

## Purpose

Say which prompt-library files an assistant must read for each command, and which are reference material to open only when needed. The full runtime specs stay authoritative; this file only controls what is loaded by default, so a run does not read every Runtime document.

Approximate size of the default load per run (command + required reads): 30–61 KB, against roughly 93–124 KB when all eight Runtime documents are read every time.

## Always Read (Every Command)

1. The command contract: `Career/00_Core_OS/Skills/<command>/SKILL.md`
2. `Runtime/runtime-io-schema.md` (object shapes and canonical order)
3. `Runtime/command-conformance-gate.md` (the end-of-command gate)
4. The command's mode file, pack and pipeline from the table below

## Per-Command Reads

| Command | Mode file | Pack | Pipeline |
|---|---|---|---|
| `/source-opportunities` | `Modes/execute-mode.md` | none | none |
| `/intake-job` | `Modes/build-mode.md` | `Packs/job-intake-pack.md` | `Pipelines/job-intake-pipeline.md` |
| `/promote-opportunity` | `Modes/execute-mode.md` | `Packs/job-intake-pack.md` | `Pipelines/job-intake-pipeline.md` |
| `/analyze-opportunity` | `Modes/analyze-mode.md` | `Packs/opportunity-analysis-pack.md` | `Pipelines/opportunity-review-pipeline.md` |
| `/discuss-opportunity` | `Modes/analyze-mode.md` | `Packs/opportunity-analysis-pack.md` | `Pipelines/opportunity-fit-pipeline.md` |
| `/build-resume` | `Modes/build-mode.md` | `Packs/resume-pack.md` | `Pipelines/application-pipeline.md` |
| `/build-application` | `Modes/build-mode.md` | `Packs/application-pack.md` (plus `resume-pack.md` for track rules) | `Pipelines/application-pipeline.md` |
| `/log-activity` | `Modes/execute-mode.md` | `Packs/compliance-pack.md` | `Pipelines/compliance-pipeline.md` |
| `/generate-weekly-cert` | `Modes/build-mode.md` | `Packs/compliance-pack.md` | `Pipelines/compliance-pipeline.md` |
| `/sync-application-tracker` | `Modes/execute-mode.md` | none | none |
| `/close-opportunity` | `Modes/execute-mode.md` | none | none |

`/build-resume` and `/build-application` also read `Career/05_Personal_Profile/writing-style.md` (voice rules, self-edit checklist, fresh-context critique pass); run `scripts/careeros lint <file>` on each draft.

Modes, packs and pipelines match the defaults that `scripts/careeros new-run` prefills (`scripts/new_run.py`). If the two disagree, fix whichever is wrong; do not guess.

## Read On Demand (Reference)

Open these only when the trigger applies. They are not skipped for conformance: the gate and `careeros check` validate the run file either way.

| Document | Read when |
|---|---|
| `Runtime/mode-selection.md` | the command does not fix the mode, the request maps to no command, or the mode in the run file is in doubt |
| `Runtime/source-routing.md` | the command's own source list is incomplete or ambiguous, or the request is not a listed command |
| `Runtime/context-loader.md` | context must be compressed or two sources conflict |
| `Runtime/prompt-assembler.md` | assembling a prompt for a request that is not a listed command |
| `Runtime/execution-flow.md` | a halt, retry or validation failure needs the lifecycle rules |
| `Runtime/operator-runbook.md` | recovering from a failed run |
| `Runtime/runtime-conformance-checklist.md` | changing the runtime or prompt library itself |
| `careeros-prompt-architecture-spec.md` | changing the architecture |
| `system-prompt.md`, `interaction-model.md`, `output-standards.md` | the command or pack cites them, or output structure is in question |

## Rules

- A command not in the table is unmapped: read all Runtime documents for that run, and add it here afterwards.
- This manifest never relaxes a halt or gate. If a required input is missing or a check fails, stop as the command contract says.
- When a command contract changes its pack, pipeline or mode, update this table in the same change.
