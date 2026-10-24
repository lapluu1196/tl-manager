"""Security and integration boundary tests; never contact a real Jira server."""

import contextlib
import io
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch
from urllib.error import HTTPError, URLError
from urllib.request import Request

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import credentials
import jira_check
import jira_mcp
import setup_mcp


class PrivateWorkspace(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / ".local").mkdir(mode=0o700)
        self.token = "test-only-fake-token"

    def save(self):
        credentials.save_jira_credentials(self.root, "https://jira.example.test", self.token)


class CredentialsTests(PrivateWorkspace):
    def test_round_trip_permissions_and_literal_values(self):
        token = "fake$(not-a-command)=token"
        credentials.save_jira_credentials(self.root, "https://jira.example.test/jira/", token)
        self.assertEqual(credentials.load_jira_credentials(self.root), {
            "JIRA_URL": "https://jira.example.test/jira", "JIRA_PERSONAL_TOKEN": token
        })
        self.assertEqual(stat.S_IMODE((self.root / ".local/secrets.env").stat().st_mode), 0o600)

    def test_invalid_urls_and_tokens_fail_without_echo(self):
        for url in ["http://jira.test", "https://u:p@jira.test", "https://jira.test?a=b",
                    "https://jira.test/#fragment", "https://jira.test\n", "https://jira.test:bad",
                    "https://jira.test\\@evil.test", "https://jira.test:99999"]:
            with self.subTest(url=url), self.assertRaises(credentials.IntegrationError):
                credentials.save_jira_credentials(self.root, url, self.token)
        for token in ["", "secret\nINJECT=true", "secret\r", "secret token"]:
            with self.subTest(token=token), self.assertRaises(credentials.IntegrationError) as error:
                credentials.save_jira_credentials(self.root, "https://jira.test", token)
            if token:
                self.assertNotIn(token, str(error.exception))

    def test_rejects_unsafe_permissions_and_symlinks(self):
        self.save()
        path = self.root / ".local/secrets.env"
        path.chmod(0o644)
        with self.assertRaises(credentials.IntegrationError):
            credentials.load_jira_credentials(self.root)
        with self.assertRaises(credentials.IntegrationError):
            credentials.save_jira_credentials(self.root, "https://jira.test", self.token)
        path.unlink()
        outside = self.root / "outside"
        outside.write_text("unchanged")
        path.symlink_to(outside)
        with self.assertRaises(credentials.IntegrationError):
            credentials.save_jira_credentials(self.root, "https://jira.test", self.token)
        self.assertEqual(outside.read_text(), "unchanged")
        path.unlink()
        (self.root / ".local").chmod(0o755)
        with self.assertRaises(credentials.IntegrationError):
            credentials.save_jira_credentials(self.root, "https://jira.test", self.token)

    def test_directory_symlink_rejected(self):
        local = self.root / ".local"
        local.rmdir()
        outside = self.root / "private"
        outside.mkdir(mode=0o700)
        local.symlink_to(outside, target_is_directory=True)
        with self.assertRaises(credentials.IntegrationError):
            credentials.load_jira_credentials(self.root)

    def test_missing_duplicate_or_malformed_credentials_rejected(self):
        for content in ["JIRA_URL=https://jira.test\n", "not an assignment\n",
                        "JIRA_URL=https://jira.test\nJIRA_URL=https://evil.test\n",
                        "JIRA_URL=https://jira.test\nJIRA_PERSONAL_TOKEN=secret\r\n"]:
            credentials.secure_write(self.root, "secrets.env", content)
            with self.assertRaises(credentials.IntegrationError):
                credentials.load_jira_credentials(self.root)

    def test_preserves_other_credentials_when_rotating_jira(self):
        credentials.secure_write(self.root, "secrets.env", "OTHER_TOKEN=literal$VALUE\n")
        self.save()
        self.assertIn("OTHER_TOKEN=literal$VALUE", (self.root / ".local/secrets.env").read_text())

    def test_private_read_rejects_path_escape(self):
        outside = self.root / "outside"
        outside.write_text("private")
        outside.chmod(0o600)
        with self.assertRaises(credentials.IntegrationError):
            credentials.secure_read(self.root, "../outside")

    def test_cli_uses_hidden_prompt_and_has_no_token_argument(self):
        with patch.object(credentials, "ROOT", self.root), \
             patch.object(credentials.getpass, "getpass", return_value=self.token) as prompt, \
             contextlib.redirect_stdout(io.StringIO()) as output:
            result = credentials.main(["set-jira-token", "--url", "https://jira.test"])
        self.assertEqual(result, 0)
        self.assertEqual(prompt.call_count, 1)
        self.assertNotIn(self.token, output.getvalue())
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            credentials.main(["set-jira-token", "--url", "https://jira.test", "--token", "forbidden"])

    def test_cli_refuses_getpass_fallback_without_printing_secret(self):
        with patch.object(credentials.getpass, "getpass", side_effect=credentials.getpass.GetPassWarning), \
             contextlib.redirect_stderr(io.StringIO()) as error:
            result = credentials.main(["set-jira-token", "--url", "https://jira.test"])
        self.assertEqual(result, 1)
        self.assertNotIn(self.token, error.getvalue())

    def test_project_filter_is_validated(self):
        self.save()
        existing = credentials.secure_read(self.root, "secrets.env")
        credentials.secure_write(self.root, "secrets.env", existing + "JIRA_PROJECTS_FILTER=APP,CORE\n")
        self.assertEqual(credentials.load_jira_credentials(self.root)["JIRA_PROJECTS_FILTER"], "APP,CORE")
        credentials.secure_write(self.root, "secrets.env", existing + "JIRA_PROJECTS_FILTER=APP OR 1=1\n")
        with self.assertRaises(credentials.IntegrationError):
            credentials.load_jira_credentials(self.root)


