#!/usr/bin/env python3
"""Manage local sprint work and the portable manager-workspace catalog."""

import argparse
from datetime import date, timedelta
import json
import os
from pathlib import Path
import re
import shutil
import sys
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from workspace_lib import (WorkspaceError, json_text, load_registry, read_json,
                           render_index, safe_path, safe_slug, safe_text, write_text)

ROOT = Path(__file__).resolve().parents[1]
COPY_MARKER = ".workspace-managed-copy"


def discovery_targets(root, entries):
    parent = safe_path(root, ".agents/skills")
    if parent.exists() and not parent.is_dir():
        raise WorkspaceError(".agents/skills must be a directory.")
    targets = []
    for entry in entries:
        source = safe_path(root, entry["path"])
        for directory, folders, files in os.walk(source, followlinks=False):
            if any((Path(directory) / name).is_symlink() for name in (*folders, *files)):
                raise WorkspaceError(f"Skill discovery does not allow nested symlinks: {entry['id']}")
        target = parent / entry["id"]
        if target.exists() and not target.is_symlink():
            if not target.is_dir() or not (target / COPY_MARKER).is_file():
                raise WorkspaceError(f"Discovery path is user-managed; move it before bootstrap: {target.name}")
            safe_path(root, f".agents/skills/{entry['id']}/{COPY_MARKER}")
        targets = [*targets, (source, target)]
    return targets


def refresh_discovery(root, entries):
    targets = discovery_targets(root, entries)
    for source, target in targets:
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.is_symlink():
            target.unlink()
        elif target.exists():
            shutil.rmtree(target)
        try:
            target.symlink_to(os.path.relpath(source, target.parent), target_is_directory=True)
        except OSError:
            # Windows may not permit symlinks without Developer Mode.
            shutil.copytree(source, target, symlinks=True)
            (target / COPY_MARKER).write_text("Refreshed by workspace bootstrap.\n", encoding="utf-8")


def index_target(root):
    target = safe_path(root, "INDEX.md")
    if target.exists() and not target.is_file():
        raise WorkspaceError("INDEX.md must be a regular file.")
    return target


def update_index(root, registry):
    write_text(index_target(root), render_index(registry))


def bootstrap(root):
    registry = load_registry(root)
    targets = ((".local/workspace.json", "config/workspace.example.json"),
               (".local/secrets.env", "config/credentials.env.example"))
    directories = [safe_path(root, x) for x in (".local", "private")]
    if any(directory.exists() and not directory.is_dir() for directory in directories):
        raise WorkspaceError(".local and private must be directories.")
    copies = [(safe_path(root, dest), safe_path(root, source)) for dest, source in targets]
    for destination, source in copies:
        if not source.is_file() or (destination.exists() and not destination.is_file()):
            raise WorkspaceError(f"Expected a regular file: {source.name} or {destination.name}.")
    index_target(root)
    discovery_targets(root, registry["workstreams"])
    for directory in directories:
        directory.mkdir(mode=0o700, exist_ok=True)
        directory.chmod(0o700)
    for destination, source in copies:
        if not destination.exists():
            write_text(destination, source.read_text(encoding="utf-8"), mode=0o600)
        destination.chmod(0o600)
    refresh_discovery(root, registry["workstreams"])
    update_index(root, registry)
    print("Workspace ready. Configure .local/workspace.json and .local/secrets.env; both stay private.")


def validate(root):
    registry = load_registry(root)
    index = safe_path(root, "INDEX.md")
    if not index.is_file() or index.read_text(encoding="utf-8") != render_index(registry):
        raise WorkspaceError("INDEX.md is missing or stale; run python3 scripts/workspace.py index.")
    print(f"Valid workspace: {len(registry['workstreams'])} workstreams. No local credentials required.")


def sprint_settings(root, start, board):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", start):
        raise WorkspaceError("Start date must use YYYY-MM-DD.")
    try:
        start_date = date.fromisoformat(start)
    except ValueError:
        raise WorkspaceError("Start date must be a valid calendar date.") from None
    local = safe_path(root, ".local/workspace.json")
    settings = read_json(local if local.exists() else safe_path(root, "config/workspace.example.json"))
    duration = settings.get("sprint_duration_days", 14)
    if type(duration) is not int or not 1 <= duration <= 90:
        raise WorkspaceError("sprint_duration_days must be an integer between 1 and 90.")
    timezone = settings.get("timezone", "Asia/Ho_Chi_Minh")
    try:
        if not isinstance(timezone, str):
            raise ValueError
        ZoneInfo(timezone)
    except (ValueError, ZoneInfoNotFoundError):
        raise WorkspaceError("timezone must name an installed IANA timezone, such as Asia/Ho_Chi_Minh.") from None
    jira = settings.get("jira", {})
    if not isinstance(jira, dict):
        raise WorkspaceError("The jira workspace setting must be an object.")
    selected_board = board if board is not None else jira.get("board_id")
    if selected_board is not None and (type(selected_board) is not int or selected_board <= 0):
        raise WorkspaceError("Board id must be a positive integer.")
    try:
        end = (start_date + timedelta(days=duration)).isoformat()
    except OverflowError:
        raise WorkspaceError("Sprint end date is outside the supported calendar.") from None
    return {"start": start, "end_exclusive": end, "duration_days": duration,
            "timezone": timezone, "board_id": selected_board}


