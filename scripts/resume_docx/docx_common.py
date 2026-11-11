#!/usr/bin/env python3
"""
Shared DOCX-layout engine used by resume_docx.py and cover_letter_docx.py.

Nothing here knows about resumes or cover letters specifically: it's font
metrics, docx style/geometry extraction, a generic "layout unit" pagination
planner (content flows freely across pages within a limit; a section that
overflows onto the next page gets a leading "(continued)" marker), basic
inline-markdown-to-docx-run rendering, core-property helpers, ATS-keyword
extraction, and LibreOffice PDF conversion/validation. Each caller supplies
its own style-name mapping, tightenable-style-key set, and data model.
"""

from __future__ import annotations

import dataclasses
import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from docx import Document
from docx.oxml.ns import qn
from docx.shared import Pt

REPO_ROOT = Path(__file__).resolve().parents[2]
JOB_OPPORTUNITIES_DIR = REPO_ROOT / "Career/06_Job_Opportunities"


class DocGenError(Exception):
    pass


# --------------------------------------------------------------------------
# Font metrics (real glyph widths, not average-character heuristics)
# --------------------------------------------------------------------------

FONT_FILENAMES = {
    (False, False): "LiberationSans-Regular.ttf",
    (True, False): "LiberationSans-Bold.ttf",
    (False, True): "LiberationSans-Italic.ttf",
    (True, True): "LiberationSans-BoldItalic.ttf",
}
# Liberation Sans is a metric-compatible substitute for Arial (the templates'
# font), so widths measured against it match Arial layout to within
# sub-point rounding.

FONT_SEARCH_DIRS = [
    Path.home() / "Library/Fonts",                    # macOS, brew cask font-liberation
    Path("/Library/Fonts"),                            # macOS, system-wide install
    Path("/usr/share/fonts/truetype/liberation"),      # Debian/Ubuntu (fonts-liberation)
    Path("/usr/share/fonts/liberation"),                # Fedora/RHEL (liberation-sans-fonts)
    Path("/usr/local/share/fonts"),                     # manual/Homebrew-on-Linux installs
    Path.home() / ".local/share/fonts",                 # per-user Linux
    Path.home() / ".fonts",                             # older per-user Linux convention
]


def _find_font_file(filename: str) -> Path:
    env_dir = os.environ.get("RESUME_DOCX_FONT_DIR")
    search_dirs = ([Path(env_dir)] if env_dir else []) + FONT_SEARCH_DIRS
    for d in search_dirs:
        candidate = d / filename
        if candidate.exists():
            return candidate
    searched = "\n  ".join(str(d) for d in search_dirs)
    raise RuntimeError(
        f"Could not find required font file {filename!r}. Searched:\n  {searched}\n"
        f"Install Liberation Sans (metric-compatible with Arial):\n"
        f"  macOS:          brew install --cask font-liberation\n"
        f"  Debian/Ubuntu:  sudo apt-get install fonts-liberation\n"
        f"  Fedora/RHEL:    sudo dnf install liberation-sans-fonts\n"
        f"Or set RESUME_DOCX_FONT_DIR to the directory containing the .ttf files."
    )


