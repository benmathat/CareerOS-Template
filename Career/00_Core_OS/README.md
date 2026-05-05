---
Last Update: 2026-05-05
Previous Update: 2026-04-22
---

# Orientation & Control

> **For an overview of the entire Career workspace, see [`../README.md`](../README.md).**  
> This file focuses specifically on the `00_Core_OS/` folder.

This folder is the **control plane** for the entire Career workspace.

Its purpose is to:
- Establish current focus and priorities
- Provide navigation into active materials
- Prevent loss of context over time

This is where you orient yourself when:
- Restarting a search
- Feeling scattered
- Reviewing progress
- Pausing or resuming activity

## What Belongs Here

- Current search status
- Indexes and summaries
- The rolling activity log
- Reusable AI prompt packs in `Prompts/` for activity-specific workflows

If this folder is neglected, the rest of the system will drift.

This folder should be reviewed regularly.

## Runtime Execution Onboarding (Current)

When you are executing CareerOS commands, start with:

1. `Prompts/README.md`
2. `Prompts/Runtime/operator-runbook.md`
3. `.cursor/commands/*.md`

Runtime outputs are emitted to:

- `.cursor/runtime/<command>.runtime-io.yaml`

Before final artifact writes, run:

- `scripts/run_command_gate.sh ".cursor/runtime/<command>.runtime-io.yaml"`

## How `career-index.md` Works

`career-index.md` is the current orientation and control anchor for the Career workspace.

---

### `career-index.md` — Strategic Anchor

**Purpose:**  
`career-index.md` provides a **stable, high-level view** of your career search.

It answers questions like:
- What roles am I targeting?
- What searches are active?
- Where are the key materials?
- Who are the important people involved?

**How it is used:**
- As the starting point when opening the Career folder
- To re-orient after a break
- To explain your search to a coach, recruiter, or advisor
- To maintain continuity over weeks or months

**Change frequency:** Low  
This file should evolve slowly and remain valid over time.

---

### Tactical Status (Optional Companion)

If you maintain a separate tactical status document, link it from `career-index.md` and treat it as high-frequency operational state.