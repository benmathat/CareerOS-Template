---
name: discuss-opportunity
description: Discuss fit and risk with the user, weigh their positions against canonical evidence, reconcile disputes, and record a resume and cover letter strategy.
argument-hint: "<opportunity folder>"
---

# /discuss-opportunity

## Purpose
Turn the one-way `analysis.md` into a two-way reconciliation. The user states why the role fits and what risks they see; those positions are weighed against canonical evidence; disputes are resolved together; the result sharpens canonical records and sets the strategy `/build-resume` and `/build-application` follow.

## Use When
- `analysis.md` exists for a confirmed opportunity (recommendation `pursue` or `consider`, or the user wants to test a `pass`)
- Before `/build-resume` or `/build-application`

## Required Inputs
- `/06_Job_Opportunities/<company>_<role>_<date>/job-opportunity.md` (`intake_status: confirmed`)
- `/06_Job_Opportunities/<company>_<role>_<date>/analysis.md`

## Optional Inputs
- Existing `discussion.md` (resume an `open` discussion; never discard its ledger)
- `09_Research_and_Market_Intelligence/` company research

## Validation
Before execution, verify the required inputs exist and `analysis.md` contains `## Track`, `## Recommendation` and (for `pursue`/`consider`) `## Resume Keyword Map`. If validation fails: STOP and return the missing requirements.

## Interaction Protocol
The discussion is interactive. Do not produce the whole artifact in one pass.

1. **Elicit the user's position first.** Before showing scores or the recommendation from `analysis.md`, ask (a few questions at a time, not a form): why they believe the role is a fit, what they would lead with, what risks or doubts they see, and what they would not want to do day to day. You may seed with the neutral open items from `analysis.md` (its context gaps and pre-application checks) but not its verdict, so the analysis does not anchor the user.
   - **Confirm compensation.** Check the posting and opportunity record. If compensation is advertised, quote the amount or range with its currency, pay period, and base/total distinction when stated, then ask: "Is the advertised compensation of <amount or range> acceptable to you for this role?" If compensation is not advertised, ask: "What compensation range would be acceptable to you for this role?" Capture currency, annual salary or hourly rate, and base versus total compensation where needed to make the answer usable. If only part of the compensation is advertised, confirm that part and ask about the missing component when it affects acceptability.
   - Record the advertised terms (or that they are not advertised), the user's answer, and any acceptable range in `## User Position`. Reuse an explicit answer already given for this opportunity; do not ask again unless the terms change or the answer is ambiguous. An unanswered question stays in `## Open Items`; do not infer acceptance from general compensation guidance. Compare the answer with `04_Career_Goals_and_Strategy/Compensation_Targets/compensation-floors.md`, including its Track 9 exception, and reconcile any conflict under the existing protocol. An opportunity-specific answer does not silently change canonical compensation guidance.
2. **Build the claim ledger.** Split what the user said into atomic claims, one per row. Check each against canonical `02_`–`05_` content and the resolved track's role target. Give each a verdict, citing the file:
   - `supported`: canonical evidence covers the claim at the stated scope
   - `partial`: evidence covers a narrower scope than claimed
   - `gap`: no canonical evidence either way
   - `contradicted`: canonical content says otherwise
   - `new-evidence`: a true fact the user supplied that is not in canonical content yet
3. **Add what the user did not say.** Show the analysis's major strengths, gaps and risks that the user's positions skipped, as ledger rows with disposition `open` until the user responds. Do not let the discussion cover only the user's side.
4. **Reconcile each non-`supported` row, blocking ones first, one at a time.** State what canonical says, then offer the outcomes:
   - `evidence-supplied`: the user provides the fact, a document, or their own attestation (record it as owner-attested with the date). It becomes a canonical proposal.
   - `reframed`: the claim is restated at the scope the evidence supports. Record the resulting wording.
   - `accepted-risk`: the gap is real and stays; record how the resume and cover letter handle it honestly.
   - `open`: unresolved. Mark blocking or non-blocking in `## Open Items`.
   Do not concede a claim because the user asserts it, and do not override the user's lived knowledge either. A preference or motivation is the user's to state and is recorded as such; a factual claim about history needs evidence or explicit owner attestation. Flag stale canonical records (for example dated assessments or preferences) and ask whether they still hold.
