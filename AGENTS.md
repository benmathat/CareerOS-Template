# AGENTS.md

Guidance for any AI coding agent (Claude Code, Cursor, Codex, etc.) working in this repository.

## What this repo is

CareerOS is **not a software project** — there is no app to build, run, or deploy, and no test suite in the conventional sense. It's a personal career-management workspace: structured markdown, an opinionated "prompt runtime" that governs how an assistant should operate on that content, and a couple of Python/shell validators for that runtime's data files.

The repo contains **real personal data** (name, employment history, applications, contacts, compensation figures) belonging to the repo owner. Treat every file under `Career/` as potentially sensitive:

- Never invent, alter, or embellish factual claims (dates, employers, titles, metrics) — see the canonical-truth rules below.
- Before anything from this repo is copied, posted, or pushed somewhere public, check [PERSONAL_DATA_CHECKLIST.md](PERSONAL_DATA_CHECKLIST.md). `scripts/prepare-template.sh <new-dir>` builds the public template from an allowlist into a fresh repo and scans it for personal data; it never pushes. Never push this repo's `main` or any branch of it to a public remote — real data must never land in that remote.
- `.gitignore` has a "Personal/sensitive information" section that is currently empty — don't assume secrets are excluded by default.

## Start here

The authoritative operating contract for an assistant in this workspace is **[Career/Career_Workspace_Assistant_prompt.md](Career/Career_Workspace_Assistant_prompt.md)**. Read it before doing any non-trivial work here — it defines the runtime-first execution model this repo expects (modes, packs, pipelines, conformance gates) in more detail than is worth duplicating in this file.

For quick orientation instead of the full contract:
- [Career/00_Core_OS/careeros-structure-map.md](Career/00_Core_OS/careeros-structure-map.md) — compressed map of the 13 top-level sections and where content belongs.
- [Career/04_Career_Goals_and_Strategy/career-tracks.md](Career/04_Career_Goals_and_Strategy/career-tracks.md) — canonical descriptive track labels, stable routing IDs, and governing role targets.
- [Career/00_Core_OS/Prompts/README.md](Career/00_Core_OS/Prompts/README.md) — how the prompt library (system/mode/task/context/output layers + runtime engine) fits together.
- [Career/QUICK_START.md](Career/QUICK_START.md) and [Career/WORKFLOWS.md](Career/WORKFLOWS.md) — human-facing workflow reference.

## Core rules that apply to every change

