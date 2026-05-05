---
Last Update: 2026-05-05
Previous Update: 2026-04-24
---

# Interview Pack

## 1. Purpose

Provide a **pre-configured prompt execution pack** for preparing, structuring, and refining interview responses using CareerOS.

This pack defines constraints, structure, and expectations only.

Runtime behavior is governed by `Prompts/Runtime/*`. This file defines only domain-specific constraints and MUST NOT restate runtime halt, validation, routing, or context-loading mechanics.

It does NOT:
- Perform mode selection directly
- Perform source routing
- Perform context loading
- Execute tasks directly

---

## 2. Scope

Use this pack when you need to:

- Prepare for an upcoming interview
- Generate answers to common behavioral questions
- Build and refine STAR stories
- Align experience to a specific role
- Practice concise, high-impact responses

---

## 3. Domain Inputs

### Required

- Target role or job description
- Relevant work experience

### Optional

- Existing stories
- Specific interview questions
- Prior interview prep notes
- Company research
- Constraints (time, tone)

---

## 4. Source Expectations

### Canonical Sources

- [`/02_Work_Experience/`](../../../02_Work_Experience/)
- [`/02_Work_Experience/Stories/`](../../../02_Work_Experience/Stories/)
- [`/03_Skills_and_Portfolio/`](../../../03_Skills_and_Portfolio/)
- [`/04_Career_Goals_and_Strategy/`](../../../04_Career_Goals_and_Strategy/)

---

### Contextual Sources

- [`/06_Job_Opportunities/`](../../../06_Job_Opportunities/)
- [`/07_Applications_and_Interviews/Interview_Prep/`](../../../07_Applications_and_Interviews/Interview_Prep/)
- [`/09_Research_and_Market_Intelligence/`](../../../09_Research_and_Market_Intelligence/)

---

### Presentation Inputs (Optional)

- [`/01_Resume_and_Profiles/`](../../../01_Resume_and_Profiles/)

Used only as:
- framing reference

Never as source-of-truth

---

Rules:

- Canonical sources are authoritative
- Contextual sources MUST NOT override canonical truth
- Missing canonical grounding MUST be surfaced as a gap
- Conflicts between sources MUST be surfaced, not resolved silently

---

## 5. Domain Constraints

```
task.objective:
Prepare interview responses for the target role.

task.constraints.hard:
- Use structured storytelling (STAR preferred)
- Keep responses concise and high-impact
- Align directly with role expectations

task.inputs.required:
- Work experience
- Stories
- Job description

task.output_type:
- Document (default for answer sets and story prep artifacts)
```

---

Additional Constraints:

Before prompt assembly, extract:

- Key stories
- Measurable outcomes
- Relevant skills
- Alignment to job requirements

Remove:

- Redundant narrative
- Irrelevant experiences

---

- Compression MUST preserve all critical facts and outcomes
- No meaningful information may be removed without justification

---

## 6. Domain Quality Gates

Each story should include:

- Situation
- Task
- Action
- Result (with metrics if possible)

Enhancements:

- Emphasize decision-making
- Highlight leadership and ownership
- Show outcomes and impact clearly

---

- All claims MUST be grounded in canonical sources or explicit inputs
- Metrics MUST be real
- Ownership MUST be clearly defined

---

### Output Formats

#### Structured Answers

- STAR format
- Clear, concise paragraphs

---

#### Story Library

- Reusable story set
- Tagged by competency

---

#### Mock Interview

- Question → Answer format
- Optional critique

---

## 7. Domain Validation Hooks

- Story selection is evidence-based and role-aligned
- Answers remain concise (60-120 seconds spoken target)
- Claims and metrics remain traceable to canonical evidence
- Canonical sources remain unchanged

---

## 8. Output Routing

Save results to:

- [`/07_Applications_and_Interviews/Interview_Prep/`](../../../07_Applications_and_Interviews/Interview_Prep/)

Suggested structure:

- Stories/
- Answers/
- Mock_Interviews/

---

- Outputs MUST NOT modify canonical sources
- Outputs MUST be traceable to source context

---

## 9. Invocation Interface

### Required Inputs

- Target role or job description

---

### Optional Inputs

- Specific questions
- Existing stories
- Constraints (time, tone)

---

### Minimal Invocation

```
Use Interview Pack

Target Role:
<job description or summary>
```

---

### Full Invocation

```
Use Interview Pack

Target Role:
<job description>

Focus:
- Behavioral questions
- Leadership examples

Inputs:
- Existing stories (optional)

Constraints:
- Keep answers under 2 minutes spoken length
```

---

## 10. Summary

The Interview Pack provides:

- Structured story extraction
- Deterministic answer generation
- Reusable interview preparation workflows

It ensures deterministic, grounded, and interview-ready outputs aligned with CareerOS domain constraints.

## 11. Question Mapping

Map interview questions to relevant story types.

### Common Mappings

- Leadership → ownership, team coordination, decision-making
- Conflict → disagreement, resolution, influence without authority
- Failure → mistake, accountability, recovery
- Achievement → measurable impact, delivery under pressure
- Initiative → proactive problem solving

---

### Selection Rule

For each question:

1. Identify competency being tested
2. Select best-matching story
3. Adapt story framing to question

## 12. Answer Compression

Target:
- 60–120 seconds spoken

Rules:
- Lead with outcome
- Minimize setup
- Focus on actions and results
- End with impact

Avoid:
- Over-explaining context
- Long chronological buildup