class LauncherTests(PrivateWorkspace):
    def test_child_env_is_clean_and_forces_read_only(self):
        env = jira_mcp.child_environment(
            {"JIRA_URL": "https://jira.test", "JIRA_PERSONAL_TOKEN": self.token},
            {"PATH": "/usr/bin", "HOME": "/home/test", "JIRA_API_TOKEN": "bad",
             "JIRA_USERNAME": "bad", "JIRA_OAUTH_ACCESS_TOKEN": "bad",
             "CONFLUENCE_PERSONAL_TOKEN": "bad", "READ_ONLY_MODE": "false",
             "MCP_VERY_VERBOSE": "true", "ENABLED_TOOLS": "jira_delete_issue",
             "PYTHONPATH": "/untrusted", "UV_INSECURE_HOST": "jira.test"},
        )
        self.assertEqual(env["JIRA_PERSONAL_TOKEN"], self.token)
        self.assertEqual(env["READ_ONLY_MODE"], "true")
        self.assertEqual(env["JIRA_SSL_VERIFY"], "true")
        self.assertEqual(env["MCP_VERY_VERBOSE"], "false")
        self.assertEqual(env["TOOLSETS"], "all")
        self.assertNotIn("JIRA_API_TOKEN", env)
        self.assertNotIn("JIRA_USERNAME", env)
        self.assertNotIn("JIRA_OAUTH_ACCESS_TOKEN", env)
        self.assertNotIn("CONFLUENCE_PERSONAL_TOKEN", env)
        self.assertNotIn("UV_INSECURE_HOST", env)
        self.assertNotIn("PYTHONPATH", env)
        self.assertNotIn("jira_delete_issue", env["ENABLED_TOOLS"])

    def test_launch_is_pinned_stdio_without_token_in_arguments(self):
        self.save()
        with patch.object(jira_mcp.shutil, "which", return_value="/usr/bin/uvx"), \
             patch.object(jira_mcp.os, "execvpe") as execute, \
             contextlib.redirect_stdout(io.StringIO()) as stdout:
            jira_mcp.launch(self.root)
        binary, argv, env = execute.call_args.args
        self.assertEqual(binary, "/usr/bin/uvx")
        self.assertIn("mcp-atlassian==0.23.1", argv)
        self.assertIn("--env-file", argv)
        self.assertIn(os.devnull, argv)
        self.assertIn("stdio", argv)
        self.assertNotIn(self.token, " ".join(argv))
        self.assertEqual(stdout.getvalue(), "")

    def test_missing_uvx_and_exec_failure_are_safe(self):
        self.save()
        with patch.object(jira_mcp.shutil, "which", return_value=None), self.assertRaises(credentials.IntegrationError):
            jira_mcp.launch(self.root)
        with patch.object(jira_mcp.shutil, "which", return_value="/usr/bin/uvx"), \
             patch.object(jira_mcp.os, "execvpe", side_effect=OSError(self.token)), \
             self.assertRaises(credentials.IntegrationError) as error:
            jira_mcp.launch(self.root)
        self.assertNotIn(self.token, str(error.exception))