class FontMetrics:
    def __init__(self) -> None:
        from fontTools.ttLib import TTFont
        self._cmaps: Dict[Tuple[bool, bool], dict] = {}
        self._hmtx = {}
        self._upm: Dict[Tuple[bool, bool], int] = {}
        self._line_units: Dict[Tuple[bool, bool], float] = {}
        for key, filename in FONT_FILENAMES.items():
            path = _find_font_file(filename)
            tt = TTFont(str(path))
            upm = tt["head"].unitsPerEm
            hhea = tt["hhea"]
            self._cmaps[key] = tt.getBestCmap()
            self._hmtx[key] = tt["hmtx"]
            self._upm[key] = upm
            self._line_units[key] = (hhea.ascent - hhea.descent + hhea.lineGap)

    def _glyph_width_units(self, key: Tuple[bool, bool], ch: str) -> float:
        cmap = self._cmaps[key]
        glyph_name = cmap.get(ord(ch)) or cmap.get(ord(" "))
        if glyph_name is None:
            return self._upm[key] * 0.5
        try:
            return self._hmtx[key][glyph_name][0]
        except KeyError:
            return self._upm[key] * 0.5

    def text_width_pt(self, text: str, size_pt: float, bold: bool = False, italic: bool = False) -> float:
        key = (bold, italic)
        upm = self._upm[key]
        units = sum(self._glyph_width_units(key, ch) for ch in text)
        return units / upm * size_pt

    def natural_line_height_pt(self, size_pt: float, bold: bool = False, italic: bool = False) -> float:
        key = (bold, italic)
        return self._line_units[key] / self._upm[key] * size_pt

    def wrap_lines(self, text: str, max_width_pt: float, size_pt: float,
                    bold: bool = False, italic: bool = False) -> List[str]:
        words = text.split()
        if not words:
            return [""]
        lines, current = [], words[0]
        for w in words[1:]:
            candidate = f"{current} {w}"
            if self.text_width_pt(candidate, size_pt, bold, italic) <= max_width_pt:
                current = candidate
            else:
                lines.append(current)
                current = w
        lines.append(current)
        return lines


# --------------------------------------------------------------------------
# Inline markdown handling
# --------------------------------------------------------------------------

_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
_ITALIC_RE = re.compile(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)")
_TOKEN_RE = re.compile(r"\*\*(.+?)\*\*|\*(.+?)\*|\[([^\]]+)\]\(([^)]+)\)")


def strip_inline_markup(text: str) -> str:
    text = _LINK_RE.sub(lambda m: m.group(1), text)
    text = _BOLD_RE.sub(lambda m: m.group(1), text)
    text = _ITALIC_RE.sub(lambda m: m.group(1), text)
    return text


def parse_inline_segments(text: str) -> List[Tuple[str, bool, bool]]:
    segments = []
    pos = 0
    for m in _TOKEN_RE.finditer(text):
        if m.start() > pos:
            segments.append((text[pos:m.start()], False, False))
        if m.group(1) is not None:
            segments.append((m.group(1), True, False))
        elif m.group(2) is not None:
            segments.append((m.group(2), False, True))
        elif m.group(3) is not None:
            segments.append((m.group(3), False, False))
        pos = m.end()
    if pos < len(text):
        segments.append((text[pos:], False, False))
    return segments


def clean_contact_line(line: str) -> str:
    def repl(m: "re.Match[str]") -> str:
        url = m.group(2)
        display = re.sub(r"^https?://", "", url).rstrip("/")
        return display
    return _LINK_RE.sub(repl, line)


# --------------------------------------------------------------------------
# Generic markdown helpers
# --------------------------------------------------------------------------

def strip_frontmatter(lines: List[str]) -> List[str]:
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return lines[i + 1:]
    return lines


def split_paragraphs(lines: List[str]) -> List[str]:
    paragraphs, current = [], []
    for line in lines:
        if line.strip():
            current.append(line.strip())
        elif current:
            paragraphs.append(" ".join(current))
            current = []
    if current:
        paragraphs.append(" ".join(current))
    return paragraphs


def extract_markdown_h2_section(text: str, heading_names: set) -> Optional[List[str]]:
    """Return the raw content lines under the first '## <heading>' section
    (case-insensitive match against heading_names), or None if not found."""
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("## ") and line[3:].strip().lower() in heading_names:
            i += 1
            content = []
            while i < len(lines) and not lines[i].startswith("## "):
                content.append(lines[i])
                i += 1
            return content
        i += 1
    return None


# --------------------------------------------------------------------------
# Style + geometry extraction from a docx template
# --------------------------------------------------------------------------

@dataclass
class StyleSpec:
    name: str
    size_pt: float
    bold: bool
    italic: bool
    space_before_pt: float
    space_after_pt: float
    line_multiple: float
    left_indent_pt: float


@dataclass
class PageGeometry:
    content_width_pt: float
    content_height_pt: float


