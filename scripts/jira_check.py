"""Verify Jira authentication and optionally save minimal private metadata."""

import argparse
from datetime import datetime, timezone
import json
import re
import ssl
import sys
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, HTTPSHandler, Request, build_opener

from credentials import IntegrationError, ROOT, load_jira_credentials, secure_write

MAX_RESPONSE_BYTES = 10 * 1024 * 1024


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, response, code, message, headers, new_url):
        raise IntegrationError("Jira redirected an authenticated request; verify the configured base URL.")


class JiraClient:
    def __init__(self, credentials):
        self.url = credentials["JIRA_URL"]
        self.token = credentials["JIRA_PERSONAL_TOKEN"]
        self.opener = build_opener(NoRedirect(), HTTPSHandler(context=ssl.create_default_context()))

    def get(self, path):
        if not path.startswith("/rest/") or any(ord(char) < 32 for char in path) or "\\" in path:
            raise IntegrationError("Jira discovery accepts only REST paths.")
        request = Request(self.url + path, headers={
            "Authorization": "Bearer " + self.token,
            "Accept": "application/json",
            "User-Agent": "tl-manager/1.0",
        }, method="GET")
        try:
            with self.opener.open(request, timeout=20) as response:
                body = response.read(MAX_RESPONSE_BYTES + 1)
            if len(body) > MAX_RESPONSE_BYTES:
                raise IntegrationError("Jira metadata response exceeds the supported size.")
            return json.loads(body)
        except HTTPError as error:
            code = error.code
            error.close()
            raise IntegrationError(f"Jira returned HTTP {code}; check access and the configured base URL.") from None
        except (URLError, TimeoutError, OSError):
            raise IntegrationError("Cannot connect securely to Jira; check the network, TLS trust, and base URL.") from None
        except (ValueError, UnicodeError):
            raise IntegrationError("Jira returned an invalid JSON response.") from None


def select_rows(payload, keys):
    if not isinstance(payload, list) or any(not isinstance(row, dict) for row in payload):
        raise IntegrationError("Jira returned unexpected metadata.")
    return [{key: row[key] for key in keys if key in row} for row in payload]


def discover_boards(client):
    rows = []
    offset = 0
    seen_ids = frozenset()
    for _ in range(1000):
        page = client.get(f"/rest/agile/1.0/board?startAt={offset}&maxResults=100")
        if not isinstance(page, dict):
            raise IntegrationError("Jira returned unexpected board pagination.")
        values = select_rows(page.get("values"), ("id", "name", "type"))
        if page.get("startAt", offset) != offset:
            raise IntegrationError("Jira board pagination did not advance correctly.")
        identifiers = [row.get("id") for row in values]
        if any(not isinstance(identifier, int) for identifier in identifiers):
            raise IntegrationError("Jira returned invalid board identifiers.")
        if len(set(identifiers)) != len(identifiers) or seen_ids.intersection(identifiers):
            raise IntegrationError("Jira board pagination repeated records; discovery is incomplete.")
        seen_ids = seen_ids.union(identifiers)
        rows = [*rows, *values]
        offset += len(values)
        total = page.get("total")
        if page.get("isLast") is True or page.get("isLast") is not False and isinstance(total, int) and offset >= total:
            return rows
        if not values:
            raise IntegrationError("Jira board pagination stopped before confirmed completion.")
    raise IntegrationError("Jira board discovery exceeded the pagination limit; discovery is incomplete.")


def discover_metadata(client):
    fields = select_rows(client.get("/rest/api/2/field"), ("id", "name", "custom", "schema"))
    projects = select_rows(client.get("/rest/api/2/project"), ("id", "key", "name"))
    try:
        boards = discover_boards(client)
        complete = True
    except IntegrationError:
        boards, complete = [], False
    statuses = select_rows(client.get("/rest/api/2/status"), ("id", "name", "statusCategory"))
    return {
        "discovered_at": datetime.now(timezone.utc).isoformat(),
        "fields": fields, "projects": projects, "boards": boards, "statuses": statuses,
        "boards_complete": complete,
    }


def check(root=ROOT, discover=False):
    client = JiraClient(load_jira_credentials(root))
    profile = client.get("/rest/api/2/myself")
    if not isinstance(profile, dict) or profile.get("active") is not True:
        raise IntegrationError("Jira did not confirm an active authenticated account.")
    print("Jira authentication OK (read-only check).")
    if not discover:
        return
    metadata = discover_metadata(client)
    secure_write(root, "jira-discovery.json", json.dumps(metadata, ensure_ascii=True, indent=2) + "\n")
    counts = ", ".join(f"{key}={len(metadata[key])}" for key in ("fields", "projects", "boards", "statuses"))
    print(f"Private metadata saved to .local/jira-discovery.json ({counts}).")
    candidates = [row["id"] for row in metadata["fields"]
                  if str(row.get("name", "")).casefold() in ("story points", "story point estimate")
                  and re.fullmatch(r"[A-Za-z0-9_]+", str(row.get("id", "")))]
    if candidates:
        print("Story point field candidates: " + ", ".join(candidates))
    if not metadata["boards_complete"]:
        print("Board discovery unavailable or incomplete; authentication remains valid.")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--discover", action="store_true", help="Save fields, projects, boards, and statuses privately.")
    args = parser.parse_args(argv)
    try:
        check(discover=args.discover)
    except IntegrationError as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
