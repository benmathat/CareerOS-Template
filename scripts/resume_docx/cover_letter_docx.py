#!/usr/bin/env python3
"""
Deterministic markdown -> DOCX/PDF cover letter generator.

Reads a canonical cover letter markdown file (see COVER_LETTER_SCHEMA.md,
matching what /build-application already produces), fills the named
styles in Career/01_Resume_and_Profiles/Templates/cover-letter-template.docx,
and uses the same font-metrics-driven pagination engine as the resume
generator (scripts/resume_docx/resume_docx.py, sharing docx_common.py):
content flows freely across pages within the page limit; if the letter
spans more than one page, page 2 opens with a leading italic
"Letter (continued)" line. The only failure condition is needing more
pages than the limit allows. No LLM step fills the template.

Usage:
    scripts/generate-cover-letter-docx.sh <input.md> [--pages N] [options]

See `main()` / `--help` for the full option list.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from docx import Document

import docx_common as dc

DEFAULT_TEMPLATE = dc.REPO_ROOT / "Career/01_Resume_and_Profiles/Templates/cover-letter-template.docx"

STYLE_NAMES = {
    "name": "Letter Name",
    "contact": "Letter Contact",
    "date": "Letter Date",
    "recipient": "Letter Recipient",
    "body": "Letter Body",
    "signature": "Letter Signature",
}
TIGHTENABLE_STYLE_KEYS = frozenset({"body"})

CoverLetterParseError = dc.DocGenError

_COVER_LETTER_FILENAME_RE = re.compile(r"^(.*)_cover_letter_\d{4}-\d{2}-\d{2}$")
_NAME_NORMALIZE_RE = re.compile(r"[^a-z0-9]+")


def _normalize_name(s: str) -> str:
    return _NAME_NORMALIZE_RE.sub("", s.lower())


# --------------------------------------------------------------------------
# Data model
# --------------------------------------------------------------------------

@dataclass
class CoverLetter:
    name: str
    contact_lines: List[str]
    date: str
    recipient_lines: List[str]
    subject: str
    body_paragraphs: List[str] = field(default_factory=list)
    signature_name: str = ""
    source_path: str = ""


# --------------------------------------------------------------------------
# Markdown parsing
# --------------------------------------------------------------------------

def _gather_block(lines: List[str], idx: int) -> Tuple[List[str], int]:
    """Collect non-blank lines up to the next blank line or '## ' heading,
    then skip trailing blank lines. Returns (block, new_idx)."""
    block = []
    while idx < len(lines) and lines[idx].strip() and not lines[idx].startswith("## "):
        block.append(lines[idx].strip())
        idx += 1
    while idx < len(lines) and not lines[idx].strip():
        idx += 1
    return block, idx


def parse_cover_letter_markdown(path: Path) -> CoverLetter:
    text = Path(path).read_text(encoding="utf-8")
    lines = dc.strip_frontmatter(text.splitlines())

    idx = 0
    while idx < len(lines) and not lines[idx].strip():
        idx += 1
    if idx >= len(lines) or not lines[idx].startswith("# "):
        found = lines[idx] if idx < len(lines) else "<end of file>"
        raise CoverLetterParseError(
            f"Expected a top-level '# Full Name' heading as the first content "
            f"line (after any frontmatter); found: {found!r}"
        )
    name = lines[idx][2:].strip()
    idx += 1

    contact_lines, idx = _gather_block(lines, idx)
    date_lines, idx = _gather_block(lines, idx)
    recipient_lines, idx = _gather_block(lines, idx)
    date = " ".join(date_lines)

    sections: List[Tuple[str, List[str]]] = []
    current_heading, current_content = None, []
    while idx < len(lines):
        line = lines[idx]
        if line.startswith("## "):
            if current_heading is not None:
                sections.append((current_heading, current_content))
            current_heading, current_content = line[3:].strip(), []
        else:
            current_content.append(line)
        idx += 1
    if current_heading is not None:
        sections.append((current_heading, current_content))

    subject = ""
    body_paragraphs: List[str] = []
    signature_name = name
    letter_found = False
    for heading, content in sections:
        norm = heading.strip().lower()
        if norm == "subject":
            subject = next((l.strip() for l in content if l.strip()), "")
        elif norm == "letter":
            letter_found = True
            paragraphs = dc.split_paragraphs(content)
            if len(paragraphs) > 1 and _normalize_name(paragraphs[-1]) == _normalize_name(name):
                signature_name = paragraphs[-1]
                body_paragraphs = paragraphs[:-1]
            else:
                body_paragraphs = paragraphs
        # Any other heading (Assumptions, Context Gaps, Warnings, ...) is
        # provenance metadata, not letter content -- intentionally dropped.

    if not contact_lines:
        raise CoverLetterParseError("Expected a contact-details line directly under the name heading.")
    if not date:
        raise CoverLetterParseError("Expected a date line after the contact details, before the recipient block.")
    if not recipient_lines:
        raise CoverLetterParseError("Expected a recipient block (e.g. 'Hiring Team' / Company / Role) after the date.")
    if not letter_found:
        raise CoverLetterParseError("No '## Letter' section found.")
    if not subject:
        raise CoverLetterParseError("No '## Subject' section found (used for the DOCX Subject property).")
    if not body_paragraphs:
        raise CoverLetterParseError("The '## Letter' section has no body paragraphs.")

    return CoverLetter(name=name, contact_lines=contact_lines, date=date,
                        recipient_lines=recipient_lines, subject=subject,
                        body_paragraphs=body_paragraphs, signature_name=signature_name,
                        source_path=str(path))


# --------------------------------------------------------------------------
# Layout units
# --------------------------------------------------------------------------

def build_layout_units(letter: CoverLetter, styles: Dict[str, dc.StyleSpec], metrics: dc.FontMetrics,
                        geometry: dc.PageGeometry, tighten_factor: float = 1.0) -> List[dc.LayoutUnit]:
    width = geometry.content_width_pt
    units: List[dc.LayoutUnit] = []

    front_paras = [
        dc.ParaSpec("name", [letter.name]),
        dc.ParaSpec("contact", [dc.clean_contact_line(l) for l in letter.contact_lines]),
        dc.ParaSpec("date", [letter.date]),
        dc.ParaSpec("recipient", [dc.clean_contact_line(l) for l in letter.recipient_lines]),
    ]
    units.append(dc.make_unit(metrics, styles, width, tighten_factor, TIGHTENABLE_STYLE_KEYS, "", False, front_paras))

    n = len(letter.body_paragraphs)
    for i, para in enumerate(letter.body_paragraphs):
        group_paras = [dc.ParaSpec("body", [para])]
        if i == n - 1:
            group_paras.append(dc.ParaSpec("signature", [letter.signature_name]))
        units.append(dc.make_unit(metrics, styles, width, tighten_factor, TIGHTENABLE_STYLE_KEYS,
                                   "Letter", i == 0, group_paras))
    return units


# --------------------------------------------------------------------------
# Core properties + ATS keywords
# --------------------------------------------------------------------------

def build_core_properties(letter: CoverLetter, ats_keywords: Optional[List[str]] = None) -> Tuple[str, str, str]:
    """Derive Title/Subject/Keywords from the letter's own content — the
    Subject property reuses the letter's own '## Subject' line verbatim,
    since that's already meant to summarize what the letter is for."""
    company = letter.recipient_lines[1] if len(letter.recipient_lines) >= 2 else ""
    role_context = letter.recipient_lines[2] if len(letter.recipient_lines) >= 3 else ""

    title = f"{letter.name} — Cover Letter"
    if company:
        title += f" — {company}"
    subject = letter.subject

    # ATS keywords lead the list, same rationale as the resume generator.
    keyword_parts: List[str] = list(ats_keywords or [])
    if company:
        keyword_parts.append(company)
    if role_context:
        keyword_parts.append(role_context)

    return (dc.truncate_text(title), dc.truncate_text(subject),
            dc.truncate_keyword_list(dc.dedupe_preserve_order(keyword_parts)))


