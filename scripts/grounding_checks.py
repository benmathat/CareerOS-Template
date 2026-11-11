"""Claim-grounding checks for submitted documents (stdlib only).

`resume.md` and `cover-letter.md` in an opportunity folder are presentation. Their
factual claims must trace to canonical content in `Career/02_`–`05_`. The checks here
are deliberately mechanical, so they catch the failures a model can make silently:

  * employment spine: every `### Employer - Title` entry in a resume matches a canonical
    role (employer, exact title) and states that role's start and end dates
  * numbers: every metric (a `$`/`%`/`+`/K/M figure, or any number of 10 or more) in a resume or
    cover letter appears somewhere in canonical content, compared by value (90K == $90,000)
  * tenure: "N years" never exceeds the span from the earliest canonical role to today
  * credentials: every education and certification item in a resume (degree, institution,
    certification, issuer, years) is covered by a single canonical item under an
    `Education` / `Certifications` heading in 02_–05_ (skills-inventory.md today)

They prove a claim is not invented from nothing, not that it is attached to the right
fact: a number that exists elsewhere in canonical content still passes. Review the
rest. A claim that is true but not canonical belongs in canonical content first;
`grounding-waivers.md` in the opportunity folder is the visible, reasoned exception.
Waiver lines read `- <claim as written> — <reason>` (an em or en dash, so claims may contain hyphens); a waiver with no reason is ignored.
"""

from __future__ import annotations

import re
from pathlib import Path

CANON_DIRS = ("02_Work_Experience", "03_Skills_and_Portfolio", "04_Career_Goals_and_Strategy", "05_Personal_Profile")
WAIVER_FILE = "grounding-waivers.md"
FM = re.compile(r"\A---\n.*?\n---\n", re.S)
NUM = re.compile(r"(?<![\w.#/-])(\$?)(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)\s?([KkMm](?![A-Za-z]))?(\+|%)?")
MONTHS = {m: i + 1 for i, m in enumerate("jan feb mar apr may jun jul aug sep oct nov dec".split())}
DATE_RANGE = re.compile(r"(?:(?P<sm>[A-Za-z]{3})[a-z]*\.?\s+(?:\d{1,2},\s*)?)?(?P<sy>\d{4})\s*[–—-]\s*"
                        r"(?:(?:(?P<em>[A-Za-z]{3})[a-z]*\.?\s+(?:\d{1,2},\s*)?)?(?P<ey>\d{4})|(?P<pres>Present))")
SUFFIXES = {"inc", "llc", "ltd", "corp", "co", "company", "group", "the"}
SKIP_LINE = re.compile(r"@|^\d{4}-\d{2}-\d{2}$|\b(requisition|req|job id|posting id|ref(erence)?)\b|\d{3}[-. ]\d{3}[-. ]\d{4}", re.I)
CRED_HEADING = re.compile(r"^(education|certifications?|credentials|licen[cs]es)$", re.I)
RESUME_CRED_SECTION = re.compile(
    r"^(education|professional development|certifications?|credentials|education\s*(?:and|&)\s*certifications?)$", re.I)
GENERIC_SUB = re.compile(r"^(education|certifications?|credentials)$", re.I)
CRED_ABBREV = (
    (r"\bb\.?\s?s\.?(?=\W|$)", "bachelor science"), (r"\bb\.?\s?a\.?(?=\W|$)", "bachelor arts"),
    (r"\bm\.?\s?s\.?(?=\W|$)", "master science"), (r"\bm\.?\s?a\.?(?=\W|$)", "master arts"),
    (r"\bmba\b", "master business administration"), (r"\bph\.?d\.?", "doctor philosophy"),
)
CRED_STOP = {"in", "of", "and", "the", "a", "at", "from", "for"}
YEARS = re.compile(r"\b(\d+)\+?\s+years?\b", re.I)


def _body(text: str) -> str:
    return FM.sub("", text, count=1)


def numbers(text: str) -> list[tuple[float, str, bool]]:
    """(value, as written, has a $/K/M/+/% marker) for each figure; years (1900-2100) are skipped."""
    out = []
    for m in NUM.finditer(text):
        dollar, n, suf, mark = m.groups()
        v = float(n.replace(",", ""))
        if suf:
            v *= 1000 if suf in "Kk" else 1_000_000
        if 1900 <= v <= 2100 and not (dollar or suf or mark):
            continue
        out.append((v, m.group(0).strip(), bool(dollar or suf or mark)))
    return out


def canonical_numbers(root: Path) -> set[float]:
    found: set[float] = set()
    for d in CANON_DIRS:
        for f in (root / "Career" / d).rglob("*.md"):
            found.update(v for v, _, _ in numbers(_body(f.read_text())))
    return found


