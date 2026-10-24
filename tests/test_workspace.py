"""Workspace lifecycle and filesystem boundary tests, using isolated workspaces."""

import contextlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import workspace


class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "workspace"
        self.root.mkdir()
        (self.root / "config").mkdir()
        self.registry = {"schema_version": 1, "workstreams": [self.entry("daily-risk")]}
        self.write_json("config/workstreams.json", self.registry)
        self.write_json("config/integrations.json", {
            "schema_version": 1, "integrations": [{"id": "jira"}]})
        self.write_json("config/workspace.example.json", {
            "schema_version": 1, "timezone": "Asia/Ho_Chi_Minh",
            "sprint_duration_days": 14})
        (self.root / "config/credentials.env.example").write_text(
            "JIRA_PERSONAL_TOKEN=\n", encoding="utf-8")
        self.create_skill("daily-risk")

    def entry(self, name):
        return {"id": name, "title": "Daily risk", "cadence": "Daily",
                "path": f"skills/{name}", "inputs": ["input.md"],
                "outputs": ["output.md"], "integrations": ["jira"]}

    def create_skill(self, name):
        base = self.root / "skills" / name
        (base / "assets").mkdir(parents=True)
        (base / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: Track risks.\n---\n\n# Risks\n",
            encoding="utf-8")
        for filename in ("input.md", "output.md"):
            (base / "assets" / filename).write_text(f"# {filename}\n", encoding="utf-8")

    def write_json(self, relative, data):
        target = self.root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(data), encoding="utf-8")

    def run_cli(self, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            code = workspace.main(list(args), root=self.root)
        return code, output.getvalue()

    def test_bootstrap_creates_private_paths_and_relative_discovery(self):
        self.assertEqual(self.run_cli("bootstrap")[0], 0)
        for directory in ("private", ".local"):
            self.assertEqual((self.root / directory).stat().st_mode & 0o777, 0o700)
        secrets = self.root / ".local/secrets.env"
        self.assertEqual(secrets.stat().st_mode & 0o777, 0o600)
        link = self.root / ".agents/skills/daily-risk"
        self.assertEqual(link.resolve(), self.root / "skills/daily-risk")
        self.assertFalse(Path(os.readlink(link)).is_absolute())
        self.assertEqual(self.run_cli("validate")[0], 0)

    def test_bootstrap_preserves_configuration_and_secret_values(self):
        self.run_cli("bootstrap")
        secret = self.root / ".local/secrets.env"
        secret.write_text("JIRA_PERSONAL_TOKEN=local-value\n", encoding="utf-8")
        settings = {"timezone": "UTC", "sprint_duration_days": 7}
        self.write_json(".local/workspace.json", settings)
        self.assertEqual(self.run_cli("bootstrap")[0], 0)
        self.assertEqual(json.loads((self.root / ".local/workspace.json").read_text()), settings)
        self.assertIn("local-value", secret.read_text())

    def test_index_and_validate_work_without_local_credentials(self):
        self.assertEqual(self.run_cli("index")[0], 0)
        self.assertEqual(self.run_cli("validate")[0], 0)
        index = (self.root / "INDEX.md").read_text()
        for expected in ("$daily-risk", "skills/daily-risk/SKILL.md", "input.md",
                         "output.md", "private/sprints", "Daily"):
            self.assertIn(expected, index)
        self.assertFalse((self.root / ".local").exists())

    def test_stale_index_reports_repair_command(self):
        (self.root / "INDEX.md").write_text("old", encoding="utf-8")
        code, output = self.run_cli("validate")
        self.assertEqual(code, 1)
        self.assertIn("index", output)

    def test_sprint_dates_templates_and_daily_directory(self):
        self.assertEqual(self.run_cli("new-sprint", "2026-s22", "--start", "2026-10-26")[0], 0)
        sprint = self.root / "private/sprints/2026-s22"
        meta = json.loads((sprint / "metadata.json").read_text())
        self.assertEqual(meta["start"], "2026-10-26")
        self.assertEqual(meta["end_exclusive"], "2026-11-09")
        self.assertEqual(meta["timezone"], "Asia/Ho_Chi_Minh")
        self.assertEqual((sprint / "daily-risk/input.md").read_text(), "# input.md\n")
        self.assertTrue((sprint / "daily-risk/daily").is_dir())
        self.assertEqual((self.root / "private").stat().st_mode & 0o777, 0o700)

    def test_sprint_uses_local_duration_and_timezone(self):
        self.write_json(".local/workspace.json", {"timezone": "UTC", "sprint_duration_days": 7})
        self.assertEqual(self.run_cli("new-sprint", "short", "--start", "2024-02-28")[0], 0)
        meta = json.loads((self.root / "private/sprints/short/metadata.json").read_text())
        self.assertEqual(meta["end_exclusive"], "2024-03-06")
        self.assertEqual(meta["timezone"], "UTC")

    def test_sprint_board_override_and_local_default(self):
        self.write_json(".local/workspace.json", {
            "timezone": "UTC", "sprint_duration_days": 14, "jira": {"board_id": 24}})
        for name, options, expected in (("default", (), 24), ("override", ("--board", "59"), 59)):
            self.assertEqual(self.run_cli("new-sprint", name, "--start", "2026-10-26", *options)[0], 0)
            meta = json.loads((self.root / f"private/sprints/{name}/metadata.json").read_text())
            self.assertEqual(meta["board_id"], expected)
        self.assertEqual(self.run_cli("new-sprint", "invalid", "--start", "2026-10-26", "--board", "-1")[0], 1)
        self.assertFalse((self.root / "private/sprints/invalid").exists())

    def test_existing_sprint_is_never_overwritten(self):
        self.run_cli("new-sprint", "sprint-one", "--start", "2026-10-26")
        target = self.root / "private/sprints/sprint-one/daily-risk/input.md"
        target.write_text("manager data", encoding="utf-8")
        self.assertEqual(self.run_cli("new-sprint", "sprint-one", "--start", "2026-10-26")[0], 1)
        self.assertEqual(target.read_text(), "manager data")

    def test_invalid_sprint_arguments_have_no_side_effects(self):
        for name, start in (("../escape", "2026-10-26"), ("/tmp/escape", "2026-10-26"),
                            ("okay", "2026-02-30"), ("okay", "20261026")):
            with self.subTest(name=name, start=start):
                self.assertEqual(self.run_cli("new-sprint", name, "--start", start)[0], 1)
                self.assertFalse((self.root / "private").exists())

    def test_invalid_sprint_settings_have_no_side_effects(self):
        for settings in ({"timezone": "No/SuchZone", "sprint_duration_days": 14},
                         {"timezone": "UTC", "sprint_duration_days": 0},
                         {"timezone": "UTC", "sprint_duration_days": True},
                         {"timezone": 42}, {"jira": []}, {"jira": {"board_id": True}}):
            self.write_json(".local/workspace.json", settings)
            self.assertEqual(self.run_cli("new-sprint", "one", "--start", "2026-10-26")[0], 1)
            self.assertFalse((self.root / "private").exists())

    def test_sprint_date_overflow_is_reported_without_writes(self):
        code, output = self.run_cli("new-sprint", "overflow", "--start", "9999-12-31")
        self.assertEqual(code, 1)
        self.assertNotIn("Traceback", output)
        self.assertFalse((self.root / "private").exists())

    def test_nontext_template_rejects_before_creating_sprint(self):
        (self.root / "skills/daily-risk/assets/output.md").write_bytes(b"\xff")
        self.assertEqual(self.run_cli("new-sprint", "one", "--start", "2026-10-26")[0], 1)
        self.assertFalse((self.root / "private").exists())

    def test_add_workstream_registers_assets_index_and_discovery(self):
        self.assertEqual(self.run_cli("add-workstream", "release-planning", "--title", "Release planning")[0], 0)
        data = json.loads((self.root / "config/workstreams.json").read_text())
        self.assertEqual(data["workstreams"][-1]["id"], "release-planning")
        self.assertTrue((self.root / "skills/release-planning/assets/input.md").is_file())
        self.assertTrue((self.root / ".agents/skills/release-planning/SKILL.md").is_file())
        self.assertIn("$release-planning", (self.root / "INDEX.md").read_text())
        self.assertEqual(self.run_cli("validate")[0], 0)

    def test_add_invalid_workstream_does_not_write(self):
        original = (self.root / "config/workstreams.json").read_bytes()
        for name, title in (("../escape", "Good"), ("UPPER", "Good"), ("new", ""),
                            ("new", "Bad\nname"), ("new", "Bad | name"), ("daily-risk", "Duplicate")):
            with self.subTest(name=name, title=title):
                self.assertEqual(self.run_cli("add-workstream", name, "--title", title)[0], 1)
                self.assertEqual((self.root / "config/workstreams.json").read_bytes(), original)
                self.assertFalse((self.root / "skills/new").exists())

    def test_registry_rejects_unsafe_and_duplicate_entries(self):
        invalid = [
            {**self.entry("daily-risk"), "path": "../escape"},
            {**self.entry("daily-risk"), "inputs": ["../secret"]},
            {**self.entry("daily-risk"), "integrations": ["missing"]},
            {**self.entry("daily-risk"), "outputs": []},
            {**self.entry("daily-risk"), "title": None},
            {**self.entry("daily-risk"), "outputs": ["input.md"]},
            None,
        ]
        for entry in invalid:
            self.write_json("config/workstreams.json", {"schema_version": 1, "workstreams": [entry]})
            self.assertEqual(self.run_cli("index")[0], 1)
        self.write_json("config/workstreams.json", {
            "schema_version": 1, "workstreams": [self.entry("daily-risk"), self.entry("daily-risk")]})
        self.assertEqual(self.run_cli("index")[0], 1)

    def test_registry_rejects_incompatible_shapes(self):
        for data in ([], {"schema_version": 2, "workstreams": []},
                     {"schema_version": 1, "workstreams": "daily-risk"}):
            self.write_json("config/workstreams.json", data)
            self.assertEqual(self.run_cli("index")[0], 1)

    def test_integrations_registry_rejects_invalid_shapes_and_duplicates(self):
        for data in ({"schema_version": 2}, {"schema_version": 1, "integrations": [None]},
                     {"schema_version": 1, "integrations": [{"id": "jira"}, {"id": "jira"}]}):
            self.write_json("config/integrations.json", data)
            self.assertEqual(self.run_cli("index")[0], 1)

    def test_missing_assets_and_invalid_frontmatter_are_rejected(self):
        path = self.root / "skills/daily-risk/assets/input.md"
        path.unlink()
        self.assertEqual(self.run_cli("index")[0], 1)
        path.write_text("input", encoding="utf-8")
        (self.root / "skills/daily-risk/SKILL.md").write_text("# No frontmatter", encoding="utf-8")
        self.assertEqual(self.run_cli("index")[0], 1)
        (self.root / "skills/daily-risk/SKILL.md").write_text(
            "---\nname: wrong-name\ndescription: Track risks.\n---\n", encoding="utf-8")
        self.assertEqual(self.run_cli("index")[0], 1)
        (self.root / "skills/daily-risk/SKILL.md").unlink()
        self.assertEqual(self.run_cli("index")[0], 1)

    def test_symlink_escape_private_and_local_is_rejected(self):
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        for directory, command in (("private", ("new-sprint", "one", "--start", "2026-10-26")),
                                   (".local", ("bootstrap",))):
            target = self.root / directory
            target.symlink_to(outside, target_is_directory=True)
            self.assertEqual(self.run_cli(*command)[0], 1)
            self.assertEqual(list(outside.iterdir()), [])
            target.unlink()

    def test_symlinked_index_or_asset_cannot_escape(self):
        outside = Path(self.temp.name) / "outside.md"
        outside.write_text("keep", encoding="utf-8")
        (self.root / "INDEX.md").symlink_to(outside)
        self.assertEqual(self.run_cli("index")[0], 1)
        self.assertEqual(outside.read_text(), "keep")
        (self.root / "INDEX.md").unlink()
        asset = self.root / "skills/daily-risk/assets/input.md"
        asset.unlink()
        asset.symlink_to(outside)
        self.assertEqual(self.run_cli("new-sprint", "one", "--start", "2026-10-26")[0], 1)

    def test_discovery_copy_fallback_refreshes_managed_copy(self):
        with patch.object(Path, "symlink_to", side_effect=OSError("No symlinks")):
            self.assertEqual(self.run_cli("bootstrap")[0], 0)
        source = self.root / "skills/daily-risk/assets/input.md"
        source.write_text("updated", encoding="utf-8")
        with patch.object(Path, "symlink_to", side_effect=OSError("No symlinks")):
            self.assertEqual(self.run_cli("bootstrap")[0], 0)
        self.assertEqual((self.root / ".agents/skills/daily-risk/assets/input.md").read_text(), "updated")

    def test_nested_skill_symlink_rejects_before_discovery(self):
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        (self.root / "skills/daily-risk/extra").symlink_to(outside, target_is_directory=True)
        for fallback in (False, True):
            with self.subTest(fallback=fallback):
                context = (patch.object(Path, "symlink_to", side_effect=OSError("No symlinks"))
                           if fallback else contextlib.nullcontext())
                with context:
                    self.assertEqual(self.run_cli("bootstrap")[0], 1)
                self.assertFalse((self.root / ".agents/skills/daily-risk").exists())
                self.assertFalse((self.root / ".local").exists())

    def test_unmanaged_discovery_directory_is_preserved(self):
        target = self.root / ".agents/skills/daily-risk"
        target.mkdir(parents=True)
        (target / "personal.md").write_text("keep", encoding="utf-8")
        self.assertEqual(self.run_cli("bootstrap")[0], 1)
        self.assertEqual((target / "personal.md").read_text(), "keep")

    def test_missing_bootstrap_template_does_not_create_private_dirs(self):
        (self.root / "config/credentials.env.example").unlink()
        self.assertEqual(self.run_cli("bootstrap")[0], 1)
        self.assertFalse((self.root / ".local").exists())

    def test_symlinked_discovery_parent_is_rejected_before_add(self):
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        (self.root / ".agents").symlink_to(outside, target_is_directory=True)
        self.assertEqual(self.run_cli("add-workstream", "release", "--title", "Release")[0], 1)
        self.assertFalse((self.root / "skills/release").exists())
        self.assertEqual(list(outside.iterdir()), [])

    def test_file_in_discovery_parent_rejects_before_any_write(self):
        (self.root / ".agents").write_text("keep", encoding="utf-8")
        self.assertEqual(self.run_cli("bootstrap")[0], 1)
        self.assertFalse((self.root / ".local").exists())
        self.assertEqual(self.run_cli("add-workstream", "release", "--title", "Release")[0], 1)
        self.assertFalse((self.root / "skills/release").exists())

    def test_directory_at_index_rejects_before_scaffolding(self):
        (self.root / "INDEX.md").mkdir()
        self.assertEqual(self.run_cli("add-workstream", "release", "--title", "Release")[0], 1)
        self.assertFalse((self.root / "skills/release").exists())
        self.assertEqual(self.run_cli("bootstrap")[0], 1)
        self.assertFalse((self.root / ".local").exists())

    def test_file_at_discovery_directory_rejects_before_scaffolding(self):
        (self.root / ".agents").mkdir()
        (self.root / ".agents/skills").write_text("keep", encoding="utf-8")
        self.assertEqual(self.run_cli("add-workstream", "release", "--title", "Release")[0], 1)
        self.assertFalse((self.root / "skills/release").exists())

    def test_file_at_private_directory_rejects_before_bootstrap(self):
        (self.root / "private").write_text("keep", encoding="utf-8")
        self.assertEqual(self.run_cli("bootstrap")[0], 1)
        self.assertFalse((self.root / ".local").exists())

    def test_malformed_config_is_concise_without_traceback(self):
        (self.root / "config/workstreams.json").write_text("{broken", encoding="utf-8")
        code, output = self.run_cli("validate")
        self.assertEqual(code, 1)
        self.assertIn("Error:", output)
        self.assertNotIn("Traceback", output)

    def test_cli_works_from_another_current_directory(self):
        scripts = self.root / "scripts"
        scripts.mkdir()
        for filename in ("workspace.py", "workspace_lib.py"):
            shutil.copyfile(Path(workspace.__file__).parent / filename, scripts / filename)
        result = subprocess.run([sys.executable, str(scripts / "workspace.py"), "index"],
                                cwd=self.temp.name, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.root / "INDEX.md").is_file())

    def test_help_names_integration_commands(self):
        result = subprocess.run([sys.executable, workspace.__file__, "--help"],
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0)
        self.assertIn("jira_check.py", result.stdout)
        self.assertIn("setup_mcp.py", result.stdout)


if __name__ == "__main__":
    unittest.main()