def _resolve(style, getter):
    s, seen = style, set()
    while s is not None and id(s) not in seen:
        seen.add(id(s))
        val = getter(s)
        if val is not None:
            return val
        s = s.base_style
    return None


def extract_style_specs(document: Document, style_names: Dict[str, str]) -> Dict[str, StyleSpec]:
    specs = {}
    for key, docx_name in style_names.items():
        style = document.styles[docx_name]
        size = _resolve(style, lambda s: s.font.size)
        bold = _resolve(style, lambda s: s.font.bold)
        italic = _resolve(style, lambda s: s.font.italic)
        space_before = _resolve(style, lambda s: s.paragraph_format.space_before)
        space_after = _resolve(style, lambda s: s.paragraph_format.space_after)
        line_spacing = _resolve(style, lambda s: s.paragraph_format.line_spacing)
        left_indent = _resolve(style, lambda s: s.paragraph_format.left_indent)
        specs[key] = StyleSpec(
            name=docx_name,
            size_pt=(size.pt if size else 10.5),
            bold=bool(bold),
            italic=bool(italic),
            space_before_pt=(space_before.pt if space_before else 0.0),
            space_after_pt=(space_after.pt if space_after else 0.0),
            line_multiple=(line_spacing if isinstance(line_spacing, (int, float)) else 1.0),
            left_indent_pt=(left_indent.pt if left_indent else 0.0),
        )
    return specs


def extract_page_geometry(document: Document) -> PageGeometry:
    from docx.shared import Emu
    section = document.sections[0]
    width = Emu(section.page_width - section.left_margin - section.right_margin)
    height = Emu(section.page_height - section.top_margin - section.bottom_margin)
    return PageGeometry(content_width_pt=width.pt, content_height_pt=height.pt)


def _tightened(spec: StyleSpec, factor: float) -> StyleSpec:
    if factor == 1.0:
        return spec
    return dataclasses.replace(spec, space_after_pt=spec.space_after_pt * factor)


# --------------------------------------------------------------------------
# Height estimation
# --------------------------------------------------------------------------

def _wrapped_line_count(metrics: FontMetrics, spec: StyleSpec, text: str, width_pt: float) -> int:
    avail = max(width_pt - spec.left_indent_pt, 20.0)
    clean = strip_inline_markup(text)
    if not clean.strip():
        return 1
    return len(metrics.wrap_lines(clean, avail, spec.size_pt, spec.bold, spec.italic))


def block_height(metrics: FontMetrics, spec: StyleSpec, texts: List[str], width_pt: float) -> float:
    total_lines = sum(_wrapped_line_count(metrics, spec, t, width_pt) for t in texts) or 1
    line_height = metrics.natural_line_height_pt(spec.size_pt, spec.bold, spec.italic) * (spec.line_multiple or 1.0)
    return spec.space_before_pt + spec.space_after_pt + line_height * total_lines


# --------------------------------------------------------------------------
# Layout units: one source of truth for both height estimation and
# rendering, so a section that overflows a page is measured and emitted
# the same way. Each LayoutUnit is the smallest chunk of content that may
# ever be separated from its neighbors by a page break; a break may be
# placed immediately before any unit.
# --------------------------------------------------------------------------

@dataclass
class ParaSpec:
    style_key: str
    lines: List[str]
    bold: bool = False
    italic: bool = False


@dataclass
class LayoutUnit:
    section: str            # display heading this unit belongs to; "" = front matter (never continued)
    is_section_start: bool  # True for the unit carrying the section's own heading
    height_pt: float
    paragraphs: List[ParaSpec]
    force_break_before: bool = False  # start a new page here unless already at a page top


PAGE_SAFETY_MARGIN_PT = 4.0  # small buffer against estimate-vs-render rounding error


def para_height(metrics: FontMetrics, styles: Dict[str, StyleSpec], spec: ParaSpec,
                 width_pt: float, tighten_factor: float, tightenable_keys: frozenset) -> float:
    style = styles[spec.style_key]
    if spec.style_key in tightenable_keys:
        style = _tightened(style, tighten_factor)
    return block_height(metrics, style, spec.lines, width_pt)


