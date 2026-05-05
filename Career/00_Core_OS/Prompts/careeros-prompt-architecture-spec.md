---
Last Update: 2026-05-05
Previous Update: 2026-04-24
---

# CareerOS Execution Architecture Specification

## 1. Purpose

Define a structured prompt architecture that enables CareerOS to operate as a **deterministic, composable, and evolvable AI system** rather than a single monolithic prompt.

This spec establishes:
- Prompt layers and responsibilities
- Interaction contracts between layers
- Standardized prompt templates
- Execution model

CareerOS is not a single prompt system.

It is a deterministic execution system composed of:
- layered prompt architecture
- runtime orchestration
- structured state transitions

---

## 2. Design Principles

### 2.1 Separation of Concerns
Each prompt has a single responsibility:
- Context definition
- Behavior shaping
- `task` execution
- Output formatting

### 2.2 Composability
Prompts are modular and can be combined dynamically based on task context.

### 2.3 Determinism over Creativity
Favor predictable, structured outputs over open-ended responses.

### 2.4 Explicit State Handling
All prompts operate with clearly defined inputs and outputs.

---

## 3. Prompt Stack Architecture

```
[ System Layer ]
        ↓
[ Mode Layer ]
        ↓
[ Task Layer ]
        ↓
[ Context Layer ]
        ↓
[ Output Layer ]
```

---

## Runtime Object Model

CareerOS operates on a sequence of structured runtime objects:

- `request`
- `task`
- `mode_selection`
- `routing_output`
- `context_block`
- `prompt_object`
- `output`
- `validation_result`
- `artifact_destination`
- `execution_trace`

Each object MUST:
- have a defined schema
- include `status` and `blocking` when applicable
- be validated before passing to the next stage

---

## Execution State Semantics

All runtime components that expose runtime gating state MUST support:

- `status: valid | partial | invalid` for general runtime objects
- `status: complete | partial_non_blocking | partial_blocking` for `context_block`
- `blocking: true | false`

Rules:

- `invalid` → MUST halt execution
- `blocking = true` → MUST halt execution
- `partial` → MAY proceed if explicitly allowed
- `complete` → MAY proceed
- `partial_non_blocking` → MAY proceed only with explicit disclosures
- `partial_blocking` → MUST halt execution

---
## Determinism Enforcement

When multiple valid paths exist:

- Prefer narrower scope
- Prefer canonical sources
- Prefer fewer inputs
- Prefer explicit over inferred

Tie-breaking rules MUST be consistent across:
- mode selection
- routing
- context loading

---

## 4. Layer Definitions

## 4.1 System Layer (Global Contract)

### Purpose
Defines invariant behavior across all interactions.

### Responsibilities
- Tone and interaction model
- Thinking style (systems, first-principles)
- Output defaults (Markdown, structured)
- Role definition (strategy partner / architect)

### Characteristics
- Static
- Rarely changed
- Applies universally

---

## 4.2 Context Layer (State Injection)

### Purpose
Provides relevant state for the current session.

### Inputs
- CareerOS repository structure
- User goals (long-term / short-term)
- Active artifacts (resume, job targets, notes)

### Responsibilities
- Establish “what is true”
- Prevent hallucination by grounding context
- Scope the problem space

### Example Components
- `/context/system.md`
- `/context/goals.md`
- `/context/constraints.md`

---

## 4.3 Mode Layer (Operational Behavior)

### Purpose
Defines *how the system behaves* for a given interaction type.

### Core Modes

#### 1. Build Mode
- Create artifacts (docs, frameworks, templates)
- High structure, high completeness

#### 2. Analyze Mode
- Evaluate artifacts
- Identify gaps, risks, inconsistencies

#### 3. Refine Mode
- Improve existing artifacts
- Optimize clarity, signal, and structure

#### 4. Execute Mode
- Perform tactical actions (write email, resume edits)
- Bias toward speed and applicability

#### 5. Architect Mode
- Design systems (CareerOS itself, workflows, frameworks)
- Focus on abstraction and structure

#### 6. Transform Mode
- Convert existing artifacts into new structures/formats
- Preserve underlying meaning while adapting presentation

### Mode Exclusivity Rules

Only ONE primary mode may be active per execution.

Secondary modes may be used only if explicitly declared.

### Mode Responsibilities

#### Build
- MUST produce net-new artifacts
- MUST NOT critique unless explicitly requested

#### Analyze
- MUST NOT modify artifacts
- MUST focus on evaluation only

#### Refine
- MUST operate on an existing artifact
- MUST produce delta improvements

#### Execute
- MUST prioritize speed over completeness
- MUST minimize abstraction

#### Architect
- MUST operate at system level
- MUST avoid tactical execution

#### Transform
- MUST operate on an existing artifact
- MUST preserve meaning while adapting format/structure
- MUST NOT introduce new facts during transformation

