"""Repo-state checks for `careeros check` (stdlib only).

The runtime IO gate validates a YAML the model wrote about itself. These checks
look at the files the run actually produced and fail on contract violations the
command contracts already state in prose:

  * opportunity records: required metadata and sections, valid track, source file present
  * analyses: required sections, parseable track and recommendation, track agrees with the record
  * lifecycle: an artifact may not exist without the stage that must precede it
  * discussions: discussion.md (from /discuss-opportunity) has its sections, a valid claim ledger,
    and cannot be closed while a blocking dispute or an unresolved canonical proposal remains
  * deliverables: no MISSING/TODO/TBD left in a resume or in a generated DOCX
  * work log: every entry has the required fields, unique ids, existing evidence paths
  * work log is append-only: an existing entry may not be edited or removed
  * provenance: a standard artifact newly added to an opportunity folder must come with a
    run file for a command allowed to create it (catches /intake-job overreaching into 06_)

Record, analysis and lifecycle rules apply only to opportunities added on or after
CONTRACT_SINCE (the day tracks and the intake pipeline landed). Older folders predate
the contract and fail it by design; they are not rewritten to satisfy it.
"""

from __future__ import annotations

import re
import zipfile
from pathlib import Path

CONTRACT_SINCE = "2026-10-06"
# From this date a resume or cover letter needs a closed discussion.md (see /discuss-opportunity).
DISCUSSION_SINCE = "2026-11-03"
VALID_TRACKS = {"track-2", "track-3", "track-4", "track-5", "track-9", "MISSING"}
QUALIFYING_VALUES = {"true", "false", "needs_review"}
# Entries written before the field was made agency-neutral use the legacy name.
QUALIFYING_FIELDS = ("qualifying", "twc_qualifying")

OPP_DIR_RE = re.compile(
    r"^Career/(06_Job_Opportunities|99_Archive/Closed_Searches)/([a-z0-9]+(?:_[a-z0-9]+)*_(\d{4}-\d{2}-\d{2}))(?:/(.*))?$"
)
FM_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)
UNRESOLVED_RE = re.compile(r"\b(MISSING|TODO|TBD|FIXME)\b")

ANALYSIS_SECTIONS = [
    "Summary", "Track", "ATS Keywords", "Role Fit", "Career Alignment", "Compensation",
    "Company Context", "Risks", "Opportunity Value", "Scoring", "Overall Assessment", "Recommendation",
]
DISCUSSION_SECTIONS = [
    "User Position", "Claim Ledger", "Reconciliations", "Canonical Proposals",
    "Keyword Map Deltas", "Resume and Cover Letter Strategy", "Open Items",
]
LEDGER_VERDICTS = {"supported", "partial", "gap", "contradicted", "new-evidence"}
LEDGER_DISPOSITIONS = {"agreed", "evidence-supplied", "reframed", "accepted-risk", "open"}
PROPOSAL_STATUSES = {"proposed", "applied", "declined", "deferred"}
LOG_FIELDS = [
    "activity_id", "activity_type", "activity_date", "employer_or_platform",
    "role_or_subject", "method", "outcome_status", "evidence", "related_opportunity",
    "related_application", "retrospective", "notes",
]
ENTRY_RE = re.compile(r"^## (\d{4}-\d{2}-\d{2}) — .+?\n.*?(?=^## |^### |\Z)", re.M | re.S)

# Which commands may create each standard artifact in an opportunity folder.
MAY_CREATE = {
    "job-opportunity.md": {"promote-opportunity"},
    "source-posting.pdf": {"promote-opportunity"},
    "analysis.md": {"analyze-opportunity"},
    "discussion.md": {"discuss-opportunity"},
    "resume.md": {"build-resume", "build-application"},
    "application-notes.md": {"build-resume", "build-application", "log-activity", "analyze-opportunity"},
    "cover-letter.md": {"build-application"},
    "next-steps.md": {"build-application"},
    "application-record.md": {"build-application", "log-activity"},
}
# Artifacts that need a prior stage to exist in the same folder.
NEEDS_ANALYSIS = ("discussion.md", "resume.md", "cover-letter.md", "application-notes.md",
                  "application-record.md", "next-steps.md")
# Artifacts that, for opportunities added on or after DISCUSSION_SINCE, also need a closed discussion.md.
NEEDS_DISCUSSION = ("resume.md", "cover-letter.md")


