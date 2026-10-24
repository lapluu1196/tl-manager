"""Publication boundaries must hold even for force-added files."""

import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_publication.py"
sys.path.insert(0, str(SCRIPT.parent))
SPEC = importlib.util.spec_from_file_location("publication", SCRIPT)
publication = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(publication)


class PublicationTests(unittest.TestCase):
    def test_private_paths_are_denied(self):
        for path in ("private/report.md", ".local/secrets.env", "x/.env", ".codex/config.toml", "backup/key.pem"):
            with self.subTest(path=path):
                self.assertTrue(publication.private_path(path))

    def test_templates_and_discovery_links_are_allowed(self):
        for path in ("config/credentials.env.example", ".env.example", "skills/daily-risk/assets/input.md", ".agents/skills/daily-risk"):
            with self.subTest(path=path):
                self.assertFalse(publication.private_path(path))

    def test_common_and_configured_secrets_are_detected(self):
        self.assertTrue(publication.secret_content(b"ghp_" + b"a" * 36, ()))
        self.assertTrue(publication.secret_content(b'JIRA_PERSONAL_TOKEN="' + b"a" * 30 + b'"', ()))
        self.assertTrue(publication.secret_content(b'{"api_key": "' + b"a" * 30 + b'"}', ()))
        self.assertTrue(publication.secret_content(b"-----BEGIN " + b"PRIVATE KEY-----", ()))
        self.assertTrue(publication.secret_content(b"embedded sensitive-value marker", (b"sensitive-value",)))

    def test_empty_and_placeholder_values_are_allowed(self):
        self.assertFalse(publication.secret_content(b"JIRA_PERSONAL_TOKEN=\nJIRA_URL=https://jira.example.com\n", ()))
        self.assertFalse(publication.secret_content(b'JIRA_PERSONAL_TOKEN="your_token_here"', ()))

    def test_source_expressions_and_deliberate_fake_values_are_allowed(self):
        for filename in (SCRIPT, SCRIPT.parent / "credentials.py", Path(__file__),
                         Path(__file__).with_name("test_jira.py")):
            with self.subTest(filename=filename.name):
                self.assertFalse(publication.secret_content(filename.read_bytes(), ()))

    def test_literal_assignments_are_detected_in_supported_formats(self):
        value = b"z" * 32
        for content in (b"JIRA_PERSONAL_TOKEN=" + value, b'token = "' + value + b'"',
                        b'{"api_key": "' + value + b'"}'):
            self.assertTrue(publication.secret_content(content, ()))

    def test_scanner_checks_index_not_worktree_and_redacts(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            file = root / "report.md"
            value = "ghp_" + "z" * 36
            file.write_text(value)
            subprocess.run(["git", "-C", str(root), "add", "report.md"], check=True)
            file.write_text("safe worktree")
            issues = publication.check_index(root)
            self.assertEqual(len(issues), 1)
            self.assertIn("report.md", issues[0])
            self.assertNotIn(value, issues[0])

    def test_local_secret_is_detected_in_other_file(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / ".local").mkdir(mode=0o700)
            (root / ".local" / "secrets.env").write_text("JIRA_PERSONAL_TOKEN=arbitrary-private-value\n")
            (root / ".local" / "secrets.env").chmod(0o600)
            (root / "notes.md").write_text("arbitrary-private-value")
            subprocess.run(["git", "-C", str(root), "add", "notes.md"], check=True)
            self.assertTrue(publication.check_index(root))

    def test_local_secret_reader_rejects_symlinks_and_unsafe_permissions(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            local = root / ".local"
            local.mkdir(mode=0o700)
            self.assertEqual(publication.local_secrets(root), ())
            secret = local / "secrets.env"
            secret.write_text("JIRA_PERSONAL_TOKEN=" + "x" * 24 + "\n")
            secret.chmod(0o644)
            with self.assertRaises(publication.IntegrationError):
                publication.local_secrets(root)
            secret.chmod(0o600)
            secret.rename(local / "other.env")
            secret.symlink_to(local / "other.env")
            with self.assertRaises(publication.IntegrationError):
                publication.local_secrets(root)
            secret.unlink()
            local.rename(root / "outside")
            local.symlink_to(root / "outside", target_is_directory=True)
            with self.assertRaises(publication.IntegrationError):
                publication.local_secrets(root)

    def test_history_blocks_secret_removed_from_latest_commit(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            file = root / "notes.md"
            value = "ghp_" + "z" * 36
            file.write_text(value)
            self.commit(root, "initial")
            file.write_text("safe latest revision")
            self.commit(root, "remove")
            self.assertFalse(publication.check_index(root))
            problems = publication.check_history(root)
            self.assertTrue(problems)
            self.assertNotIn(value, "\n".join(problems))
            result = subprocess.run([sys.executable, str(SCRIPT), "--history"],
                                    cwd=root, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn(value, result.stderr)

    def test_history_blocks_private_file_removed_from_latest_commit(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / "private").mkdir()
            file = root / "private/review.md"
            file.write_text("internal review")
            self.commit(root, "initial")
            file.unlink()
            self.commit(root, "remove")
            self.assertFalse(publication.check_index(root))
            self.assertTrue(publication.check_history(root))

    def test_history_accepts_unborn_and_clean_repositories(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            self.assertFalse(publication.check_history(root))
            (root / "README.md").write_text("Safe template")
            self.commit(root, "initial")
            self.assertFalse(publication.check_history(root))

    @staticmethod
    def commit(root, message):
        subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(root), "-c", "user.name=Test", "-c",
                        "user.email=test@example.com", "-c", "commit.gpgsign=false",
                        "-c", "core.hooksPath=/dev/null",
                        "commit", "-qm", message], check=True)

    def test_force_added_private_data_is_denied(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / "private").mkdir()
            (root / "private" / "review.md").write_text("internal report")
            subprocess.run(["git", "-C", str(root), "add", "-f", "private/review.md"], check=True)
            self.assertTrue(publication.check_index(root))

    def test_cli_safe_repository_and_error(self):
        import sys
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            failed = subprocess.run([sys.executable, str(SCRIPT)], cwd=root, capture_output=True, text=True)
            self.assertNotEqual(failed.returncode, 0)
            self.assertNotIn("Traceback", failed.stderr)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / "README.md").write_text("Safe template")
            subprocess.run(["git", "-C", str(root), "add", "README.md"], check=True)
            passed = subprocess.run([sys.executable, str(SCRIPT)], cwd=root, capture_output=True, text=True)
            self.assertEqual(passed.returncode, 0, passed.stderr)


if __name__ == "__main__":
    unittest.main()