---

## 4.4 Task Layer (Instruction Payload)

### Purpose
Defines the *specific job to be done*.

### Task Schema (STRICT)
```
task:
  objective: (single, explicit outcome)
  scope:
    in_scope:
    out_of_scope:
  inputs:
    required:
    optional:
  constraints:
    hard:
    soft:
  success_criteria:
  output_type: (must map to Output Layer)
```

This schema makes tasks:
- Comparable
- Validatable
- Composable in pipelines

### Example
```
task:
  objective: Create a resume tailored for District Executive role
  scope:
    in_scope:
      - Leadership impact bullets
      - Volunteer leadership alignment to role requirements
    out_of_scope:
      - Cover letter generation
  inputs:
    required:
      - Base resume
      - Job description
    optional:
      - Existing accomplishment inventory
  constraints:
    hard:
      - 1 page
    soft:
      - Prefer concise, high-signal bullets
  success_criteria:
    - Resume aligns to top 3 role priorities
    - Bullet language is specific and measurable where possible
  output_type: Document
```

---

## 4.5 Output Layer (Formatting Contract)

### Purpose
Standardizes outputs for usability and reuse.

### Responsibilities
- Enforce Markdown structure
- Ensure scannability
- Enable copy/paste into external systems

### Output Types
- Document
- Framework
- Template
- Checklist
- Analysis

### Output Type Contracts

Each output type MUST conform to a predefined structure:

#### Document
- Title
- Sections
- Subsections

#### Framework
- Components
- Relationships
- Rules

#### Checklist
- Items
- Completion Criteria

#### Template
- Purpose
- Fillable fields
- Usage instructions
- Example or default structure

#### Analysis
- Findings
- Gaps
- Risks
- Recommendations

These contracts MUST align directly with:
- `/00_Core_OS/Prompts/Templates/Outputs/`

---

## 4.6 Layer Contract Rules

Each layer MUST adhere to the following contract boundaries:

### System Layer
- Defines behavior only
- MUST NOT include task-specific instructions
- MUST NOT include contextual data

### Context Layer
- Defines facts and state only
- MUST NOT include instructions or directives
- MUST NOT include output formatting

### Mode Layer
- Defines behavior patterns only
- MUST NOT include task-specific inputs
- MUST NOT override System Layer rules

### Task Layer
- Defines the objective and constraints only
- MUST NOT redefine behavior or system rules
- MUST NOT include formatting instructions beyond expected output type

### Output Layer
- Defines formatting and structure only
- MUST NOT introduce new task logic or constraints

---

## 5. Prompt Composition Model

### 5.1 Composition Pattern

```
FINAL PROMPT =
    System Layer
  + Mode Layer
  + Task Layer
  + Context Layer
  + Output Layer
```

---

## 6. Standard Prompt Templates

### 6.1 Architect Template

```
Mode: Architect

task:
- objective:
- scope:
- constraints:

Output:
- Structured specification
- Clear sections
- Implementation-ready
```

---

### 6.2 Analysis Template

```
Mode: Analyze

task:
- artifact:
- evaluation_criteria:
- depth:

Output:
- Findings
- Gaps
- Recommendations
```

---

### 6.3 Build Template

```
Mode: Build

task:
- objective:
- inputs:
- constraints:

Output:
- Complete artifact
- Structured Markdown
```

---

### 6.4 Transform Template

```
Mode: Transform

task:
- objective:
- source_artifact:
- target_structure:
- transformation_constraints:

Output:
- Meaning-preserving transformed artifact
- Structured Markdown
```

---

## 7. Execution Model

### 7.1 Runtime Execution Flow

1. Normalize / Validate `task`
2. Select Mode
3. Route Sources
4. Load Context
5. Assemble Prompt
6. Execute
7. Validate Output
8. Route Artifact
9. (Optional) Iterate

---

### 7.2 Iteration Loop

```
Build → Analyze → Refine → Finalize
```

---

## 8. Failure Modes & Mitigations

### 8.1 Ambiguous Tasks
**Mitigation:** Enforce explicit Task Layer structure

### 8.2 Context Drift
**Mitigation:** Re-inject Context Layer each session

### 8.3 Over-generalized Output
**Mitigation:** Strengthen constraints and output schema

### 8.4 Prompt Entanglement
**Mitigation:** Maintain strict layer boundaries

---

## Failure Handling

Execution MUST halt when:

- task is invalid
- Mode selection is invalid or blocking
- Routing is invalid or blocking
- Context is partial_blocking
- Prompt assembly fails
- Output validation fails

All failures MUST:
- return structured runtime state
- include failure reason
- preserve upstream objects

---

## 9. Implementation Path

### Phase 1: Baseline
- Define System Layer
- Create core Mode prompts