def make_unit(metrics: FontMetrics, styles: Dict[str, StyleSpec], width_pt: float, tighten_factor: float,
              tightenable_keys: frozenset, section: str, is_section_start: bool,
              paragraphs: List[ParaSpec]) -> LayoutUnit:
    h = sum(para_height(metrics, styles, p, width_pt, tighten_factor, tightenable_keys) for p in paragraphs)
    return LayoutUnit(section=section, is_section_start=is_section_start, height_pt=h, paragraphs=paragraphs)


def grouped_units(heading: str, groups: List[Tuple[List[ParaSpec], List[ParaSpec]]],
                   metrics: FontMetrics, styles: Dict[str, StyleSpec], width_pt: float,
                   tighten_factor: float, tightenable_keys: frozenset,
                   heading_style_key: str = "heading1", include_heading: bool = True) -> List[LayoutUnit]:
    """groups: list of (starter, rest) where `starter` (e.g. a job's role+employer+first
    bullet, or a subheading+first bullet) is glued together and may only be preceded by a
    break; each item in `rest` is independently breakable."""
    units: List[LayoutUnit] = []
    heading_spec = ParaSpec(heading_style_key, [heading.upper()])
    first = True
    for starter, rest in groups:
        paras = ([heading_spec] if (first and include_heading) else []) + starter
        units.append(make_unit(metrics, styles, width_pt, tighten_factor, tightenable_keys, heading, first, paras))
        first = False
        for item in rest:
            units.append(make_unit(metrics, styles, width_pt, tighten_factor, tightenable_keys, heading, False, [item]))
    return units


# --------------------------------------------------------------------------
# Pagination: decide where forced breaks (and "(continued)" markers) go.
# The caller controls every page break itself, so the rendered page count
# is exactly what this plan predicts (mid-unit content never splits, since
# every LayoutUnit is by construction the smallest unsplittable chunk).
# --------------------------------------------------------------------------

@dataclass
class PaginationPlan:
    pages_used: int
    breaks_before: Dict[int, bool]
    continued_section: Dict[int, str]
    oversized_unit: Optional[int] = None


def continued_marker_spec(section: str, style_key: str = "body") -> ParaSpec:
    return ParaSpec(style_key, [f"{section} (continued)"], italic=True)


def simulate_pagination(units: List[LayoutUnit], page_height_pt: float, metrics: FontMetrics,
                         styles: Dict[str, StyleSpec], width_pt: float, tighten_factor: float,
                         tightenable_keys: frozenset, marker_style_key: str = "body") -> PaginationPlan:
    usable_height = page_height_pt - PAGE_SAFETY_MARGIN_PT
    breaks_before: Dict[int, bool] = {}
    continued_section: Dict[int, str] = {}
    pages_used = 1
    remaining = usable_height
    for i, unit in enumerate(units):
        if unit.height_pt > usable_height:
            return PaginationPlan(pages_used, breaks_before, continued_section, oversized_unit=i)
        marker_needed = i > 0 and bool(unit.section) and not unit.is_section_start
        overhead = (para_height(metrics, styles, continued_marker_spec(unit.section, marker_style_key),
                                 width_pt, tighten_factor, tightenable_keys)
                    if marker_needed else 0.0)
        forced = i > 0 and unit.force_break_before and remaining < usable_height
        if i > 0 and (forced or (unit.height_pt + overhead) > remaining):
            breaks_before[i] = True
            pages_used += 1
            remaining = usable_height
            if marker_needed:
                continued_section[i] = unit.section
                remaining -= overhead
        remaining -= unit.height_pt
    return PaginationPlan(pages_used=pages_used, breaks_before=breaks_before, continued_section=continued_section)


def describe_unit(unit: LayoutUnit, heading_style_key: str = "heading1") -> str:
    candidates = [" ".join(l for l in p.lines if l).strip()
                  for p in unit.paragraphs if p.style_key != heading_style_key]
    candidates = [c for c in candidates if c] or [
        " ".join(l for l in p.lines if l).strip() for p in unit.paragraphs
    ]
    if not candidates:
        return "(empty)"
    longest = max(candidates, key=len)
    return longest[:70] + ("…" if len(longest) > 70 else "")


