#!/usr/bin/env python3
"""Poll the Claude Code Atom feed for new releases.

Fetches https://raw.githubusercontent.com/anthropics/claude-code/main/feed.xml
(or a local file via --feed-file), diffs entries against
state/last_seen.json, and writes any new entries to state/pending/<version>.json.

Exit codes:
  0 - success (stdout: "NEW_UPDATE\\n<ver1>\\n<ver2>..." or "NO_UPDATE")
  2 - fetch/parse error (message on stderr)
"""
import argparse
import html
import json
import os
import re
import sys
import urllib.request
import urllib.error
from html.parser import HTMLParser
from xml.etree import ElementTree as ET

FEED_URL = "https://raw.githubusercontent.com/anthropics/claude-code/main/feed.xml"
ATOM_NS = "{http://www.w3.org/2005/Atom}"
USER_AGENT = "cc-changelog-digest/1.0 (+https://github.com/tkmnkmr/cc-changelog-digest)"
TIMEOUT_SECONDS = 30

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_DIR = os.path.join(ROOT_DIR, "state")
LAST_SEEN_PATH = os.path.join(STATE_DIR, "last_seen.json")
PENDING_DIR = os.path.join(STATE_DIR, "pending")

VERSION_RE = re.compile(r"(\d+\.\d+\.\d+)")


