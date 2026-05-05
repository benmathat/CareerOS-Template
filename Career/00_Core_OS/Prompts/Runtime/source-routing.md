---
Last Update: 2026-05-05
Previous Update: 2026-04-24
---

# Source Routing (Runtime Contract)

## 1. Purpose

Define how the Prompt Runtime selects, prioritizes, and combines CareerOS sources to produce grounded, minimal, and mode-compatible context.

This file is the **Routing Layer** between `task`/`mode_selection` and context loading.

It MUST:
- Select the minimum viable source set
- Preserve canonical vs contextual boundaries
- Produce deterministic routing outputs
- Prevent context bloat and source-of-truth violations

It MUST NOT:
- Introduce task logic
- Override System, Context, or Mode contracts
- Treat presentation artifacts as canonical truth

---

## 2. Path Convention

This specification uses **logical paths** relative to `Career/`.

Examples:
- Logical path: `/02_Work_Experience/Stories/`
- Repository path: `Career/02_Work_Experience/Stories/`
- GitHub link from this file: `[02_Work_Experience/Stories](../../../02_Work_Experience/Stories/)`

### 2.1 Path Representation Rules

- Use **logical paths** in routing logic and prose
- Use **repository-relative Markdown links** only when navigability matters
- Do NOT assume repository root in routing statements
- Treat `Career/` as the logical routing root in all decisions

---

## 3. Routing Principles

### 3.1 Canonical vs Contextual

- **Canonical Sources** = durable truth expected to remain valid over time
- **Contextual Sources** = opportunity-, workflow-, or session-specific context

Rule:
- Prefer canonical truth by default
- Use contextual sources only when task-specific relevance requires them

### 3.2 Truth vs Presentation

- Truth belongs in canonical and system-controlled domains
- Presentation artifacts are derivatives, not authorities

Rule:
- Presentation artifacts MUST NOT be treated as source-of-truth

### 3.3 Minimal Viable Context

- Load only what is required for successful execution
- Prefer targeted files over broad folder injection
- Prefer narrower domain slices before whole-domain loading

Rule:
- Default to minimal viable context

### 3.4 Routing Determinism

Given the same `task`, `mode_selection`, and available sources, routing MUST produce the same source set.

---

## 4. Source Domain Model

### 4.1 System Domains

Used for architecture, orchestration, indexes, and control logic.

- [`/00_Core_OS/`](../../../00_Core_OS/)
  - Indexes, maps, prompt runtime, architecture specs

### 4.2 Presentation Domains

Used for externally-facing representations.

- [`/01_Resume_and_Profiles/`](../../../01_Resume_and_Profiles/)
  - Resume variants, cover letters, profiles

### 4.3 Canonical Truth Domains

Used for durable truth and reusable evidence.

- [`/02_Work_Experience/`](../../../02_Work_Experience/)
  - Roles, projects, metrics, long-form stories
- [`/03_Skills_and_Portfolio/`](../../../03_Skills_and_Portfolio/)
  - Capability evidence, artifacts, proof
- [`/04_Career_Goals_and_Strategy/`](../../../04_Career_Goals_and_Strategy/)
  - Role targets, constraints, direction
- [`/05_Personal_Profile/`](../../../05_Personal_Profile/)
  - Values, preferences, non-negotiables

### 4.4 Execution Domains

Used for active opportunities, applications, and tactical workflows.

- [`/06_Job_Opportunities/`](../../../06_Job_Opportunities/)
  - Job descriptions, company context
- [`/07_Applications_and_Interviews/`](../../../07_Applications_and_Interviews/)
  - Interview prep, tailored stories, application materials
- [`/08_Networking_and_References/`](../../../08_Networking_and_References/)
  - Contacts, references, relationship notes
- [`/09_Research_and_Market_Intelligence/`](../../../09_Research_and_Market_Intelligence/)
  - Market data, company research, compensation insights

### 4.5 Reflection Domains

Used for adaptation, review, and compliance tracking.

- [`/10_Coaching_Feedback_and_Notes/`](../../../10_Coaching_Feedback_and_Notes/)
  - Coaching inputs, lessons learned
- [`/11_Job_Search_Activities/`](../../../11_Job_Search_Activities/)
  - Activity logs, compliance tracking

---