# --------------------------------------------------------------------------
# DOCX rendering
# --------------------------------------------------------------------------

def clear_body(document: Document) -> None:
    body = document.element.body
    for child in list(body):
        if child.tag != qn("w:sectPr"):
            body.remove(child)


def add_inline_runs(paragraph, text: str) -> None:
    for seg_text, bold, italic in parse_inline_segments(text):
        if not seg_text:
            continue
        run = paragraph.add_run(seg_text)
        if bold:
            run.bold = True
        if italic:
            run.italic = True


def add_multiline_paragraph(document: Document, style_name: str, lines: List[str], tighten: float = 1.0):
    p = document.add_paragraph(style=style_name)
    if tighten != 1.0 and p.paragraph_format.space_after is not None:
        p.paragraph_format.space_after = Pt(p.paragraph_format.space_after.pt * tighten)
    for i, line in enumerate(lines):
        if i > 0:
            p.add_run().add_break()
        add_inline_runs(p, line)
    return p


def render_docx_from_plan(template_path: Path, output_path: Path, style_names: Dict[str, str],
                           units: List[LayoutUnit], plan: PaginationPlan,
                           core_properties: Tuple[str, str, str], tightenable_keys: frozenset,
                           tighten_factor: float = 1.0) -> None:
    document = Document(str(template_path))
    clear_body(document)

    title, subject, keywords = core_properties
    document.core_properties.title = title
    document.core_properties.subject = subject
    document.core_properties.keywords = keywords

    for i, unit in enumerate(units):
        pending_break = i in plan.breaks_before
        if pending_break and i in plan.continued_section:
            marker = continued_marker_spec(plan.continued_section[i])
            p = add_multiline_paragraph(document, style_names[marker.style_key], marker.lines, tighten=tighten_factor)
            for r in p.runs:
                r.italic = True
            p.paragraph_format.page_break_before = True
            pending_break = False
        for j, pspec in enumerate(unit.paragraphs):
            t = tighten_factor if pspec.style_key in tightenable_keys else 1.0
            p = add_multiline_paragraph(document, style_names[pspec.style_key], pspec.lines, tighten=t)
            if pspec.bold:
                for r in p.runs:
                    r.bold = True
            if pspec.italic:
                for r in p.runs:
                    r.italic = True
            if pending_break and j == 0:
                p.paragraph_format.page_break_before = True
                pending_break = False

    document.save(str(output_path))


# --------------------------------------------------------------------------
# Core document properties (Title/Subject/Keywords)
# --------------------------------------------------------------------------

CORE_PROPERTY_MAX_LEN = 255  # python-docx / OOXML core-property string limit


def dedupe_preserve_order(items: List[str]) -> List[str]:
    seen = set()
    out = []
    for item in items:
        item = item.strip()
        if item and item not in seen:
            seen.add(item)
            out.append(item)
    return out


def truncate_text(value: str, max_len: int = CORE_PROPERTY_MAX_LEN) -> str:
    if len(value) <= max_len:
        return value
    return value[: max_len - 1].rstrip() + "…"


def truncate_keyword_list(parts: List[str], max_len: int = CORE_PROPERTY_MAX_LEN) -> str:
    """Keep whole keyword phrases, dropping trailing ones rather than
    cutting the last one mid-word."""
    kept: List[str] = []
    total = 0
    for part in parts:
        addition = (", " if kept else "") + part
        if total + len(addition) > max_len:
            break
        kept.append(part)
        total += len(addition)
    return ", ".join(kept)


# --------------------------------------------------------------------------
# ATS keywords: extracted during /analyze-opportunity into analysis.md's
# '## ATS Keywords' section, consumed by generators to populate Keywords.
# --------------------------------------------------------------------------

ATS_KEYWORDS_HEADING_NAMES = {"ats keywords"}


