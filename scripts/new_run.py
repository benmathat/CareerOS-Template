"""Scaffold a runtime IO run file (stdlib only; used by `careeros new-run`).

Everything derivable from the command, date, slug and target is prefilled.
Everything that needs judgment is the literal marker `TODO`. `careeros gate`
and `careeros check` refuse a run file that still contains one, so a skeleton
can never be mistaken for a finished run.
"""

from __future__ import annotations

import re

MARKER = "TODO"
UNFILLED_RE = re.compile(rf"(?:^|[:\-]\s+|\[\s*){MARKER}\b")

PROTECTED = ["/02_Work_Experience/", "/03_Skills_and_Portfolio/",
             "/04_Career_Goals_and_Strategy/", "/05_Personal_Profile/"]

# Per-command constants, taken from the command contracts and prior runs.
# Where neither fixes a value it is MARKER (never a guess): the model must decide.
# dest: default artifact_destination path; {opp} is the target opportunity folder name.
COMMANDS: dict[str, dict] = {
    "source-opportunities": dict(pack="NONE", pipeline="NONE", mode="execute",
                                 state="existing", otype="Document", ti="none", profile="opportunity_sourcing",
                                 dest="/09_Research_and_Market_Intelligence/Opportunity_Sourcing/Reports/",
                                 file=None, excluded=[]),
    "intake-job": dict(pack="job-intake-pack", pipeline="job-intake-pipeline", mode="build",
                       state="new", otype="Document", ti="structure_only", profile="job_intake",
                       dest="/INBOX/Job_Postings/", file=None, excluded=PROTECTED),
    "promote-opportunity": dict(pack="job-intake-pack", pipeline="job-intake-pipeline", mode="execute",
                                state="existing", otype="Document", ti="none", profile="promote",
                                dest="/06_Job_Opportunities/{opp}/", file="job-opportunity.md",
                                excluded=PROTECTED),
    "analyze-opportunity": dict(pack="opportunity-analysis-pack", pipeline="opportunity-review-pipeline",
                                mode="analyze", state="new", otype="Document", ti="none",
                                profile="opportunity_analysis", dest="/06_Job_Opportunities/{opp}/",
                                file="analysis.md", excluded=[]),
    "discuss-opportunity": dict(pack="opportunity-analysis-pack", pipeline="opportunity-fit-pipeline",
                                mode="analyze", state="new", otype="Document", ti="none",
                                profile="opportunity_discussion", dest="/06_Job_Opportunities/{opp}/",
                                file="discussion.md", excluded=[]),
    "build-resume": dict(pack="resume-pack", pipeline="application-pipeline", mode="build",
                         state="new", otype="Document", ti="none", profile="resume",
                         dest="/06_Job_Opportunities/{opp}/", file="resume.md", excluded=[]),
    "build-application": dict(pack="application-pack", pipeline="application-pipeline", mode="build",
                              state="new", otype="Document", ti="none", profile=None,
                              dest="/06_Job_Opportunities/{opp}/", file=None, excluded=[]),
    "log-activity": dict(pack="compliance-pack", pipeline="compliance-pipeline", mode="execute",
                         state="existing", otype="Document", ti="none", profile="compliance_log",
                         dest="/11_Job_Search_Activities/", file="Work_Search_Log.md", excluded=PROTECTED),
    "generate-weekly-cert": dict(pack="compliance-pack", pipeline="compliance-pipeline", mode="build",
                                 state="new", otype="Document", ti="none", profile=None,
                                 dest="/11_Job_Search_Activities/Weekly_Certifications/", file=None,
                                 excluded=PROTECTED),
    "sync-application-tracker": dict(pack=MARKER, pipeline=MARKER,
                                     mode="execute", state="existing", otype="Document", ti="none",
                                     profile=None, dest="/07_Applications_and_Interviews/Applications/",
                                     file="application-tracker.md", excluded=PROTECTED),
    "close-opportunity": dict(pack=MARKER, pipeline=MARKER, mode="execute",
                              state="existing", otype="Document", ti="none", profile=None,
                              dest="/99_Archive/Closed_Searches/{opp}/", file="job-opportunity.md",
                              excluded=PROTECTED),
}

CLASS_PREFIXES = [("presentation", ("/01_",)), ("canonical", ("/02_", "/03_", "/04_", "/05_")),
                  ("execution", ("/06_", "/07_", "/08_", "/09_")),
                  ("reflection", ("/10_", "/11_", "/99_Archive/")), ("staging", ("/INBOX/",))]


def destination_class(path: str) -> str:
    for cls, prefixes in CLASS_PREFIXES:
        if path.startswith(prefixes):
            return cls
    return MARKER


def unfilled_lines(text: str) -> list[tuple[int, str]]:
    return [(n, l.strip()) for n, l in enumerate(text.splitlines(), 1) if UNFILLED_RE.search(l)]