def _norm_company(name: str) -> str:
    words = [w for w in re.sub(r"\(.*?\)", " ", name.lower()).replace("&", " and ").replace(".", "").split()
             if re.sub(r"\W", "", w) not in SUFFIXES]
    return re.sub(r"\W", "", words[0]) if words else ""


def _norm_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", title.lower().replace("&", " and ")).strip()


def _span(m: re.Match) -> tuple[tuple[int, int | None], tuple[int, int | None] | None]:
    """((year, month|None), end|None for Present)."""
    mo = lambda s: MONTHS.get((s or "")[:3].lower())
    start = (int(m.group("sy")), mo(m.group("sm")))
    end = None if m.group("pres") else (int(m.group("ey")), mo(m.group("em")))
    return start, end


def canonical_roles(root: Path) -> list[dict]:
    roles = []
    for f in sorted((root / "Career/02_Work_Experience/Roles").glob("*.md")):
        text = f.read_text()
        field = lambda k: (re.search(rf"^- \*\*{k}:\*\*\s*(.+)$", text, re.M) or [None, ""])[1].strip()
        company, title, frame = field("Company"), field("Title"), field("Timeframe")
        dm = DATE_RANGE.search(frame)
        if company and title and dm:
            start, end = _span(dm)
            roles.append({"company": _norm_company(company), "title": _norm_title(title), "start": start,
                          "end": end, "label": f"{company} - {title}", "file": f.name})
            # `## Positions` lists sub-positions at one employer: `- **Title:** Mon YYYY – Mon YYYY`
            pos = re.search(r"^## Positions\n(.*?)(?=^## |\Z)", text, re.M | re.S)
            for pm in re.finditer(r"^- \*\*(.+?):\*\*\s*(.+)$", pos.group(1) if pos else "", re.M):
                pd = DATE_RANGE.search(pm.group(2))
                if pd:
                    ps, pe = _span(pd)
                    roles.append({"company": _norm_company(company), "title": _norm_title(pm.group(1)),
                                  "start": ps, "end": pe, "label": f"{company} - {pm.group(1).strip()}",
                                  "file": f.name})
    return roles


def _same(a, b) -> bool:
    """Compare (year, month) tuples; a missing month on either side compares by year only."""
    if a is None or b is None:
        return a is b
    return a[0] == b[0] and (a[1] is None or b[1] is None or a[1] == b[1])


def _fmt(p) -> str:
    return "Present" if p is None else (f"{p[0]}" if p[1] is None else f"{list(MONTHS)[p[1] - 1].title()} {p[0]}")


def employment_problems(rel: str, text: str, roles: list[dict]) -> list[str]:
    sec = re.search(r"^## (?:Professional |Work )?Experience\n(.*?)(?=^## |\Z)", _body(text), re.M | re.S)
    if not sec:
        return []
    p = []
    for em in re.finditer(r"^### (.+?)\n+(.*?)(?=^### |\Z)", sec.group(1), re.M | re.S):
        heading, block = em.group(1).strip(), em.group(2)
        parts = re.split(r"\s+[-–—]\s+", heading, maxsplit=1)
        if len(parts) != 2 or parts[0].strip().lower() == "earlier career":
            continue  # an aggregate "Earlier Career - ..." entry lists its own employers inline
        company, title = _norm_company(parts[0]), _norm_title(parts[1])
        same_company = [r for r in roles if r["company"] == company]
        candidates = [r for r in same_company if r["title"] == title]
        match = candidates[0] if candidates else None
        if not match:
            known = "; ".join(r["label"] for r in same_company) or "no role at that employer"
            p.append(f"{rel}: '{heading}' matches no canonical role ({known})")
            continue
        dm = DATE_RANGE.search(block.split("\n- ", 1)[0])
        if not dm:
            p.append(f"{rel}: '{heading}' has no parseable dates")
            continue
        start, end = _span(dm)
        hit = next((r for r in candidates if _same(start, r["start"]) and _same(end, r["end"])), None)
        if not hit:
            p.append(f"{rel}: '{heading}' dates {_fmt(start)} – {_fmt(end)} differ from canonical "
                     f"{_fmt(match['start'])} – {_fmt(match['end'])} ({match['file']})")
    return p


def waivers(folder: Path) -> set[str]:
    f = folder / WAIVER_FILE
    if not f.is_file():
        return set()
    out = set()
    for line in f.read_text().splitlines():
        m = re.match(r"^- (.+?)\s+[—–]\s+\S", line)
        if m:
            out.add(m.group(1).strip().strip("`"))
    return out


def number_problems(rel: str, text: str, canon: set[float], waived: set[str]) -> list[str]:
    body = _body(text).split("\n## Assumptions")[0]
    body = "\n".join(l for l in body.splitlines() if not SKIP_LINE.search(l.strip()))
    body = re.sub(r"\]\(.*?\)", "]", body)  # link targets
    body = YEARS.sub("", body)  # tenure is checked against role dates instead, see tenure_problems
    p = []
    for v, written, marked in numbers(body):
        if (marked or v >= 10) and v not in canon and written not in waived:
            p.append(f"{rel}: figure '{written}' not found in canonical content (02_–05_)")
    return p


