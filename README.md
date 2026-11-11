# CareerOS

A **career operating system** for long-term career management and focused job searching: structured markdown, an AI-assistant "prompt runtime" that governs how an assistant works on that content, and a few small scripts that enforce the mechanical rules.

CareerOS is not an app. There is nothing to build or deploy. You fill in a workspace, and an AI coding assistant (Claude Code, Cursor, Codex, etc.) operates on it through defined commands.

## Key Features

- **Strategy before volume**: clarity of direction over mass applications
- **Truth separated from polish**: raw experience and metrics live apart from resumes and cover letters
- **Grounded claims only**: resumes and letters may state only what traces back to your canonical records; scripts check employers, dates, metrics and credentials against them
- **Canonical vs tactical**: durable truth (roles, stories, goals) lives in `Career/02_`–`05_`; per-application variants live in `Career/06_Job_Opportunities/` and `Career/07_Applications_and_Interviews/`
- **Command-driven workflow**: each step of a search is a command with a written contract and a pass/fail conformance gate
- **Agency-neutral compliance (optional)**: if you are claiming unemployment benefits, set your agency and its rules once in `Career/11_Job_Search_Activities/compliance-profile.md`; the logging and certification commands read it. Skip it otherwise
- **Compounding learning**: every application, interview and rejection feeds the next one
- **Built for iteration**: supports multiple searches, pivots, pauses and restarts without losing context

## Structure

The workspace has 13 sections under `Career/`:

- `INBOX/` - Staging area for incoming documents and postings
- `00_Core_OS/` - Orientation, prompt runtime, command skills, run records
- `01_Resume_and_Profiles/` - External representation: baselines, templates, profiles
- `02_Work_Experience/` - Raw career data (roles, projects, stories)
- `03_Skills_and_Portfolio/` - Proof of capability
- `04_Career_Goals_and_Strategy/` - Direction, constraints, career tracks
- `05_Personal_Profile/` - Self-knowledge and work preferences
- `06_Job_Opportunities/` - One folder per opportunity, from posting to application
- `07_Applications_and_Interviews/` - Application tracker, interview prep, feedback loop
- `08_Networking_and_References/` - Relationships
- `09_Research_and_Market_Intelligence/` - Company research and sourcing history
- `10_Coaching_Feedback_and_Notes/` - Improvement engine
- `11_Job_Search_Activities/` - Compliance log and weekly certifications
- `99_Archive/` - Closed searches, preserved without clutter

## Commands

The assistant runs these as skills. Each contract lives in `Career/00_Core_OS/Skills/<command>/SKILL.md`. In Claude Code, invoke one as `/<name>`; in Codex, use `$<name>`.

| Command | Purpose |
|---------|---------|
| `source-opportunities` | Find and screen postings; keep sourcing history |
| `intake-job` | Stage a raw posting (PDF, URL or text) in `INBOX/` |
| `promote-opportunity` | Move a reviewed posting into `06_Job_Opportunities/` |
| `analyze-opportunity` | Produce a decision-ready fit analysis from your canonical evidence |
| `discuss-opportunity` | Weigh your view against the evidence and record a resume and letter strategy |
| `build-resume` | Generate a tailored resume from canonical evidence |
| `build-application` | Build the full application package |
| `log-activity` | Record a search activity in the compliance log |
| `generate-weekly-cert` | Produce a weekly work-search certification summary |
| `sync-application-tracker` | Reconcile the tracker with application records |
| `close-opportunity` | Archive a finished opportunity and update the records |

## Getting Started

1. Clone or copy this repo as the start of your own **private** workspace. It will hold personal data, so do not publish it.
2. Read `Career/QUICK_START.md` and fill in the first foundations (current focus, target role, work history, preferences).
3. Point your AI assistant at the repo. `CLAUDE.md` and `AGENTS.md` load the operating rules, and `Career/Career_Workspace_Assistant_prompt.md` is the assistant's full contract.
4. Run commands through the assistant. Start with `source-opportunities` or `intake-job`, then follow `Career/WORKFLOWS.md`.
5. Once, per clone, enable the pre-commit check: `git config core.hooksPath scripts/hooks`.

## Scripts

All under `scripts/`; Python 3 is required.

- `scripts/careeros` - deterministic helpers (stdlib only): `today`, `slug`, `new-run`, `touch`, `gate`, `close`, `lapsed`, `index`, `lint`, `check`. Run `scripts/careeros` with no arguments for the list. Use these instead of doing the same thing by hand.
- `scripts/careeros check` - the same validation the pre-commit hook runs: runtime IO files, frontmatter, opportunity records, and claim grounding for resumes and cover letters.
- `scripts/run_command_gate.sh <runtime-io-file>` - validate a runtime IO record (installs PyYAML on first run).
- `scripts/generate-resume-docx.sh <resume.md>` and `scripts/generate-cover-letter-docx.sh <cover-letter.md>` - render formatted DOCX/PDF files from the markdown. Formats are in `scripts/resume_docx/SCHEMA.md` and `COVER_LETTER_SCHEMA.md`; install `scripts/resume_docx/requirements.txt` first.

There is no other build, lint or test step.

## Documentation

- **[Career/README.md](Career/README.md)** - Complete system overview
- **[Career/QUICK_START.md](Career/QUICK_START.md)** - First-hour setup
- **[Career/WORKFLOWS.md](Career/WORKFLOWS.md)** and **[Career/WORKFLOW_INDEX.md](Career/WORKFLOW_INDEX.md)** - Workflows and reference
- **[Career/STATUS_DEFINITIONS.md](Career/STATUS_DEFINITIONS.md)** - Status definitions
- **[AGENTS.md](AGENTS.md)** - Rules for any AI agent working in the repo
- **[Career/00_Core_OS/Prompts/README.md](Career/00_Core_OS/Prompts/README.md)** - Prompt system overview
- **[Career/00_Core_OS/Prompts/Runtime/operator-runbook.md](Career/00_Core_OS/Prompts/Runtime/operator-runbook.md)** - Command execution protocol
- **[Career/00_Core_OS/careeros-structure-map.md](Career/00_Core_OS/careeros-structure-map.md)** - Compressed structure map

## License

This is a personal career management system. Use it as you see fit for your own career development.

## Contributing

This is a personal workspace template. Feel free to fork and adapt it to your needs. Keep your own copy private: it will contain your employment history, applications and contacts.