def parse_ats_keywords(text: str) -> List[str]:
    content = extract_markdown_h2_section(text, ATS_KEYWORDS_HEADING_NAMES)
    if content is None:
        return []
    keywords = []
    for line in content:
        stripped = line.strip()
        if stripped.startswith(("- ", "* ")):
            keywords.append(strip_inline_markup(stripped[2:].strip()))
    return dedupe_preserve_order(keywords)


def load_ats_keywords(path: Path) -> List[str]:
    """path may be an analysis.md file directly, or an opportunity folder
    containing one. Raises DocGenError if explicitly pointed at something
    that doesn't resolve to a usable keyword list."""
    candidate = path / "analysis.md" if path.is_dir() else path
    if not candidate.exists():
        raise DocGenError(f"ATS keywords file not found: {candidate}")
    keywords = parse_ats_keywords(candidate.read_text(encoding="utf-8"))
    if not keywords:
        raise DocGenError(f"No '## ATS Keywords' bullet list found in {candidate}.")
    return keywords


_OPPORTUNITY_FOLDER_RE = re.compile(r"^(.+)_(\d{4}-\d{2}-\d{2})$")

# Generic editable sources inside opportunity folders.
GENERIC_RESUME_MARKDOWN_NAMES = frozenset({"resume.md"})
GENERIC_COVER_LETTER_MARKDOWN_NAMES = frozenset({"cover-letter.md"})


def parse_opportunity_folder_name(folder_name: str) -> Optional[Tuple[str, str]]:
    """Return (company_role_prefix, YYYY-MM-DD) when folder_name matches the
    promoted opportunity naming convention; otherwise None."""
    m = _OPPORTUNITY_FOLDER_RE.match(folder_name)
    if not m:
        return None
    return m.group(1), m.group(2)


def opportunity_folder_for_input(input_path: Path) -> Optional[Path]:
    """If input lives directly under a promoted opportunity folder, return that
    folder path; otherwise None."""
    parent = input_path.resolve().parent
    if not JOB_OPPORTUNITIES_DIR.is_dir():
        return None
    try:
        parent.relative_to(JOB_OPPORTUNITIES_DIR.resolve())
    except ValueError:
        return None
    if parent == JOB_OPPORTUNITIES_DIR.resolve():
        return None
    if parse_opportunity_folder_name(parent.name) is None:
        return None
    return parent


# --------------------------------------------------------------------------
# Shareable file names: <kind>_<INITIALS>-<terse company and role>-<YYYY-MM>
# --------------------------------------------------------------------------

# Words dropped from the terse slug (articles, prepositions, company suffixes).
SLUG_DROP_WORDS = frozenset({
    "a", "an", "and", "at", "for", "in", "of", "the", "to",
    "inc", "llc", "ltd", "corp", "co", "plc", "gmbh",
})

# Multi-word titles first (longest match wins), then single words. Only
# standard abbreviations belong here; extend the table, not the algorithm.
SLUG_PHRASE_ABBREVIATIONS = {
    ("chief", "executive", "officer"): "ceo",
    ("chief", "financial", "officer"): "cfo",
    ("chief", "information", "officer"): "cio",
    ("chief", "operating", "officer"): "coo",
    ("chief", "product", "officer"): "cpo",
    ("chief", "technology", "officer"): "cto",
    ("executive", "vice", "president"): "evp",
    ("senior", "vice", "president"): "svp",
    ("vice", "president"): "vp",
    ("information", "technology"): "it",
}
SLUG_WORD_ABBREVIATIONS = {
    "administration": "admin",
    "administrator": "admin",
    "assistant": "asst",
    "associate": "assoc",
    "development": "dev",
    "developer": "dev",
    "director": "dir",
    "engineer": "eng",
    "engineering": "eng",
    "junior": "jr",
    "management": "mgmt",
    "manager": "mgr",
    "operations": "ops",
    "senior": "sr",
    "software": "sw",
    "technical": "tech",
    "technology": "tech",
}
_NAME_SUFFIXES = frozenset({"jr", "sr", "ii", "iii", "iv", "phd", "md", "mba"})
SHAREABLE_PREFIXES = {"resume": "resume", "cover_letter": "cover-letter"}


