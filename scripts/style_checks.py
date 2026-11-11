"""Prose-style warnings for resumes and cover letters (stdlib only).

Mechanical half of Career/05_Personal_Profile/writing-style.md. These checks are
WARNINGS: `careeros check` prints them and still passes, and `careeros lint <file>`
always exits 0. They catch the patterns a human editor removed from Claude drafts
(spoken-word affect, aphorisms, colon-stacked bullets, ambiguous or abbreviated
figures, self-reference in a resume, leaked working notes). Judgment rules stay in
the style guide and the fresh-context critique pass.

To add a rule for a recurring fix, extend PHRASES or add a function and register it
in `style_warnings`; add a case to scripts/test_style_checks.py.
"""

from __future__ import annotations

import re
from pathlib import Path

FM = re.compile(r"\A---\n.*?\n---\n", re.S)
BULLET = re.compile(r"^\s*[-*]\s+(?:\*\*(?P<label>[^*]+?):\*\*\s*)?(?P<body>.*\S)\s*$")
CONTRACTION = re.compile(r"\b[A-Za-z]+(?:n't|'(?:d|m|ll|re|ve))\b", re.I)
PRONOUN = re.compile(r"\b(he|his|him|himself|she|her|hers|herself)\b", re.I)
OWN = re.compile(r"\b(my|his|her|their)\s+own\b", re.I)
ABBREV_MONEY = re.compile(r"\$\d[\d.,]*\s?[KkMmBb]\b")
PROJECTED_MONEY = re.compile(r"\b(projected|estimated|forecast(?:ed)?)\s+\$", re.I)
LEAK = re.compile(
    r"\b(not yet established|not established|no (?:customer )?adoption|to be confirmed)\b", re.I)
SENTENCE_LIMIT = 45  # words, cover letter

# (regex, message). Applies to resume and cover letter; extend as fixes recur.
PHRASES = (
    (re.compile(r"\bactually\b", re.I), "filler intensifier 'actually'"),
    (re.compile(r"\bnobody\b", re.I), "colloquial 'nobody'; name who or what"),
    (re.compile(r"\bwalked into\b", re.I), "idiom 'walked into'; use a plain verb"),
    (re.compile(r"\bkill decision\b", re.I), "insider jargon 'kill decision'; say 'decision to eliminate'"),
    (re.compile(r"\bceas(?:e|ed|ing)\b", re.I), "stiff verb 'cease'; prefer 'end' or 'stop'"),
    (re.compile(r"\bI'd rather\b", re.I), "conversational 'I'd rather'"),
    (re.compile(r"\b(?:the )?(?:harder|hardest|real|key) (?:part|thing|question)\b", re.I),
     "aphorism opener ('the harder part…'); state the point plainly"),
    (re.compile(r"\bearned alignment\b", re.I), "slogan phrasing 'earned alignment'"),
    (re.compile(r"\bit asks for\b|\bthe role asks for\b", re.I),
     "personified posting ('asks for'); say 'centers on' or 'requires'"),
    (re.compile(r"\bI (?:will|do|can|would) not (?:claim|pretend)\b|\bI (?:lack|have not worked in|have no (?:direct )?experience)\b|\bI am not (?:an? )?(?:expert|specialist)\b", re.I),
     "volunteers a gap; leave it unclaimed and record it in application-notes.md (writing-style rule 14)"),
)


# Where submitted-material drafts live. The automatic check ignores everything else, so prompt-library
# files such as Packs/resume-pack.md (which match the resume-<label>.md name) are never linted.
SCOPES = ("Career/06_Job_Opportunities/", "Career/99_Archive/Closed_Searches/", "Career/01_Resume_and_Profiles/")
SKIP = ("Career/01_Resume_and_Profiles/Templates/",)


def doc_kind(name: str) -> str | None:
    """'letter' for cover-letter.md, 'resume' for resume.md and resume-<label>.md."""
    if name == "cover-letter.md":
        return "letter"
    if re.fullmatch(r"resume(-[a-z0-9-]+)?\.md", name):
        return "resume"
    return None


