"""Validation and safe filesystem helpers for the manager workspace."""

import json
import os
from pathlib import Path
import re
import tempfile


class WorkspaceError(ValueError):
    """An actionable configuration or workspace error."""


def safe_path(root, relative):
    """Reject symlinks even inside the root: managed writes never follow them."""
    text = str(relative)
    parts = text.split("/")
    if not text or "\\" in text or ":" in text or any(p in ("", ".", "..") for p in parts):
        raise WorkspaceError(f"Unsafe workspace path: {text}")
    candidate = root
    for index, part in enumerate(parts):
        candidate = candidate / part
        if candidate.is_symlink():
            raise WorkspaceError(f"Symlinks are not allowed at managed path: {text}")
        if index < len(parts) - 1 and candidate.exists() and not candidate.is_dir():
            raise WorkspaceError(f"Expected a directory in managed path: {text}")
    if not candidate.resolve().is_relative_to(root.resolve()):
        raise WorkspaceError(f"Path escapes workspace: {text}")
    return candidate


def safe_slug(value, *, sprint=False):
    pattern = r"[a-z0-9][a-z0-9]*(?:-[a-z0-9]+)*" if sprint else r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*"
    if not isinstance(value, str) or len(value) > 64 or not re.fullmatch(pattern, value):
        raise WorkspaceError("Use a slug of at most 64 lowercase letters, digits and single hyphens.")
    return value


def safe_text(value, name):
    if (not isinstance(value, str) or not value.strip() or len(value) > 200
            or not value.isprintable() or "|" in value):
        raise WorkspaceError(f"{name} must be a nonempty single line, at most 200 characters, without '|'.")
    return value.strip()


def read_json(path):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        raise WorkspaceError(f"Cannot read valid JSON from {path.name}.") from None
    if not isinstance(data, dict):
        raise WorkspaceError(f"{path.name} must contain a JSON object.")
    return data


def write_text(path, content, mode=0o644):
    """Replace complete files atomically without exposing partial output."""
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def json_text(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def integration_ids(root):
    registry = read_json(safe_path(root, "config/integrations.json"))
    entries = registry.get("integrations")
    if registry.get("schema_version") != 1 or not isinstance(entries, list):
        raise WorkspaceError("integrations.json requires schema_version 1 and an integrations list.")
    names = []
    for entry in entries:
        if not isinstance(entry, dict):
            raise WorkspaceError("Each integration must be an object with an id.")
        names = [*names, safe_slug(entry.get("id"))]
    if len(names) != len(set(names)):
        raise WorkspaceError("Integration ids must be unique.")
    return set(names)


def validate_skill(root, entry):
    path = safe_path(root, entry["path"] + "/SKILL.md")
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        raise WorkspaceError(f"Missing or unreadable skill: {entry['path']}/SKILL.md") from None
    frontmatter = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.DOTALL)
    if not frontmatter:
        raise WorkspaceError(f"Skill {entry['id']} requires YAML frontmatter.")
    name = re.search(r"^name:\s*([^\r\n]+)$", frontmatter[1], re.MULTILINE)
    description = re.search(r"^description:[ \t]*(\S[^\r\n]*)$", frontmatter[1], re.MULTILINE)
    if not name or name[1].strip().strip("\"'") != entry["id"] or not description:
        raise WorkspaceError(f"Skill {entry['id']} requires matching name and nonempty description.")
    for filename in (*entry["inputs"], *entry["outputs"]):
        if not safe_path(root, f"{entry['path']}/assets/{filename}").is_file():
            raise WorkspaceError(f"Missing template: {entry['path']}/assets/{filename}")


def validate_entry(entry, integrations):
    if not isinstance(entry, dict):
        raise WorkspaceError("Every workstream must be an object.")
    name = safe_slug(entry.get("id"))
    if entry.get("path") != f"skills/{name}":
        raise WorkspaceError(f"Workstream {name} path must be skills/{name}.")
    safe_text(entry.get("title"), "Title")
    safe_text(entry.get("cadence"), "Cadence")
    for field in ("inputs", "outputs"):
        values = entry.get(field)
        if not isinstance(values, list) or not values:
            raise WorkspaceError(f"Workstream {name} needs a nonempty {field} list.")
        for filename in values:
            if not isinstance(filename, str) or not re.fullmatch(r"[a-z0-9][a-z0-9._-]*\.md", filename):
                raise WorkspaceError(f"Invalid asset filename in {name}.")
    assets = [*entry["inputs"], *entry["outputs"]]
    if len(assets) != len(set(assets)):
        raise WorkspaceError(f"Template filenames must be unique in {name}.")
    links = entry.get("integrations")
    if not isinstance(links, list) or any(not isinstance(x, str) or x not in integrations for x in links):
        raise WorkspaceError(f"Workstream {name} refers to unknown integrations.")


def load_registry(root):
    registry = read_json(safe_path(root, "config/workstreams.json"))
    entries = registry.get("workstreams")
    if registry.get("schema_version") != 1 or not isinstance(entries, list) or not entries:
        raise WorkspaceError("workstreams.json requires schema_version 1 and a nonempty workstreams list.")
    integrations = integration_ids(root)
    names = []
    for entry in entries:
        validate_entry(entry, integrations)
        validate_skill(root, entry)
        names = [*names, entry["id"]]
    if len(names) != len(set(names)):
        raise WorkspaceError("Workstream ids and paths must be unique.")
    return registry


def render_index(registry):
    lines = [
        "# Danh mục công việc quản lý", "",
        "Tạo tự động từ `config/workstreams.json`; cập nhật bằng `python3 scripts/workspace.py index`.", "",
        "Bắt đầu tại [README.md](README.md). Mỗi đầu việc có hướng dẫn, mẫu đầu vào và mẫu kết quả riêng.", "",
        "| Đầu việc | Tần suất | Hướng dẫn | Đầu vào | Kết quả | Lệnh gọi skill |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for entry in registry["workstreams"]:
        base = entry["path"]
        inputs = ", ".join(f"[{x}]({base}/assets/{x})" for x in entry["inputs"])
        outputs = ", ".join(f"[{x}]({base}/assets/{x})" for x in entry["outputs"])
        lines = [*lines, f"| {entry['title']} | {entry['cadence']} | [{entry['id']}]({base}/SKILL.md) | {inputs} | {outputs} | `${entry['id']}` |"]
    return "\n".join([*lines, "", "## Dữ liệu làm việc", "",
        "Đầu vào và báo cáo thực tế của sprint nằm tại `private/sprints/<sprint-id>/<workstream>/`.",
        "Cập nhật hằng ngày nằm tại `private/sprints/<sprint-id>/daily-risk/daily/`.",
        "Dữ liệu riêng tư và thông tin xác thực trong `.local/` không được đưa vào Git; chuyển chúng qua kênh riêng được phê duyệt.", "",
        "## Các lệnh quản lý workspace", "", "```sh", "python3 scripts/workspace.py bootstrap",
        "python3 scripts/workspace.py validate",
        "python3 scripts/workspace.py new-sprint <sprint-id> --start YYYY-MM-DD --board <board-id>",
        'python3 scripts/workspace.py add-workstream <slug> --title "Tên đầu việc"', "```", "",
        "Chọn mã sprint và ngày bắt đầu thực tế; lệnh bootstrap không tự tạo sprint hiện tại.",
        "Kiểm tra Jira: `python3 scripts/jira_check.py --help`. Thiết lập MCP: `python3 scripts/setup_mcp.py --help`.", ""])
