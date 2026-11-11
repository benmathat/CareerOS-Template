---
Last Update: 2026-11-06
Previous Update: 2026-11-05
---

# Opportunity Sourcing

Saved research outputs from [source-opportunities](../../00_Core_OS/Skills/source-opportunities/SKILL.md). Preferences, priority order, and screening rules remain in [search-strategy.md](../../04_Career_Goals_and_Strategy/search-strategy.md) and its canonical references.

## Reports

- Weekly: `Reports/YYYY-MM-DD_weekly.md` (actual local run date, not a guessed scheduled date).
- On demand: `Reports/YYYY-MM-DD_broader.md`.
- Additional same-day reports: append `_02`, `_03`, etc. before `.md`. Use a matching unique runtime slug. Never overwrite published reports.
- Follow [report-template.md](report-template.md). Empty sections say `None`; unavailable facts say `Unknown` with a reason. Preserve source URLs and the date actually checked.
- Reports are research shortlists, not confirmed opportunities, full analyses, application decisions, or compliance logs. No synthetic initial report or historical backfill is created at setup.

## Identity and Duplicates

Use a stable `candidate_id` across reports. Prefer `normalized-employer:requisition-id` when a requisition is stated; otherwise use the canonical employer/ATS posting URL. Keep the original source URL too. Normalize only known tracking parameters (`utm_*`, `source`, `ref`, `referrer`) and fragments; preserve functional identifiers such as `gh_jid`, `jobId`, or `reqId`. Do not merge distinct location-specific requisitions merely because titles match.

When an employer-side URL or requisition becomes available for a previously unverified lead, match by prior URL, employer, title, and location before creating a new ID. Reuse the existing ID and include the new URL as an alias in the history note. If identity is uncertain, flag a possible duplicate and exclude it from the new-opportunity count until resolved.

Before each run, read [sourcing-history.md](sourcing-history.md) and [owner-decisions.md](owner-decisions.md) (owner decisions such as `not_pursuing`; observations in the history are never decisions) and compare against staged, active, and archived opportunities. A candidate's first/last seen dates and prior reports derive from its rows; do not rewrite history to maintain rolling dates.

## History Events

Append one row per candidate included anywhere in a published report, including recorded exclusions. Use these event types:

| Event | Meaning | Counts toward weekly target? |
|---|---|---|
| `new` | Employer-verified, screened candidate never previously shortlisted or tracked; a previously unverified lead can qualify once verified | Yes |
| `repeat` | Previously shortlisted candidate; give a concrete reason for resurfacing, such as changed terms or a user request | No |
| `tracked` | Already staged, active, or archived in CareerOS; link the record and do not automatically reopen a closed search | No |
| `lead` | Opening not verified at employer/ATS, or identity unresolved | No |
| `excluded` | Known constraint/fit failure discovered while screening; record the actual reason | No |

Every history row has a unique pair `(report path, candidate_id)`. Before appending, check that pair: retry only missing rows. Preserve earlier rows and any owner notes. Current rows describe observations, not user decisions; never infer that silence means rejection. Unknown compensation belongs in the report and note, even when the opening is employer-verified.

If a report exists without all its history rows (for example after an interrupted write), recover missing rows from that report before searching again. If a row links a missing report or inconsistent identity, stop and surface the discrepancy; do not silently discard history. Sourcing history begins at the first real run. Existing opportunity records still participate in duplicate checks even without a history row.

## Publication and Recovery

Prepare the report and history delta in memory or a temporary location, pass the runtime gate, write the new report, then append the history rows and run `scripts/careeros touch` on history. Do not overwrite a report on retry. Confirm every new history link resolves and every report candidate has exactly one matching row. Return the saved report link in the Orca result. A partial publication is not a completed run; report it and finish the missing history append before proceeding.
