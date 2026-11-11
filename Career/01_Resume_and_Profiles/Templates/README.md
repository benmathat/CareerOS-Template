---
Last Update: 2026-11-05
Previous Update: 2026-10-29
---

# Resume & Cover Letter DOCX Templates

This folder holds the two formatting references used for shareable
application materials — [resume-template.docx](resume-template.docx) and
[cover-letter-template.docx](cover-letter-template.docx) — and is the
target of the two deterministic generators in `scripts/`. Both documents
contain placeholders only; this folder controls presentation, not career
facts.

## Track Positioning and Shared Layout

These formatting templates serve all employment tracks. Resolve the track and role target before authoring targeted content; `/build-resume` and `/build-application` enforce the Resume Pack's Track Resolution and Positioning Rules. Formatting an approved existing resume is a separate conversion step and does not require reclassifying or rewriting it.

Track 2 leads with software product / engineering leadership, Track 3 with MSP technical account management, and Track 4 with Strategic Portfolio & Transformation Governance. Use the governing role target for wording and emphasis, and canonical evidence for facts. A missing matching track baseline is non-blocking; a missing or unresolved opportunity track blocks targeted content generation.

Keep track provenance in internal application notes/records and runtime context. Do not add internal track labels or role-target paths to the submitted resume or cover letter. See `../README.md` for baseline conventions and track mappings.

## Resume Template

### Purpose

Use `resume-template.docx` as the formatting reference for shareable
resumes and as an editable starting point in LibreOffice Writer.

### Fillable fields

Replace all bracketed text: name, headline, contact details, summary, core skills, job titles, employers, locations, dates, achievement bullets, education, and relevant credentials. Repeat or remove entire experience blocks as needed. Remove optional fields and their separators when unused.

### Usage instructions

1. Open the template in LibreOffice Writer and immediately save a copy with a role-specific filename ending in `.docx`.
2. Replace placeholders with verified content. When pasting, use unformatted text to retain the destination paragraph style.
3. Use the paragraph styles below to adjust formatting consistently. Duplicate an existing bullet or experience block when adding content.
4. Save in DOCX format. If LibreOffice asks which format to use, keep the Word/DOCX format.
5. Reopen the saved file and review every page before sharing. Search for `[` and `]` to catch remaining placeholders. Check wrapping, page breaks, contact details, dates, and links.

### Formatting reference

The template uses US Letter paper, 0.70-inch margins on all four sides, black text, and Arial. It uses a single column, native list bullets, and ordinary editable paragraphs. Contact details are in the document body.

| Paragraph style | Use | Size |
| --- | --- | --- |
| Title | Name | 24 pt bold |
| Resume Headline | Professional headline | 11.5 pt |
| Resume Contact | Contact details and visible URLs | 9.5 pt |
| Heading 1 | Section headings | 10.5 pt bold |
| Resume Role | Job title | 11 pt bold |
| Resume Employer | Employer, location, and dates | 10 pt |
| Resume Body | Summary / Executive Profile and skills | 10.5 pt |
| Resume Bullet | Achievement bullets with hanging indent | 10.5 pt |
| Resume Education | Education and credentials | 10.5 pt |

Headings and job headers stay with the following paragraph. Individual bullets stay together, but experience sections can flow across pages. The default page budget is three pages unless a different limit is explicitly requested; shorten or prioritize content before reducing type size.

### Generating future resumes (deterministic, no LLM fill step)

`scripts/generate-resume-docx.sh` reads a markdown resume and fills this
template in code — parsing and layout are deterministic, not a prompt
asking an assistant to type into the template. Run it from the repo root:

```bash
scripts/generate-resume-docx.sh Career/06_Job_Opportunities/<company>_<role>_<date>/resume.md
```