### Phase 2: Context Structuring
- Formalize `/context` files
- Standardize inputs

### Phase 3: Template Library
- Build reusable `task` templates
- Create Output schemas

### Phase 4: Tooling Integration
- Integrate with Cursor workflows
- Enable rapid prompt composition

---

## 10. Future Extensions

- Dynamic mode selection (AI-routed)
- Context auto-loading
- Prompt versioning
- Execution logging
- Performance evaluation metrics

---

## 11. Summary

CareerOS is a layered execution architecture with strict contracts:

- `System` defines invariant behavior
- `Context` provides grounded state only
- `Mode` controls behavioral posture with exclusivity rules
- `task` uses strict schema for validation and composability
- `Output` enforces type-specific structure contracts

Runtime enforces deterministic assembly, validation gates, and pipeline orchestration.

Primary mode inventory is explicitly six-mode and first-class:
`build`, `analyze`, `refine`, `execute`, `architect`, `transform`.


---

## 12. Execution System Architecture

The original prompt architecture defines how a **single prompt** is constructed and executed.

CareerOS extends this into a full **operational system** by introducing additional layers that govern context selection, execution reuse, and multi-step workflows.

---
### 12.X Runtime Flow (Canonical)

task
  ↓
Mode Selection
  ↓
Source Routing
  ↓
Context Loading
  ↓
Prompt Assembly
  ↓
Execution
  ↓
Output Validation
  ↓
Artifact Routing
  ↓
Iteration (optional)

---

### 12.1 Source Routing Layer

**Purpose**
Defines how context is selected from CareerOS.

**Responsibilities**
- Map tasks and modes to relevant CareerOS domains
- Enforce canonical vs contextual boundaries
- Minimize context while maximizing signal

**Reference**
- `/00_Core_OS/Prompts/Runtime/source-routing.md`

---

### 12.2 Prompt Assembler

**Purpose**
Construct a deterministic, execution-ready prompt from system components.

**Responsibilities**
- Combine System, Mode, `task`, and Output layers
- Inject context based on routing rules
- Apply context compression and formatting
- Enforce consistent prompt structure

**Reference**
- `/00_Core_OS/Prompts/Runtime/prompt-assembler.md`

---

### 12.3 Execution Packs

**Purpose**
Provide reusable, pre-configured prompt compositions for common workflows.

**Examples**
- Resume Pack
- Interview Pack
- Opportunity Analysis Pack

**Characteristics**
- Pre-wired Mode + Routing + `task` + Output
- Minimal user input required
- Deterministic and repeatable

Each Pack MUST define:
- Mode
- Source Routing Rules
- `task` Template
- Output Template

---

### 12.4 Pipelines (Orchestration Layer)

**Purpose**
Define multi-step workflows and control flow across prompts.

**Examples**
- Application Pipeline
- Opportunity Review Pipeline

**Responsibilities**
- Define execution order of packs
- Implement decision gates (e.g., pursue vs pass)
- Coordinate lifecycle progression of opportunities

Each Pipeline MUST define:
- Steps
- Inputs per step
- Outputs per step
- Decision gates
- State transitions

---

### 12.5 System Flow

The full CareerOS execution model:

```
CareerOS Structure
    ↓
Source Routing
    ↓
Prompt Assembler
    ↓
Execution Unit
    ├─ Pack
    └─ Pipeline
    ↓
Outputs / Artifacts
```

---

### 12.6 Architectural Distinction

| Layer | Function |
|------|--------|
| Prompt Layers | Define how a single prompt works |
| Routing | Determines what context is used |
| Assembler | Constructs prompts deterministically |
| Packs | Execute single-step workflows |
| Pipelines | Orchestrate multi-step processes |

---

## 13. Updated Summary

CareerOS Prompt Architecture transforms prompting from:

- Ad hoc instructions → structured system
- Single prompt → layered architecture
- Reactive usage → intentional operation
- Isolated execution → orchestrated workflows

This enables:

- Consistency
- Reusability
- Scalability
- Deterministic behavior
- End-to-end workflow execution

The system now functions as a **career operating system**, not just a prompt framework.

---

## 14. Validation Layer (NEW)

### Purpose
Ensure outputs and executions conform to system rules.

### Responsibilities
- Validate layer ordering
- Validate task schema completeness
- Validate output structure
- Detect context leakage or hallucination

### Enforcement Points
- Pre-execution (task validation)
- Post-execution (output validation)
- Pipeline checkpoints

Validation MUST enforce:

- runtime object integrity
- status/blocking correctness
- deterministic transitions
- context grounding

---

## 15. Non-Goals

- Not a general-purpose conversational assistant
- Not optimized for open-ended chat behavior
- Not a creative writing system
- Not a memory store
- Not a general-purpose reasoning engine

CareerOS is a structured execution system.
