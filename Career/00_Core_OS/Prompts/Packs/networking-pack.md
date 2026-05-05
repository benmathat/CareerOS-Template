---
Last Update: 2026-04-24
Previous Update: 2026-04-22
---

# Networking Pack

## 1. Purpose

Provide a **deterministic execution pack** for converting networking intent into:
- targeted outreach
- structured conversations
- tracked interactions
- compounding relationships

This pack transforms networking from ad hoc activity into a **repeatable system** aligned with CareerOS.

This pack defines constraints, structure, and orchestration expectations only.

Runtime behavior is governed by `Prompts/Runtime/*`. This file defines only domain-specific constraints and MUST NOT restate runtime halt, validation, routing, or context-loading mechanics.

It does NOT:
- Perform mode selection directly
- Perform source routing
- Perform context loading
- Execute tasks directly

---

## 2. Scope

Use this pack when you need to:
- identify and prioritize contacts
- draft outreach messages
- execute and track interactions
- manage follow-ups
- evolve relationships over time

This pack governs **execution and tracking**, not long-term relationship philosophy.

---

## 3. Execution Profile

### Modes
- Primary: `execute`
- Secondary: `analyze` (for prioritization and refinement)

### Workflow Pattern

```
Target → Prioritize → Draft → Send → Track → Follow-up → Evolve Relationship
```

---

## 4. Source Routing

### Relationship Context
- `/08_Networking_and_References/`

### Opportunity Context (if applicable)
- `/06_Job_Opportunities/`

### Strategic Alignment
- `/04_Career_Goals_and_Strategy/`

Rules:

- Canonical sources are authoritative
- Contextual sources MUST NOT override canonical truth
- Missing canonical grounding MUST be surfaced as a gap
- Conflicts between sources MUST be surfaced, not resolved silently

---

## 5. Context Assembly Rules

### Required Signals
- who the contact is (role, company, relevance)
- why this contact matters
- objective of outreach

### Optional Signals
- prior interaction history
- shared connections or context
- active opportunity linkage

### Context Compression
Extract:
- relevance signal (why them)
- positioning signal (why you)
- opportunity linkage (if any)
- prior interaction status

Remove:
- generic descriptors
- non-actionable background

Additional Rules:

- Required signals MUST be sufficient to support outreach decisions
- Missing signals MUST be surfaced as context gaps
- Assumptions MUST be explicitly labeled when used

---

## 6. Contact State Model

Each contact should exist in one of the following states:

```text
target → contacted → responded → engaged → inactive
```

### State Definitions
- **target**: identified but not contacted
- **contacted**: outreach sent
- **responded**: reply received
- **engaged**: meaningful interaction (conversation, referral, interview)
- **inactive**: no response or relationship paused

State Rules:

- State transitions MUST be explicit and recorded
- No state may be inferred without supporting interaction data
- State changes MUST be traceable to logged activity

---

## 7. Outreach Composition Model (CRITICAL)

All outreach MUST follow this structure:

### 7.1 Message Structure

1. **Context Anchor**
   - why you are reaching out to *this specific person*

2. **Credible Positioning**
   - who you are in a way that aligns to their context

3. **Specific Ask**
   - clear, low-friction request
   - example: short call, quick guidance, referral insight

4. **Optional Exit**
   - reduce pressure
   - allow easy non-response

---

### 7.2 Message Constraints

- concise (3–6 sentences preferred)
- specific (no generic templates)
- relevant to recipient
- low-friction ask
- no fluff or filler

Additional Rules:

- All claims MUST be grounded in canonical context or explicit inputs
- Personalization MUST be traceable to context signals
- Assumptions MUST be labeled if used to bridge missing context

---

## 8. Follow-Up Model

### Standard Cadence

- Day 0: initial outreach
- Day 3–5: follow-up #1
- Day 7–10: final follow-up

### Rules

- each follow-up adds value or context
- do not repeat the same message
- stop after final follow-up unless new signal emerges

### Follow-Up Types
- reminder (light nudge)
- value-add (new context, update, or insight)
- close-loop (final message)

Additional Rules:

- Follow-up timing MUST be consistent with cadence unless overridden by signal
- Follow-ups MUST not introduce new unsupported claims
- Gaps in context MUST be surfaced if follow-up content requires them

---

## 9. Interaction Tracking

### Required Actions

After each interaction:
- update contact record in `/08_Networking_and_References/`
- record:
  - date
  - message or interaction summary
  - status change
  - next step

Tracking Rules:

- All interactions MUST be recorded consistently
- Missing data MUST be marked as `MISSING`
- No interaction may be omitted once execution occurs

---

## 10. Compliance Hook

### When to Trigger

After any of the following:
- outreach sent
- follow-up sent
- response received
- informational interview or conversation completed

### Action

→ Recommend: `/log-activity`

### Purpose
- capture networking as a qualifying work search activity
- record contact, method, and outcome
- optionally link evidence (email, LinkedIn message, notes)

### Constraint

Do NOT recommend `/log-activity` for:
- internal drafting
- contact research only

---

## 11. Output Set

- prioritized contact list
- outreach draft(s)
- follow-up sequence
- contact update notes

Output Rules:

- Outputs MUST align with `output-standards.md`
- Outputs MUST include required disclosures (assumptions, gaps, warnings)
- Outputs MUST reflect context status (complete vs partial)

---

## 12. Output Routing

### Contact Records
- `/08_Networking_and_References/`

### Opportunity-Linked Notes
- `/07_Applications_and_Interviews/`

Additional Rules:

- Outputs MUST NOT modify canonical sources
- Outputs MUST be traceable to source context
- No artifacts may be written if validation fails

---

## 13. Quality Criteria

All outputs must be:

- personalized (specific to recipient)
- grounded in context
- aligned with career objectives
- concise and high-signal
- actionable

Additional Requirements:

- Assumptions are explicitly labeled when present
- Context gaps are surfaced when materially relevant
- No unsupported claims are introduced
- Outputs align with context status (complete vs partial)

---

## 14. Remediation Patterns

### Weak Targeting
- Refine contact selection
- Improve relevance signals

### Low Response Rate
- Revise messaging
- Adjust positioning or ask

## 15. Invocation Interface

### Minimal

```text
Use Networking Pack

task.objective:
Target:
```

### Full

```text
Use Networking Pack

task.objective:
Target:
Context:
- prior interactions
- opportunity linkage

Constraints:
- tone
- length
- ask
```

---

## 16. Validation Hooks

- Contact selection is grounded and justified
- Outreach content is traceable to context signals
- No unsupported or fabricated claims are present
- All assumptions and gaps are explicitly labeled
- Interaction tracking is complete and consistent
- State transitions are valid and traceable

---

## 17. Summary

The Networking Pack provides:

- a deterministic outreach system
- structured message composition
- consistent follow-up behavior
- relationship lifecycle tracking
- integration with compliance requirements

It ensures deterministic, grounded, and traceable networking execution aligned with CareerOS runtime constraints.