## 5. Routing Inputs

Routing MUST be based on normalized runtime inputs:

- `mode_selection.primary_mode`
- `mode_selection.secondary_mode` (optional)
- `task.objective`
- `task.artifact_state` = `new | existing | none`
- `task.output_type`
- `request.pipeline` (optional workflow hint)
- `request.intent` (for opportunity-specific intent disambiguation)
- `task.target_artifact` (optional)

If an input is missing, it MUST be inferred or declared as an assumption.

If required inputs cannot be reliably inferred:

- Set `routing_output.status: invalid`
- Set `routing_output.blocking: true`
- Record missing inputs in `assumptions`

---

## Routing Validation

Before producing output:

- All required inputs are present or explicitly inferred
- Mode and workflow are not in conflict
- Output destination is determinable
- Required source set is non-empty

If validation fails:

- Set `routing_output.status: invalid`
- Set `routing_output.blocking: true`
- Do NOT return incomplete routing without flags

---

## 6. Routing Output Contract

routing_output:
  status: valid|partial|invalid
  blocking: true|false
  source_set:
    required:
    optional:
    excluded:
  selection_rationale:
  conflict_rules_applied:
  output_destination:
  assumptions:
  completeness:
    required_sources_resolved: true|false
    assumptions_used: true|false
  confidence: high|medium|low

Definitions:
- `status` = overall validity of `routing_output`
- `blocking` = whether downstream execution must halt
- `required` = sources that must be loaded for task completion
- `optional` = sources eligible only if needed after required sources
- `excluded` = sources that must not be used for this run
- `output_destination` = logical target path for resulting artifact when applicable

### Required Source Rule

A source MUST be classified as `required` only if:

- The task cannot be completed without it
- It contains primary truth or mandatory context
- Its absence would degrade output correctness

Optional sources MUST NOT be necessary for task completion.

---

## 7. Routing by Mode

### 7.1 Build Mode

Goal: create complete, net-new artifacts

Required default sources:
- `/02_Work_Experience/`
- `/03_Skills_and_Portfolio/`
- `/04_Career_Goals_and_Strategy/`
- `/05_Personal_Profile/`

Optional sources:
- `/06_Job_Opportunities/`
- `/07_Applications_and_Interviews/`
- `/08_Networking_and_References/`
- `/09_Research_and_Market_Intelligence/`

Excluded by default:
- `/01_Resume_and_Profiles/` as primary truth source

Rules:
- Add execution domains only when tied to a specific opportunity or workflow
- Do not route presentation artifacts as authoritative inputs
- Required sources MUST be sufficient for task completion without relying on optional sources.

### 7.2 Analyze Mode

Goal: evaluate artifacts, decisions, or workflows

Required default sources:
- `target_artifact`

Optional sources:
- `/02_Work_Experience/`
- `/03_Skills_and_Portfolio/`
- `/04_Career_Goals_and_Strategy/`
- `/05_Personal_Profile/`
- `/06_Job_Opportunities/`
- `/07_Applications_and_Interviews/`
- `/08_Networking_and_References/`
- `/09_Research_and_Market_Intelligence/`
- `/10_Coaching_Feedback_and_Notes/`
- `/11_Job_Search_Activities/`

Rules:
- Artifact under analysis MUST be loaded first
- Canonical sources validate truth
- Contextual sources supply situational relevance only when needed
- Required sources MUST be sufficient for task completion without relying on optional sources.

### 7.3 Refine Mode

Goal: improve an existing artifact

Required default sources:
- `target_artifact`

Optional sources:
- `/02_Work_Experience/`
- `/03_Skills_and_Portfolio/`
- `/04_Career_Goals_and_Strategy/`
- `/05_Personal_Profile/`
- `/10_Coaching_Feedback_and_Notes/`

Rules:
- Route canonical sources for truth validation
- Route reflection sources only when refinement is driven by feedback
- Required sources MUST be sufficient for task completion without relying on optional sources.

### 7.4 Execute Mode

Goal: produce tactical, immediately usable outputs

Required default sources:
- `/06_Job_Opportunities/`
- `/07_Applications_and_Interviews/`
- `/08_Networking_and_References/`
- `/09_Research_and_Market_Intelligence/`