def find_ats_keywords_source(input_path: Path) -> Optional[Path]:
    return dc.find_ats_keywords_source(input_path, _COVER_LETTER_FILENAME_RE)


load_ats_keywords = dc.load_ats_keywords


def render_from_plan(letter: CoverLetter, template_path: Path, output_path: Path,
                      units: List[dc.LayoutUnit], plan: dc.PaginationPlan, tighten_factor: float = 1.0,
                      ats_keywords: Optional[List[str]] = None) -> None:
    core_properties = build_core_properties(letter, ats_keywords=ats_keywords)
    dc.render_docx_from_plan(template_path, output_path, STYLE_NAMES, units, plan,
                              core_properties, TIGHTENABLE_STYLE_KEYS, tighten_factor=tighten_factor)


def verify_content(pdf_text: str, letter: CoverLetter) -> List[str]:
    probes: List[Tuple[str, str]] = [("name", letter.name)]
    for i, p in enumerate(letter.body_paragraphs):
        probes.append((f"body paragraph {i + 1}", p))
    return dc.verify_content(pdf_text, probes)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate a page-fit-aware DOCX (and PDF) cover letter from a "
                    "canonical markdown source. See scripts/resume_docx/COVER_LETTER_SCHEMA.md "
                    "for the expected markdown structure."
    )
    parser.add_argument("input", help="Path to the canonical cover letter markdown file.")
    parser.add_argument("--template", default=str(DEFAULT_TEMPLATE),
                         help="Path to the DOCX template (default: Templates/cover-letter-template.docx).")
    parser.add_argument("--output",
                         help="Output .docx path. Default: for opportunity-folder "
                              "cover-letter.md, 'cover-letter_<INITIALS>-<company-role>-<YYYY-MM>.docx' "
                              "beside the input; otherwise input path with .docx extension.")
    parser.add_argument("--pages", type=int, default=1,
                         help="Maximum page count (default: 1). Content flows freely across "
                              "however many pages it actually needs, up to this limit; if the "
                              "letter spans more than one page, the next page opens with a "
                              "leading italic 'Letter (continued)' line. Exceeding this limit "
                              "is the only thing that fails generation (unless --allow-overflow).")
    parser.add_argument("--allow-overflow", action="store_true",
                         help="Write the artifact even if it needs more pages than --pages.")
    parser.add_argument("--fit", action="store_true",
                         help="Allow bounded whitespace tightening (body paragraph spacing "
                              "only) to try to reach the target page count. Never alters "
                              "wording or removes content.")
    parser.add_argument("--no-pdf", action="store_true",
                         help="Skip PDF conversion/validation (DOCX is still produced, "
                              "but the page count is not verified against real rendering).")
    parser.add_argument("--keep-workdir", action="store_true",
                         help="Keep the temporary render/validation working directory.")
    parser.add_argument("--ats-keywords",
                         help="Path to an analysis.md (or its opportunity folder) whose "
                              "'## ATS Keywords' section should lead the DOCX's Keywords "
                              "property. Without this, the tool prefers sibling analysis.md "
                              "for opportunity-folder inputs, else tries to auto-detect a "
                              "single unambiguous match under Career/06_Job_Opportunities/ "
                              "from a legacy long '<company>_<role>_cover_letter_<date>' filename; "
                              "if none is found, Keywords falls back to letter-derived "
                              "terms only.")
    args = parser.parse_args(argv)
    if args.pages < 1:
        print("FAIL: --pages must be a positive integer.", file=sys.stderr)
        return 2

    input_path = Path(args.input).resolve()
    output_path = (
        Path(args.output).resolve()
        if args.output
        else dc.default_shareable_output_path(input_path, "cover_letter")
    )
    template_path = Path(args.template).resolve()

    try:
        letter = parse_cover_letter_markdown(input_path)
    except CoverLetterParseError as e:
        print(f"FAIL: could not parse {input_path}:\n  {e}", file=sys.stderr)
        return 2

    if not template_path.exists():
        print(f"FAIL: template not found at {template_path}", file=sys.stderr)
        return 2

    ats_keywords: List[str] = []
    if args.ats_keywords:
        ats_path = Path(args.ats_keywords).resolve()
        try:
            ats_keywords = load_ats_keywords(ats_path)
        except CoverLetterParseError as e:
            print(f"FAIL: {e}", file=sys.stderr)
            return 2
        print(f"Using {len(ats_keywords)} ATS keyword(s) from {ats_path}.")
    else:
        auto = find_ats_keywords_source(input_path)
        if auto is not None:
            try:
                ats_keywords = load_ats_keywords(auto)
                print(f"Using {len(ats_keywords)} ATS keyword(s) auto-detected from {auto}.")
            except CoverLetterParseError:
                pass  # analysis.md exists but has no ATS Keywords section; not fatal

    document = Document(str(template_path))
    styles = dc.extract_style_specs(document, STYLE_NAMES)
    geometry = dc.extract_page_geometry(document)
    try:
        metrics = dc.FontMetrics()
    except RuntimeError as e:
        print(f"FAIL: {e}", file=sys.stderr)
        return 2

    def plan_at(factor: float) -> Tuple[List[dc.LayoutUnit], dc.PaginationPlan]:
        u = build_layout_units(letter, styles, metrics, geometry, tighten_factor=factor)
        p = dc.simulate_pagination(u, geometry.content_height_pt, metrics, styles,
                                    geometry.content_width_pt, tighten_factor=factor,
                                    tightenable_keys=TIGHTENABLE_STYLE_KEYS)
        return u, p

    def print_breakdown(u: List[dc.LayoutUnit]) -> None:
        breakdown: Dict[str, float] = {}
        for unit in u:
            label = unit.section if unit.section else "Header"
            breakdown[label] = breakdown.get(label, 0.0) + unit.height_pt
        for label, h in breakdown.items():
            print(f"  - {label}: {h / 72:.2f}in")

    tighten_factor = 1.0
    units, plan = plan_at(tighten_factor)

    if plan.oversized_unit is not None:
        bad = units[plan.oversized_unit]
        print(f"FAIL: a single item in '{bad.section or 'Header'}' is "
              f"{bad.height_pt / 72:.2f}in tall, taller than one page "
              f"({geometry.content_height_pt / 72:.2f}in). It can never fit on any page.",
              file=sys.stderr)
        print(f"  Offending content: {dc.describe_unit(bad)!r}", file=sys.stderr)
        print("Shorten it — no page-count option can fix this.", file=sys.stderr)
        return 2

    print(f"Estimated pages needed: {plan.pages_used} (limit: {args.pages}, "
          f"{geometry.content_height_pt / 72:.2f}in usable per page).")
    print_breakdown(units)

    if plan.pages_used > args.pages and args.fit:
        for factor in (0.85, 0.7):
            candidate_units, candidate_plan = plan_at(factor)
            if candidate_plan.oversized_unit is None and candidate_plan.pages_used <= args.pages:
                units, plan, tighten_factor = candidate_units, candidate_plan, factor
                print(f"Applying --fit spacing reduction (factor {factor}) to reach the "
                      f"{args.pages}-page limit.")
                break
        else:
            units, plan, tighten_factor = candidate_units, candidate_plan, 0.7
            print(f"Applied maximum --fit spacing reduction (factor 0.7); still "
                  f"{plan.pages_used} page(s) needed.")

    if plan.pages_used > args.pages and not args.allow_overflow:
        print(f"FAIL: content needs {plan.pages_used} page(s), exceeding the "
              f"{args.pages}-page limit.", file=sys.stderr)
        print("No DOCX/PDF was written. Trim content (see the breakdown above), "
              "raise --pages, or pass --allow-overflow to write anyway.", file=sys.stderr)
        return 2

    workdir = Path(tempfile.mkdtemp(prefix="cover_letter_docx_"))
    pdf_path: Optional[Path] = None
    try:
        draft_docx = workdir / (output_path.stem + ".docx")
        render_from_plan(letter, template_path, draft_docx, units, plan, tighten_factor=tighten_factor,
                          ats_keywords=ats_keywords)

        if not args.no_pdf:
            try:
                pdf_path = dc.convert_to_pdf(draft_docx, workdir)
            except RuntimeError as e:
                print(f"FAIL: {e}", file=sys.stderr)
                return 2
            actual_pages = dc.count_pdf_pages(pdf_path)
            print(f"Rendered PDF has {actual_pages} page(s) (limit: {args.pages}, planned: {plan.pages_used}).")
            if actual_pages != plan.pages_used:
                print(f"WARNING: the layout plan targeted {plan.pages_used} page(s) but the "
                      f"real render produced {actual_pages}; the font-metric estimate and "
                      f"LibreOffice's own layout disagree slightly.")
            if actual_pages > args.pages and not args.allow_overflow:
                print(f"FAIL: rendered output is {actual_pages} page(s), exceeding the "
                      f"{args.pages}-page target.", file=sys.stderr)
                if args.keep_workdir:
                    print(f"Draft files kept for inspection at: {workdir}", file=sys.stderr)
                else:
                    kept = Path(tempfile.mkdtemp(prefix="cover_letter_docx_overflow_"))
                    shutil.copyfile(draft_docx, kept / draft_docx.name)
                    shutil.copyfile(pdf_path, kept / pdf_path.name)
                    print(f"Draft files kept for inspection at: {kept}", file=sys.stderr)
                return 2
            for w in verify_content(dc.extract_pdf_text(pdf_path), letter):
                print(f"WARNING: {w}")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(draft_docx, output_path)
        print(f"Wrote {output_path}")
        if pdf_path is not None:
            pdf_final_path = output_path.with_suffix(".pdf")
            shutil.copyfile(pdf_path, pdf_final_path)
            print(f"Wrote {pdf_final_path}")
    finally:
        if args.keep_workdir:
            print(f"Working directory kept at: {workdir}")
        else:
            shutil.rmtree(workdir, ignore_errors=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())