For opportunity-folder `resume.md`, the default shareable outputs are
`resume_<INITIALS>-<company-role>-<YYYY-MM>.docx` / `.pdf` in the same
folder (not `resume.docx`); see [Shareable file names](#shareable-file-names).
Non-opportunity baselines under `01_Resume_and_Profiles/` still default to
the input stem with a `.docx` extension.

By default it caps output at three pages, produces both `.docx` and `.pdf`,
and refuses to write anything if the content
needs more pages than the limit — it prints how many pages the content
actually needs instead of silently truncating or shrinking type. Within
that limit, content flows freely across pages: if a section (Core
Strengths, Professional Experience, Education, ...) runs past the bottom
of a page, the tool breaks it cleanly between entries or bullets (never
mid-bullet) and opens the next page with a leading italic
"*\<Section\> (continued)*" line, so a reader always knows what they're
looking at. A section landing fresh at the top of a page — not a
continuation of one already started — gets no such line. The only
failure condition is needing more pages than the limit allows (or a
single bullet/entry too long to ever fit one page, which no page-count
option can fix). Useful options:

- `--pages N` — page limit (default 3). Not capped at 3 — set it as high
  as the content genuinely needs.
- `--fit` — allow small, bounded reductions to bullet/body paragraph
  spacing (never wording or content) to try to fit within the limit.
- `--allow-overflow` — write the artifact anyway even if it needs more
  pages than the limit, still with clean breaks and continuation lines
  throughout.
- `--no-pdf` — skip the LibreOffice PDF conversion/page-count check (DOCX
  generation itself never depends on LibreOffice).
- `--ats-keywords <path>` — an `analysis.md` (or its opportunity folder)
  whose `## ATS Keywords` section (produced by `/analyze-opportunity`)
  should lead the DOCX's Keywords property. Without this flag, the tool
  prefers the `analysis.md` beside an opportunity-folder `resume.md`; for a
  legacy long `<company>_<role>_resume_<date>` input it auto-detects a
  single unambiguous match under `Career/06_Job_Opportunities/`; if none is
  found, Keywords falls back to resume-derived terms only.

The tool measures actual glyph widths for the template's font (via
metric-compatible Liberation Sans) to plan exactly where every page break
falls — it doesn't rely on the word processor's own pagination — then
renders the real DOCX and, when LibreOffice is available, converts it to
PDF and counts the actual pages as a ground-truth check rather than
trusting the estimate alone.

It also sets the DOCX's Title, Subject, and Keywords file properties
from the resume's own content (name/headline, most recent job title,
job titles and employers, skill-category subheadings) rather than
leaving the template's placeholder values in place — useful when the
file is searched, indexed, or opened outside the app that generated it.
When a matching opportunity analysis has ATS keywords on file (see
`--ats-keywords` above), those lead the Keywords property, since that's
what a target-role screen actually searches for.

See [`scripts/resume_docx/SCHEMA.md`](../../../scripts/resume_docx/SCHEMA.md)
for the exact markdown structure it expects (matching what `/build-resume`
and the existing tailored resumes already produce).

For a newly tailored resume, follow `/build-resume` and its required
opportunity analysis and canonical evidence first — this template and
generator supply layout only, they do not replace that workflow. For an
approved existing resume, treat DOCX generation as a format conversion
and surface factual conflicts rather than silently revising them. Keep
provenance notes, review comments, and runtime records outside the shared
resume.

### Manual alternative

For a one-off touch-up, you can still open `resume-template.docx` directly
in LibreOffice Writer and edit it by hand — see "Usage instructions" above.
This is fine for small edits, but for a full resume prefer the script:
it is repeatable, doesn't depend on careful manual find-and-replace, and
checks the actual page count before you share the file.

## Cover Letter Template

### Purpose

Use `cover-letter-template.docx` as the formatting reference for
shareable cover letters, styled to match the resume template (same
Arial/US Letter/0.70-inch-margin conventions) so a resume and cover
letter submitted together read as one coordinated set.

### Fillable fields

Replace all bracketed text: name, contact details, date, recipient
block (addressee / company / role), opening/body/closing paragraphs,
and the closing signature name.

### Usage instructions

Same as the resume template: open in LibreOffice Writer, save a copy
immediately with a role-specific filename, replace placeholders with
unformatted-paste text to retain paragraph styles, and review every
page (search for `[` and `]`) before sharing.

### Formatting reference

US Letter paper, 0.70-inch margins on all four sides, black text, Arial.

| Paragraph style | Use | Size |
| --- | --- | --- |
| Letter Name | Sender name | 18 pt bold |
| Letter Contact | Sender contact details | 9.5 pt |
| Letter Date | Date line | 10.5 pt |
| Letter Recipient | Addressee / company / role block | 10.5 pt |
| Letter Body | Opening/body/closing paragraphs | 10.5 pt |
| Letter Signature | Closing signature name | 10.5 pt |

Name, contact, date, and recipient block are kept together as one unit
and never split across pages. Body paragraphs can flow across pages if
the letter runs long; the closing signature is never separated from the
paragraph before it.

### Generating cover letters (deterministic, no LLM fill step)

`scripts/generate-cover-letter-docx.sh` reads a markdown cover letter —
the same structure `/build-application` already produces — and fills
this template in code, using the same font-metrics-driven pagination
engine as the resume generator (they share `scripts/resume_docx/docx_common.py`):

```bash
scripts/generate-cover-letter-docx.sh Career/06_Job_Opportunities/<company>_<role>_<date>/cover-letter.md
```

