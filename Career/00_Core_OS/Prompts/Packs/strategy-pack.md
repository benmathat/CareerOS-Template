---
Last Update: 2026-04-22
Previous Update:
---

# Strategy Pack

## Purpose

Provide domain-specific constraints and structure for clarifying direction, evaluating trade-offs, and setting role pursuit priorities.

This pack defines constraints, structure, and orchestration expectations only.

Runtime behavior is governed by `Prompts/Runtime/*`. This file defines only domain-specific constraints and MUST NOT restate runtime halt, validation, routing, or context-loading mechanics.

It does NOT:
- Perform mode selection directly
- Perform source routing
- Perform context loading
- Execute tasks directly

## Mode Profile

- primary: `architect`
- secondary: `analyze`

## Required Inputs

- strategic question or decision
- time horizon (near-term vs long-term)

Rules:

- Required inputs MUST be sufficient to support a decision
- Missing required inputs MUST be surfaced as context gaps

## Optional Inputs

- current pipeline snapshot
- constraints (compensation, geography, lifestyle)
- personal non-negotiables

## Source Routing

- goals and strategy: `04_Career_Goals_and_Strategy/`
- personal constraints: `05_Personal_Profile/`
- current execution signals: `06`, `07`, `10`

Additional Rules:

- Canonical sources define strategic baseline
- Contextual sources MUST NOT override canonical truth
- Missing canonical grounding MUST be surfaced as a gap
- Conflicts between sources MUST be surfaced, not resolved silently

## Output Set

- decision framework
- options and trade-offs
- selected direction with rationale
- 30-60 day action plan

Output Rules:

- Outputs MUST align with `output-standards.md`
- Outputs MUST include required disclosures (assumptions, gaps, warnings)
- Outputs MUST reflect context status (complete vs partial)
- All recommendations MUST be grounded in context or explicitly labeled assumptions

## Output Routing

- strategic artifacts to `04_Career_Goals_and_Strategy/`
- operating updates to `00_Core_OS/`

Additional Rules:

- Outputs MUST NOT modify canonical sources
- Outputs MUST be traceable to source context
- No artifacts may be written if validation fails

## Evaluation Rules

- All options MUST be explicitly compared using consistent criteria
- Trade-offs MUST be clearly defined and justified
- Selected direction MUST be supported by evidence or labeled assumptions
- Context gaps MUST be surfaced where they impact decision quality

## Validation Hooks

- Decision framework is complete and consistent
- All options are evaluated using the same criteria
- Recommendations are grounded or explicitly labeled assumptions
- Trade-offs are clearly articulated
- Context gaps are surfaced when present
- No unsupported or fabricated conclusions are present

## Invocation

```text
Use Strategy Pack

Decision:
Horizon:
Constraints:
```


## Summary

The Strategy Pack ensures deterministic, grounded, and decision-ready strategic outputs aligned with CareerOS runtime constraints.