Optional sources:
- `/02_Work_Experience/`
- `/03_Skills_and_Portfolio/`
- `/04_Career_Goals_and_Strategy/`
- `/05_Personal_Profile/`
- `/01_Resume_and_Profiles/`

Rules:
- Prioritize execution context first
- Use canonical domains only as grounding support
- Use presentation domains only as formatting/reference baselines
- Required sources MUST be sufficient for task completion without relying on optional sources.

### 7.5 Architect Mode

Goal: design systems, workflows, and reusable frameworks

Required default sources:
- `/00_Core_OS/`

Optional sources:
- `/02_Work_Experience/`
- `/03_Skills_and_Portfolio/`
- `/04_Career_Goals_and_Strategy/`
- `/05_Personal_Profile/`
- `/06_Job_Opportunities/`
- `/07_Applications_and_Interviews/`
- `/08_Networking_and_References/`
- `/09_Research_and_Market_Intelligence/`
- `/10_Coaching_Feedback_and_Notes/`
- `/11_Job_Search_Activities/`

Rules:
- System domains drive structure
- Canonical domains ground design intent
- Execution and reflection domains may validate practicality but MUST NOT define architecture on their own
- Required sources MUST be sufficient for task completion without relying on optional sources.

---

## 8. Routing by Workflow Type

### Resume / Profile Work

Required:
- `/02_Work_Experience/`
- `/03_Skills_and_Portfolio/`
- `/04_Career_Goals_and_Strategy/`

Optional:
- `/01_Resume_and_Profiles/`
- `/06_Job_Opportunities/`

Excluded as truth:
- `/07_Applications_and_Interviews/` unless adapting to a specific opportunity

### Application Work

Required:
- `/06_Job_Opportunities/`
- `/02_Work_Experience/`
- `/03_Skills_and_Portfolio/`
- `/04_Career_Goals_and_Strategy/`

Optional:
- `/01_Resume_and_Profiles/`
- `/07_Applications_and_Interviews/`
- `/11_Job_Search_Activities/`

Compliance Hook:
- Recommend `/log-activity` only after a real-world qualifying application action is completed.

### Interview Prep

Required:
- `/06_Job_Opportunities/`
- `/07_Applications_and_Interviews/Interview_Prep/`
- `/02_Work_Experience/Stories/`

Optional:
- `/03_Skills_and_Portfolio/`
- `/08_Networking_and_References/`
- `/10_Coaching_Feedback_and_Notes/`

Compliance Hook:
- Scheduling and completion are separate real-world events.

### Networking

Required:
- `/08_Networking_and_References/`

Optional:
- `/04_Career_Goals_and_Strategy/`
- `/06_Job_Opportunities/`
- `/11_Job_Search_Activities/`

Compliance Hook:
- Recommend `/log-activity` only when contact, meeting, referral request, or follow-up was actually performed.

---

### 8.1 Resume Tailoring

Required:
- `/02_Work_Experience/`
- `/03_Skills_and_Portfolio/`
- `/04_Career_Goals_and_Strategy/`
- `/06_Job_Opportunities/`

Optional:
- `/01_Resume_and_Profiles/`
- `/09_Research_and_Market_Intelligence/`

Output destination:
- `/01_Resume_and_Profiles/`

### 8.2 Interview Preparation

Required:
- `/02_Work_Experience/Stories/`
- `/07_Applications_and_Interviews/Interview_Prep/`
- `/06_Job_Opportunities/`

Optional:
- `/09_Research_and_Market_Intelligence/`
- `/08_Networking_and_References/`

Output destination:
- `/07_Applications_and_Interviews/Interview_Prep/`

### 8.3 Story Extraction

Required:
- `/02_Work_Experience/`
- `/03_Skills_and_Portfolio/`

Optional:
- `/10_Coaching_Feedback_and_Notes/`

Output destination:
- `/02_Work_Experience/Stories/`

### 8.4 Opportunity Analysis

Required:
- `/06_Job_Opportunities/`
- `/09_Research_and_Market_Intelligence/`
- `/04_Career_Goals_and_Strategy/`

Optional:
- `/05_Personal_Profile/`

Output destination:
- `/06_Job_Opportunities/` or `/07_Applications_and_Interviews/` depending on whether analysis remains opportunity-scoped or advances into execution

### 8.5 Networking / Outreach

