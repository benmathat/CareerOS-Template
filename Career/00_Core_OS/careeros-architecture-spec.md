# CareerOS Architecture Specification

## Version
v1.0 (Foundational)

## Purpose

This document defines the **architectural model** of CareerOS as a system.  
It formalizes structure, boundaries, entities, and lifecycle rules to ensure consistent operation across human and AI interaction.

CareerOS is not a document repository.  
It is an **operating system for career management and job search execution**.

---

## 1. System Definition

### 1.1 Core Concept

CareerOS is a:

> **Career-centric operating system with an embedded job-search execution layer**

It enables:
- deliberate career direction
- structured execution
- reusable knowledge
- compounding learning

---

### 1.2 Design Principles

### 1. Strategy Before Volume
All execution is constrained by defined direction.

### 2. Truth Separated from Presentation
Raw experience is never overwritten by polished artifacts.

### 3. Canonical vs Tactical Separation
Reusable narratives are distinct from context-specific adaptations.

### 4. One Source of Truth
Each concept has a canonical home.

### 5. Compounding Learning
All activity produces reusable signal.

### 6. Designed for Iteration
Supports multiple career cycles without loss of context.

---

## 2. Architectural Layers

CareerOS is composed of the following layers:

### Layer 1: Control
System instructions, operating state, workflows

**Location:**
`00_Core_OS/`

---

### Layer 2: Truth Base
Durable representation of the individual

**Includes:**
- Work experience
- Skills
- Personal profile

**Locations:**
- `02_Work_Experience/`
- `03_Skills_and_Portfolio/`
- `05_Personal_Profile/`

---

### Layer 3: Direction
Defines intent and constraints

**Includes:**
- Career goals
- Role targets
- Strategy

**Location:**
`04_Career_Goals_and_Strategy/`

---

### Layer 4: Market Interface
External inputs and signals

**Includes:**
- Opportunities
- Networking
- Market research

**Locations:**
- `06_Job_Opportunities/`
- `08_Networking_and_References/`
- `09_Research_and_Market_Intelligence/`

---

### Layer 5: Execution
Active job search output

**Includes:**
- Resumes
- Applications
- Interview prep

**Locations:**
- `01_Resume_and_Profiles/`
- `07_Applications_and_Interviews/`

---

### Layer 6: Learning
Feedback and improvement

**Location:**
`10_Coaching_Feedback_and_Notes/`

---

### Layer 7: Compliance
Regulatory and tracking requirements

**Location:**
`11_Job_Search_Activities/`

---

### Layer 8: Retention
Inactive or historical material

**Location:**
`99_Archive/`

---

## 3. Control Plane

### 3.1 Definition

The Control Plane governs:
- how the system is used
- what is active
- what matters now

---

### 3.2 Components

### System Documentation
- README
- structure maps
- workflows

### Operating State (Critical)
Defines:
- current search phase
- active priorities
- target roles
- constraints

### Prompts / Control Surfaces
- assistant instructions
- compressed context maps

### Indexes / Registries
- canonical lists of active entities

---

### 3.3 Requirement

CareerOS must maintain a **clear distinction between:**
- documentation
- system state
- artifacts

---

## 4. Canonical Entities

CareerOS operates on defined entities.

---

### 4.1 Role Target
A defined type of role being pursued.

**Upstream:**
- Career strategy

**Downstream:**
- Opportunities
- Resume variants

---

### 4.2 Opportunity
A specific job opening or lead.

**Upstream:**
- Role target
- Market input

**Downstream:**
- Application
- Interview process

---

### 4.3 Company of Interest
A tracked organization independent of a specific role.

---

### 4.4 Application
A submitted candidacy for an opportunity.

**Lifecycle:**
- Draft → Submitted → Interview → Closed

---

### 4.5 Contact
A person in the network (recruiter, hiring manager, peer)

---

### 4.6 Reference
A validated contact used for endorsement

---

### 4.7 Canonical Story
Full-fidelity narrative of real experience

**Location:**
`02_Work_Experience/Stories/`

---

### 4.8 Tactical Story
Adapted narrative for a specific use

**Location:**
`07_Applications_and_Interviews/.../Stories/`

---

### 4.9 Work Search Activity
A logged action for compliance

**Location:**
`11_Job_Search_Activities/`

---

### 4.10 Research Artifact
Structured knowledge about:
- companies
- roles
- market conditions

---

## 5. Artifact Classification

All artifacts must be classified as:

---

### 5.1 Durable
Persists across all searches

Examples:
- Work history
- Skills
- Canonical stories
- Personal values

---

### 5.2 Tactical
Used within a search cycle

Examples:
- Tailored resumes
- Applications
- Interview prep

---

### 5.3 Transient
Short-lived processing artifacts

Examples:
- Raw notes
- Intake drafts
- Scratch documents

---

## 6. Relationships

Artifacts must explicitly or implicitly reference related entities.

---

### Required Relationships

| Entity | Must Relate To |
|--------|---------------|
| Application | Opportunity |
| Opportunity | Role Target |
| Resume Variant | Role Target |
| Tactical Story | Canonical Story |
| Work Activity | Application or Opportunity |
| Contact | Opportunity or Company |

---

## 7. Lifecycle Model

### 7.1 Opportunity Lifecycle

```text
Prospect → Qualified → Applied → Interviewing → Closed
```

---

### 7.2 Application Lifecycle

```text
Draft → Submitted → Active → Closed
```

---

### 7.3 Artifact States

- Active
- Dormant
- Superseded
- Archived

---

### 7.4 Transition Rules

Artifacts must move to `99_Archive/` when:
- no longer relevant to current strategy
- replaced by newer versions
- tied to closed opportunities

---

## 8. Boundary Rules

### 8.1 Truth vs Presentation

- Truth lives in:
  - `02_Work_Experience/`
  - `03_Skills_and_Portfolio/`
- Presentation lives in:
  - `01_Resume_and_Profiles/`

---

### 8.2 Strategy vs Execution

- Strategy:
  - `04_Career_Goals_and_Strategy/`
- Execution:
  - `07_Applications_and_Interviews/`

---

### 8.3 Execution vs Compliance

- Execution:
  - Applications, interviews
- Compliance:
  - Activity logs only

---

### 8.4 Networking vs Opportunities

- Networking = relationships
- Opportunities = roles

They may reference each other but must not collapse.

---

## 9. System Behavior Expectations

CareerOS must:

- maintain a single source of truth
- prevent duplication of core artifacts
- support reuse across contexts
- preserve historical state
- enable decision-making, not just storage

---

## 10. Operating Model

### 10.1 Flow

```text
Truth → Strategy → Opportunity → Application → Interview → Feedback → Refinement
```

---

### 10.2 Feedback Loop

All outcomes must feed back into:
- Strategy
- Stories
- Resume improvements

---

### 10.3 System Priority

The system prioritizes:

1. Clarity of direction
2. Quality of execution
3. Learning over time

---

## 11. Architectural Summary

CareerOS is:

- a **knowledge system**
- a **decision system**
- an **execution system**
- a **learning system**
- a **compliance system**

It succeeds when:
- decisions improve over time
- effort decreases per application
- outcomes improve through reuse

---

## End of Document