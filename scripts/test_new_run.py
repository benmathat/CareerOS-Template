#!/usr/bin/env python3
"""Tests for `careeros new-run` (stdlib + PyYAML).

    python3 scripts/test_new_run.py

The structural test fills each scaffolded skeleton's TODO slots with values from
a real, valid past run of the same command and requires the conformance gate to
pass. If the runtime IO schema or validator changes, the skeleton must change
with it or this fails.
"""
import copy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import new_run  # noqa: E402

try:
    import yaml
except ImportError:  # run_command_gate.sh installs it on first use
    yaml = None

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "Career/00_Core_OS/Runs"
CAREEROS = str(ROOT / "scripts/careeros")

# command -> a known-good past run to take judgment values from
REFERENCES = {
    "log-activity": "2026-10-07_log-activity_hp_strategic_programs_manager_application_submitted",
    "promote-opportunity": "2026-10-07_promote-opportunity_hp_strategic_programs_manager",
    "analyze-opportunity": "2026-10-07_analyze-opportunity_hp_strategic_programs_manager",
    "discuss-opportunity": "2026-11-03_discuss-opportunity_one_degree_head_of_product_engineering_2026_11_03",
    "build-resume": "2026-10-07_build-resume_hp_strategic_programs_manager",
    "intake-job": "2026-10-07_intake-job_hp_strategic_programs_manager",
}


def overlay(skel, ref, path="runtime_io"):
    """Replace TODO slots in skel with the same-path value from ref."""
    if skel == new_run.MARKER:
        return copy.deepcopy(ref)
    if isinstance(skel, dict):
        out = {}
        for k, v in skel.items():
            if not isinstance(ref, dict) or k not in ref:
                raise AssertionError(f"skeleton key not in reference run: {path}.{k}")
            out[k] = overlay(v, ref[k], f"{path}.{k}")
        return out
    if isinstance(skel, list) and new_run.MARKER in skel:
        kept = [x for x in skel if x != new_run.MARKER]
        extra = [x for x in (ref or []) if x not in kept]
        return kept + extra if kept else list(ref)
    if isinstance(skel, list):
        return [overlay(s, ref[i] if i < len(ref) else ref[-1], f"{path}[{i}]") for i, s in enumerate(skel)] \
            if skel and isinstance(skel[0], dict) else skel
    return skel


def gate(path):
    r = subprocess.run([CAREEROS, "gate", str(path)], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


@unittest.skipUnless(yaml, "PyYAML not installed")
class Scaffold(unittest.TestCase):
    def test_filled_sourcing_scaffold_passes_gate_without_pack_or_pipeline(self):
        ref_path = RUNS / (REFERENCES["log-activity"] + ".runtime-io.yaml")
        if not ref_path.exists():
            self.skipTest("reference runtime fixture not present")
        # Borrow generic judgment fields; keep sourcing's command, mode, scope
        # destination and absent-pack declarations from its own scaffold.
        text = new_run.render("source-opportunities", "weekly", "2026-01-02", None,
                              "2026-01-02_weekly.md", None)
        filled = overlay(yaml.safe_load(text), yaml.safe_load(ref_path.read_text()))
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "run.runtime-io.yaml"
            path.write_text(yaml.safe_dump(filled, sort_keys=False))
            rc, output = gate(path)
        self.assertEqual(rc, 0, output)

    def test_every_command_renders_valid_yaml(self):
        for cmd in new_run.COMMANDS:
            text = new_run.render(cmd, "some_slug", "2026-01-02", "acme_role_2026-01-02", None, None)
            data = yaml.safe_load(text)
            self.assertEqual(data["runtime_io"]["request"]["command"], f"/{cmd}")
            self.assertTrue(new_run.unfilled_lines(text), cmd)

    def test_skeleton_fails_gate_until_filled(self):
        text = new_run.render("log-activity", "x", "2026-01-02", None, None, None)
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "run.runtime-io.yaml"
            p.write_text(text)
            rc, out = gate(p)
        self.assertEqual(rc, 1)
        self.assertIn("unfilled TODO", out)

    def test_filled_skeleton_passes_gate(self):
        for cmd, ref_name in REFERENCES.items():
            ref_path = RUNS / f"{ref_name}.runtime-io.yaml"
            if not ref_path.exists():
                self.skipTest(f"reference run not present: {ref_name}")
            with self.subTest(command=cmd):
                ref = yaml.safe_load(ref_path.read_text())
                text = new_run.render(cmd, "some_slug", "2026-10-07", "acme_role_2026-10-07", None, None)
                filled = overlay(yaml.safe_load(text), ref)
                with tempfile.TemporaryDirectory() as d:
                    p = Path(d) / "run.runtime-io.yaml"
                    p.write_text(yaml.safe_dump(filled, sort_keys=False))
                    rc, out = gate(p)
                self.assertEqual(rc, 0, out)


class Cli(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([CAREEROS, "new-run", *args], capture_output=True, text=True)

    def test_unknown_command(self):
        self.assertEqual(self.run_cli("no-such-command", "x").returncode, 2)

    def test_bad_date(self):
        self.assertEqual(self.run_cli("log-activity", "x", "--date", "10/07/2026").returncode, 2)

    def test_unnormalized_target(self):
        self.assertEqual(self.run_cli("build-resume", "x", "--target", "Some Folder").returncode, 2)

    @unittest.skipUnless(yaml, "PyYAML not installed")
    def test_sourcing_scaffold_does_not_publish_or_change_history(self):
        slug = "zz_sourcing_selftest"
        run = RUNS / f"2099-01-01_source-opportunities_{slug}.runtime-io.yaml"
        research = ROOT / "Career/09_Research_and_Market_Intelligence/Opportunity_Sourcing"
        history = research / "sourcing-history.md"
        before = history.read_bytes()
        report = research / "Reports/2099-01-01_weekly.md"
        self.assertFalse(report.exists())
        try:
            result = self.run_cli("source-opportunities", slug, "--date", "2099-01-01",
                                  "--file", report.name)
            self.assertEqual(result.returncode, 0, result.stderr)
            data = yaml.safe_load(run.read_text())["runtime_io"]
            self.assertEqual(data["artifact_destination"]["class"], "execution")
            self.assertEqual(data["artifact_destination"]["filename"], report.name)
            rc, output = gate(run)
            self.assertNotEqual(rc, 0, output)  # Unfilled research cannot be published.
            self.assertFalse(report.exists())
            self.assertEqual(history.read_bytes(), before)
        finally:
            run.unlink(missing_ok=True)

    def test_writes_once_and_never_overwrites(self):
        slug = "zz_new_run_selftest"
        path = ROOT / "Career/00_Core_OS/Runs" / f"2099-01-01_log-activity_{slug}.runtime-io.yaml"
        try:
            first = self.run_cli("log-activity", slug, "--date", "2099-01-01")
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertTrue(path.exists())
            self.assertEqual(first.stdout.strip(), str(path.relative_to(ROOT)))
            second = self.run_cli("log-activity", slug, "--date", "2099-01-01")
            self.assertEqual(second.returncode, 1)
        finally:
            path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
