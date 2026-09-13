#!/usr/bin/env python3
"""Mark one or more versions as seen and remove their pending JSON files.

Usage:
    python3 scripts/mark_seen.py <version> [<version> ...]
"""
import json
import os
import sys
from datetime import datetime, timezone

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_DIR = os.path.join(ROOT_DIR, "state")
LAST_SEEN_PATH = os.path.join(STATE_DIR, "last_seen.json")
PENDING_DIR = os.path.join(STATE_DIR, "pending")


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


def main():
    if len(sys.argv) < 2:
        print("usage: python3 scripts/mark_seen.py <version> [<version> ...]", file=sys.stderr)
        sys.exit(1)

    versions = sys.argv[1:]
    data = load_last_seen()
    seen = list(data["seen_versions"])

    for v in versions:
        if v not in seen:
            seen.append(v)
        pending_path = os.path.join(PENDING_DIR, f"{v}.json")
        if os.path.exists(pending_path):
            os.remove(pending_path)
            print(f"removed {pending_path}")
        else:
            print(f"note: {pending_path} did not exist", file=sys.stderr)

    data["seen_versions"] = seen
    data["last_checked"] = datetime.now(timezone.utc).isoformat()
    save_last_seen(data)
    print(f"marked seen: {', '.join(versions)}")


if __name__ == "__main__":
    main()