For opportunity-folder `cover-letter.md`, the default shareable outputs
are `cover-letter_<INITIALS>-<company-role>-<YYYY-MM>.docx` / `.pdf` in the
same folder (see [Shareable file names](#shareable-file-names)). ATS
keywords auto-detect prefers sibling `analysis.md`.

Cover letters are conventionally one page, so the default page limit is
1. All the resume generator's options apply the same way: `--pages N`,
`--fit`, `--allow-overflow`, `--no-pdf`, `--ats-keywords <path>`. If the
letter genuinely needs more than one page, it flows freely between
paragraphs (never mid-paragraph) and the continuing page opens with a
leading italic "*Letter (continued)*" line.

The DOCX's Title/Subject/Keywords properties are set from the letter's
own content: Subject reuses the letter's own `## Subject` line verbatim;
Keywords leads with ATS terms (when found) followed by the company/role
from the recipient block.

See [`scripts/resume_docx/COVER_LETTER_SCHEMA.md`](../../../scripts/resume_docx/COVER_LETTER_SCHEMA.md)
for the exact markdown structure it expects.

For a newly tailored cover letter, follow `/build-application` first —
this template and generator supply layout only.

### Manual alternative

Same tradeoff as the resume template: fine for a one-off touch-up in
LibreOffice Writer, but prefer the script for anything you're actually
submitting.

## Assumptions

One-page US Letter layouts and Arial are design defaults because no page size, font, or visual reference was supplied for either template. These are low-risk formatting choices and may be changed. Neither one-page placeholder layout guarantees that any amount of replacement text will fit. Font substitutions on another computer may change wrapping.

## Validation

`resume-template.docx` was rendered with LibreOffice and visually inspected; a separate copy was saved back to DOCX through LibreOffice and rendered again to check layout and text retention. `cover-letter-template.docx` was built programmatically with the same font/margin/style conventions and verified structurally (styles, margins, paragraph content) via python-docx; it has not had the same LibreOffice visual-render pass, since LibreOffice was not available for interactive verification when it was created — repeat the page review after replacing content, and treat a first real render as the actual visual check for this template specifically.

## Shareable file names

Shareable DOCX/PDF copies of an opportunity's resume and cover letter use
one terse, predictable name so a file is recognizable when it leaves the
workspace (an attachment, a recruiter's inbox):

```text
resume_<INITIALS>-<company-role>-<YYYY-MM>.docx
cover-letter_<INITIALS>-<company-role>-<YYYY-MM>.docx
```

for example `resume_JQP-acme-sr-mgr-product-2026-10.docx`.

- `<INITIALS>` are the initials of whoever CareerOS is configured for: the
  first letter of each word of the `# Full Name` heading at the top of the
  markdown file being rendered (suffixes such as Jr or PhD ignored), in
  capitals. For `# Jane Q. Public` that is `JQP`. Nothing else is configured.
- `<company-role>` is the opportunity folder's `<company>_<role>` part,
  made as terse as possible without changing which company or role it is.
  The role stays consistent with the folder name; only its wording shrinks.
  Words are lowercase and joined with hyphens. Filler words (of, and, the,
  for, in, a, an, at, to) and company suffixes (Inc, LLC, Ltd, Corp, Co)
  are dropped, and standard abbreviations replace long titles:

  | Title element | Abbreviation | Title element | Abbreviation |
  |---|---|---|---|
  | Senior | sr | Manager / Management | mgr / mgmt |
  | Junior | jr | Director | dir |
  | Vice President | vp | Senior Vice President | svp |
  | Executive Vice President | evp | Chief (Executive / Financial / Information / Operating / Product / Technology) Officer | ceo / cfo / cio / coo / cpo / cto |
  | Engineer / Engineering | eng | Developer / Development | dev |
  | Software | sw | Technical / Technology | tech |
  | Information Technology | it | Operations | ops |
  | Administrator / Administration | admin | Assistant / Associate | asst / assoc |

  Add an abbreviation only when it is standard; extend the tables in
  `scripts/resume_docx/docx_common.py` (`SLUG_PHRASE_ABBREVIATIONS`,
  `SLUG_WORD_ABBREVIATIONS`) and this list together, and add a case to
  `scripts/test_shareable_names.py`.
- `<YYYY-MM>` is the year and month of the opportunity folder's date.
- The opportunity folder itself keeps the normalized
  `<company>_<role>_<YYYY-MM-DD>` name and the generic `resume.md` /
  `cover-letter.md` sources; this convention applies only to the shareable
  copies the generator writes. Files generated before this convention keep
  their old names unless regenerated.