def tenure_problems(rel: str, text: str, roles: list[dict], today_year: int) -> list[str]:
    if not roles:
        return []
    span = today_year - min(r["start"][0] for r in roles)
    body = _body(text).split("\n## Assumptions")[0]
    return [f"{rel}: '{m.group(0)}' exceeds the {span} years since the earliest canonical role"
            for m in YEARS.finditer(body) if int(m.group(1)) > span]


def cred_tokens(text: str) -> frozenset[str]:
    t = re.sub(r"[*_`]", "", text.lower()).replace("&", " and ")
    for pat, full in CRED_ABBREV:
        t = re.sub(pat, full, t)
    return frozenset(w for w in re.findall(r"[a-z0-9]+", t) if w not in CRED_STOP)


def _sections(text: str):
    """(level, heading, body lines) for each markdown heading."""
    out, cur = [], None
    for line in text.splitlines():
        m = re.match(r"^(#{1,6})\s+(.*?)\s*#*$", line)
        if m:
            cur = (len(m.group(1)), m.group(2).strip(), [])
            out.append(cur)
        elif cur is not None:
            cur[2].append(line)
    return out


def canonical_credentials(root: Path) -> list[frozenset[str]]:
    """One token set per non-empty line under an Education / Certifications / Credentials heading."""
    found: list[frozenset[str]] = []
    for d in CANON_DIRS:
        for f in (root / "Career" / d).rglob("*.md"):
            secs = _sections(_body(f.read_text()))
            for i, (level, head, lines) in enumerate(secs):
                if not CRED_HEADING.match(head):
                    continue
                body = list(lines)
                for lv, _, ln in secs[i + 1:]:  # include deeper subsections
                    if lv <= level:
                        break
                    body += ln
                found += [t for t in (cred_tokens(re.sub(r"^\s*[-*|]\s*", "", l)) for l in body) if t]
    return found


def resume_credentials(text: str) -> list[str]:
    """Education / certification items claimed in a resume, one string per item."""
    items: list[str] = []
    secs = _sections(_body(text))
    for i, (level, head, lines) in enumerate(secs):
        if level != 2 or not RESUME_CRED_SECTION.match(re.sub(r"\s+", " ", head)):
            continue
        blocks, cur = [], None  # (heading|None, lines); a block under ### is one item
        for lv, h, ln in secs[i + 1:]:
            if lv <= 2:
                break
            if lv == 3 and not GENERIC_SUB.match(h):
                blocks.append((h, ln))
            elif lv == 3:
                lines = lines + ln
        for h, ln in blocks:
            items.append(" ".join([h] + [l for l in ln if l.strip()]))
        for l in lines:
            l = re.sub(r"^\s*[-*]\s*", "", l).strip()
            for x in re.split(r"[;·]", l):
                x = re.sub(r"^\**(education|certifications?):\**\s*", "", x.strip(), flags=re.I).strip()
                if x:
                    items.append(x)
    return items


def credential_problems(rel: str, text: str, canon: list[frozenset[str]], waived: set[str]) -> list[str]:
    p = []
    for item in resume_credentials(text):
        toks = cred_tokens(item)
        if toks and not any(toks <= c for c in canon) and item not in waived and item.replace("*", "") not in waived:
            p.append(f"{rel}: education/certification '{re.sub(r'[*_]', '', item)[:90]}' "
                     "is not covered by one canonical Education/Certifications item (02_–05_)")
    return p


def is_resume_name(name: str) -> bool:
    """resume.md and labeled variants such as resume-3page.md."""
    return re.fullmatch(r"resume(-[a-z0-9-]+)?\.md", name) is not None


def grounding_problems(root: Path, folder: Path, rel: str, today_year: int) -> list[str]:
    docs = sorted(f.name for f in folder.glob("resume*.md") if is_resume_name(f.name))
    docs += [n for n in ("cover-letter.md",) if (folder / n).is_file()]
    if not docs:
        return []
    roles, canon, waived = canonical_roles(root), canonical_numbers(root), waivers(folder)
    creds = canonical_credentials(root) if any(is_resume_name(n) for n in docs) else []
    out: list[str] = []
    for name in docs:
        text = (folder / name).read_text()
        out += number_problems(f"{rel}/{name}", text, canon, waived)
        out += tenure_problems(f"{rel}/{name}", text, roles, today_year)
        if is_resume_name(name):
            out += credential_problems(f"{rel}/{name}", text, creds, waived)
            out += [x for x in employment_problems(f"{rel}/{name}", text, roles)
                    if not any(f"'{w}'" in x for w in waived)]
    return out