def frontmatter(text: str) -> dict[str, str]:
    """Top-level `key: value` pairs of a leading frontmatter block (no YAML dependency)."""
    m = FM_RE.match(text)
    out: dict[str, str] = {}
    if m:
        for line in m.group(1).splitlines():
            k = re.match(r"^([A-Za-z0-9_][A-Za-z0-9_ .-]*):[ \t]*(.*)$", line)
            if k:
                out[k.group(1)] = k.group(2).strip().strip("\"'")
    return out


def opportunity_location(path: str) -> tuple[str, str, str, str] | None:
    """(section, folder, folder_date, file-within-folder) for a repo-relative path, else None."""
    m = OPP_DIR_RE.match(path)
    return (m.group(1), m.group(2), m.group(3), m.group(4) or "") if m else None


def added_date(folder_date: str, fm: dict[str, str]) -> str:
    return fm.get("date_added") or fm.get("date_downloaded") or folder_date


def in_scope(folder_date: str, fm: dict[str, str]) -> bool:
    return added_date(folder_date, fm) >= CONTRACT_SINCE


def record_problems(rel: str, text: str, folder: Path, section: str) -> list[str]:
    fm = frontmatter(text)
    p: list[str] = []
    for key, value in fm.items():
        if value == "":
            p.append(f"{rel}: frontmatter '{key}' is empty (set it to MISSING)")
    for key in ("company", "role", "intake_status", "track"):
        if not fm.get(key):
            p.append(f"{rel}: required frontmatter '{key}' is absent (use MISSING if unknown)")
    if not (fm.get("source_pdf") or fm.get("posting_file")):
        p.append(f"{rel}: needs source_pdf or posting_file")
    if not (fm.get("date_added") or fm.get("date_downloaded")):
        p.append(f"{rel}: needs date_added or date_downloaded")
    track = fm.get("track")
    if track and track not in VALID_TRACKS:
        p.append(f"{rel}: track '{track}' is not one of track-2, track-3, track-4, track-5, track-9, MISSING")
    status = fm.get("intake_status")
    allowed = {"confirmed"} if section == "06_Job_Opportunities" else {"reviewed", "confirmed"}
    if status and status not in allowed:
        p.append(f"{rel}: intake_status is '{status}', expected {' or '.join(sorted(allowed))} here")
    src = fm.get("source_pdf") or fm.get("posting_file")
    if src and src != "MISSING" and not (folder / src).exists():
        p.append(f"{rel}: source file '{src}' not found in the folder")
    for heading in ("Raw Source", "Structured Extraction"):
        if not re.search(rf"^##\s+(?:\d+\.\s+)?{heading}\b", text, re.M):
            p.append(f"{rel}: missing required section '{heading}'")
    return p


