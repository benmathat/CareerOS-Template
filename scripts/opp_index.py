"""Generated index of opportunity folders, grouped by career track (stdlib only).

The index is a *view* over each folder's job-opportunity.md frontmatter. Nothing is moved,
so folder paths, run files and links stay stable when a track assignment changes.

    careeros index            print the index
    careeros index --write    refresh the generated block in 06_Job_Opportunities/README.md
    careeros index --check    exit 1 if that block is stale
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

BEGIN = "<!-- BEGIN GENERATED: opportunity-index (careeros index --write) -->"
END = "<!-- END GENERATED: opportunity-index -->"
TRACKS_FILE = "Career/04_Career_Goals_and_Strategy/career-tracks.md"
ARTIFACTS = [("analysis.md", "analysis"), ("resume.md", "resume"),
             ("cover-letter.md", "cover letter"), ("application-record.md", "applied")]
# Display order follows the confirmed employment sourcing priority; ids never imply rank in data.
TRACK_ORDER = ["track-2", "track-4", "track-5", "track-3", "track-9", "track-1"]
FM_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)
LABEL_RE = re.compile(r"^\|\s*`(track-\d+)`\s*\|\s*([^|]+?)\s*\|", re.M)


def _fm(text: str) -> dict[str, str]:
    m = FM_RE.match(text)
    out: dict[str, str] = {}
    for line in (m.group(1).splitlines() if m else []):
        k, sep, v = line.partition(":")
        if sep and k.strip() and not line.startswith((" ", "\t")):
            out[k.strip()] = v.strip().strip("\"'")
    return out


def track_labels(root: Path) -> dict[str, str]:
    labels: dict[str, str] = {}
    for tid, label in LABEL_RE.findall((root / TRACKS_FILE).read_text()):
        labels.setdefault(tid, label)  # first table is canonical; later tables repeat ids
    return labels


def collect(root: Path, opps_dir: str) -> list[dict]:
    rows = []
    for d in sorted((root / opps_dir).iterdir()):
        f = d / "job-opportunity.md"
        if not f.is_file():
            continue
        fm = _fm(f.read_text())
        rows.append({
            "folder": d.name,
            "company": fm.get("company", "MISSING"),
            "role": fm.get("role", "MISSING"),
            "status": fm.get("status", "MISSING"),
            "added": fm.get("date_added", "MISSING"),
            "track": fm.get("track", "MISSING"),
            "have": [label for name, label in ARTIFACTS if (d / name).is_file()],
        })
    return rows


def _cell(s: str) -> str:
    return s.replace("|", "\\|")


def render(root: Path, opps_dir: str) -> str:
    labels = track_labels(root)
    rows = collect(root, opps_dir)
    groups: dict[str, list[dict]] = {}
    for r in rows:
        groups.setdefault(r["track"] if r["track"] in labels else "MISSING", []).append(r)
    known = [t for t in TRACK_ORDER if t in groups]
    known += sorted(t for t in groups if t not in known and t != "MISSING")
    if "MISSING" in groups:
        known.append("MISSING")
    lines = [f"_{len(rows)} open opportunities. Generated from each `job-opportunity.md`; "
             "edit the folder's record, not this block. Group order follows the sourcing "
             "priority in `career-tracks.md` and is not a ranking of individual roles._", ""]
    for t in known:
        title = labels.get(t, "Unrouted (track missing or unrecognized)")
        lines += [f"### {title} ({len(groups[t])})", "",
                  "| Company | Role | Status | Added | Materials |", "|---|---|---|---|---|"]
        for r in sorted(groups[t], key=lambda r: r["added"], reverse=True):
            lines.append(f"| [{_cell(r['company'])}]({r['folder']}/job-opportunity.md) | "
                         f"{_cell(r['role'])} | {r['status']} | {r['added']} | "
                         f"{', '.join(r['have']) or '—'} |")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def block(root: Path, opps_dir: str) -> str:
    return f"{BEGIN}\n\n## Index by Career Track\n\n{render(root, opps_dir)}\n{END}"


def update_readme(readme: str, new_block: str) -> str:
    if BEGIN in readme and END in readme:
        head, _, rest = readme.partition(BEGIN)
        _, _, tail = rest.partition(END)
        return head + new_block + tail
    return readme.rstrip() + "\n\n" + new_block + "\n"


def run(root: Path, opps_dir: str, args: list[str]) -> int:
    readme = root / opps_dir / "README.md"
    new_block = block(root, opps_dir)
    if "--write" in args or "--check" in args:
        current = readme.read_text()
        updated = update_readme(current, new_block)
        if "--check" in args:
            if updated != current:
                print(f"stale: {opps_dir}/README.md (run: scripts/careeros index --write)", file=sys.stderr)
                return 1
            print("opportunity index is current")
            return 0
        if updated != current:
            readme.write_text(updated)
            print(f"updated {opps_dir}/README.md")
        else:
            print("opportunity index already current")
        return 0
    print(new_block)
    return 0
