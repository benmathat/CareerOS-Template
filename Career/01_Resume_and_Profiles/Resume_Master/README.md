---
Last Update: 2026-10-07
Previous Update: 2026-09-25
---

# Master Resume – Comprehensive Presentation Baseline

## Purpose
This folder contains a **comprehensive, reusable resume content baseline** derived from canonical experience records. Keep useful, verified content even when it is too long or outside a particular track's positioning.

Canonical facts live in `../../02_Work_Experience/` and other canonical sections (`02_`–`05_`); this presentation baseline consumes those sources and does not override them.

This is an **optional presentation input** for:
- Tailored resumes
- Cover letters
- LinkedIn optimization
- Interview preparation

---

## What Belongs Here
- Full work history
- All roles and titles
- Expanded bullet points
- Metrics and outcomes
- Projects that didn’t make the final resume
- Experiments, failures, and recoveries

## What Does NOT Belong Here
- Job-specific tailoring
- Keyword stuffing
- Design/layout experimentation

---

## Recommended Structure

```text
Resume_Master/
├── resume-master.md
├── role-bullets-expanded.md
├── metrics-and-impact.md
└── career-timeline.md
```

## Editing Rules
- Optimize for accuracy and completeness; update canonical evidence first when a fact changes
- Use clear, factual language
- Prefer numbers and outcomes over responsibilities
- No concern for length

## Note on `resume-pdf.tex` / `resume-date-div.lua`

These two files are a legacy Pandoc + XeLaTeX formatting pipeline and, per
"What Does NOT Belong Here" above, are layout experimentation that doesn't
belong among these reusable content baselines — they're artifacts of an earlier
approach, not something to build on. They are not referenced by any
command or workflow doc in this repo.

The current, primary path to a shareable, formatted resume (DOCX/PDF) is
`scripts/generate-resume-docx.sh <path-to-opportunity>/resume.md`, which fills
`Career/01_Resume_and_Profiles/Templates/resume-template.docx`
deterministically and checks the result actually fits the page budget. See
that template folder's README. Use the opportunity-folder `resume.md` as
the input, not this master file directly (see its own SCHEMA note on why).

## Track Use

The master is a track-neutral pool of verified achievements. Its existing summary is a presentation variant, not a universal positioning instruction.

For a targeted resume, resolve the opportunity's track and load its role target before choosing or rewriting the headline, summary, skills, and bullets. Track 2 emphasizes software product / engineering leadership; Track 3 emphasizes MSP technical account management; Track 4 emphasizes Strategic Portfolio & Transformation Governance. Preserve the scope of every achievement when reusing it across tracks.

See `../README.md` for track-baseline registration and `../../04_Career_Goals_and_Strategy/career-tracks.md` for the authoritative track mapping. Keep track provenance in internal notes/records rather than submitted resume content.
