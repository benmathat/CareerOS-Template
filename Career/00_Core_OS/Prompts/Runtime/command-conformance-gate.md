---
Last Update: 2026-05-05
Previous Update:
---

# Command Conformance Gate (Deterministic End-of-Run Protocol)

## 1. Purpose

Define a deterministic conformance gate that MUST run at the end of every command execution.

This gate is a manual protocol (script-backable) that enforces:

- required runtime object completeness
- status/blocking correctness
- source and boundary compliance
- artifact write safety

If any required gate check fails, execution MUST stop and artifact writes MUST be blocked.

---

## 2. Invocation Timing

Run this gate after runtime object emission and before final artifact write confirmation.

Required sequence:

1. Emit runtime objects (`runtime-io-schema.md`)
2. Run command conformance gate (this file)
3. If pass -> finalize write and return success
4. If fail -> halt and return structured failure state

---

## 3. Required Gate Checks (All Must Pass)

### A) Runtime Object Presence

- [ ] `request` exists
- [ ] `task` exists
- [ ] `mode_selection` exists
- [ ] `routing_output` exists
- [ ] `context_block` exists
- [ ] `prompt_object` exists
- [ ] `output` exists
- [ ] `validation_result` exists
- [ ] `artifact_destination` exists
- [ ] `execution_trace` exists

### B) Status and Blocking Integrity

- [ ] `mode_selection.status` is not `invalid`
- [ ] `mode_selection.blocking` is `false`
- [ ] `routing_output.status` is not `invalid`
- [ ] `routing_output.blocking` is `false`
- [ ] `context_block.status` is not `partial_blocking`
- [ ] `context_block.handoff.prompt_assembler_ready` is `true`
- [ ] `context_block.handoff.execution_may_continue` is `true`

### C) `task` and Output Compliance

- [ ] `task.output_type` is valid (`Document|Framework|Template|Checklist|Analysis`)
- [ ] `validation_result.passed` reflects actual check outcomes
- [ ] Output structure matches `task.output_type` contract
- [ ] Output hard constraints are satisfied

### D) Boundary and Grounding Compliance

- [ ] No claims outside loaded context unless labeled assumptions
- [ ] Assumptions requiring labels are visible in output
- [ ] No canonical/presentation boundary violations
- [ ] No excluded source used as authority

### E) Artifact Routing Safety

- [ ] `artifact_destination.path` matches workflow scope
- [ ] `artifact_destination.write_allowed` is `true` only when all required checks pass
- [ ] No artifact write occurs when `validation_result.passed` is `false`

### F) Halt Trace Integrity

When halted:

- [ ] `execution_trace.halted_at` is populated
- [ ] `execution_trace.reason` is populated
- [ ] upstream runtime objects are preserved

---

## 4. Deterministic Fail Policy (Hard Stop)

If any required check fails:

- Set `validation_result.passed: false`
- Append failures to `validation_result.failures`
- Set `artifact_destination.write_allowed: false`
- Set `artifact_destination.write_reason: Conformance gate failed`
- Set `execution_trace.halted_at: command_conformance_gate`
- Set `execution_trace.reason` to the first blocking failure
- STOP command finalization

No exceptions.

---

## 5. Gate Output Record (Required)

Each command run MUST emit:

```yaml
conformance_gate:
  protocol: command-conformance-gate.md
  status: pass|fail
  checks_run:
    total:
    passed:
    failed:
  failures:
  evaluated_at_step: end_of_command_run
```

This record may be included under `validation_result` or as a sibling runtime object extension.

---

## 6. Script-Backed Validation (Required)

At end of each command run, execute:

```bash
scripts/run_command_gate.sh ".cursor/runtime/<command-name>.runtime-io.yaml"
```

Rules:

- Exit code `0` = gate pass
- Non-zero exit code = gate fail and mandatory stop
- Do NOT finalize writes on non-zero exit
- Runtime IO file path convention: `.cursor/runtime/<command-name>.runtime-io.yaml`
- The validator parses **structured YAML** (PyYAML). Invalid YAML, ambiguous documents, or envelopes where a required root object is not a mapping MUST fail the gate.
- Dependency: `pip install -r scripts/requirements-runtime-validator.txt` (or run `scripts/run_command_gate.sh`, which installs it if missing).
- Runtime IO MUST include machine-verifiable compliance fields:
  - `validation_result.checks.constraints_satisfied`
  - `validation_result.checks.output_structure_compliant`
  - `validation_result.checks.source_grounding_compliant`
  - `validation_result.checks.boundary_rules_compliant`
  - `validation_result.checks.assumption_labels_present`
  - `output.disclosures.assumptions_labeled`
  - `validation_result.conformance_gate`

The script-backed validator MUST preserve:

- deterministic check order
- deterministic fail policy
- deterministic emitted failure signals

---

## 7. Summary

This gate enforces deterministic command finalization.

No command may finish successfully unless required runtime objects, statuses, boundaries, and write safety checks all pass.