def terse_slug(prefix: str) -> str:
    """Terse, hyphen-joined slug for an opportunity folder's `<company>_<role>`
    prefix: filler words dropped, standard abbreviations applied, lowercase.
    The role stays consistent with the folder name; only its wording shrinks."""
    words = [w for w in re.split(r"[_\-\s]+", prefix.lower()) if w]
    out: List[str] = []
    i = 0
    while i < len(words):
        for length in (3, 2):
            phrase = tuple(words[i:i + length])
            if len(phrase) == length and phrase in SLUG_PHRASE_ABBREVIATIONS:
                out.append(SLUG_PHRASE_ABBREVIATIONS[phrase])
                i += length
                break
        else:
            word = words[i]
            i += 1
            if word in SLUG_DROP_WORDS:
                continue
            out.append(SLUG_WORD_ABBREVIATIONS.get(word, word))
    return "-".join(out)


def owner_initials(markdown_path: Path) -> str:
    """Initials of whoever the document is written for: the first letters of
    the `# Full Name` heading (generational and degree suffixes ignored)."""
    for line in markdown_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            tokens = [t for t in line[2:].split()
                      if t.strip(".,").lower() not in _NAME_SUFFIXES]
            initials = "".join(t[0].upper() for t in tokens if t[0].isalpha())
            if initials:
                return initials
            break
    raise DocGenError(f"Could not read the owner's name (a '# Full Name' heading) from {markdown_path}.")


def shareable_stem(artifact_kind: str, initials: str, prefix: str, date: str) -> str:
    """`resume_JQP-acme-head-sw-dev-2026-10` (date is YYYY-MM-DD in, YYYY-MM out)."""
    return f"{SHAREABLE_PREFIXES[artifact_kind]}_{initials}-{terse_slug(prefix)}-{date[:7]}"


def default_shareable_output_path(input_path: Path, artifact_kind: str) -> Path:
    """Default DOCX path for an input markdown file.

    Opportunity-folder `resume.md` / `cover-letter.md` map to terse shareable
    names derived from the parent folder and the owner's initials:
      <company>_<role>_<date>/resume.md
        -> resume_<INITIALS>-<terse company and role>-<YYYY-MM>.docx
      <company>_<role>_<date>/cover-letter.md
        -> cover-letter_<INITIALS>-<terse company and role>-<YYYY-MM>.docx

    Non-opportunity inputs keep the historical default (same stem, .docx).
    """
    input_path = input_path.resolve()
    folder = opportunity_folder_for_input(input_path)
    if folder is not None:
        parsed = parse_opportunity_folder_name(folder.name)
        assert parsed is not None
        prefix, date = parsed
        name = input_path.name.lower()
        generic = {"resume": GENERIC_RESUME_MARKDOWN_NAMES,
                   "cover_letter": GENERIC_COVER_LETTER_MARKDOWN_NAMES}[artifact_kind]
        if name in generic:
            stem = shareable_stem(artifact_kind, owner_initials(input_path), prefix, date)
            return folder / f"{stem}.docx"
    return input_path.with_suffix(".docx")


def find_ats_keywords_source_for_prefix(prefix: str) -> Optional[Path]:
    if not JOB_OPPORTUNITIES_DIR.is_dir():
        return None
    pattern = re.compile(rf"^{re.escape(prefix)}_\d{{4}}-\d{{2}}-\d{{2}}$")
    matches = [d / "analysis.md" for d in JOB_OPPORTUNITIES_DIR.iterdir()
               if d.is_dir() and pattern.match(d.name) and (d / "analysis.md").exists()]
    return matches[0] if len(matches) == 1 else None


def find_ats_keywords_source(input_path: Path, filename_suffix_re: "re.Pattern") -> Optional[Path]:
    """Best-effort, unambiguous-only auto-detection.

    Prefer sibling `analysis.md` when the input lives in an opportunity
    folder (including generic `resume.md` / `cover-letter.md`). Otherwise
    match the input filename's naming convention (via filename_suffix_re,
    which must capture the '<company>_<role>' prefix in group 1) against
    '<company>_<role>_<date>' opportunity folders. Returns None (never
    raises) if there's no single unambiguous match — this is an
    enhancement, not a requirement."""
    folder = opportunity_folder_for_input(input_path)
    if folder is not None:
        sibling = folder / "analysis.md"
        if sibling.exists():
            return sibling
    m = filename_suffix_re.match(input_path.stem)
    if not m:
        return None
    return find_ats_keywords_source_for_prefix(m.group(1))