def analysis_problems(rel: str, text: str, record_text: str | None) -> list[str]:
    p: list[str] = []
    for name in ANALYSIS_SECTIONS:
        if not re.search(rf"^##\s+{re.escape(name)}\b", text, re.M):
            p.append(f"{rel}: missing required section '{name}'")
    ats = re.search(r"^## ATS Keywords\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    if ats is not None and not ats.group(1).strip():
        p.append(f"{rel}: '## ATS Keywords' is empty")
    sec = re.search(r"^## Track\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    tv = re.search(r"Track:\**\s*`?(track-\d|MISSING)", sec.group(1)) if sec else None
    if sec is not None and not tv:
        p.append(f"{rel}: '## Track' has no parseable 'Track: track-N' line")
    rec = re.search(r"^## Recommendation\n+(.*?)(?=^## |\Z)", text, re.M | re.S)
    if rec is not None and not re.search(r"\b(pursue|consider|pass)\b", rec.group(1), re.I):
        p.append(f"{rel}: '## Recommendation' has no pursue/consider/pass value")
    if tv and record_text:
        rt = frontmatter(record_text).get("track")
        if rt and rt != "MISSING" and tv.group(1) != "MISSING" and rt != tv.group(1):
            p.append(f"{rel}: track {tv.group(1)} conflicts with job-opportunity.md track {rt}; flag, do not pick one")
    return p


def lifecycle_problems(rel_folder: str, folder: Path) -> list[str]:
    files = {f.name for f in folder.iterdir()} if folder.is_dir() else set()
    record = folder / "job-opportunity.md"
    fm = frontmatter(record.read_text()) if record.is_file() else {}
    p: list[str] = []
    if "analysis.md" in files and fm.get("intake_status") != "confirmed" and fm.get("status") != "closed":
        p.append(f"{rel_folder}: analysis.md exists but intake_status is '{fm.get('intake_status', 'absent')}', not confirmed")
    for name in NEEDS_ANALYSIS:
        if name in files and "analysis.md" not in files:
            p.append(f"{rel_folder}: {name} exists without analysis.md (run /analyze-opportunity first)")
    folder_date = re.search(r"(\d{4}-\d{2}-\d{2})$", folder.name)
    if folder_date and added_date(folder_date.group(1), fm) >= DISCUSSION_SINCE:
        needing = [n for n in NEEDS_DISCUSSION if n in files]
        if needing and "discussion.md" not in files:
            p.append(f"{rel_folder}: {', '.join(needing)} exist without discussion.md "
                     "(run /discuss-opportunity first)")
        elif needing:
            status = frontmatter((folder / "discussion.md").read_text()).get("discussion_status")
            if status != "closed":
                p.append(f"{rel_folder}: {', '.join(needing)} exist but discussion.md is "
                         f"'{status or 'absent'}', not closed")
    if fm.get("status") == "submitted" and "application-record.md" not in files:
        p.append(f"{rel_folder}: status is submitted but application-record.md is absent")
    return p


def _section(text: str, name: str) -> str | None:
    m = re.search(rf"^##\s+{re.escape(name)}\b[^\n]*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1) if m else None


def discussion_problems(rel: str, text: str) -> list[str]:
    """Structure and closure rules for discussion.md (the /discuss-opportunity artifact)."""
    p: list[str] = []
    fm = frontmatter(text)
    status = fm.get("discussion_status")
    if status not in ("open", "closed"):
        p.append(f"{rel}: frontmatter 'discussion_status' must be open or closed")
    for name in DISCUSSION_SECTIONS:
        if _section(text, name) is None:
            p.append(f"{rel}: missing required section '{name}'")
    for m in re.finditer(r"\b(TODO|TBD|FIXME)\b", text):
        p.append(f"{rel}: unresolved marker '{m.group(1)}'")
        break
    ledger = _section(text, "Claim Ledger") or ""
    rows = [[c.strip() for c in l.strip().strip("|").split("|")]
            for l in ledger.splitlines() if re.match(r"^\|\s*C\d+\s*\|", l)]
    if _section(text, "Claim Ledger") is not None and not rows:
        p.append(f"{rel}: '## Claim Ledger' has no rows (| C1 | claim | verdict | evidence | disposition |)")
    for r in rows:
        if len(r) != 5:
            p.append(f"{rel}: ledger row {r[0]} needs 5 columns: id, claim, verdict, evidence, disposition")
            continue
        cid, _, verdict, evidence, disp = r
        if verdict not in LEDGER_VERDICTS:
            p.append(f"{rel}: ledger {cid} verdict '{verdict}' is not one of {', '.join(sorted(LEDGER_VERDICTS))}")
        if not evidence:
            p.append(f"{rel}: ledger {cid} cites no evidence (name the file, or 'none found')")
        if disp not in LEDGER_DISPOSITIONS:
            p.append(f"{rel}: ledger {cid} disposition '{disp}' is not one of {', '.join(sorted(LEDGER_DISPOSITIONS))}")
        elif status == "closed" and disp == "open":
            p.append(f"{rel}: closed but ledger {cid} is still open")
        elif verdict != "supported" and disp == "agreed":
            p.append(f"{rel}: ledger {cid} is {verdict} yet 'agreed'; reconcile it (evidence-supplied, reframed or accepted-risk)")
    for l in (_section(text, "Canonical Proposals") or "").splitlines():
        m = re.match(r"^\s*-\s*\[([a-z]+)\]", l)
        if m and m.group(1) not in PROPOSAL_STATUSES:
            p.append(f"{rel}: canonical proposal status '{m.group(1)}' is not one of {', '.join(sorted(PROPOSAL_STATUSES))}")
        elif m and m.group(1) == "proposed" and status == "closed":
            p.append(f"{rel}: closed but a canonical proposal is still [proposed]: {l.strip()[:70]}")
    if status == "closed" and re.search(r"\[blocking\]", _section(text, "Open Items") or ""):
        p.append(f"{rel}: closed but 'Open Items' still lists a [blocking] item")
    return p


def docx_text(data: bytes) -> str:
    import io
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        xml = z.read("word/document.xml").decode(errors="ignore")
    return re.sub(r"<[^>]+>", " ", xml)


def deliverable_problems(rel: str, data: bytes) -> list[str]:
    """Submitted artifacts must not carry unresolved markers."""
    try:
        text = docx_text(data) if rel.endswith(".docx") else (data.decode(errors="ignore") if re.search(r"/resume(-[a-z0-9-]+)?\.md$", rel) else "")
    except (zipfile.BadZipFile, KeyError):
        return [f"{rel}: not a readable DOCX"]
    hits = sorted(set(UNRESOLVED_RE.findall(text)))
    return [f"{rel}: contains unresolved marker(s) {', '.join(hits)}; a submitted document must not"] if hits else []


def log_entries(text: str) -> list[tuple[str, str]]:
    """(heading date, full block) for every detailed entry in Work_Search_Log.md."""
    return [(m.group(1), m.group(0)) for m in ENTRY_RE.finditer(text)]


def log_path_exists(base: Path, ref: str) -> bool:
    """A log path resolves if it exists, or if it points into 06_Job_Opportunities/ and the
    folder has since been archived by /close-opportunity (log entries are append-only)."""
    target = ref.split()[0]
    if (base / target).resolve().exists():
        return True
    archived = target.replace("06_Job_Opportunities/", "99_Archive/Closed_Searches/", 1)
    return archived != target and (base / archived).resolve().exists()


def log_problems(rel: str, text: str, base: Path) -> list[str]:
    p: list[str] = []
    seen: dict[str, str] = {}
    for date, block in log_entries(text):
        y = re.search(r"```yaml\n(.*?)```", block, re.S)
        title = block.splitlines()[0][:60]
        if not y:
            p.append(f"{rel}: entry '{title}' has no yaml block")
            continue
        fields = {m.group(1): m.group(2).strip() for m in re.finditer(r"^([a-z_]+):[ \t]*(.*)$", y.group(1), re.M)}
        missing = [k for k in LOG_FIELDS if k not in fields]
        qual = next((fields[k] for k in QUALIFYING_FIELDS if k in fields), None)
        if qual is None:
            missing.append("qualifying")
        if missing:
            p.append(f"{rel}: entry '{title}' missing field(s): {', '.join(missing)}")
        aid = fields.get("activity_id", "")
        if aid:
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}_[a-z0-9_]+", aid) or not aid.startswith(date):
                p.append(f"{rel}: activity_id '{aid}' must be {date}_<company>_<activity>")
            if aid in seen:
                p.append(f"{rel}: duplicate activity_id '{aid}'")
            seen[aid] = title
        if fields.get("activity_date") and fields["activity_date"] != date:
            p.append(f"{rel}: entry '{title}' heading date {date} != activity_date {fields['activity_date']}")
        if qual and qual.lower() not in QUALIFYING_VALUES:
            p.append(f"{rel}: qualifying '{qual}' must be true, false or needs_review")
        for key in ("evidence", "related_opportunity", "related_application"):
            v = fields.get(key, "")
            if v and v not in {"MISSING", "null", "None", "~"} and not log_path_exists(base, v):
                p.append(f"{rel}: {key} path does not exist: {v[:80]}")
    return p


def log_append_only_problems(rel: str, old: str, new: str) -> list[str]:
    """Existing entries must survive verbatim; corrections are appended as new notes."""
    p = []
    for date, block in log_entries(old):
        if block.strip() not in new:
            p.append(f"{rel}: existing entry '{block.splitlines()[0][:70]}' was edited or removed "
                     "(append a correction note instead)")
    return p


def provenance_problems(added: list[str], run_commands: set[str]) -> list[str]:
    """New standard artifacts in an opportunity folder need a run for a command allowed to make them."""
    p = []
    for path in added:
        loc = opportunity_location(path)
        if not loc or loc[0] != "06_Job_Opportunities" or "/" in loc[3]:
            continue
        allowed = MAY_CREATE.get(loc[3])
        if allowed and not (allowed & run_commands):
            ran = ", ".join(sorted(run_commands)) or "none"
            p.append(f"{path}: added without a run file for {' / '.join(sorted(allowed))} in the same commit "
                     f"(runs staged: {ran})")
    return p
