# Runtime IO Staging

This directory stores per-command runtime emission files used by the CareerOS command conformance gate.

## Purpose

- Hold structured runtime objects for a command run (`request` through `execution_trace`)
- Provide a deterministic artifact for validation and audit
- Block final writes when conformance fails

## File Convention

- One file per command run:
  - `.cursor/runtime/<command>.runtime-io.yaml`
- Examples:
  - `.cursor/runtime/build-resume.runtime-io.yaml`
  - `.cursor/runtime/build-application.runtime-io.yaml`

## Validation

Before finalizing artifact writes, run:

`scripts/run_command_gate.sh ".cursor/runtime/<command>.runtime-io.yaml"`

The gate validates YAML structure and runtime contract conformance. Non-zero exit means stop and fix the runtime file before continuing.

## Starter Files

Starter runtime files are pre-generated for supported commands in this folder. Replace `STARTER` placeholders with real run data before production use.
