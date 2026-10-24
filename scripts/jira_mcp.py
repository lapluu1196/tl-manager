"""Launch the pinned Jira MCP server with a minimal read-only environment."""

import os
import shutil
import sys

from credentials import IntegrationError, ROOT, load_jira_credentials

MCP_PACKAGE = "mcp-atlassian==0.23.1"
ENABLED_TOOLS = (
    "jira_search", "jira_get_issue", "jira_search_fields", "jira_get_agile_boards",
    "jira_get_board_issues", "jira_get_sprints_from_board", "jira_get_sprint_issues",
    "jira_get_transitions", "jira_get_worklog", "jira_get_all_projects",
    "jira_get_project_issue_types", "jira_get_project_versions",
)
FORWARD_ENV = frozenset({
    "PATH", "HOME", "USER", "LOGNAME", "LANG", "LC_ALL", "LC_CTYPE", "TZ",
    "TMPDIR", "TMP", "TEMP", "SYSTEMROOT", "WINDIR", "XDG_CACHE_HOME",
    "UV_CACHE_DIR", "UV_PYTHON_INSTALL_DIR", "UV_PYTHON_DOWNLOADS", "UV_OFFLINE",
    "SSL_CERT_FILE", "SSL_CERT_DIR", "REQUESTS_CA_BUNDLE",
    "HTTPS_PROXY", "https_proxy", "NO_PROXY", "no_proxy",
})


def child_environment(credentials, ambient):
    return {
        **{key: value for key, value in ambient.items() if key in FORWARD_ENV},
        **credentials,
        "READ_ONLY_MODE": "true",
        "JIRA_SSL_VERIFY": "true",
        "ENABLED_TOOLS": ",".join(ENABLED_TOOLS),
        "TOOLSETS": "all",
        "MCP_VERBOSE": "false",
        "MCP_VERY_VERBOSE": "false",
        "MCP_LOGGING_STDOUT": "false",
        "MCP_ATLASSIAN_USE_SYSTEM_TRUSTSTORE": "true",
        "PYTHON_DOTENV_DISABLED": "1",
        "UV_NO_CONFIG": "true",
    }


def launch(root=ROOT):
    credentials = load_jira_credentials(root)
    executable = shutil.which("uvx")
    if executable is None:
        raise IntegrationError("uvx is missing; install uv, then restart the workspace MCP server.")
    # Upstream otherwise loads .env with override=True, bypassing the clean environment.
    arguments = [
        executable, "--python", "3.12", MCP_PACKAGE,
        "--env-file", os.devnull, "--transport", "stdio",
    ]
    try:
        os.execvpe(executable, arguments, child_environment(credentials, os.environ))
    except OSError:
        raise IntegrationError("Could not start the Jira MCP process.") from None


def main():
    try:
        launch()
    except IntegrationError as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
