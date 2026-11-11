# Canonical markdown schema for `resume_docx.py`

This is the markdown structure `scripts/resume_docx/resume_docx.py` parses
deterministically (no LLM step) into the DOCX template's named styles. It
matches the structure already used by `Resume_Master/resume-master.md` and
the tailored resumes under `01_Resume_and_Profiles/` — this is a
description of the existing convention, not a new format to migrate to.

```markdown
# Full Name
City, State · Phone · Email · [linkedin.com/in/handle](https://www.linkedin.com/in/handle)

## Headline
Optional one-line role identity, rendered between the name and the contact line (targeted resumes use e.g. `HEAD OF PRODUCT | PRODUCT STRATEGY & DEVELOPMENT`). Omit the whole section if you don't have one.

## Summary
One or more paragraphs. Blank line separates paragraphs.

## Executive Profile
Short paragraph on professional scope and distinguishing background
(`## Summary` is accepted as an alias; the heading text is preserved).

## Core Capabilities
Optional, about six capabilities as bullets (rendered as a single list; a
two-column layout is not implemented).
- Product strategy

## Core Strengths
(legacy; still supported)
- A flat bullet, OR:

### A subheading
- A bullet grouped under it
- Another bullet

## Professional Experience

### Employer Name - Job Title
**Month YYYY – Month YYYY | Location**
Optional 1–2 sentence role description (plain text between the dates line and the bullets).
- Achievement bullet. **Bold** and *italic* inline markup is preserved.
- Another bullet.

### Earlier Employer - Earlier Title
::: resume-date
**Month YYYY – Month YYYY | Location**
:::
- Achievement bullet.

## Education
### Institution Name
**Degree**
*Year or year range*

## Professional Development
- **Certification Name** - Issuing Organization
```

## Rules the parser enforces

- The first content line (after any `---`-delimited frontmatter) must be
  `# Full Name`.
- A contact line must follow directly under the name, OR be given as its
  own `## Contact Information` (or `## Contact`) section. At least one
  non-blank line is required either way.
- `## Professional Experience` (or `Experience` / `Work Experience`) is
  required, with at least one `### Employer - Title` entry. The heading
  text needs a hyphen, en dash, or em dash surrounded by spaces to split
  employer from title.
- Each experience entry needs a dates/location line immediately after the
  `### ` heading, either as `**Dates | Location**` or wrapped in a
  `::: resume-date` fenced div (both forms already exist in this repo).
  Dates come first, location second, separated by `|`.
- Each experience entry needs at least one bullet (`- ` or `* `).
- `## Education` entries can be `### Institution` blocks (bold degree
  line, optional italic year line) or a single line like
  `**Institution** — Degree (Year)`.
- `## Professional Development` / `## Certifications` / `## Credentials`
  bullets are parsed as `**Name** - Organization` (or a plain bullet if
  no separator is found) and are merged with Education under one
  "Education and Credentials" heading in the output, matching the
  template's design.
- Any other `## ` heading (e.g. `## Volunteer Work`, `## Retail and
  Warehouse Experience`) is preserved verbatim under its own heading in the
  output — nothing is silently dropped, per this repo's canonical-truth
  rules. It keeps its markdown position relative to the main blocks: before
  `## Professional Experience`, between experience and education, or after
  education and credentials. (Headings listed as skills headings, such as
  `## Tools & Methods`, `## Core Skills` and `## Core Capabilities`, still
  render before experience.)
- On a parse error, the tool prints exactly which line/entry failed and
  writes nothing.

## Manual page break

A line holding exactly `<!-- page-break -->` just before a `### Employer - Title`
entry starts a new page at that entry (skipped when the entry would already
begin a page). Use it sparingly, for example to start a long employer block on a
fresh page; the section continues with the usual "(continued)" line. The comment
is inert in any markdown viewer. Remember that a forced break can push the total
over the page limit.

## Inline formatting

`**bold**` and `*italic*` become real DOCX run formatting. `[text](url)`
becomes plain visible text (the label) everywhere except the contact
line, where it becomes the visible URL (matching the template's "visible
URLs" convention) with the `https://` prefix stripped.

## What this is not

This schema is for a **share-ready** resume — the output of `/build-resume`
or an equivalent tailored resume in `01_Resume_and_Profiles/`. It is not
meant to be run directly against `Resume_Master/resume-master.md`: that
file is the full, untrimmed canonical record (see its own README) and
will almost always overflow any page budget. Generate or select a
tailored, page-budgeted resume first, then run this tool on that file.

## Multiple positions at one employer

Write each position as its own `### Employer - Title` entry with its own
dates line, newest first. Consecutive entries with the same employer and
location are grouped by the renderer: the employer name and overall date
span appear once, followed by each position as `Title | Dates`. No markdown
change is needed.

Every employer follows one model:

```
Employer Name
Location | Overall tenure          (only when the employer has multiple positions)
Position Title | Position dates
Brief role description.
- Selected accomplishment
Earlier Position | Position dates
Role description or selected accomplishment.
```

A single-position employer omits the location/tenure line, so its location is
not shown in the rendered resume (it stays in the markdown dates line).

Visual hierarchy in experience: the employer name renders in capitals in the bold
Resume Role style, the location/tenure line in regular type, and each position line
(`Title | Dates`) in italics, so employer, tenure and position read as three levels.
