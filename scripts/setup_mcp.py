"""Add a machine-local Codex Jira MCP entry without changing global settings."""

import argparse
import json
import os
from pathlib import Path
import sys
import tempfile
import tomllib

from credentials import IntegrationError, ROOT
from jira_mcp import ENABLED_TOOLS


def expected_entry(root):
    return {
        "command": str(Path(sys.executable).absolute()),
        "args": [str(Path(root).absolute() / "scripts/jira_mcp.py")],
        "startup_timeout_sec": 120,
        "tool_timeout_sec": 120,
        "enabled_tools": list(ENABLED_TOOLS),
    }


def read_config(path):
    if path.is_symlink():
        raise IntegrationError("Refusing a symlink for local Codex config.")
    if not path.exists():
        return "", {}
    if not path.is_file():
        raise IntegrationError("Local Codex config must be a regular file.")
    try:
        text = path.read_text(encoding="utf-8")
        return text, tomllib.loads(text)
    except (OSError, UnicodeError, tomllib.TOMLDecodeError):
        raise IntegrationError("Cannot read the existing local Codex TOML; repair it before setup.") from None


def configure(root=ROOT):
    directory = Path(root) / ".codex"
    if directory.is_symlink():
        raise IntegrationError("Refusing a symlink for the local Codex directory.")
    directory.mkdir(mode=0o700, exist_ok=True)
    path = directory / "config.toml"
    original, parsed = read_config(path)
    expected = expected_entry(root)
    servers = parsed.get("mcp_servers", {})
    if not isinstance(servers, dict):
        raise IntegrationError("Existing mcp_servers configuration is incompatible; no changes made.")
    if "jira_datacenter" in servers:
        if servers["jira_datacenter"] == expected:
            return False
        raise IntegrationError("Existing jira_datacenter MCP entry differs; review it manually before setup.")
    stanza = "\n[mcp_servers.jira_datacenter]\n" + "".join(
        f"{key} = {json.dumps(value, ensure_ascii=True)}\n" for key, value in expected.items()
    )
    content = original + ("\n" if original and not original.endswith("\n") else "") + stanza
    try:
        tomllib.loads(content)
    except tomllib.TOMLDecodeError:
        raise IntegrationError("Existing local Codex TOML cannot accept the MCP entry; no changes made.") from None
    temporary = None
    try:
        descriptor, temporary = tempfile.mkstemp(prefix=".config-", dir=directory)
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        if read_config(path)[0] != original:
            raise IntegrationError("Local Codex config changed during setup; no changes made.")
        os.replace(temporary, path)
    finally:
        if temporary and os.path.exists(temporary):
            os.unlink(temporary)
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(argv)
    try:
        changed = configure()
    except IntegrationError as error:
        print(str(error), file=sys.stderr)
        return 1
    except OSError:
        print("Cannot safely update local Codex configuration.", file=sys.stderr)
        return 1
    print("Local Codex Jira MCP configured." if changed else "Local Codex Jira MCP is already configured.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