class HttpTests(PrivateWorkspace):
    def response(self, payload):
        response = Mock()
        response.read.return_value = json.dumps(payload).encode()
        response.__enter__ = Mock(return_value=response)
        response.__exit__ = Mock(return_value=False)
        return response

    def test_https_auth_request_has_timeout_and_context_path(self):
        opener = Mock()
        opener.open.return_value = self.response({"active": True})
        with patch.object(jira_check, "build_opener", return_value=opener):
            client = jira_check.JiraClient({"JIRA_URL": "https://jira.test/jira", "JIRA_PERSONAL_TOKEN": self.token})
            self.assertEqual(client.get("/rest/api/2/myself"), {"active": True})
        request = opener.open.call_args.args[0]
        self.assertEqual(request.full_url, "https://jira.test/jira/rest/api/2/myself")
        self.assertEqual(request.get_header("Authorization"), "Bearer " + self.token)
        self.assertEqual(request.get_header("User-agent"), "tl-manager/1.0")
        self.assertEqual(request.get_method(), "GET")
        self.assertEqual(opener.open.call_args.kwargs["timeout"], 20)

    def test_redirect_refused_for_every_status(self):
        handler = jira_check.NoRedirect()
        for status in [301, 302, 303, 307, 308]:
            with self.subTest(status=status), self.assertRaises(credentials.IntegrationError):
                handler.redirect_request(Request("https://jira.test"), None, status, "redirect", {}, "https://evil.test")

    def test_http_network_and_malformed_errors_do_not_echo_body(self):
        opener = Mock()
        with patch.object(jira_check, "build_opener", return_value=opener):
            client = jira_check.JiraClient({"JIRA_URL": "https://jira.test", "JIRA_PERSONAL_TOKEN": self.token})
        for error in [HTTPError("https://jira.test", 401, self.token, {}, io.BytesIO(self.token.encode())),
                      URLError(self.token), TimeoutError(self.token)]:
            opener.open.side_effect = error
            with self.assertRaises(credentials.IntegrationError) as caught:
                client.get("/rest/api/2/myself")
            self.assertNotIn(self.token, str(caught.exception))
        opener.open.side_effect = None
        response = self.response({})
        response.read.return_value = self.token.encode()
        opener.open.return_value = response
        with self.assertRaises(credentials.IntegrationError) as caught:
            client.get("/rest/api/2/myself")
        self.assertNotIn(self.token, str(caught.exception))

    def test_discovery_is_minimal_private_and_no_names_on_stdout(self):
        self.save()
        metadata = [
            {"active": True, "displayName": "Private Person"},
            [{"id": "customfield_10000", "name": "Story Points", "custom": True}],
            [{"id": "100", "key": "PRIVATE", "name": "Private Project", "irrelevant": "private"}],
            {"values": [{"id": 10, "name": "Private Board", "type": "scrum", "other": "private"}], "isLast": True},
            [{"id": "3", "name": "In Progress", "statusCategory": {"key": "indeterminate"}}],
        ]
        with patch.object(jira_check.JiraClient, "get", side_effect=metadata) as get, \
             contextlib.redirect_stdout(io.StringIO()) as stdout:
            jira_check.check(self.root, discover=True)
        output = stdout.getvalue()
        for name in ("Private Person", "Private Project", "Private Board"):
            self.assertNotIn(name, output)
        self.assertNotIn("PRIVATE", output)
        self.assertIn("customfield_10000", output)
        path = self.root / ".local/jira-discovery.json"
        self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
        payload = json.loads(path.read_text())
        self.assertEqual(payload["projects"][0]["key"], "PRIVATE")
        self.assertNotIn("irrelevant", payload["projects"][0])
        self.assertEqual(get.call_count, 5)

    def test_boards_paginate_and_reject_missing_progress(self):
        client = Mock()
        client.get.side_effect = [
            {"values": [{"id": 1, "name": "First", "type": "scrum"}], "isLast": False, "startAt": 0},
            {"values": [{"id": 2, "name": "Second", "type": "scrum"}], "isLast": True, "startAt": 1},
        ]
        self.assertEqual(len(jira_check.discover_boards(client)), 2)
        self.assertIn("startAt=1", client.get.call_args.args[0])
        client.get.side_effect = [{"values": [], "isLast": False}]
        with self.assertRaises(credentials.IntegrationError):
            jira_check.discover_boards(client)

    def test_board_access_failure_still_records_valid_auth_and_incomplete_discovery(self):
        self.save()
        with patch.object(jira_check.JiraClient, "get", side_effect=[
            {"active": True}, [], [], credentials.IntegrationError("Jira HTTP 403."), []
        ]), contextlib.redirect_stdout(io.StringIO()) as stdout:
            jira_check.check(self.root, discover=True)
        data = json.loads((self.root / ".local/jira-discovery.json").read_text())
        self.assertFalse(data["boards_complete"])
        self.assertIn("unavailable", stdout.getvalue())

    def test_repeated_board_page_is_incomplete(self):
        client = Mock()
        client.get.return_value = {"values": [{"id": 1, "name": "First"}], "isLast": False}
        with self.assertRaises(credentials.IntegrationError):
            jira_check.discover_boards(client)
        self.assertEqual(client.get.call_count, 2)

    def test_inactive_account_fails_before_discovery(self):
        self.save()
        with patch.object(jira_check.JiraClient, "get", return_value={"active": False}) as get, \
             self.assertRaises(credentials.IntegrationError):
            jira_check.check(self.root, discover=True)
        self.assertEqual(get.call_count, 1)
        self.assertFalse((self.root / ".local/jira-discovery.json").exists())