Required:
- `/08_Networking_and_References/`
- `/04_Career_Goals_and_Strategy/`

Optional:
- `/06_Job_Opportunities/`
- `/07_Applications_and_Interviews/`

Output destination:
- `/08_Networking_and_References/` or `/07_Applications_and_Interviews/` depending on whether the output is relationship-log oriented or application-support oriented

---

## 9. Conflict Resolution Rules

### 9.1 Canonical vs Contextual

- Canonical wins by default
- Contextual overrides only when the task is explicitly opportunity- or workflow-specific

### 9.2 Multiple Canonical Sources

When canonical sources conflict, prefer in order:
1. Most specific
2. Most recent
3. Most quantified
4. Most directly tied to the `task` objective

### 9.3 Presentation vs Canonical

- Presentation artifacts NEVER override canonical truth
- Presentation artifacts may influence phrasing, structure, or formatting only

### 9.4 Missing Data

- Do NOT hallucinate
- Return `Context Gaps`
- Request minimal additional input or use closest valid canonical evidence with explicit labeling

If conflicts affect routing decisions:

- Record decision in `conflict_rules_applied`
- Reduce `confidence` level when ambiguity remains

---

## 10. Source Selection Heuristics

When narrowing files within a routed domain, prefer in order:

1. Indexed or mapped files
2. Structured artifacts over freeform notes
3. Files explicitly referenced by the `task`
4. Recent files when recency matters
5. Quantified evidence over qualitative claims
6. Narrow subdirectories over top-level folder sweeps

---

## Determinism Enforcement

When multiple valid routing options exist:

- Prefer narrower scope over broader
- Prefer canonical over contextual
- Prefer indexed or structured sources
- Prefer fewer sources over many

Tie-breakers MUST be consistent and repeatable.

---

## 11. Output Routing Rules

### 11.1 Canonical Outputs

Route to canonical domains only when the output is expected to remain true over time.

Eligible destinations:
- `/02_Work_Experience/`
- `/03_Skills_and_Portfolio/`
- `/04_Career_Goals_and_Strategy/`
- `/05_Personal_Profile/`

### 11.2 Execution Outputs

Route to execution domains when the output is opportunity-, application-, or session-specific.

Eligible destinations:
- `/01_Resume_and_Profiles/`
- `/06_Job_Opportunities/`
- `/07_Applications_and_Interviews/`
- `/08_Networking_and_References/`

### 11.3 Reflection Outputs

Route to reflection domains when the output captures feedback, lessons, or compliance activity.

Eligible destinations:
- `/10_Coaching_Feedback_and_Notes/`
- `/11_Job_Search_Activities/`

### 11.4 Routing Rule

If content would still be true next month, prefer canonical output routing.
If content is tied to an active opportunity, application, or session, prefer execution routing.
If content is a lesson, review, or activity record, prefer reflection routing.

---

## 12. Validation Checks

Before returning routing results, the runtime MUST verify:

- Required sources align with selected mode
- Excluded sources are not acting as authorities
- Source set is minimal rather than comprehensive
- Output destination matches content durability and workflow scope

If validation fails:
- Recompute routing
- Do NOT return invalid source selection

---

## 13. Failure Handling

### Missing Required Inputs

- Set `routing_output.status: invalid`
- Set `routing_output.blocking: true`
- Record missing inputs in `assumptions`

### Ambiguous Routing

- Select minimal viable source set
- Record ambiguity in `assumptions`
- Set `confidence: medium` or `low`

### Conflicting Signals

- Prioritize in order:
  1. `mode_selection.primary_mode`
  2. `task.objective`
  3. `request.pipeline`
- Record override decision in `conflict_rules_applied`

### Empty Required Source Set

- Set `routing_output.status: invalid`
- Set `routing_output.blocking: true`

### Over-Broad Source Selection

- Reduce to minimal viable context
- Prefer high-relevance and high-signal sources

---

## 14. Summary

This routing layer ensures:

- Deterministic source selection
- Strict separation of truth, presentation, execution, and reflection
- Minimal and grounded context loading
- Correct output destination routing

It is the control point that ensures routing outputs are valid, minimal, and sufficient for downstream context loading and execution. It determines whether routing is complete, incomplete-but-usable, or invalid-and-blocking.