- **Use descriptive track labels.** In conversation, questions, recommendations, and human-facing summaries, use the labels in `career-tracks.md` rather than track numbers. Keep existing `track-*` values for structured fields, routing, validation, and historical compatibility. Numbers are identifiers, not priority. Do not ask the user to remember or rank numbered tracks.
- **Canonical truth boundary.** Long-form, durable truth (roles, metrics, stories, goals, preferences) lives in canonical sections — especially `Career/02_Work_Experience/`, `04_Career_Goals_and_Strategy/`, `05_Personal_Profile/`. Application- or interview-specific variants live in execution sections, especially `Career/07_Applications_and_Interviews/`. Never let a tactical/contextual artifact silently override canonical content — if they conflict, flag it rather than picking one.
- **Grounded claims only.** Don't state something as fact unless it traces back to content already in the workspace; otherwise mark it as an explicit assumption or a context gap.
- **Frontmatter hygiene.** Many markdown files carry `Last Update` / `Previous Update` frontmatter. When you edit such a file, run `scripts/careeros touch <file>` — it sets `Last Update` to today and moves the old value into `Previous Update`.
- **Never hardcode or guess the date.** Always pull the current date from the system (`scripts/careeros today`) before writing it anywhere; `.cursorrules` is just a pointer back to this file.
- **Command entry points** are defined in [Career/00_Core_OS/Skills/*/SKILL.md](Career/00_Core_OS/Skills) (`source-opportunities`, `intake-job`, `promote-opportunity`, `analyze-opportunity`, `discuss-opportunity`, `build-resume`, `build-application`, `log-activity`, `generate-weekly-cert`, `sync-application-tracker`, `close-opportunity`). If a user request maps to one of these, follow that skill's contract rather than improvising an equivalent workflow.
- **Tool adapters, one source.** Command contracts live only in `Career/00_Core_OS/Skills/<command>/SKILL.md`, and runtime IO files in `Career/00_Core_OS/Runs/`. `.claude/skills`, `.cursor/skills` and `.agents/skills` (where Codex looks) are symlinks to the Skills directory; in Codex, invoke a skill with `$<name>` or `/skills` instead of `/<name>`, and `CLAUDE.md` just imports this file and the assistant prompt. `.claude/settings.json` holds the shared Claude Code permissions (canonical sections `02_`–`05_` prompt before edits) and a SessionStart hook that injects the system date. Edit the neutral copies, never the adapters.
- **Fail-safe over speculative completion.** If required inputs are missing or a conformance check would fail, stop and surface the gap rather than finalizing a write.

## Validating runtime IO files

Several commands produce/consume structured YAML "runtime IO" objects (see [Career/00_Core_OS/Prompts/Runtime/runtime-io-schema.md](Career/00_Core_OS/Prompts/Runtime/runtime-io-schema.md)). Validate one with:

```bash
scripts/run_command_gate.sh <path-to-runtime-io-file>
```

This installs PyYAML on first run if missing and shells out to `scripts/validate_runtime_io.py`. There is no other build/lint/test step in this repo — don't look for `npm test`, `pytest`, etc.

## Deterministic helpers and the pre-commit gate

Mechanical rules live in code, not prose. `scripts/careeros` (stdlib-only Python) provides:

- `today` — system date; `slug <company> <role> [date]` — the normalized `<company>_<role>_<YYYY-MM-DD>` name
- `new-run <command> <slug> [--target <opportunity-folder>] [--file <artifact>] [--state new|existing|none]` — **start every runtime IO run with this.** Writes `Career/00_Core_OS/Runs/<date>_<command>_<slug>.runtime-io.yaml` (one per run, never overwritten) with everything derivable prefilled (command, pack, pipeline, mode, output type, task id, destination) and every judgment field set to `TODO`. Fill each `TODO` with grounded content; `gate`/`check` refuse the file while any remain
- `run-path <command> <slug>` — just the path, if you need it without a skeleton
- `touch <file>...` — frontmatter date rotation; `gate <file>` — runtime IO conformance gate
- `close <folder> --outcome pass|withdrawn|rejected|no_response --reason "…"` — the mechanics of `/close-opportunity` (archive folder, status fields, Closed_Searches README row, tracker row); `--dry-run` previews. The reason must come from the user.
- `lapsed [--days 30] [--all]` — read-only report of in-flight applications with no activity for N days (a derived view, not a tracker status); close one the user decides to end with `close --outcome no_response`
- `index [--write|--check]` — regenerates the by-track index in `Career/06_Job_Opportunities/README.md`
- `check [--staged|--all]` — fails on a runtime IO file that doesn't pass the gate, a *new* run file whose command/date/slug/`artifact_destination` disagree with the repo, an un-normalized new opportunity folder name, a `job-opportunity.md` still at `intake_status: draft` under `06_Job_Opportunities/`, markdown whose YAML frontmatter is malformed (e.g. mangled by an editor formatter; `--all` checks every tracked file), or edited markdown whose `Last Update`/`Previous Update` weren't rotated Also checks repo *state* against the command contracts (`scripts/state_checks.py`): record/analysis/lifecycle rules for opportunities added on or after 2026-10-06, no `MISSING`/`TODO`/`TBD` in a resume or generated DOCX, work-log entry fields and append-only history, and claim grounding (`scripts/grounding_checks.py`: a resume's employer, title and dates must match a role in `02_Work_Experience/Roles/`, every metric in a resume or cover letter must appear in canonical `02_`–`05_` content, "N years" can't exceed the career span, and every education/certification item must be covered by one item under an `Education`/`Certifications` heading in `02_`–`05_` (today `skills-inventory.md`); a true figure that isn't canonical yet goes into canonical content first, or into a reasoned line in the opportunity folder's `grounding-waivers.md`: `- <claim as written> — <reason>`), and provenance (a new standard artifact in an opportunity folder needs a run file for a command allowed to create it, which is what stops `/intake-job` from writing into `06_`)

`scripts/hooks/pre-commit` runs `check --staged`. Hooks aren't versioned by git, so enable it once per clone: `git config core.hooksPath scripts/hooks`. Bypass deliberately with `git commit --no-verify`. Prefer these over doing the same thing by hand.

## Generating shareable resume and cover letter files (DOCX/PDF)

`/build-resume` and `/build-application` write opportunity-scoped markdown
into `Career/06_Job_Opportunities/<company>_<role>_<date>/` as `resume.md`,
`cover-letter.md`, `application-notes.md`, `application-record.md`, and
`next-steps.md`. Reusable baselines stay under
`Career/01_Resume_and_Profiles/`.

To turn a resume or cover letter into a formatted file for submission, use:

- `scripts/generate-resume-docx.sh <path-to-resume.md>`
- `scripts/generate-cover-letter-docx.sh <path-to-cover-letter.md>`

For opportunity-folder inputs, these default to terse DOCX/PDF outputs
in the same folder, named `resume_<INITIALS>-<company-role>-<YYYY-MM>` and
`cover-letter_<INITIALS>-<company-role>-<YYYY-MM>` (for example
`resume_JQP-acme-sr-mgr-product-2026-10.docx`), and prefer sibling
`analysis.md` for ATS keywords. `<INITIALS>` come from the `# Full Name`
heading of the markdown being rendered; `<company-role>` is the opportunity
folder's company and role made as terse as possible (filler words dropped,
standard abbreviations such as Senior to sr, Manager to mgr, Vice President
to vp). The rules and the abbreviation table are in
[Shareable file names](Career/01_Resume_and_Profiles/Templates/README.md#shareable-file-names);
never hand-name these files. See [Career/01_Resume_and_Profiles/Templates/README.md](Career/01_Resume_and_Profiles/Templates/README.md)
for usage, [scripts/resume_docx/SCHEMA.md](scripts/resume_docx/SCHEMA.md)
for the resume markdown structure, and
[scripts/resume_docx/COVER_LETTER_SCHEMA.md](scripts/resume_docx/COVER_LETTER_SCHEMA.md)
for the cover letter markdown structure. Do not hand-edit a DOCX/PDF into
existence, or ask a user to manually retype content into
`Templates/resume-template.docx` or `Templates/cover-letter-template.docx`,
when these scripts can do it. (They share a layout engine,
`scripts/resume_docx/docx_common.py` — extend that, not either script
individually, for anything not specific to one document type.)

`/analyze-opportunity` extracts likely ATS keywords verbatim from the job
posting into `analysis.md`'s `## ATS Keywords` section. Pass that file (or
let either generator auto-detect it) via `--ats-keywords` so a targeted
resume or cover letter's Keywords property reflects the posting it's for,
not just terms pulled from the document's own content.

## Git hygiene specific to this repo

- Commit and push only when the user asks. In Claude Code this is enforced: `.claude/settings.json` has `ask` rules on `git commit*` and `git push*`. Cursor and Codex rely on this rule alone (pushes are also guarded by `scripts/hooks/pre-push`). Check `git status` first so previously staged files aren't swept into the commit.
- Recent commit history mixes real content updates. Before committing, re-check `git status`/`git diff` for anything that looks like it belongs in the sanitization checklist above rather than a normal commit.
- Don't push to any remote configured for the public template (see `scripts/prepare-template.sh`) with unsanitized content.

## Model notes

Model-specific behaviors worth knowing, kept short on purpose: add an entry only after a real failure has been observed, with the date, the model, what happened, and the rule or check that now prevents it. Prefer turning a failure into a `careeros check` rule over a note. No entries yet. Failures to watch for: skipping or reordering runtime object emission, partial frontmatter rotation, writing outside the declared destination.
