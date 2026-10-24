"""Private literal environment storage; no shell expansion or token arguments."""

import argparse
import getpass
import ipaddress
import os
from pathlib import Path
import re
import secrets
import stat
import sys
import warnings
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


class IntegrationError(Exception):
    """A fixed, safe message suitable for terminal output."""


def validate_url(value):
    try:
        parsed = urlsplit(value)
        host = parsed.hostname or ""
        port = parsed.port
        valid = parsed.scheme == "https" and host and not (
            parsed.username is not None or parsed.password is not None
            or parsed.query or parsed.fragment or "?" in value or "#" in value
            or "\\" in value or any(ord(char) <= 32 or ord(char) >= 127 for char in value)
        )
        if ":" in host:
            ipaddress.IPv6Address(host)
        elif not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?", host):
            valid = False
        if not valid or (port is not None and port == 0):
            raise ValueError
    except (ValueError, TypeError):
        raise IntegrationError("JIRA_URL must be an HTTPS base URL without credentials, query, or fragment.") from None
    return value.rstrip("/")


def validate_token(value):
    if not value or any(ord(char) <= 32 or ord(char) >= 127 for char in value):
        raise IntegrationError("Jira PAT is missing or contains unsupported whitespace/control characters.")
    return value


def _private_directory(root):
    if os.name != "posix":
        raise IntegrationError("Private credentials require POSIX permissions; use Linux, macOS, or WSL.")
    try:
        descriptor = os.open(Path(root) / ".local", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        metadata = os.fstat(descriptor)
        if metadata.st_uid != os.getuid() or stat.S_IMODE(metadata.st_mode) != 0o700:
            os.close(descriptor)
            raise IntegrationError(".local must belong to you with mode 0700; run bootstrap first.")
        return descriptor
    except OSError:
        raise IntegrationError("Cannot open private .local directory; run bootstrap and reject symlinks.") from None


def _validate_private_file(metadata):
    if not stat.S_ISREG(metadata.st_mode) or metadata.st_uid != os.getuid() or stat.S_IMODE(metadata.st_mode) != 0o600:
        raise IntegrationError("Private files must be regular, owned by you, and mode 0600; symlinks are forbidden.")


def secure_read(root, filename, missing_ok=False):
    if Path(filename).name != filename or filename in (".", ".."):
        raise IntegrationError("Private input must use a simple filename.")
    directory = _private_directory(root)
    try:
        try:
            descriptor = os.open(filename, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
        except FileNotFoundError:
            if missing_ok:
                return ""
            raise IntegrationError("Local Jira credentials are missing; run credentials.py set-jira-token.") from None
        with os.fdopen(descriptor, "r", encoding="utf-8", newline="") as stream:
            _validate_private_file(os.fstat(stream.fileno()))
            content = stream.read(1048577)
        if len(content) > 1048576:
            raise IntegrationError("Private configuration exceeds the supported size.")
        return content
    except (OSError, UnicodeError):
        raise IntegrationError("Cannot safely read private configuration.") from None
    finally:
        os.close(directory)


def secure_write(root, filename, content):
    if Path(filename).name != filename or filename in (".", ".."):
        raise IntegrationError("Private output must use a simple filename.")
    directory = _private_directory(root)
    temporary = ".write-" + secrets.token_hex(12)
    try:
        try:
            _validate_private_file(os.stat(filename, dir_fd=directory, follow_symlinks=False))
        except FileNotFoundError:
            pass
        descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=directory)
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, filename, src_dir_fd=directory, dst_dir_fd=directory)
        os.fsync(directory)
    except OSError:
        raise IntegrationError("Cannot safely write private configuration.") from None
    finally:
        try:
            os.unlink(temporary, dir_fd=directory)
        except FileNotFoundError:
            pass
        os.close(directory)


def parse_literal_env(content):
    if "\r" in content or "\x00" in content:
        raise IntegrationError("Private configuration must use literal KEY=VALUE lines with LF endings.")
    values = {}
    for line in content.split("\n"):
        if not line or line.startswith("#"):
            continue
        key, separator, value = line.partition("=")
        if not separator or not re.fullmatch(r"[A-Z][A-Z0-9_]*", key) or key in values:
            raise IntegrationError("Private configuration contains an invalid or duplicate assignment.")
        values = {**values, key: value}
    return values


def load_jira_credentials(root=ROOT):
    values = parse_literal_env(secure_read(root, "secrets.env"))
    result = {
        "JIRA_URL": validate_url(values.get("JIRA_URL", "")),
        "JIRA_PERSONAL_TOKEN": validate_token(values.get("JIRA_PERSONAL_TOKEN", "")),
    }
    projects = values.get("JIRA_PROJECTS_FILTER", "")
    if projects:
        if not re.fullmatch(r"[A-Z][A-Z0-9_]*(?:,[A-Z][A-Z0-9_]*)*", projects):
            raise IntegrationError("JIRA_PROJECTS_FILTER must contain comma-separated project keys.")
        result = {**result, "JIRA_PROJECTS_FILTER": projects}
    return result


def save_jira_credentials(root, url, token):
    updated = {
        **parse_literal_env(secure_read(root, "secrets.env", missing_ok=True)),
        "JIRA_URL": validate_url(url),
        "JIRA_PERSONAL_TOKEN": validate_token(token),
    }
    secure_write(root, "secrets.env", "".join(f"{key}={value}\n" for key, value in sorted(updated.items())))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    command = commands.add_parser("set-jira-token", help="Prompt for a Jira Data Center PAT.")
    command.add_argument("--url", required=True)
    args = parser.parse_args(argv)
    try:
        url = validate_url(args.url)
        with warnings.catch_warnings():
            warnings.simplefilter("error", getpass.GetPassWarning)
            token = getpass.getpass("Jira Personal Access Token (hidden): ")
        save_jira_credentials(ROOT, url, token)
    except getpass.GetPassWarning:
        print("A terminal with hidden input is required; run this command in your terminal.", file=sys.stderr)
        return 1
    except (IntegrationError, EOFError, KeyboardInterrupt) as error:
        message = str(error) if isinstance(error, IntegrationError) else "Credential entry cancelled."
        print(message, file=sys.stderr)
        return 1
    print("Jira credentials saved locally with mode 0600.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