# --------------------------------------------------------------------------
# Render validation (LibreOffice ground truth)
# --------------------------------------------------------------------------

SOFFICE_SEARCH_PATHS = [
    "/Applications/LibreOffice.app/Contents/MacOS/soffice",  # macOS
    "/usr/bin/soffice",                                        # Linux (common)
    "/usr/local/bin/soffice",                                  # Linux/Homebrew-on-Linux
    "/opt/libreoffice/program/soffice",                        # Linux, vendor installers
    "C:\\Program Files\\LibreOffice\\program\\soffice.exe",    # Windows
]


def find_soffice_binary() -> str:
    env_bin = os.environ.get("RESUME_DOCX_SOFFICE_BIN")
    if env_bin:
        return env_bin
    for name in ("soffice", "libreoffice"):
        found = shutil.which(name)
        if found:
            return found
    for path in SOFFICE_SEARCH_PATHS:
        if Path(path).exists():
            return path
    searched = "\n  ".join(["(PATH)"] + SOFFICE_SEARCH_PATHS)
    raise RuntimeError(
        f"Could not find a LibreOffice ('soffice') executable. Searched:\n  {searched}\n"
        f"Install LibreOffice, set RESUME_DOCX_SOFFICE_BIN to its full path, or pass "
        f"--no-pdf to skip PDF conversion and page-count validation."
    )


def convert_to_pdf(docx_path: Path, out_dir: Path) -> Path:
    soffice_bin = find_soffice_binary()
    profile_dir = out_dir / "lo_profile"
    profile_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        soffice_bin, "--headless", "--norestore",
        f"-env:UserInstallation=file://{profile_dir}",
        "--convert-to", "pdf", "--outdir", str(out_dir), str(docx_path),
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except FileNotFoundError as e:
        raise RuntimeError(
            f"Could not run LibreOffice at {soffice_bin!r}. Install it, set "
            f"RESUME_DOCX_SOFFICE_BIN to its full path, or pass --no-pdf to skip "
            f"PDF conversion and page-count validation."
        ) from e
    if result.returncode != 0:
        raise RuntimeError(f"LibreOffice conversion failed: {result.stderr or result.stdout}")
    pdf_path = out_dir / (docx_path.stem + ".pdf")
    if not pdf_path.exists():
        detail = (result.stdout or result.stderr or "no output").strip()
        raise RuntimeError(
            f"LibreOffice did not produce a PDF at {pdf_path} (soffice said: {detail!r}). "
            f"This usually means the local LibreOffice install can't load any document "
            f"in headless mode (a container/sandbox issue, not a problem with this DOCX). "
            f"Pass --no-pdf to skip PDF conversion and page-count validation."
        )
    return pdf_path


def count_pdf_pages(pdf_path: Path) -> int:
    from pypdf import PdfReader
    return len(PdfReader(str(pdf_path)).pages)


def extract_pdf_text(pdf_path: Path) -> str:
    from pypdf import PdfReader
    reader = PdfReader(str(pdf_path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def verify_content(pdf_text: str, probes: List[Tuple[str, str]]) -> List[str]:
    """probes: list of (label, text) pairs to confirm appear in the
    rendered PDF. Returns human-readable warnings for any that don't —
    a soft check (font substitution/hyphenation can cause false positives),
    not a hard failure."""
    warnings: List[str] = []
    norm_pdf = re.sub(r"\s+", " ", pdf_text).lower()
    for label, text in probes:
        probe = re.sub(r"\s+", " ", strip_inline_markup(text)).strip().lower()[:40]
        if probe and probe not in norm_pdf:
            warnings.append(f"could not confirm {label} text in rendered PDF: {text[:70]!r}")
    return warnings
