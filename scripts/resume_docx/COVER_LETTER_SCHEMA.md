# Canonical markdown schema for `cover_letter_docx.py`

This is the markdown structure `scripts/resume_docx/cover_letter_docx.py`
parses deterministically (no LLM step) into the cover letter DOCX
template's named styles. It matches the structure `/build-application`
already produces — this describes the existing convention, not a new
format to migrate to.

```markdown
# Full Name
City, State · Phone · Email · [linkedin.com/in/handle](https://www.linkedin.com/in/handle)

2026-09-24

Hiring Team
Company Name
Role Title — Job ID 12345

## Subject
Application — Role Title

## Letter

Opening paragraph: the role, why you're writing, and a brief statement of fit.

Body paragraph: your most relevant experience and a quantified achievement.
**Bold** and *italic* inline markup is preserved.

Closing paragraph: reiterate interest, a call to action, and thanks.

Full Name
```

## Rules the parser enforces

- The first content line (after any `---`-delimited frontmatter) must be
  `# Full Name`.
- A contact line must follow directly under the name (same convention as
  the resume generator).
- A single date line must follow, separated from the contact line by a
  blank line.
- A recipient block (addressee / company / role — typically 2-3 lines,
  e.g. `Hiring Team` / `Company Name` / `Role Title`) must follow the
  date, separated by a blank line. Rendered as-is; not otherwise
  validated for content.
- `## Subject` is required: a single line used for the DOCX's Subject
  file property (not rendered as visible text in the letter body — this
  repo's established cover letters don't print a subject/Re: line).
- `## Letter` is required, with at least one body paragraph
  (blank-line-separated, same as the resume generator's paragraph
  handling).
- If the `## Letter` section's last paragraph is just the sender's name
  (matched against the `# Full Name` heading, case/punctuation-insensitive),
  it's treated as the closing signature and rendered in a distinct style,
  kept on the same page as the paragraph before it. If not found, the
  name from the heading is used as the signature and every paragraph in
  `## Letter` is treated as body content.
- Any other heading (`## Assumptions`, `## Context Gaps`, `## Warnings`,
  etc.) is provenance metadata, not letter content — read but never
  rendered into the DOCX/PDF.
- On a parse error, the tool prints exactly which line/section failed
  and writes nothing.

## Inline formatting

Same as the resume generator: `**bold**` and `*italic*` become real DOCX
run formatting; `[text](url)` becomes plain visible text everywhere
except the contact and recipient lines, where it becomes the visible URL
(`https://` prefix stripped).

## Pagination

Cover letters are conventionally one page. If content genuinely needs
more (`--pages 2` or higher, or `--allow-overflow`), the letter flows
freely between paragraphs — never mid-paragraph — and a page that
continues the letter opens with a leading italic "Letter (continued)"
line, same mechanism as the resume generator's per-section markers. The
closing signature is never separated from the paragraph before it.