def new_sprint(root, name, start, board=None):
    safe_slug(name, sprint=True)
    settings = sprint_settings(root, start, board)
    registry = load_registry(root)
    target = safe_path(root, f"private/sprints/{name}")
    if target.exists():
        raise WorkspaceError(f"Sprint {name} already exists; no files changed.")
    templates = [(entry["id"], filename,
                  safe_path(root, f"{entry['path']}/assets/{filename}").read_text(encoding="utf-8"))
                 for entry in registry["workstreams"]
                 for filename in (*entry["inputs"], *entry["outputs"])]
    private = safe_path(root, "private")
    private.mkdir(mode=0o700, exist_ok=True)
    private.chmod(0o700)
    target.mkdir(parents=True, mode=0o700)
    metadata = {"schema_version": 1, "id": name, **settings}
    write_text(target / "metadata.json", json_text(metadata), mode=0o600)
    for entry in registry["workstreams"]:
        folder = target / entry["id"]
        folder.mkdir(mode=0o700)
        if entry["id"] == "daily-risk":
            (folder / "daily").mkdir(mode=0o700)
    for workstream, filename, content in templates:
        write_text(target / workstream / filename, content, mode=0o600)
    print(f"Created private/sprints/{name}: {start} through {settings['end_exclusive']} (exclusive).")


def scaffold(name, title):
    description = json.dumps(f"Manage {title}. Use when preparing inputs, reviewing evidence, or recording decisions for this workstream.", ensure_ascii=False)
    return (f"---\nname: {name}\ndescription: {description}\n---\n\n# {title}\n\n"
            "Read `assets/input.md` for required inputs and use `assets/output.md` for the result.\n\n"
            "1. Confirm scope, owner, deadline and success criteria with the manager.\n"
            "2. Read the relevant private sprint folder and list missing evidence.\n"
            "3. Draft decisions, risks and next actions with owners and dates.\n"
            "4. Keep personal data and real reports under `private/`; never include credentials.\n"
            "5. Ask for approval before changing external systems.\n\n"
            "Document assumptions explicitly; do not invent facts or personal performance conclusions.\n")


def add_workstream(root, name, title):
    safe_slug(name)
    title = safe_text(title, "Title")
    registry = load_registry(root)
    target = safe_path(root, f"skills/{name}")
    if target.exists() or any(x["id"] == name for x in registry["workstreams"]):
        raise WorkspaceError(f"Workstream {name} already exists.")
    entry = {"id": name, "title": title, "cadence": "As needed", "path": f"skills/{name}",
             "inputs": ["input.md"], "outputs": ["output.md"], "integrations": []}
    updated = {**registry, "workstreams": [*registry["workstreams"], entry]}
    discovery_targets(root, updated["workstreams"])
    index_target(root)
    (target / "assets").mkdir(parents=True)
    write_text(target / "SKILL.md", scaffold(name, title))
    write_text(target / "assets/input.md", f"# {title}: Input\n\n"
               "| Scope | Owner | Deadline | Success criteria | Evidence |\n| --- | --- | --- | --- | --- |\n| | | | | |\n")
    write_text(target / "assets/output.md", f"# {title}: Output\n\n"
               "| Decision or action | Evidence | Owner | Due date | Status |\n| --- | --- | --- | --- | --- |\n| | | | | |\n\n"
               "## Assumptions and Risks\n\nRecord evidence gaps and unresolved dependencies.\n")
    write_text(safe_path(root, "config/workstreams.json"), json_text(updated))
    update_index(root, updated)
    refresh_discovery(root, updated["workstreams"])
    print(f"Added {name}. Customize skills/{name}/SKILL.md and its templates; catalog and discovery updated.")


def parser():
    result = argparse.ArgumentParser(description=__doc__, epilog=(
        "Jira connectivity: python3 scripts/jira_check.py --help. "
        "MCP integration: python3 scripts/setup_mcp.py --help."))
    commands = result.add_subparsers(dest="command", required=True)
    commands.add_parser("bootstrap", help="Create private local paths and refresh skill discovery.")
    commands.add_parser("index", help="Regenerate INDEX.md from the catalog.")
    commands.add_parser("validate", help="Check catalog, skills, templates and index; works in CI.")
    sprint = commands.add_parser("new-sprint", help="Create a private sprint without overwriting existing work.")
    sprint.add_argument("id")
    sprint.add_argument("--start", required=True, metavar="YYYY-MM-DD")
    sprint.add_argument("--board", type=int, help="Jira board id; defaults to local jira.board_id if set.")
    workstream = commands.add_parser("add-workstream", help="Register a new workstream and usable skill scaffold.")
    workstream.add_argument("slug")
    workstream.add_argument("--title", required=True)
    return result


def main(argv=None, *, root=ROOT):
    args = parser().parse_args(argv)
    root = Path(root).resolve()
    try:
        if args.command == "bootstrap":
            bootstrap(root)
        elif args.command == "validate":
            validate(root)
        elif args.command == "index":
            update_index(root, load_registry(root))
            print("Updated INDEX.md.")
        elif args.command == "new-sprint":
            new_sprint(root, args.id, args.start, args.board)
        elif args.command == "add-workstream":
            add_workstream(root, args.slug, args.title)
    except (WorkspaceError, OSError, UnicodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