class SetupTests(PrivateWorkspace):
    def test_inline_mcp_table_reports_safe_error_without_modification(self):
        directory = self.root / ".codex"
        directory.mkdir()
        path = directory / "config.toml"
        original = 'mcp_servers = { other = { command = "custom" } }\n'
        path.write_text(original)
        with self.assertRaises(credentials.IntegrationError):
            setup_mcp.configure(self.root)
        self.assertEqual(path.read_text(), original)

    def test_help_and_unknown_arguments_never_write_config(self):
        for arguments, expected_status in [(["--help"], 0), (["--unexpected"], 2)]:
            with patch.object(setup_mcp, "configure") as configure, \
                 contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()), \
                 self.assertRaises(SystemExit) as exit_status:
                setup_mcp.main(arguments)
            self.assertEqual(exit_status.exception.code, expected_status)
            configure.assert_not_called()

    def test_setup_preserves_unrelated_settings_and_is_idempotent(self):
        directory = self.root / ".codex"
        directory.mkdir()
        path = directory / "config.toml"
        original = '[features]\nmulti_agent = true\n\n[mcp_servers.other]\ncommand = "other"\n'
        path.write_text(original)
        self.assertTrue(setup_mcp.configure(self.root))
        first = path.read_text()
        self.assertTrue(first.startswith(original))
        self.assertFalse(setup_mcp.configure(self.root))
        self.assertEqual(first, path.read_text())
        parsed = setup_mcp.tomllib.loads(first)
        config = parsed["mcp_servers"]["jira_datacenter"]
        self.assertTrue(Path(config["command"]).is_absolute())
        self.assertTrue(Path(config["args"][0]).is_absolute())
        self.assertEqual(config["enabled_tools"], list(jira_mcp.ENABLED_TOOLS))
        self.assertNotIn(self.token, first)

    def test_conflicting_entry_or_symlink_is_not_overwritten(self):
        directory = self.root / ".codex"
        directory.mkdir()
        path = directory / "config.toml"
        original = '[mcp_servers.jira_datacenter]\ncommand = "custom"\n'
        path.write_text(original)
        with self.assertRaises(credentials.IntegrationError):
            setup_mcp.configure(self.root)
        self.assertEqual(path.read_text(), original)
        path.unlink()
        target = self.root / "outside-config"
        target.write_text("original")
        path.symlink_to(target)
        with self.assertRaises(credentials.IntegrationError):
            setup_mcp.configure(self.root)
        self.assertEqual(target.read_text(), "original")


if __name__ == "__main__":
    unittest.main()
