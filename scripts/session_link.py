#!/usr/bin/env python3
"""Best-effort discovery of the current Claude session id.

Order of attempts:
  1. CLAUDE_SESSION_ID environment variable.
  2. Newest file under ~/.claude/sessions/, scanned for a UUID-like id.

Always exits 0. Prints a JSON object: {"session_id": "..."} on success,
or {} if nothing could be found.
"""
import glob
import json
import os
import re
import sys

SESSIONS_DIR = os.path.expanduser("~/.claude/sessions")
UUID_RE = re.compile(
    r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
)


def from_env():
    val = os.environ.get("CLAUDE_SESSION_ID")
    if val:
        return val.strip()
    return None


def from_sessions_dir():
    if not os.path.isdir(SESSIONS_DIR):
        return None
    try:
        files = glob.glob(os.path.join(SESSIONS_DIR, "**", "*"), recursive=True)
        files = [f for f in files if os.path.isfile(f)]
        if not files:
            return None
        newest = max(files, key=os.path.getmtime)

        # First, try the filename itself.
        m = UUID_RE.search(os.path.basename(newest))
        if m:
            return m.group(0)

        # Fall back to scanning file contents (best effort, bounded read).
        with open(newest, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read(65536)
        m = UUID_RE.search(content)
        if m:
            return m.group(0)
    except Exception:
        return None
    return None


def main():
    try:
        session_id = from_env() or from_sessions_dir()
    except Exception:
        session_id = None

    if session_id:
        json.dump({"session_id": session_id}, sys.stdout)
    else:
        json.dump({}, sys.stdout)
    sys.stdout.write("\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
