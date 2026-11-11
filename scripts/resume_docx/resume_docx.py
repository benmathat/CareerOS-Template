#!/usr/bin/env python3
"""
Deterministic markdown -> DOCX/PDF resume generator.

Reads a canonical resume markdown file (see SCHEMA.md), fills the named
styles in Career/01_Resume_and_Profiles/Templates/resume-template.docx,
and uses real font metrics to plan every page break itself (content
flows freely across pages within the page limit; a section that
continues onto the next page gets a leading italic "(continued)" line).
A LibreOffice render/validate pass then confirms the real page count
matches the plan. The only failure condition is needing more pages than
the limit allows. No LLM step is involved in filling the template:
parsing and layout are code, not prose generation.

The generic DOCX-layout engine (font metrics, pagination, rendering,
LibreOffice validation) lives in docx_common.py, shared with
cover_letter_docx.py.

Usage:
    scripts/generate-resume-docx.sh <input.md> [--pages N] [options]

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

DEFAULT_TEMPLATE = dc.REPO_ROOT / "Career/01_Resume_and_Profiles/Templates/resume-template.docx"

STYLE_NAMES = {
    "title": "Title",
    "headline": "Resume Headline",
    "contact": "Resume Contact",
    "heading1": "Heading 1",
    "role": "Resume Role",
    "employer": "Resume Employer",
    "body": "Resume Body",
    "bullet": "Resume Bullet",
    "education": "Resume Education",
}
TIGHTENABLE_STYLE_KEYS = frozenset({"body", "bullet", "education"})

SKILLS_HEADINGS = {
    "core strengths", "core skills", "skills", "tools & methods",
    "tools and methods", "technical skills", "key skills", "core capabilities",
}
EXPERIENCE_HEADINGS = {"professional experience", "experience", "work experience"}
EDUCATION_HEADINGS = {"education"}
CREDENTIALS_HEADINGS = {
    "professional development", "certifications", "credentials",
    "professional development & certifications",
    "professional development and certifications",
}

ResumeParseError = dc.DocGenError  # backward-compatible alias

# A line holding exactly this, just before a `### Employer - Title` entry, starts a new
# page there (when the entry is not already at the top of a page).
PAGE_BREAK_DIRECTIVE = "<!-- page-break -->"


# --------------------------------------------------------------------------
# Data model
# --------------------------------------------------------------------------

@dataclass
class ExperienceEntry:
    employer: str
    title: str
    dates: str = ""
    location: str = ""
    bullets: List[str] = field(default_factory=list)
    description: List[str] = field(default_factory=list)
    page_break_before: bool = False  # set by a `<!-- page-break -->` line before the entry


@dataclass
class EducationEntry:
    label: str
    org: str = ""
    detail: str = ""


@dataclass
class GenericSection:
    heading: str
    bullets: List[str] = field(default_factory=list)
    paragraphs: List[str] = field(default_factory=list)
    subsections: List[Tuple[str, List[str]]] = field(default_factory=list)
    # Where an unrecognized section sits relative to the experience and education
    # blocks in the markdown: "before_experience", "before_education" (after the
    # experience block) or "end" (after education and credentials).
    anchor: str = "end"


@dataclass
class Resume:
    name: str
    contact_lines: List[str]
    headline: Optional[str] = None
    summary_paragraphs: List[str] = field(default_factory=list)
    summary_heading: str = "Summary"
    skill_sections: List[GenericSection] = field(default_factory=list)
    experience: List[ExperienceEntry] = field(default_factory=list)
    experience_heading: str = "Professional Experience"
    education: List[EducationEntry] = field(default_factory=list)
    credentials: List[EducationEntry] = field(default_factory=list)
    other_sections: List[GenericSection] = field(default_factory=list)
    source_path: str = ""


# --------------------------------------------------------------------------
# Markdown parsing
# --------------------------------------------------------------------------

_DASH_SPLIT_RE = re.compile(r"\s[-–—]\s")
_YEAR_PAREN_RE = re.compile(r"\(([^)]+)\)\s*$")
_BOLD_LINE_RE = re.compile(r"^\*\*(.+?)\*\*\s*[-–—:]?\s*(.*)$")
_CRED_BOLD_RE = re.compile(r"^\*\*(.+?)\*\*\s*[-–—]\s*(.*)$")
_RESUME_FILENAME_RE = re.compile(r"^(.*)_resume_\d{4}-\d{2}-\d{2}$")


def _parse_generic_section(heading: str, lines: List[str]) -> GenericSection:
    section = GenericSection(heading=heading)
    if any(l.startswith("### ") for l in lines):
        current_sub, current_bullets = None, []
        for line in lines:
            if line.startswith("### "):
                if current_sub is not None:
                    section.subsections.append((current_sub, current_bullets))
                current_sub, current_bullets = line[4:].strip(), []
            elif line.strip().startswith(("- ", "* ")):
                current_bullets.append(line.strip()[2:].strip())
            elif line.strip():
                current_bullets.append(line.strip())
        if current_sub is not None:
            section.subsections.append((current_sub, current_bullets))
    else:
        bullets = [l.strip()[2:].strip() for l in lines if l.strip().startswith(("- ", "* "))]
        if bullets:
            section.bullets = bullets
            first = next(i for i, l in enumerate(lines) if l.strip().startswith(("- ", "* ")))
            section.paragraphs = dc.split_paragraphs(lines[:first])
        else:
            section.paragraphs = dc.split_paragraphs(lines)
    return section


def _split_employer_title(header_text: str) -> Tuple[str, str]:
    m = _DASH_SPLIT_RE.search(header_text)
    if not m:
        raise ResumeParseError(
            f"Could not split employer and title from Professional Experience "
            f"heading {header_text!r}. Expected 'Employer - Title' "
            f"(a hyphen/en dash/em dash surrounded by spaces)."
        )
    return header_text[:m.start()].strip(), header_text[m.end():].strip()


def _parse_date_location(text: str) -> Tuple[str, str]:
    text = text.strip()
    if text.startswith("**") and text.endswith("**"):
        text = text[2:-2].strip()
    parts = [p.strip() for p in text.split("|")]
    dates = parts[0] if parts else ""
    location = parts[1] if len(parts) > 1 else ""
    return dates, location


def _parse_experience(lines: List[str]) -> List[ExperienceEntry]:
    entries: List[ExperienceEntry] = []
    i, n = 0, len(lines)
    current: Optional[ExperienceEntry] = None
    pending_page_break = False
    while i < n:
        line = lines[i]
        if line.strip() == PAGE_BREAK_DIRECTIVE:
            pending_page_break = True
            i += 1
            continue
        if line.startswith("### "):
            if current is not None:
                entries.append(current)
            employer, title = _split_employer_title(line[4:].strip())
            current = ExperienceEntry(employer=employer, title=title, page_break_before=pending_page_break)
            pending_page_break = False
            i += 1
            while i < n and not lines[i].strip():
                i += 1
            if i < n and lines[i].strip().startswith(":::"):
                i += 1
                fence_content = []
                while i < n and lines[i].strip() != ":::":
                    if lines[i].strip():
                        fence_content.append(lines[i].strip())
                    i += 1
                i += 1
                if fence_content:
                    current.dates, current.location = _parse_date_location(fence_content[0])
            elif i < n and lines[i].strip().startswith("**"):
                current.dates, current.location = _parse_date_location(lines[i].strip())
                i += 1
            continue
        stripped = line.strip()
        if stripped.startswith(("- ", "* ")) and current is not None:
            current.bullets.append(stripped[2:].strip())
        elif stripped and current is not None and not current.bullets:
            current.description.extend(dc.split_paragraphs([stripped]) or [stripped])
        i += 1
    if current is not None:
        entries.append(current)
    if not entries:
        raise ResumeParseError("Professional Experience section has no '### Employer - Title' entries.")
    for e in entries:
        if not e.dates:
            raise ResumeParseError(f"Missing dates/location line for experience entry: {e.employer} - {e.title}")
        if not e.bullets and not e.description:
            raise ResumeParseError(f"Experience entry has no description or achievement bullets: {e.employer} - {e.title}")
    return entries


def _parse_education(lines: List[str]) -> List[EducationEntry]:
    entries: List[EducationEntry] = []
    i, n = 0, len(lines)
    while i < n:
        stripped = lines[i].strip()
        if not stripped:
            i += 1
            continue
        if stripped.startswith("### "):
            institution = stripped[4:].strip()
            i += 1
            degree, detail = "", ""
            while i < n and not lines[i].strip():
                i += 1
            if i < n and lines[i].strip().startswith("**") and lines[i].strip().endswith("**"):
                degree = lines[i].strip()[2:-2].strip()
                i += 1
            while i < n and not lines[i].strip():
                i += 1
            if (i < n and lines[i].strip().startswith("*") and lines[i].strip().endswith("*")
                    and not lines[i].strip().startswith("**")):
                detail = lines[i].strip()[1:-1].strip()
                i += 1
            entries.append(EducationEntry(label=degree or institution,
                                           org=institution if degree else "",
                                           detail=detail))
            continue
        if stripped.startswith("**"):
            m = _BOLD_LINE_RE.match(stripped)
            if m:
                institution, rest = m.group(1).strip(), m.group(2).strip()
                year_m = _YEAR_PAREN_RE.search(rest)
                detail = year_m.group(1).strip() if year_m else ""
                degree = _YEAR_PAREN_RE.sub("", rest).strip() if year_m else rest
                entries.append(EducationEntry(label=degree or institution,
                                               org=institution if degree else "",
                                               detail=detail))
            else:
                entries.append(EducationEntry(label=dc.strip_inline_markup(stripped)))
            i += 1
            continue
        if stripped.startswith(("- ", "* ")):
            entries.append(EducationEntry(label=dc.strip_inline_markup(stripped[2:].strip())))
            i += 1
            continue
        entries.append(EducationEntry(label=dc.strip_inline_markup(stripped)))
        i += 1
    if not entries:
        raise ResumeParseError("Education section has no parseable entries.")
    return entries


def _parse_credentials(lines: List[str]) -> List[EducationEntry]:
    entries: List[EducationEntry] = []
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith(("- ", "* ")):
            continue
        body = stripped[2:].strip()
        m = _CRED_BOLD_RE.match(body)
        if m:
            entries.append(EducationEntry(label=m.group(1).strip(), org=m.group(2).strip()))
            continue
        parts = _DASH_SPLIT_RE.split(body, maxsplit=1)
        if len(parts) == 2:
            entries.append(EducationEntry(label=dc.strip_inline_markup(parts[0]).strip(),
                                           org=dc.strip_inline_markup(parts[1]).strip()))
        else:
            entries.append(EducationEntry(label=dc.strip_inline_markup(body).strip()))
    if not entries:
        raise ResumeParseError("Professional Development/Certifications section has no bullet entries.")
    return entries


def parse_resume_markdown(path: Path) -> Resume:
    text = Path(path).read_text(encoding="utf-8")
    lines = dc.strip_frontmatter(text.splitlines())

    idx = 0
    while idx < len(lines) and not lines[idx].strip():
        idx += 1
    if idx >= len(lines) or not lines[idx].startswith("# "):
        found = lines[idx] if idx < len(lines) else "<end of file>"
        raise ResumeParseError(
            f"Expected a top-level '# Full Name' heading as the first content "
            f"line (after any frontmatter); found: {found!r}"
        )
    name = lines[idx][2:].strip()
    idx += 1

    contact_lines: List[str] = []
    while idx < len(lines) and not lines[idx].startswith("## "):
        if lines[idx].strip():
            contact_lines.append(lines[idx].strip())
        idx += 1

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

    if not contact_lines:
        CONTACT_HEADINGS = {"contact information", "contact", "contact details"}
        remaining = []
        for heading, content in sections:
            if not contact_lines and heading.strip().lower() in CONTACT_HEADINGS:
                contact_lines = [l.strip() for l in content if l.strip()]
            else:
                remaining.append((heading, content))
        sections = remaining
    if not contact_lines:
        raise ResumeParseError(
            "Expected a contact-details line directly under the name heading "
            "(or a '## Contact Information' section) before Summary/Experience."
        )

    resume = Resume(name=name, contact_lines=contact_lines, source_path=str(path))

    seen_experience = seen_education = False
    for heading, content in sections:
        norm = heading.strip().lower()
        if norm == "headline":
            resume.headline = next((l.strip() for l in content if l.strip()), None)
        elif norm in ("summary", "executive profile"):
            resume.summary_paragraphs = dc.split_paragraphs(content)
            resume.summary_heading = heading.strip()
        elif norm in SKILLS_HEADINGS:
            resume.skill_sections.append(_parse_generic_section(heading, content))
        elif norm in EXPERIENCE_HEADINGS:
            resume.experience = _parse_experience(content)
            resume.experience_heading = heading
            seen_experience = True
        elif norm in EDUCATION_HEADINGS:
            resume.education = _parse_education(content)
            seen_education = True
        elif norm in CREDENTIALS_HEADINGS:
            resume.credentials = _parse_credentials(content)
            seen_education = True
        else:
            other = _parse_generic_section(heading, content)
            other.anchor = ("end" if seen_education else
                            "before_education" if seen_experience else "before_experience")
            resume.other_sections.append(other)

    if not resume.experience:
        raise ResumeParseError(
            "No 'Professional Experience' section found (looked for a "
            "'## Professional Experience' / '## Experience' heading)."
        )
    return resume


def _education_heading(resume: Resume) -> Optional[str]:
    if resume.education and resume.credentials:
        return "EDUCATION AND CREDENTIALS"
    if resume.education:
        return "EDUCATION"
    if resume.credentials:
        return "CREDENTIALS"
    return None


# --------------------------------------------------------------------------
# Layout units (resume-specific composition over the shared engine)
# --------------------------------------------------------------------------

def _generic_section_units(heading: str, section: GenericSection, metrics: dc.FontMetrics,
                            styles: Dict[str, dc.StyleSpec], width_pt: float,
                            tighten_factor: float) -> List[dc.LayoutUnit]:
    groups: List[Tuple[List[dc.ParaSpec], List[dc.ParaSpec]]] = []
    if section.subsections:
        for sub, bullets in section.subsections:
            bullet_specs = [dc.ParaSpec("bullet", [b]) for b in bullets]
            starter = [dc.ParaSpec("body", [sub], bold=True)] + bullet_specs[:1]
            groups.append((starter, bullet_specs[1:]))
    elif section.bullets:
        bullet_specs = [dc.ParaSpec("bullet", [b]) for b in section.bullets]
        intro_specs = [dc.ParaSpec("body", [p]) for p in section.paragraphs]
        if intro_specs:
            groups.append((intro_specs + bullet_specs[:1], bullet_specs[1:]))
        else:
            groups.append((bullet_specs[:1], bullet_specs[1:]))
    else:
        para_specs = [dc.ParaSpec("body", [p]) for p in section.paragraphs]
        groups.append((para_specs[:1], para_specs[1:]))
    if not groups:
        groups = [([], [])]
    return dc.grouped_units(heading, groups, metrics, styles, width_pt, tighten_factor, TIGHTENABLE_STYLE_KEYS)


_DATE_SPLIT_RE = re.compile(r"\s*[\u2013\u2014-]\s*")


def _employer_span(jobs: List[ExperienceEntry]) -> str:
    """Overall dates for consecutive roles at one employer (newest first):
    earliest start to latest end."""
    start = _DATE_SPLIT_RE.split(jobs[-1].dates, maxsplit=1)[0].strip()
    parts = _DATE_SPLIT_RE.split(jobs[0].dates, maxsplit=1)
    end = parts[1].strip() if len(parts) > 1 else ""
    return f"{start} \u2013 {end}" if end else start


def _group_by_employer(experience: List[ExperienceEntry]) -> List[List[ExperienceEntry]]:
    """Group consecutive entries sharing employer and location, so multiple
    positions at one organization show a single employer heading."""
    groups: List[List[ExperienceEntry]] = []
    for job in experience:
        if groups and groups[-1][0].employer == job.employer and groups[-1][0].location == job.location:
            groups[-1].append(job)
        else:
            groups.append([job])
    return groups


def _experience_units(resume: Resume, metrics: dc.FontMetrics, styles: Dict[str, dc.StyleSpec],
                       width_pt: float, tighten_factor: float) -> List[dc.LayoutUnit]:
    groups: List[Tuple[List[dc.ParaSpec], List[dc.ParaSpec]]] = []
    forced: List[bool] = []
    for employer_jobs in _group_by_employer(resume.experience):
        multi = len(employer_jobs) > 1
        for idx, job in enumerate(employer_jobs):
            bullet_specs = [dc.ParaSpec("bullet", [b]) for b in job.bullets]
            desc_specs = [dc.ParaSpec("body", [d]) for d in job.description]
            # One model for every employer: employer name; for multiple positions a
            # "Location | overall tenure" line; then "Title | Dates" for each position.
            # A single-position employer omits the location/tenure line.
            head = []
            if idx == 0:
                head.append(dc.ParaSpec("role", [job.employer.upper()]))
                if multi:
                    org_line = " | ".join(x for x in [job.location, _employer_span(employer_jobs)] if x)
                    head.append(dc.ParaSpec("employer", [org_line]))
            head.append(dc.ParaSpec("body", [" | ".join(x for x in [job.title, job.dates] if x)], italic=True))
            starter = head + desc_specs + bullet_specs[:1]
            groups.append((starter, bullet_specs[1:]))
            forced.append(job.page_break_before)
    units = dc.grouped_units(resume.experience_heading, groups, metrics, styles, width_pt,
                              tighten_factor, TIGHTENABLE_STYLE_KEYS)
    pos = 0
    for (starter, rest), force in zip(groups, forced):
        units[pos].force_break_before = force
        pos += 1 + len(rest)
    return units


def _education_units(resume: Resume, metrics: dc.FontMetrics, styles: Dict[str, dc.StyleSpec],
                      width_pt: float, tighten_factor: float) -> List[dc.LayoutUnit]:
    label = _education_heading(resume)
    if not label:
        return []
    entries = resume.education + resume.credentials
    entry_specs = [dc.ParaSpec("education", [" | ".join(x for x in [e.label, e.org, e.detail] if x)])
                   for e in entries]
    groups = [(entry_specs[:1], entry_specs[1:])]
    return dc.grouped_units(label, groups, metrics, styles, width_pt, tighten_factor, TIGHTENABLE_STYLE_KEYS)


def build_layout_units(resume: Resume, styles: Dict[str, dc.StyleSpec], metrics: dc.FontMetrics,
                        geometry: dc.PageGeometry, tighten_factor: float = 1.0) -> List[dc.LayoutUnit]:
    width = geometry.content_width_pt
    units: List[dc.LayoutUnit] = []

    front_paras = [dc.ParaSpec("title", [resume.name])]
    if resume.headline:
        front_paras.append(dc.ParaSpec("headline", [resume.headline]))
    front_paras.append(dc.ParaSpec("contact", [dc.clean_contact_line(l) for l in resume.contact_lines]))
    units.append(dc.make_unit(metrics, styles, width, tighten_factor, TIGHTENABLE_STYLE_KEYS, "", False, front_paras))

    if resume.summary_paragraphs:
        para_specs = [dc.ParaSpec("body", [p]) for p in resume.summary_paragraphs]
        groups = [(para_specs[:1], para_specs[1:])]
        units.extend(dc.grouped_units(resume.summary_heading, groups, metrics, styles, width, tighten_factor, TIGHTENABLE_STYLE_KEYS))

    for section in resume.skill_sections:
        units.extend(_generic_section_units(section.heading, section, metrics, styles, width, tighten_factor))

    def other_units(anchor: str) -> None:
        for section in resume.other_sections:
            if section.anchor == anchor:
                units.extend(_generic_section_units(section.heading, section, metrics, styles, width, tighten_factor))

    # Unrecognized sections keep their markdown position relative to experience and education.
    other_units("before_experience")
    units.extend(_experience_units(resume, metrics, styles, width, tighten_factor))
    other_units("before_education")
    units.extend(_education_units(resume, metrics, styles, width, tighten_factor))
    other_units("end")

    return units


# --------------------------------------------------------------------------
# Core properties + ATS keywords
# --------------------------------------------------------------------------

def build_core_properties(resume: Resume, ats_keywords: Optional[List[str]] = None) -> Tuple[str, str, str]:
    """Derive Title/Subject/Keywords from the resume's own content — no
    invented claims, just what's already in the document (plus, for
    Keywords only, ATS terms extracted verbatim from a target job posting's
    opportunity analysis, when supplied)."""
    latest_title = resume.experience[0].title if resume.experience else ""

    if resume.headline:
        title = f"{resume.name} — {resume.headline}"
        subject = resume.headline
    else:
        title = f"{resume.name} — Resume"
        subject = latest_title or "Resume"

    # ATS keywords lead the list — they're what a target-role screen searches
    # for, so truncation (if any) should drop generic resume-derived terms
    # before it drops these.
    keyword_parts: List[str] = list(ats_keywords or [])
    if resume.headline:
        keyword_parts.append(resume.headline)
    for job in resume.experience:
        keyword_parts.append(job.title)
        keyword_parts.append(job.employer)
    for section in resume.skill_sections:
        for subheading, _bullets in section.subsections:
            keyword_parts.append(subheading)

    return (dc.truncate_text(title), dc.truncate_text(subject),
            dc.truncate_keyword_list(dc.dedupe_preserve_order(keyword_parts)))


def find_ats_keywords_source(input_resume_path: Path) -> Optional[Path]:
    return dc.find_ats_keywords_source(input_resume_path, _RESUME_FILENAME_RE)


load_ats_keywords = dc.load_ats_keywords


def render_from_plan(resume: Resume, template_path: Path, output_path: Path,
                      units: List[dc.LayoutUnit], plan: dc.PaginationPlan, tighten_factor: float = 1.0,
                      ats_keywords: Optional[List[str]] = None) -> None:
    core_properties = build_core_properties(resume, ats_keywords=ats_keywords)
    dc.render_docx_from_plan(template_path, output_path, STYLE_NAMES, units, plan,
                              core_properties, TIGHTENABLE_STYLE_KEYS, tighten_factor=tighten_factor)


def verify_content(pdf_text: str, resume: Resume) -> List[str]:
    probes: List[Tuple[str, str]] = [("name", resume.name)]
    for job in resume.experience:
        for b in job.bullets:
            probes.append((f"{job.employer} bullet", b))
    for entry in resume.education + resume.credentials:
        probes.append(("education/credential", entry.label))
    return dc.verify_content(pdf_text, probes)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate a page-fit-aware DOCX (and PDF) resume from a "
                    "canonical markdown source. See scripts/resume_docx/SCHEMA.md "
                    "for the expected markdown structure."
    )
    parser.add_argument("input", help="Path to the canonical resume markdown file.")
    parser.add_argument("--template", default=str(DEFAULT_TEMPLATE),
                         help="Path to the DOCX template (default: Templates/resume-template.docx).")
    parser.add_argument("--output",
                         help="Output .docx path. Default: for opportunity-folder "
                              "resume.md, 'resume_<INITIALS>-<company-role>-<YYYY-MM>.docx' beside "
                              "the input; otherwise input path with .docx extension.")
    parser.add_argument("--pages", type=int, default=3,
                         help="Maximum page count (default: 3). Content flows freely across "
                              "however many pages it actually needs, up to this limit; a "
                              "section that overflows onto the next page gets a leading "
                              "italic '<Section> (continued)' line. Exceeding this limit is "
                              "the only thing that fails generation (unless --allow-overflow).")
    parser.add_argument("--allow-overflow", action="store_true",
                         help="Write the artifact even if it needs more pages than --pages.")
    parser.add_argument("--fit", action="store_true",
                         help="Allow bounded whitespace tightening (bullet/body/education "
                              "paragraph spacing only) to try to reach the target page count. "
                              "Never alters wording or removes content.")
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
                              "from a legacy long '<company>_<role>_resume_<date>' filename; "
                              "if none is found, Keywords falls back to resume-derived terms only.")
    args = parser.parse_args(argv)
    if args.pages < 1:
        print("FAIL: --pages must be a positive integer.", file=sys.stderr)
        return 2

    input_path = Path(args.input).resolve()
    output_path = (
        Path(args.output).resolve()
        if args.output
        else dc.default_shareable_output_path(input_path, "resume")
    )
    template_path = Path(args.template).resolve()

    try:
        resume = parse_resume_markdown(input_path)
    except ResumeParseError as e:
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
        except ResumeParseError as e:
            print(f"FAIL: {e}", file=sys.stderr)
            return 2
        print(f"Using {len(ats_keywords)} ATS keyword(s) from {ats_path}.")
    else:
        auto = find_ats_keywords_source(input_path)
        if auto is not None:
            try:
                ats_keywords = load_ats_keywords(auto)
                print(f"Using {len(ats_keywords)} ATS keyword(s) auto-detected from {auto}.")
            except ResumeParseError:
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
        u = build_layout_units(resume, styles, metrics, geometry, tighten_factor=factor)
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

    workdir = Path(tempfile.mkdtemp(prefix="resume_docx_"))
    pdf_path: Optional[Path] = None
    try:
        draft_docx = workdir / (output_path.stem + ".docx")
        render_from_plan(resume, template_path, draft_docx, units, plan, tighten_factor=tighten_factor,
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
                    kept = Path(tempfile.mkdtemp(prefix="resume_docx_overflow_"))
                    shutil.copyfile(draft_docx, kept / draft_docx.name)
                    shutil.copyfile(pdf_path, kept / pdf_path.name)
                    print(f"Draft files kept for inspection at: {kept}", file=sys.stderr)
                return 2
            for w in verify_content(dc.extract_pdf_text(pdf_path), resume):
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
