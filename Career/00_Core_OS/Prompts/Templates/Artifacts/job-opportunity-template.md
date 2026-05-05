---
id: <YYYYMMDD-company-role>
company: <string | MISSING>
role: <string | MISSING>
status: intake            # intake | analyzing | hold | pursue | applying | submitted | interviewing | pass | closed
source: <pdf | url | text | MISSING>
date_added: <YYYY-MM-DD>
location: <string | MISSING>
work_type: <onsite | hybrid | remote | MISSING>
compensation: <string | MISSING>
posting_url: <url | MISSING>
posting_file: <path | MISSING>
---

# Opportunity: <Company> — <Role>

## Template Rules

- This template defines structure only (no execution logic)
- All fields MUST be populated or set to `MISSING`
- No inferred or fabricated data is allowed
- All content MUST be traceable to source or labeled assumptions
- Include `Assumptions` and `Context Gaps` sections when applicable

---

## 1. Raw Source

### Job Description (Extracted)
- <verbatim or minimally structured extraction>

### Key Responsibilities (Extracted)
- <list or MISSING>

### Requirements (Extracted)
- <list or MISSING>

### Preferred Qualifications (Extracted)
- <list or MISSING>

### Benefits / Compensation Notes
- <notes or MISSING>

---

## 2. Structured Extraction (AI-Normalized)

### Role Type
- <string | MISSING>

### Seniority Level
- <string | MISSING>

### Functional Scope
- IT Operations
- Strategy
- Infrastructure
- Security / Compliance
- Product / Engineering
- Other: <string | MISSING>

### Domain / Industry
- <string | MISSING>

### Key Systems / Tools
- <list | MISSING>

### Leadership Scope
- Team size: <string | MISSING>
- Reports to: <string | MISSING>
- Budget ownership: <string | MISSING>
- Vendor ownership: <string | MISSING>

---

## 3. Signal Analysis (Pre-Analysis Layer)

### Core Signals
- <list | MISSING>

### Hidden Signals (Implied Expectations)
- <list | MISSING>

### Success Definition (What “good” looks like in this role)
- <list | MISSING>

---

## 4. Fit Snapshot (Quick Read)

### Alignment
- Strong: <items | MISSING>
- Moderate: <items | MISSING>
- Weak: <items | MISSING>

### Gaps
- <list | MISSING>

### Risk Flags
- <list | MISSING>

---

## 5. Opportunity Analysis (Output of Analysis Pack)

### Recommendation
- pursue | consider | pass

### Rationale
- 

### Key Drivers
- 

### Blocking Issues
- 

### Positioning Strategy
- 

### Assumptions
- <list | NONE>

### Context Gaps
- <list | NONE>

---

## 6. Decision Gate

### Decision
- pursue | hold | pass

### Decision Date
- 

### Decision Notes
- 

### Assumptions
- <list | NONE>

### Context Gaps
- <list | NONE>

---

## 7. Execution Artifacts (Populated Later)

### Resume
- path: <path | MISSING>

### Cover Letter
- path: <path | MISSING>

### Application Notes
- path: <path | MISSING>

### Next Steps
- path: <path | MISSING>

---

## 8. Application Tracking

### Status
- <applying | submitted | interviewing | closed | MISSING>

### Submission Date
- <YYYY-MM-DD | MISSING>

### Contact / Recruiter
- <string | MISSING>

### Follow-Up Date
- <YYYY-MM-DD | MISSING>

### Notes
- <text | MISSING>

---

## 9. Interview Tracking (If Applicable)

### Interview Stages
- <list | MISSING>

### Key Themes
- <list | MISSING>

### Story Mapping
- <list | MISSING>

### Feedback / Outcomes
- <list | MISSING>

---

## 10. Metadata

### Priority Rank
- <number | MISSING>

### Last Reviewed
- <YYYY-MM-DD | MISSING>

### Next Action
- <string | MISSING>

### Tags
- <list | MISSING>

---

## Validation Checklist

- [ ] All required fields are populated or `MISSING`
- [ ] No inferred or fabricated data is present
- [ ] All content is traceable to source or labeled assumptions
- [ ] Assumptions and Context Gaps are included where applicable
- [ ] Structure matches template exactly