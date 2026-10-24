"""Reject private artifacts and recognizable secrets in Git snapshots and history."""

import argparse
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

from credentials import IntegrationError, parse_literal_env, secure_read


FORBIDDEN_PARTS = {"private", ".local", ".venv", "__pycache__"}
SECRET_PATTERNS = (
    rb"gh[pousr]_[A-Za-z0-9]{30,}",
    rb"github_pat_[A-Za-z0-9_]{40,}",
    rb"\bAKIA[A-Z0-9]{16}\b",
    rb"\bsk-(?:proj-)?[A-Za-z0-9_-]{32,}",
    rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    rb"\bBearer\s+[A-Za-z0-9._~+/-]{24,}=*",
)
SECRET_NAME = rb"(?:[A-Z][A-Z0-9_]*)?(?:TOKEN|PASSWORD|SECRET|API_KEY|PAT)"
QUOTED_ASSIGNMENT = re.compile(
    rb'''(?i)(?<![A-Z0-9_])["']?''' + SECRET_NAME
    + rb'''["']?[ \t]*[:=][ \t]*(["'])([^"'\r\n]*?)\1'''
)
ENV_ASSIGNMENT = re.compile(
    rb"(?m)^" + SECRET_NAME + rb'''[ \t]*=[ \t]*([^\s"'`]+)[ \t]*$'''
)


def private_path(filename):
    path = PurePosixPath(filename)
    return (
        bool(FORBIDDEN_PARTS.intersection(path.parts))
        or filename == ".codex/config.toml"
        or (path.name.startswith(".env") and path.name != ".env.example")
        or path.suffix.lower() in {".pem", ".key", ".p12", ".pfx"}
        or path.name in {"credentials.json", "secrets.json", "secrets.env"}
    )


def placeholder(value):
    lowered = value.lower()
    return (
        len(value) < 12
        or lowered.startswith((b"your_", b"example", b"placeholder", b"replace_", b"${", b"<"))
        or lowered in {b"test-only-fake-token", b"fake$(not-a-command)=token"}
    )


def secret_content(content, known_secrets):
    literals = [value for _, value in QUOTED_ASSIGNMENT.findall(content)]
    return (
        any(secret in content for secret in known_secrets if secret)
        or any(re.search(pattern, content) for pattern in SECRET_PATTERNS)
        or any(not placeholder(value) for value in [*literals, *ENV_ASSIGNMENT.findall(content)])
    )


def local_secrets(root):
    directory = root / ".local"
    if not directory.exists() and not directory.is_symlink():
        return ()
    values = parse_literal_env(secure_read(root, "secrets.env", missing_ok=True))
    return tuple(value.encode() for key, value in values.items()
                 if re.search(r"TOKEN|PASSWORD|SECRET|API_KEY|PAT", key) and value)


def git(root, *arguments):
    result = subprocess.run(
        ["git", "-C", str(root), *arguments], capture_output=True, check=False,
    )
    if result.returncode:
        raise ValueError("Unable to inspect Git objects; run inside an initialized repository.")
    return result.stdout


def check_index(root):
    records = git(root, "ls-files", "--stage", "-z").split(b"\0")
    secrets = local_secrets(root)
    problems = []
    for record in records:
        if not record:
            continue
        metadata, filename = record.split(b"\t", 1)
        mode, object_id, stage = metadata.split()
        name = filename.decode("utf-8", errors="replace")
        if private_path(name):
            problems.append(f"{name}: private path staged for publication")
        elif stage != b"0" or mode == b"160000":
            problems.append(f"{name}: unresolved entry or unreviewed nested repository")
        elif secret_content(git(root, "cat-file", "blob", object_id.decode()), secrets):
            problems.append(f"{name}: possible credential detected (value hidden)")
    return problems


def check_history(root):
    if git(root, "rev-parse", "--is-shallow-repository").strip() == b"true":
        raise ValueError("Complete history is required; fetch without a shallow depth.")
    secrets = local_secrets(root)
    problems, inspected = [], set()
    for commit in git(root, "rev-list", "--all").splitlines():
        revision = commit.decode("ascii")
        if secret_content(git(root, "cat-file", "commit", revision), secrets):
            problems = [*problems, f"commit {revision}: possible credential in metadata (value hidden)"]
        for record in git(root, "ls-tree", "-r", "-z", "--full-tree", revision).split(b"\0"):
            if not record:
                continue
            metadata, filename = record.split(b"\t", 1)
            mode, kind, object_id = metadata.split()
            name = filename.decode("utf-8", errors="replace")
            entry = (mode, object_id, filename)
            if entry in inspected:
                continue
            inspected = inspected | {entry}
            prefix = f"{name} (commit {revision[:12]})"
            if private_path(name):
                problems = [*problems, f"{prefix}: private path in history"]
            elif kind != b"blob" or mode == b"160000":
                problems = [*problems, f"{prefix}: unreviewed nested repository"]
            elif secret_content(git(root, "cat-file", "blob", object_id.decode()), secrets):
                problems = [*problems, f"{prefix}: possible credential detected (value hidden)"]
    return problems


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--history", action="store_true",
                        help="Also inspect all reachable commits; requires complete Git history.")
    args = parser.parse_args(argv)
    try:
        root = Path(git(Path.cwd(), "rev-parse", "--show-toplevel").decode().strip())
        problems = check_index(root)
        if args.history:
            problems = [*problems, *check_history(root)]
    except (OSError, UnicodeError, ValueError, IntegrationError):
        print("Publication check failed: cannot inspect repository or local credential metadata.", file=sys.stderr)
        return 1
    if problems:
        print("Publication blocked:\n" + "\n".join(problems), file=sys.stderr)
        return 1
    scope = "Git index and all reachable commit history" if args.history else "Git index"
    print(f"Publication check passed for {scope}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
