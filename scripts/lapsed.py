"""Report applications with no activity for a while (stdlib only, read-only).

"Lapsed" is a derived view, not a tracker status: an in-flight application whose most recent
dated activity is at least N days old. The user decides whether to close it, using
`careeros close <folder> --outcome no_response --reason "..."`.

    careeros lapsed [--days 30] [--all]

Last activity is the latest of: the application record's submission_date, work search log
entries linked to the opportunity folder, and entry-marker dates in the tracker row's Last Action (`**YYYY-MM-DD:**`, not dates
mentioned in prose).
Dates in the future are ignored. A later reply or a new log entry resets the clock.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path

IN_FLIGHT = {"applied", "recruiter screen", "hiring manager", "panel / onsite", "final", "on hold"}
ISO = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")
ENTRY = re.compile(r"(?:^|\*\*)(\d{4}-\d{2}-\d{2}):")  # an entry marker, not a date mentioned in prose
FOLDER = re.compile(r"\b([a-z0-9]+(?:_[a-z0-9]+)*_\d{4}-\d{2}-\d{2})\b")


def _dates(text: str, today: dt.date) -> list[dt.date]:
    out = []
    for s in ISO.findall(text):
        try:
            d = dt.date.fromisoformat(s)
        except ValueError:
            continue
        if d <= today:
            out.append(d)
    return out


def tracker_rows(text: str) -> list[list[str]]:
    a, b = text.find("## Active Applications"), text.find("## Follow-Ups Due")
    rows = []
    for line in text[a:b].splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.startswith("|") and len(cells) >= 10 and re.match(r"[A-Z0-9]+-", cells[0]):
            rows.append(cells)
    return rows


def log_dates(log: str, folder: str, today: dt.date) -> list[dt.date]:
    out = []
    for block in re.findall(r"```yaml\n(.*?)```", log, re.S):
        if f"/{folder}/" in block:
            m = re.search(r"^activity_date:\s*(\d{4}-\d{2}-\d{2})", block, re.M)
            if m:
                out += _dates(m.group(1), today)
    return out


def find(root: Path, opps: str, tracker: str, log_path: str, today: dt.date) -> list[dict]:
    rows = tracker_rows((root / tracker).read_text())
    log = (root / log_path).read_text() if (root / log_path).is_file() else ""
    result = []
    for c in rows:
        if c[6].lower() not in IN_FLIGHT:
            continue
        folders = [f for f in FOLDER.findall(" ".join(c)) if (root / opps / f).is_dir()]
        folder = folders[0] if folders else None
        ds = _dates(" ".join(ENTRY.findall(c[7])), today)
        if folder:
            rec = root / opps / folder / "application-record.md"
            if rec.is_file():
                m = re.search(r"^submission_date:\s*(\d{4}-\d{2}-\d{2})", rec.read_text(), re.M)
                if m:
                    ds += _dates(m.group(1), today)
            ds += log_dates(log, folder, today)
        last = max(ds) if ds else None
        result.append({"id": c[0], "company": c[1], "role": c[2], "status": c[6],
                       "folder": folder, "last": last,
                       "days": (today - last).days if last else None})
    return result


def run(root: Path, opps: str, tracker: str, log_path: str, args: list[str],
        today: dt.date | None = None) -> int:
    ap = argparse.ArgumentParser(prog="careeros lapsed")
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--all", action="store_true", help="show every in-flight application")
    a = ap.parse_args(args)
    today = today or dt.date.today()
    rows = find(root, opps, tracker, log_path, today)
    lapsed = [r for r in rows if r["days"] is not None and r["days"] >= a.days]
    unknown = [r for r in rows if r["days"] is None]
    shown = rows if a.all else lapsed
    shown = sorted(shown, key=lambda r: -(r["days"] if r["days"] is not None else -1))
    print(f"{len(rows)} in-flight, {len(lapsed)} with no activity for {a.days}+ days "
          f"(as of {today}); read-only, nothing changed.")
    for r in shown:
        age = f"{r['days']}d" if r["days"] is not None else "no date"
        close = (f"careeros close Career/06_Job_Opportunities/{r['folder']} --outcome no_response "
                 f"--reason \"<your words>\"") if r["folder"] else "(no folder match)"
        print(f"- {r['id']}  {r['company']} — {r['role']}  [{r['status']}, last activity "
              f"{r['last'] or 'unknown'}, {age}]\n    {close}")
    if unknown and not a.all:
        print(f"{len(unknown)} in-flight row(s) have no dated activity; see --all.")
    return 0
