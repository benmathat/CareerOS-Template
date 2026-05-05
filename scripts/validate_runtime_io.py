#!/usr/bin/env python3
"""Deterministic runtime IO conformance validator.

Parses the payload as structured YAML (no regex-based key matching).
Implements checks documented in:
Career/00_Core_OS/Prompts/Runtime/command-conformance-gate.md

Requires: pip install -r scripts/requirements-runtime-validator.txt
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore[assignment]

REQUIRED_ROOT_KEYS = [
    "request",
    "task",
    "mode_selection",
    "routing_output",
    "context_block",
    "prompt_object",
    "output",
    "validation_result",
    "artifact_destination",
    "execution_trace",
]

VALID_MODES = {"build", "analyze", "refine", "execute", "architect", "transform"}
VALID_OUTPUT_TYPES = {"Document", "Framework", "Template", "Checklist", "Analysis"}
VALID_GENERAL_STATUS = {"valid", "partial", "invalid"}
VALID_CONTEXT_STATUS = {"complete", "partial_non_blocking", "partial_blocking"}
VALID_ARTIFACT_STATES = {"new", "existing", "none"}
VALID_URGENCY = {"speed", "balanced", "depth"}
VALID_TRANSFORMATION_INTENTS = {
    "none",
    "structure_only",
    "format_only",
    "audience_adaptation",
    "structure_change",
    "format_change",
    "artifact_conversion",
}
VALID_CONFIDENCE = {"high", "medium", "low"}
VALID_RISK_LEVELS = {"low", "medium", "high"}
VALID_DESTINATION_CLASSES = {"presentation", "canonical", "execution", "reflection"}


def extract_yaml_fenced_blocks(text: str) -> list[str]:
    """Return contents of ```yaml / ```yml fenced blocks in order."""
    blocks: list[str] = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith("```"):
            lang = stripped[3:].strip().lower()
            if lang in ("yaml", "yml"):
                i += 1
                buf: list[str] = []
                while i < len(lines) and not lines[i].strip().startswith("```"):
                    buf.append(lines[i])
                    i += 1
                blocks.append("\n".join(buf))
            i += 1
            continue
        i += 1
    return blocks


def load_yaml_documents(block: str) -> list[Any]:
    if yaml is None:
        raise RuntimeError("PyYAML is not installed")
    try:
        return list(yaml.safe_load_all(block))
    except yaml.YAMLError as exc:
        raise ValueError(f"YAML parse error: {exc}") from exc


def is_runtime_envelope(data: Any) -> bool:
    if not isinstance(data, dict):
        return False
    inner: dict | None = None
    if "runtime_io" in data and isinstance(data["runtime_io"], dict):
        inner = data["runtime_io"]
    elif all(k in data for k in REQUIRED_ROOT_KEYS):
        inner = data
    else:
        return False
    return all(isinstance(inner.get(k), dict) for k in REQUIRED_ROOT_KEYS)


def unwrap_envelope(data: dict) -> dict:
    if "runtime_io" in data and isinstance(data["runtime_io"], dict):
        return data["runtime_io"]
    return data


def load_envelope_from_file(path: Path) -> tuple[dict | None, list[str]]:
    """Return (envelope dict, errors). errors are returned only when no valid envelope is found."""
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    blocks = extract_yaml_fenced_blocks(text)
    if not blocks:
        blocks = [text]

    candidates: list[tuple[int, dict]] = []
    for idx, block in enumerate(blocks):
        block = block.strip()
        if not block:
            continue
        try:
            docs = load_yaml_documents(block)
        except ValueError as exc:
            errors.append(f"YAML block {idx + 1}: {exc}")
            continue
        for doc in docs:
            if doc is None:
                continue
            if is_runtime_envelope(doc):
                candidates.append((idx, unwrap_envelope(doc)))

    if candidates:
        return candidates[0][1], []

    if errors:
        return None, errors
    return None, ["no YAML document contains a complete runtime_io envelope (all root keys as mappings)"]


def scalar_str(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        s = value.strip()
        return s if s else None
    return None


def normalize_scalar(value: Any) -> str | None:
    s = scalar_str(value)
    if s is None:
        return None
    return s.strip().strip('"').strip("'")


def is_yaml_false(value: Any) -> bool:
    if value is False:
        return True
    if isinstance(value, str):
        return value.strip().lower() in ("false", "no", "0", "")
    return False


def is_yaml_true(value: Any) -> bool:
    if value is True:
        return True
    if isinstance(value, str):
        return value.strip().lower() in ("true", "yes", "1")
    return False


def require_mapping(parent: dict, key: str, failures: list[str], *, path: str) -> dict | None:
    value = parent.get(key)
    if not isinstance(value, dict):
        failures.append(f"{path}.{key} must be a mapping")
        return None
    return value


def require_list(parent: dict, key: str, failures: list[str], *, path: str) -> list[Any] | None:
    value = parent.get(key)
    if not isinstance(value, list):
        failures.append(f"{path}.{key} must be a list")
        return None
    return value


def require_non_empty_scalar(parent: dict, key: str, failures: list[str], *, path: str) -> str | None:
    value = normalize_scalar(parent.get(key))
    if value in (None, "MISSING", "NONE"):
        failures.append(f"{path}.{key} is missing or empty")
        return None
    return value


def require_scalar_allow_none(parent: dict, key: str, failures: list[str], *, path: str) -> str | None:
    value = normalize_scalar(parent.get(key))
    if value in (None, "MISSING"):
        failures.append(f"{path}.{key} is missing or empty")
        return None
    return value


def require_enum(
    parent: dict,
    key: str,
    allowed: set[str],
    failures: list[str],
    *,
    path: str,
) -> str | None:
    value = require_non_empty_scalar(parent, key, failures, path=path)
    if value is None:
        return None
    if value not in allowed:
        failures.append(f"{path}.{key} is invalid: {value}")
        return None
    return value


def is_placeholder_list(items: list[Any]) -> bool:
    if not items:
        return True
    normalized: set[str | None] = set()
    for item in items:
        if isinstance(item, (dict, list)):
            return False
        normalized.add(normalize_scalar(item))
    return normalized.issubset({"MISSING", "NONE", None})


def require_non_empty_list(parent: dict, key: str, failures: list[str], *, path: str) -> list[Any] | None:
    items = require_list(parent, key, failures, path=path)
    if items is None:
        return None
    if is_placeholder_list(items):
        failures.append(f"{path}.{key} must contain at least one concrete value")
        return None
    return items


def collect_context_sources(context_block: dict) -> list[tuple[str, str]]:
    results: list[tuple[str, str]] = []
    for tier_name in ("canonical_context", "contextual_context", "supporting_context"):
        tier = context_block.get(tier_name)
        if not isinstance(tier, list):
            continue
        for item in tier:
            if isinstance(item, dict):
                path = normalize_scalar(item.get("path"))
                if path:
                    results.append((tier_name, path))
    return results


def path_matches_rule(path: str, rule: str) -> bool:
    normalized_path = path.rstrip("/")
    normalized_rule = rule.rstrip("/")
    return normalized_path == normalized_rule or normalized_path.startswith(normalized_rule + "/")


def path_matches_any(path: str, rules: list[str]) -> bool:
    return any(path_matches_rule(path, rule) for rule in rules if rule)


def detect_markdown_artifact(output: dict) -> str | None:
    candidates = (
        output.get("markdown"),
        output.get("content"),
        output.get("rendered_markdown"),
        output.get("artifact_markdown"),
        output.get("body"),
        output.get("text"),
    )
    for value in candidates:
        if isinstance(value, str) and value.strip():
            return value
    return None


def has_markdown_heading(text: str, heading: str) -> bool:
    return re.search(rf"(?mi)^##\s+{re.escape(heading)}(?:\b.*)?$", text) is not None


def validate_task_schema(task: dict, failures: list[str]) -> None:
    for key in ("id", "name", "objective", "destination"):
        require_non_empty_scalar(task, key, failures, path="task")

    require_enum(task, "mode_intent", VALID_MODES, failures, path="task")
    require_enum(task, "artifact_state", VALID_ARTIFACT_STATES, failures, path="task")
    require_enum(task, "output_type", VALID_OUTPUT_TYPES, failures, path="task")
    require_enum(task, "urgency", VALID_URGENCY, failures, path="task")

    transformation_intent = require_non_empty_scalar(task, "transformation_intent", failures, path="task")
    if transformation_intent is not None and transformation_intent not in VALID_TRANSFORMATION_INTENTS:
        failures.append(f"task.transformation_intent is invalid: {transformation_intent}")

    inputs = require_mapping(task, "inputs", failures, path="task")
    if inputs is not None:
        require_non_empty_list(inputs, "required", failures, path="task.inputs")
        require_list(inputs, "optional", failures, path="task.inputs")

    sources = require_mapping(task, "sources", failures, path="task")
    if sources is not None:
        require_non_empty_list(sources, "required", failures, path="task.sources")
        require_list(sources, "optional", failures, path="task.sources")
        require_list(sources, "excluded", failures, path="task.sources")

    constraints = require_mapping(task, "constraints", failures, path="task")
    if constraints is not None:
        require_non_empty_list(constraints, "hard", failures, path="task.constraints")
        require_list(constraints, "soft", failures, path="task.constraints")

    scope = require_mapping(task, "scope", failures, path="task")
    if scope is not None:
        require_non_empty_list(scope, "in_scope", failures, path="task.scope")
        require_non_empty_list(scope, "out_of_scope", failures, path="task.scope")

    assumptions = require_list(task, "assumptions", failures, path="task")
    if assumptions is not None:
        for idx, assumption in enumerate(assumptions):
            if not isinstance(assumption, dict):
                failures.append(f"task.assumptions[{idx}] must be a mapping")
                continue
            require_non_empty_scalar(assumption, "assumption", failures, path=f"task.assumptions[{idx}]")
            require_non_empty_scalar(assumption, "reason", failures, path=f"task.assumptions[{idx}]")
            risk = require_non_empty_scalar(assumption, "risk", failures, path=f"task.assumptions[{idx}]")
            if risk is not None and risk not in VALID_RISK_LEVELS:
                failures.append(f"task.assumptions[{idx}].risk is invalid: {risk}")
            if "must_label_in_output" not in assumption:
                failures.append(f"task.assumptions[{idx}].must_label_in_output must be present")

    context_gaps = require_list(task, "context_gaps", failures, path="task")
    if context_gaps is not None:
        for idx, gap in enumerate(context_gaps):
            if not isinstance(gap, dict):
                failures.append(f"task.context_gaps[{idx}] must be a mapping")
                continue
            require_non_empty_scalar(gap, "missing_information", failures, path=f"task.context_gaps[{idx}]")
            require_non_empty_scalar(gap, "why_needed", failures, path=f"task.context_gaps[{idx}]")
            if "blocking" not in gap:
                failures.append(f"task.context_gaps[{idx}].blocking must be present")
            require_non_empty_scalar(gap, "suggested_source", failures, path=f"task.context_gaps[{idx}]")
            require_non_empty_scalar(
                gap,
                "suggested_user_action",
                failures,
                path=f"task.context_gaps[{idx}]",
            )

    require_non_empty_list(task, "success_criteria", failures, path="task")

    mode_details = task.get("mode_details")
    if not isinstance(mode_details, dict):
        failures.append("task.mode_details must be a mapping")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate runtime IO YAML structure and conformance."
    )
    parser.add_argument("file", help="Path to runtime IO YAML or Markdown file")
    args = parser.parse_args()

    if yaml is None:
        print(
            "FAIL: PyYAML is required. Install with:\n"
            "  pip install -r scripts/requirements-runtime-validator.txt",
            file=sys.stderr,
        )
        return 2

    path = Path(args.file)
    if not path.exists():
        print(f"FAIL: runtime IO file not found: {path}")
        return 2

    envelope, load_errors = load_envelope_from_file(path)
    failures: list[str] = []
    warnings: list[str] = []

    if envelope is None:
        failures.extend(load_errors)
        if not failures:
            failures.append("could not load a valid runtime_io envelope")
        print("FAIL: runtime IO conformance check failed")
        for item in failures:
            print(f"- {item}")
        return 1

    for key in REQUIRED_ROOT_KEYS:
        node = envelope.get(key)
        if node is None:
            failures.append(f"missing required root key: {key}")
        elif not isinstance(node, dict):
            failures.append(f"root `{key}` must be a mapping, got {type(node).__name__}")

    if failures:
        print("FAIL: runtime IO conformance check failed")
        for item in failures:
            print(f"- {item}")
        return 1

    request = envelope["request"]
    task = envelope["task"]
    mode_selection = envelope["mode_selection"]
    routing_output = envelope["routing_output"]
    context_block = envelope["context_block"]
    prompt_object = envelope["prompt_object"]
    output = envelope["output"]
    validation_result = envelope["validation_result"]
    artifact_destination = envelope["artifact_destination"]
    execution_trace = envelope["execution_trace"]

    require_non_empty_scalar(request, "command", failures, path="request")
    require_non_empty_scalar(request, "intent", failures, path="request")
    request_inputs = require_mapping(request, "inputs", failures, path="request")
    if request_inputs is not None:
        require_non_empty_list(request_inputs, "required", failures, path="request.inputs")
        require_list(request_inputs, "optional", failures, path="request.inputs")
    require_scalar_allow_none(request, "pack", failures, path="request")
    require_scalar_allow_none(request, "pipeline", failures, path="request")

    validate_task_schema(task, failures)

    ms_status = normalize_scalar(mode_selection.get("status"))
    if ms_status not in VALID_GENERAL_STATUS:
        failures.append(f"mode_selection.status is invalid: {ms_status}")
    elif ms_status == "invalid":
        failures.append("mode_selection.status is invalid")
    if is_yaml_true(mode_selection.get("blocking")):
        failures.append("mode_selection.blocking is true")
    primary_mode = require_enum(mode_selection, "primary_mode", VALID_MODES, failures, path="mode_selection")
    secondary_mode = mode_selection.get("secondary_mode")
    if secondary_mode is not None:
        secondary_normalized = normalize_scalar(secondary_mode)
        if secondary_normalized not in (None, "NONE", "MISSING") and secondary_normalized not in VALID_MODES:
            failures.append(f"mode_selection.secondary_mode is invalid: {secondary_normalized}")
    require_non_empty_scalar(mode_selection, "rationale", failures, path="mode_selection")
    require_list(mode_selection, "assumptions", failures, path="mode_selection")
    require_enum(mode_selection, "confidence", VALID_CONFIDENCE, failures, path="mode_selection")

    ro_status = normalize_scalar(routing_output.get("status"))
    if ro_status not in VALID_GENERAL_STATUS:
        failures.append(f"routing_output.status is invalid: {ro_status}")
    elif ro_status == "invalid":
        failures.append("routing_output.status is invalid")
    if is_yaml_true(routing_output.get("blocking")):
        failures.append("routing_output.blocking is true")

    source_set = require_mapping(routing_output, "source_set", failures, path="routing_output")
    routed_required_paths: list[str] = []
    routed_optional_paths: list[str] = []
    routed_excluded_paths: list[str] = []
    if source_set is not None:
        required_paths = require_non_empty_list(source_set, "required", failures, path="routing_output.source_set")
        optional_paths = require_list(source_set, "optional", failures, path="routing_output.source_set")
        excluded_paths = require_list(source_set, "excluded", failures, path="routing_output.source_set")
        routed_required_paths = [normalize_scalar(item) for item in (required_paths or []) if normalize_scalar(item)]
        routed_optional_paths = [normalize_scalar(item) for item in (optional_paths or []) if normalize_scalar(item)]
        routed_excluded_paths = [normalize_scalar(item) for item in (excluded_paths or []) if normalize_scalar(item)]
    require_non_empty_scalar(routing_output, "selection_rationale", failures, path="routing_output")
    require_list(routing_output, "conflict_rules_applied", failures, path="routing_output")
    output_destination = require_non_empty_scalar(routing_output, "output_destination", failures, path="routing_output")
    require_list(routing_output, "assumptions", failures, path="routing_output")
    completeness = require_mapping(routing_output, "completeness", failures, path="routing_output")
    if completeness is not None:
        if "required_sources_resolved" not in completeness:
            failures.append("routing_output.completeness.required_sources_resolved must be present")
        if "assumptions_used" not in completeness:
            failures.append("routing_output.completeness.assumptions_used must be present")
    require_enum(routing_output, "confidence", VALID_CONFIDENCE, failures, path="routing_output")

    cb_status = normalize_scalar(context_block.get("status"))
    if cb_status not in VALID_CONTEXT_STATUS:
        failures.append(f"context_block.status is invalid: {cb_status}")
    elif cb_status == "partial_blocking":
        failures.append("context_block.status is partial_blocking")

    task_alignment = require_mapping(context_block, "task_alignment", failures, path="context_block")
    if task_alignment is not None:
        alignment_objective = require_non_empty_scalar(
            task_alignment, "objective", failures, path="context_block.task_alignment"
        )
        alignment_mode = require_enum(
            task_alignment, "mode", VALID_MODES, failures, path="context_block.task_alignment"
        )
        alignment_output_type = require_enum(
            task_alignment,
            "output_type",
            VALID_OUTPUT_TYPES,
            failures,
            path="context_block.task_alignment",
        )
        require_non_empty_scalar(
            task_alignment,
            "durability_class",
            failures,
            path="context_block.task_alignment",
        )
        if alignment_objective and alignment_objective != normalize_scalar(task.get("objective")):
            failures.append("context_block.task_alignment.objective must match task.objective")
        if alignment_mode and primary_mode and alignment_mode != primary_mode:
            failures.append("context_block.task_alignment.mode must match mode_selection.primary_mode")
        if alignment_output_type and alignment_output_type != normalize_scalar(task.get("output_type")):
            failures.append("context_block.task_alignment.output_type must match task.output_type")

    for tier_name in ("canonical_context", "contextual_context", "supporting_context"):
        tier = context_block.get(tier_name)
        if tier is not None and not isinstance(tier, list):
            failures.append(f"context_block.{tier_name} must be a list when present")
    for list_name in ("context_gaps", "conflicts", "assumptions", "warnings"):
        node = context_block.get(list_name)
        if node is not None and not isinstance(node, list):
            failures.append(f"context_block.{list_name} must be a list when present")

    handoff = context_block.get("handoff")
    if not isinstance(handoff, dict):
        failures.append("context_block.handoff must be a mapping")
    else:
        if is_yaml_false(handoff.get("prompt_assembler_ready")):
            failures.append("context_block.handoff.prompt_assembler_ready is false")
        if is_yaml_false(handoff.get("execution_may_continue")):
            failures.append("context_block.handoff.execution_may_continue is false")
        if "required_user_clarification" not in handoff:
            failures.append("context_block.handoff.required_user_clarification must be present")

    system_contracts = require_non_empty_list(prompt_object, "system_contracts", failures, path="prompt_object")
    if system_contracts is not None:
        required_contracts = {"system-prompt.md", "interaction-model.md", "output-standards.md"}
        present_contracts = {normalize_scalar(item) for item in system_contracts if normalize_scalar(item)}
        missing_contracts = required_contracts - present_contracts
        if missing_contracts:
            failures.append(
                "prompt_object.system_contracts missing required entries: "
                + ", ".join(sorted(missing_contracts))
            )
    mode_contract = require_mapping(prompt_object, "mode_contract", failures, path="prompt_object")
    if mode_contract is not None:
        mode_contract_primary = require_enum(
            mode_contract, "primary_mode", VALID_MODES, failures, path="prompt_object.mode_contract"
        )
        if mode_contract_primary and primary_mode and mode_contract_primary != primary_mode:
            failures.append("prompt_object.mode_contract.primary_mode must match mode_selection.primary_mode")
    prompt_task = require_mapping(prompt_object, "task", failures, path="prompt_object")
    if prompt_task is not None:
        prompt_task_id = require_non_empty_scalar(prompt_task, "id", failures, path="prompt_object.task")
        prompt_task_output_type = require_enum(
            prompt_task, "output_type", VALID_OUTPUT_TYPES, failures, path="prompt_object.task"
        )
        if prompt_task_id and prompt_task_id != normalize_scalar(task.get("id")):
            failures.append("prompt_object.task.id must match task.id")
        if prompt_task_output_type and prompt_task_output_type != normalize_scalar(task.get("output_type")):
            failures.append("prompt_object.task.output_type must match task.output_type")
    prompt_routing = require_mapping(prompt_object, "routing", failures, path="prompt_object")
    if prompt_routing is not None:
        if normalize_scalar(prompt_routing.get("status")) != ro_status:
            failures.append("prompt_object.routing.status must match routing_output.status")
        if normalize_scalar(prompt_routing.get("blocking")) != normalize_scalar(routing_output.get("blocking")):
            failures.append("prompt_object.routing.blocking must match routing_output.blocking")
    prompt_context = require_mapping(prompt_object, "context", failures, path="prompt_object")
    if prompt_context is not None and normalize_scalar(prompt_context.get("status")) != cb_status:
        failures.append("prompt_object.context.status must match context_block.status")
    output_contract = require_mapping(prompt_object, "output_contract", failures, path="prompt_object")
    if output_contract is not None:
        require_non_empty_scalar(output_contract, "template", failures, path="prompt_object.output_contract")
    require_list(prompt_object, "validation_requirements", failures, path="prompt_object")

    output_type = normalize_scalar(task.get("output_type"))
    if output_type not in VALID_OUTPUT_TYPES:
        failures.append(f"task.output_type is invalid: {output_type}")

    if normalize_scalar(task.get("mode_intent")) != primary_mode:
        failures.append("task.mode_intent must match mode_selection.primary_mode")

    if normalize_scalar(output.get("output_type")) != output_type:
        failures.append("output.output_type must match task.output_type")
    output_status = normalize_scalar(output.get("status"))
    if output_status not in VALID_GENERAL_STATUS:
        failures.append(f"output.status is invalid: {output_status}")
    if "blocking" not in output:
        failures.append("output.blocking must be present")

    preview = output.get("artifact_preview")
    if not isinstance(preview, dict):
        failures.append("output.artifact_preview must be a mapping")
    elif output_type in VALID_OUTPUT_TYPES:
        required_by_type = {
            "Document": ["title", "sections"],
            "Framework": ["components", "relationships", "rules"],
            "Template": ["purpose", "fillable_fields", "usage_instructions"],
            "Checklist": ["items", "completion_criteria"],
            "Analysis": ["findings", "gaps", "risks", "recommendations"],
        }
        for rk in required_by_type.get(output_type, []):
            if rk not in preview or preview[rk] in (None, ""):
                failures.append(
                    f"output.artifact_preview missing or empty `{rk}` for task.output_type `{output_type}`"
                )

    checks = validation_result.get("checks")
    if not isinstance(checks, dict):
        failures.append("validation_result.checks must be a mapping")
    else:
        for key in (
            "constraints_satisfied",
            "output_structure_compliant",
            "source_grounding_compliant",
            "boundary_rules_compliant",
            "assumption_labels_present",
        ):
            if key not in checks:
                failures.append(f"validation_result.checks.{key} must be present")
        if is_yaml_false(checks.get("constraints_satisfied")):
            failures.append("output hard constraints are not satisfied")
        if is_yaml_false(checks.get("source_grounding_compliant")):
            failures.append("claims are not fully grounded in loaded context")
        if is_yaml_false(checks.get("assumption_labels_present")):
            failures.append("required assumption labels are not present")
        if is_yaml_false(checks.get("boundary_rules_compliant")):
            failures.append("canonical/presentation boundary rules are not compliant")
        if is_yaml_false(checks.get("output_structure_compliant")):
            failures.append("output structure does not match task.output_type contract")

    disclosures = output.get("disclosures")
    if disclosures is not None and not isinstance(disclosures, dict):
        failures.append("output.disclosures must be a mapping when present")
    elif isinstance(disclosures, dict):
        for key in ("assumptions_labeled", "context_gaps_labeled", "warnings_included"):
            if key not in disclosures:
                failures.append(f"output.disclosures.{key} must be present")
        if is_yaml_false(disclosures.get("assumptions_labeled")):
            failures.append("output disclosures indicate assumptions are not labeled")

    markdown_output = detect_markdown_artifact(output)
    if markdown_output is not None:
        if output_type == "Document":
            if not re.search(r"(?m)^#\s+\S", markdown_output):
                failures.append("Document output markdown must include a title heading")
            if not re.search(r"(?m)^##\s+\S", markdown_output):
                failures.append("Document output markdown must include section headings")
            if not re.search(r"(?m)^###\s+\S", markdown_output):
                failures.append("Document output markdown must include subsection headings")
        elif output_type == "Checklist":
            if not has_markdown_heading(markdown_output, "Checklist"):
                failures.append("Checklist output markdown must include a `## Checklist` section")
            if not re.search(r"(?m)^- \[ \]\s+\S", markdown_output):
                failures.append("Checklist output markdown must include actionable checklist items")
        elif output_type == "Analysis":
            for heading in ("Findings", "Recommendations"):
                if not has_markdown_heading(markdown_output, heading):
                    failures.append(f"Analysis output markdown must include a `## {heading}` section")

        assumption_labels_required = False
        for assumptions_list in (task.get("assumptions"), context_block.get("assumptions")):
            if not isinstance(assumptions_list, list):
                continue
            if any(
                isinstance(item, dict) and is_yaml_true(item.get("must_label_in_output"))
                for item in assumptions_list
            ):
                assumption_labels_required = True
                break
        if assumption_labels_required and not has_markdown_heading(markdown_output, "Assumptions"):
            failures.append("output markdown must include an `## Assumptions` section when labels are required")
        if isinstance(context_block.get("context_gaps"), list) and context_block.get("context_gaps"):
            if not has_markdown_heading(markdown_output, "Context Gaps"):
                failures.append("output markdown must include a `## Context Gaps` section when gaps exist")
        if isinstance(context_block.get("warnings"), list) and context_block.get("warnings"):
            if not has_markdown_heading(markdown_output, "Warnings"):
                failures.append("output markdown must include a `## Warnings` section when warnings exist")

    loaded_context_paths = collect_context_sources(context_block)
    allowed_context_paths = routed_required_paths + routed_optional_paths
    if loaded_context_paths and not allowed_context_paths:
        failures.append("context was loaded but routing_output.source_set.required/optional is empty")
    for tier_name, context_path in loaded_context_paths:
        if path_matches_any(context_path, routed_excluded_paths):
            failures.append(
                f"{tier_name} path `{context_path}` is excluded by routing_output.source_set.excluded"
            )
        if allowed_context_paths and not path_matches_any(context_path, allowed_context_paths):
            failures.append(f"{tier_name} path `{context_path}` is outside routed required/optional sources")
        if tier_name == "canonical_context" and re.match(r"^/(01_|06_|07_|08_|09_|10_|11_)", context_path):
            failures.append(f"canonical_context path `{context_path}` violates canonical boundary rules")

    task_destination = normalize_scalar(task.get("destination"))
    if task_destination and output_destination and task_destination != output_destination:
        failures.append("task.destination must match routing_output.output_destination")

    destination_class = normalize_scalar(artifact_destination.get("class"))
    destination_path = normalize_scalar(artifact_destination.get("path")) or ""
    class_to_prefixes = {
        "presentation": ("/01_",),
        "canonical": ("/02_", "/03_", "/04_", "/05_"),
        "execution": ("/06_", "/07_", "/08_", "/09_"),
        "reflection": ("/10_", "/11_"),
    }
    if destination_class not in VALID_DESTINATION_CLASSES:
        failures.append(f"artifact_destination.class is invalid: {destination_class}")
    elif not destination_path.startswith(class_to_prefixes[destination_class]):
        failures.append(
            f"artifact_destination.path `{destination_path}` does not match class `{destination_class}`"
        )
    filename = require_non_empty_scalar(artifact_destination, "filename", failures, path="artifact_destination")
    if filename and "/" in filename:
        failures.append("artifact_destination.filename must be a filename, not a path")
    require_non_empty_scalar(artifact_destination, "write_reason", failures, path="artifact_destination")

    validation_passed = normalize_scalar(validation_result.get("passed"))
    write_allowed = normalize_scalar(artifact_destination.get("write_allowed"))
    if validation_passed == "false" and write_allowed == "true":
        failures.append(
            "artifact_destination.write_allowed cannot be true when validation_result.passed is false"
        )

    steps_completed = require_list(execution_trace, "steps_completed", failures, path="execution_trace")
    if steps_completed is not None and not steps_completed:
        failures.append("execution_trace.steps_completed must not be empty")
    halted_at = normalize_scalar(execution_trace.get("halted_at"))
    halt_reason = normalize_scalar(execution_trace.get("reason"))
    require_non_empty_scalar(execution_trace, "runtime_state", failures, path="execution_trace")
    if validation_passed == "false" or write_allowed == "false":
        if not halted_at:
            failures.append("execution_trace.halted_at must be populated when halted")
        if not halt_reason:
            failures.append("execution_trace.reason must be populated when halted")
    elif halted_at and not halt_reason:
        warnings.append("execution_trace.halted_at is set but execution_trace.reason is missing")

    gate = None
    if isinstance(validation_result.get("conformance_gate"), dict):
        gate = validation_result["conformance_gate"]
    elif isinstance(envelope.get("conformance_gate"), dict):
        gate = envelope["conformance_gate"]

    if gate is None:
        failures.append("missing required conformance_gate record")
    else:
        gate_status = normalize_scalar(gate.get("status"))
        gate_protocol = normalize_scalar(gate.get("protocol"))
        gate_step = normalize_scalar(gate.get("evaluated_at_step"))
        if gate_protocol != "command-conformance-gate.md":
            failures.append("conformance_gate.protocol must be command-conformance-gate.md")
        if gate_step != "end_of_command_run":
            failures.append("conformance_gate.evaluated_at_step must be end_of_command_run")
        if gate_status not in {"pass", "fail"}:
            failures.append("conformance_gate.status must be pass|fail")
        cr = gate.get("checks_run")
        if cr is not None:
            if not isinstance(cr, dict):
                failures.append("conformance_gate.checks_run must be a mapping")
            else:
                for sub in ("total", "passed", "failed"):
                    v = cr.get(sub)
                    if v is not None and not isinstance(v, int):
                        failures.append(f"conformance_gate.checks_run.{sub} must be an integer when present")

    gate_status_final = normalize_scalar(gate.get("status")) if isinstance(gate, dict) else None

    if failures:
        if validation_passed == "true":
            failures.append("validation_result.passed is true but gate checks failed")
        if gate_status_final == "pass":
            failures.append("conformance_gate.status must be fail when any gate check fails")
    else:
        if validation_passed == "false":
            failures.append("validation_result.passed is false but all gate checks passed")
        elif validation_passed != "true":
            failures.append(
                "validation_result.passed must be explicitly true when all gate checks pass"
            )
        if write_allowed != "true":
            failures.append(
                "artifact_destination.write_allowed must be true when all gate checks pass"
            )
        if gate_status_final != "pass":
            failures.append("conformance_gate.status must be pass when all gate checks pass")

    if write_allowed == "true" and failures:
        failures.append("artifact_destination.write_allowed cannot be true when any gate check fails")

    if failures:
        print("FAIL: runtime IO conformance check failed")
        for item in failures:
            print(f"- {item}")
        if warnings:
            print("WARN:")
            for item in warnings:
                print(f"- {item}")
        return 1

    print("PASS: runtime IO conformance check passed")
    if warnings:
        print("WARN:")
        for item in warnings:
            print(f"- {item}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