def _list(key: str, values: list[str], indent: int) -> str:
    pad = " " * indent
    if not values:
        return f"{pad}{key}: []"
    return f"{pad}{key}:\n" + "\n".join(f"{pad}  - {v}" for v in values)


def render(command: str, slug: str, date: str, opp: str | None, filename: str | None,
           state: str | None) -> str:
    c = COMMANDS[command]
    dest = c["dest"].format(opp=opp or MARKER)
    file_ = filename or c["file"] or MARKER
    if command == "intake-job" and not filename:
        file_ = MARKER  # the staged name is <company>_<role>_<date>.md; the model knows the company/role
    cls = destination_class(dest)
    state = state or c["state"]
    task_id = f"{command.replace('-', '_')}_{date.replace('-', '_')}_{slug}"
    name = "".join(p.capitalize() for p in command.split("-"))
    ctx = {"mode": c["mode"], "otype": c["otype"], "durability": cls}
    T = MARKER
    return f"""# Scaffolded by `careeros new-run {command} {slug}` on {date}.
# Prefilled: command, pack, pipeline, mode, output type, task id, destination, contract lists.
# Replace every {T} with grounded content. `careeros gate` refuses this file while any {T} remains.
runtime_io:
  request:
    command: /{command}
    intent: {T}
    inputs:
      required:
        - {T}
      optional: []
    pack: {c['pack']}
    pipeline: {c['pipeline']}
  task:
    id: {task_id}
    name: {name}
    objective: {T}
    mode_intent: {c['mode']}
    artifact_state: {state}
    output_type: {c['otype']}
    urgency: balanced
    transformation_intent: {c['ti']}
    inputs:
      required:
        - {T}
      optional: []
    sources:
      required:
        - {T}
      optional: []
{_list('excluded', c['excluded'], 6)}
    constraints:
      hard:
        - {T}
      soft: []
    scope:
      in_scope:
        - {T}
      out_of_scope:
        - {T}
    assumptions: []
    context_gaps: []
    success_criteria:
      - {T}
    destination: {dest}
    mode_details:
      command: {command}
{f"      profile: {c['profile']}" if c['profile'] else f"      profile: {T}"}
  mode_selection:
    status: valid
    blocking: false
    primary_mode: {c['mode']}
    secondary_mode: null
    rationale: {T}
    assumptions: []
    confidence: {T}
  routing_output:
    status: valid
    blocking: false
    source_set:
      required:
        - {T}
      optional: []
{_list('excluded', c['excluded'], 6)}
    selection_rationale: {T}
    conflict_rules_applied: []
    output_destination: {dest}
    assumptions: []
    completeness:
      required_sources_resolved: {T}
      assumptions_used: {T}
    confidence: {T}
  context_block:
    status: {T}
    task_alignment:
      objective: {T}
      mode: {ctx['mode']}
      output_type: {ctx['otype']}
      durability_class: {ctx['durability']}
    canonical_context: []
    contextual_context:
      - path: {T}
        source_type: contextual
        key_facts:
          - {T}
        key_metrics: []
        constraints: []
        decisions: []
        freshness: {T}
        relevance_to_task: {T}
    supporting_context: []
    context_gaps: []
    conflicts: []
    assumptions: []
    warnings: []
    handoff:
      prompt_assembler_ready: {T}
      execution_may_continue: {T}
      required_user_clarification: {T}
  prompt_object:
    system_contracts:
      - system-prompt.md
      - interaction-model.md
      - output-standards.md
    mode_contract:
      primary_mode: {c['mode']}
    task:
      id: {task_id}
      output_type: {c['otype']}
    routing:
      status: valid
      blocking: false
    context:
      status: {T}
    output_contract:
      template: {T}
    validation_requirements:
      - {T}
  output:
    output_type: {c['otype']}
    status: {T}
    blocking: {T}
    artifact_preview:
      title: {T}
      sections:
        - {T}
    disclosures:
      assumptions_labeled: {T}
      context_gaps_labeled: {T}
      warnings_included: {T}
  validation_result:
    passed: {T}
    checks:
      constraints_satisfied: {T}
      output_structure_compliant: {T}
      source_grounding_compliant: {T}
      boundary_rules_compliant: {T}
      assumption_labels_present: {T}
    failures: []
    warnings: []
    conformance_gate:
      protocol: command-conformance-gate.md
      status: {T}
      checks_run:
        total: {T}
        passed: {T}
        failed: {T}
      failures: []
      evaluated_at_step: end_of_command_run
  artifact_destination:
    class: {cls}
    path: {dest}
    filename: {file_}
    write_allowed: {T}
    write_reason: {T}
  execution_trace:
    steps_completed:
      - validate_inputs
      - emit_runtime_io
      - command_conformance_gate
      - {T}
    halted_at: null
    reason: null
    runtime_state: {T}
"""