5. **Propose canonical updates.** List each edit to `02_`–`05_` (file, exact change, why). Apply one only after the user approves that item, using the normal Edit permission prompt and `scripts/careeros touch <file>`. Mark each `[applied]`, `[declined]` or `[deferred]`.
6. **Set the strategy.** With the user, write the resume and cover letter strategy: lead themes, supporting themes, what must not be claimed, how each accepted gap is addressed, and the cover-letter angle (motivation in the user's own words, never invented). Record Resume Keyword Map changes as deltas (`GAP` to evidence, narrowed scope, reordered tier).
7. **Close or leave open.** Set `discussion_status: closed` only when no ledger row is `open`, no canonical proposal is `[proposed]`, and no `[blocking]` item remains. Otherwise leave it `open` and tell the user what blocks closure.

If the discussion shows a disqualifier or changes the recommendation, say so in `## Reconciliations` (effect on recommendation: unchanged, upgraded or downgraded, with reasons). Do not edit `analysis.md`. For a `pass`, point the user to `/close-opportunity`.

## Output
`/06_Job_Opportunities/<opportunity-folder>/discussion.md`:

```markdown
---
discussion_status: open | closed
---

# Opportunity Discussion

## User Position
(the user's fit thesis, risks, lead themes and dislikes, in their words; advertised compensation or not advertised, and their compensation acceptance or acceptable range)

## Claim Ledger
| id | claim | verdict | evidence | disposition |
|---|---|---|---|---|
| C1 | ... | supported | 02_Work_Experience/Roles/<file>.md | agreed |
(verdict: supported | partial | gap | contradicted | new-evidence)
(disposition: agreed | evidence-supplied | reframed | accepted-risk | open)

## Reconciliations
(one entry per non-supported row: what canonical says, what was decided, resulting wording; effect on recommendation)

## Canonical Proposals
- [applied|declined|deferred|proposed] <file>: <change>

## Keyword Map Deltas

## Resume and Cover Letter Strategy

## Open Items
- [blocking|non-blocking] <item>
```

`careeros check` validates this structure (`scripts/state_checks.py`).

## Downstream Contract
For opportunities added on or after 2026-11-03, `/build-resume` and `/build-application` require a `discussion.md` with `discussion_status: closed`. They apply its Keyword Map Deltas on top of `analysis.md` and follow its strategy. Where the two differ, `discussion.md` governs positioning and `analysis.md` stays the original assessment.

## Must NOT
- edit `analysis.md`, `job-opportunity.md`, or any other file in the opportunity folder besides `discussion.md`
- edit `02_`–`05_` without per-item user approval, or state a fact there that is not in the user's words, a document, or canonical content
- generate resumes, cover letters or application artifacts
- decide a dispute for the user, or close the discussion on their behalf
- commit, push, or stage anything unless the user asks

## Failure Handling
- Missing inputs: do not infer; list them.
- A user claim with no evidence is a `gap`, not a fact. Carry it as a gap, never as an assumption silently treated as true.

## Runtime IO Emission (Required)

Start the run file with `scripts/careeros new-run discuss-opportunity <slug> --target <opportunity-folder>`. Replace every `TODO` with grounded content before the gate.
Emit the runtime objects in the order defined in `Career/00_Core_OS/Prompts/Runtime/runtime-io-schema.md` (`request`, `task`, `mode_selection`, `routing_output`, `context_block`, `prompt_object`, `output`, `validation_result`, `artifact_destination`, `execution_trace`). Do not skip objects; preserve upstream objects if halted; do not write `discussion.md` when `validation_result.passed` is `false`.
The run covers `discussion.md`. Canonical edits are separate, user-approved steps after the gate passes, and are listed under `## Canonical Proposals`.

## Deterministic Conformance Gate (Required)
At end of the run, execute `Career/00_Core_OS/Prompts/Runtime/command-conformance-gate.md` and
`scripts/run_command_gate.sh "Career/00_Core_OS/Runs/<YYYY-MM-DD>_discuss-opportunity_<slug>.runtime-io.yaml"`.
If any check fails: STOP, set `validation_result.passed: false` and `artifact_destination.write_allowed: false`, populate `execution_trace.halted_at` and `execution_trace.reason`, and write nothing until the gate passes.
