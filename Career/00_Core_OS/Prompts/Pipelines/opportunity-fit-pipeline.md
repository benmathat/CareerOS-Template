---
Last Update: 2026-11-03
---

# Opportunity Fit Pipeline (Per-Opportunity Pipeline Contract)

## 1. Purpose

Orchestrate the path from a confirmed opportunity to a reconciled, evidence-grounded positioning strategy for **one** opportunity, before any resume or cover letter is built.

`opportunity-review-pipeline` manages the whole portfolio. This pipeline governs a single opportunity's fit decision and is the stage between analysis and artifact generation.

Runtime behavior is governed by `Prompts/Runtime/*`. This file defines only workflow-specific constraints and MUST NOT restate runtime halt, validation, routing, or context-loading mechanics.

## 2. Stages

```text
Analyze  →  Discuss  →  Reconcile  →  Record  →  Hand off
```

| Stage | Command | Output |
|---|---|---|
| 1. Analyze | `/analyze-opportunity` | `analysis.md` (original assessment; never rewritten later) |
| 2. Discuss | `/discuss-opportunity` | user position, then claim ledger |
| 3. Reconcile | `/discuss-opportunity` | disposition for every non-supported claim |
| 4. Record | `/discuss-opportunity` | `discussion.md`; user-approved edits to `02_`–`05_` |
| 5. Hand off | `/build-resume`, `/build-application` | artifacts built on `analysis.md` plus `discussion.md` |

## 3. Stage Rules

- **User position precedes verdict.** The user states their fit thesis and risks before seeing scores or the recommendation.
- **Weigh, don't defer.** Every user claim is checked against canonical content and the resolved track's role target. A claim is not accepted because it is asserted, and the user's lived knowledge is not overridden: factual claims without evidence are `gap` until the user supplies evidence or owner attestation.
- **Two-sided ledger.** The analysis's material strengths, gaps and risks the user did not raise are also put to the user.
- **Reconciliation outcomes** are exactly `evidence-supplied`, `reframed`, `accepted-risk` or `open`. Every decision names who made it.
- **Canonical hygiene.** A true fact goes into canonical `02_`–`05_` first, by a per-item user-approved edit, and only then into an artifact. `discussion.md` is an execution-layer record and never overrides canonical content; conflicts are flagged, not silently resolved.
- **Closure.** Hand-off requires `discussion_status: closed`: no `open` ledger row, no `[proposed]` canonical edit, no `[blocking]` item.
- **Recommendation changes** (including toward `pass` or a disqualifier) are recorded in `discussion.md`; `analysis.md` is not edited. A `pass` routes to `/close-opportunity`.

## 4. Inputs and Outputs

```yaml
request:
  run: opportunity_fit_pipeline
  opportunity: /06_Job_Opportunities/<company>_<role>_<date>/
outputs:
  analysis: analysis.md
  discussion: discussion.md        # discussion_status: closed to hand off
  canonical_updates: user-approved edits under 02_-05_ (listed in discussion.md)
```

## 5. Failure Handling

- Missing or unconfirmed record or analysis: stop and name what is missing.
- User unavailable or evidence pending: leave `discussion_status: open`, list `[blocking]` items, and stop. Do not build artifacts.
- Canonical edit declined: record `[declined]` and carry the claim as a gap or reframe it; do not use the fact in an artifact.

## 6. Validation Hooks

- `careeros check` validates `discussion.md` structure and closure rules (`scripts/state_checks.py`).
- For opportunities added on or after 2026-11-03, a resume or cover letter without a closed `discussion.md` fails the check.