class _HTMLToTextParser(HTMLParser):
    """Very small HTML->Markdown-ish plain text converter.

    Handles the tags actually seen in the feed's <content>: <p>, <br>,
    <li>, <ul>/<ol>, <code>, plus generic entity decoding. Anything else
    is passed through as text.
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self._parts = []
        self._in_code = False

    def handle_starttag(self, tag, attrs):
        if tag == "li":
            self._parts.append("\n- ")
        elif tag == "br":
            self._parts.append("\n")
        elif tag == "p":
            if self._parts:
                self._parts.append("\n")
        elif tag == "code":
            self._in_code = True
            self._parts.append("`")

    def handle_endtag(self, tag):
        if tag == "code":
            self._in_code = False
            self._parts.append("`")
        elif tag == "p":
            self._parts.append("\n")
        elif tag == "li":
            self._parts.append("\n")

    def handle_data(self, data):
        self._parts.append(data)

    def get_text(self):
        text = "".join(self._parts)
        # Collapse 3+ newlines, strip trailing/leading whitespace per line
        lines = [line.rstrip() for line in text.split("\n")]
        # Drop leading bullet marker duplication like "- • foo" -> "- foo"
        cleaned = []
        for line in lines:
            stripped = line.strip()
            if not stripped:
                if cleaned and cleaned[-1] != "":
                    cleaned.append("")
                continue
            # normalize existing bullet characters (•, *, -) to "- "
            m = re.match(r"^-\s*[•\-\*]\s*(.*)$", stripped)
            if m:
                stripped = "- " + m.group(1)
            else:
                m2 = re.match(r"^[•\*]\s*(.*)$", stripped)
                if m2:
                    stripped = "- " + m2.group(1)
            cleaned.append(stripped)
        # collapse multiple blank lines
        result_lines = []
        prev_blank = False
        for line in cleaned:
            if line == "":
                if prev_blank:
                    continue
                prev_blank = True
            else:
                prev_blank = False
            result_lines.append(line)
        return "\n".join(result_lines).strip("\n")


def html_to_text(content_html):
    parser = _HTMLToTextParser()
    parser.feed(content_html)
    return parser.get_text()


def extract_version(title):
    m = VERSION_RE.search(title or "")
    return m.group(1) if m else None


def fetch_feed_text(feed_file=None):
    if feed_file:
        with open(feed_file, "r", encoding="utf-8") as f:
            return f.read()
    req = urllib.request.Request(FEED_URL, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
            return resp.read().decode("utf-8")
    except urllib.error.URLError as e:
        print(f"error: failed to fetch feed: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:  # noqa: BLE001
        print(f"error: unexpected error fetching feed: {e}", file=sys.stderr)
        sys.exit(2)


def parse_entries(feed_text):
    try:
        root = ET.fromstring(feed_text)
    except ET.ParseError as e:
        print(f"error: failed to parse feed XML: {e}", file=sys.stderr)
        sys.exit(2)

    entries = []
    for entry_el in root.findall(f"{ATOM_NS}entry"):
        title_el = entry_el.find(f"{ATOM_NS}title")
        updated_el = entry_el.find(f"{ATOM_NS}updated")
        content_el = entry_el.find(f"{ATOM_NS}content")
        link = None
        for link_el in entry_el.findall(f"{ATOM_NS}link"):
            if link_el.get("rel") == "alternate":
                link = link_el.get("href")
                break
        if link is None:
            # fall back to any link
            link_el = entry_el.find(f"{ATOM_NS}link")
            if link_el is not None:
                link = link_el.get("href")

        title = title_el.text if title_el is not None else ""
        updated = updated_el.text if updated_el is not None else None
        content_html = content_el.text if content_el is not None else ""
        content_html = html.unescape(content_html or "")

        version = extract_version(title)
        if not version:
            continue

        entries.append(
            {
                "version": version,
                "title": title,
                "updated": updated,
                "link": link,
                "content_html": content_html,
            }
        )
    return entries


def load_last_seen():
    if not os.path.exists(LAST_SEEN_PATH):
        return {"seen_versions": [], "last_checked": None}
    with open(LAST_SEEN_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    data.setdefault("seen_versions", [])
    data.setdefault("last_checked", None)
    return data


def save_last_seen(data):
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(LAST_SEEN_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def classify_text(content_text):
    """Best-effort call into classify.py; returns None if unavailable."""
    try:
        from classify import classify_lines  # type: ignore
    except Exception:
        scripts_dir = os.path.dirname(os.path.abspath(__file__))
        if scripts_dir not in sys.path:
            sys.path.insert(0, scripts_dir)
        try:
            from classify import classify_lines  # type: ignore
        except Exception:
            return None
    lines = [l for l in content_text.split("\n") if l.strip().startswith("-")]
    return classify_lines(lines)


def write_pending(entry):
    os.makedirs(PENDING_DIR, exist_ok=True)
    content_text = html_to_text(entry["content_html"])
    pre_classified = classify_text(content_text)
    pending = {
        "version": entry["version"],
        "title": entry["title"],
        "updated": entry["updated"],
        "link": entry["link"],
        "content_html": entry["content_html"],
        "content_text": content_text,
        "pre_classified": pre_classified,
    }
    path = os.path.join(PENDING_DIR, f"{entry['version']}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(pending, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--feed-file", help="Read feed XML from a local file instead of the network")
    parser.add_argument("--force", metavar="VERSION", help="Force a version into pending/ even if already seen (dry run)")
    args = parser.parse_args()

    feed_text = fetch_feed_text(args.feed_file)
    entries = parse_entries(feed_text)
    # feed entries are expected newest-first already; sort defensively is
    # not attempted since ordering by version string is unreliable.

    last_seen = load_last_seen()
    seen_versions = set(last_seen["seen_versions"])
    is_first_run = len(seen_versions) == 0

    new_entries = [e for e in entries if e["version"] not in seen_versions]

    if is_first_run and new_entries:
        # Only the newest entry counts as "new" on a first run, to avoid
        # blasting the full history on initial setup.
        new_entries = new_entries[:1]

    forced_written = []
    if args.force:
        forced_entry = next((e for e in entries if e["version"] == args.force), None)
        if forced_entry is not None:
            write_pending(forced_entry)
            forced_written.append(forced_entry["version"])

    written_versions = list(forced_written)
    for e in new_entries:
        if e["version"] in written_versions:
            continue
        write_pending(e)
        written_versions.append(e["version"])

    from datetime import datetime, timezone

    last_seen["last_checked"] = datetime.now(timezone.utc).isoformat()
    save_last_seen(last_seen)

    if written_versions:
        print("NEW_UPDATE")
        for v in written_versions:
            print(v)
    else:
        print("NO_UPDATE")
    sys.exit(0)


if __name__ == "__main__":
    main()