LIST_SECTIONS = re.compile(r"skill|competenc|keyword|education|certif|credential|development|training|tools|technolog", re.I)


def _lines(text: str) -> list[tuple[int, str, str]]:
    """(1-based line number, text, current ## section) for body lines, skipping frontmatter, headings and rules."""
    offset = 0
    m = FM.match(text)
    if m:
        offset = text[: m.end()].count("\n")
        text = text[m.end():]
    out, section = [], ""
    for i, line in enumerate(text.split("\n"), start=1 + offset):
        s = line.strip()
        if re.match(r"##\s", s):
            section = s.lstrip("#").strip()
        if not s or s.startswith("#") or re.fullmatch(r"[-*_]{3,}", s) or s.startswith("|"):
            continue
        out.append((i, line, section))
    return out


def _sentences(line: str) -> list[str]:
    return [s for s in re.split(r"(?<=[.!?])\s+", line.strip()) if s]


def style_warnings(rel: str, text: str, kind: str) -> list[str]:
    """Warnings for one document; `kind` is 'resume' or 'letter'. Never raises on odd input."""
    out: list[str] = []
    for n, line, section in _lines(text):
        listy = bool(LIST_SECTIONS.search(section))  # skills and credential lists legitimately use colons and semicolons
        where = f"{rel}:{n}"
        plain = re.sub(r"\*\*|__|\[([^\]]*)\]\([^)]*\)", lambda m: m.group(1) or "", line)
        plain = plain.replace("’", "'")
        # Contact line (phone, email, URL) is not prose.
        if "@" in plain or "linkedin.com" in plain:
            continue
        for m in CONTRACTION.finditer(plain):
            out.append(f"{where}: contraction '{m.group(0)}'; use the full form")
        for rx, msg in PHRASES:
            if rx.search(plain):
                out.append(f"{where}: {msg}")
        for m in PROJECTED_MONEY.finditer(plain):
            out.append(f"{where}: figure after '{m.group(1)}' does not say what it measures (cost, revenue, savings)")
        if LEAK.search(plain):
            out.append(f"{where}: reads like working notes ('{LEAK.search(plain).group(0)}'); "
                       "write the limit as a full clause or leave the outcome unclaimed, and record gaps in application-notes.md")

        if kind == "resume":
            for m in PRONOUN.finditer(plain):
                out.append(f"{where}: pronoun '{m.group(0)}' in a resume; drop it")
            for m in OWN.finditer(plain):
                out.append(f"{where}: '{m.group(0)}' adds nothing in a resume")
            b = BULLET.match(line)
            if b and not listy:
                body = re.sub(r"\*\*", "", b.group("body"))
                body = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", body)  # a URL's colon is not prose
                if ":" in body:
                    out.append(f"{where}: colon inside a bullet body; split into verb-led sentences")
                if body.count(";") >= 2:
                    out.append(f"{where}: two or more semicolons in one bullet; split into sentences")
        else:
            for m in ABBREV_MONEY.finditer(plain):
                out.append(f"{where}: '{m.group(0)}' abbreviated in a letter; spell it out ($1.5 million)")
            for m in OWN.finditer(plain):
                out.append(f"{where}: '{m.group(0)}' adds nothing; drop 'own'")
            for s in _sentences(plain):
                words = len(s.split())
                if words > SENTENCE_LIMIT:
                    out.append(f"{where}: sentence of {words} words; split it")
                elif ":" in s and words > 30:
                    out.append(f"{where}: long sentence built on a colon ({words} words); use verb-led sentences")
    return list(dict.fromkeys(out))


def file_warnings(root: Path, rel: str, text: str | None = None) -> list[str]:
    """Warnings for a repo-relative path; [] when it is not a resume or cover letter."""
    kind = doc_kind(Path(rel).name)
    if kind is None or not rel.startswith(SCOPES) or rel.startswith(SKIP):
        return []
    if text is None:
        try:
            text = (root / rel).read_text()
        except OSError:
            return []
    return style_warnings(rel, text, kind)
