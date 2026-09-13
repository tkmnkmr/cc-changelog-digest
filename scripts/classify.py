#!/usr/bin/env python3
"""Classify Claude Code changelog lines into digest categories.

Reworked (not copy-pasted) from the keyword-dictionary approach in
~/code/rss-changelog-monitor/changelog_parser.py, adapted to this
project's category set:

  breaking / major / model / added / changed / removed / fixed / other

Usage as a library:
    from classify import classify_line, classify_lines

Usage as a CLI:
    cat lines.txt | python3 scripts/classify.py > classified.json
"""
import json
import re
import sys

# Category keyword definitions, checked in priority order (lower number
# wins when multiple categories match the same line).
CATEGORY_KEYWORDS = {
    "breaking": {
        "priority": 1,
        "keywords": [
            "breaking", "breaking change", "must", "required migration",
            "migration required", "incompatible", "backwards incompatible",
            "no longer supported", "requires you to", "you must now",
        ],
    },
    "model": {
        "priority": 2,
        "keywords": [
            "opus", "sonnet", "haiku", "fable", "claude opus", "claude sonnet",
            "claude haiku", "model", "models", "claude-3", "claude-4",
            "claude 3", "claude 4",
        ],
    },
    "removed": {
        "priority": 3,
        "keywords": [
            "removed", "deprecated", "deprecation", "no longer", "drop support",
            "dropped support", "end of life", "unsupported", "obsolete",
            "disabled by default", "sunset",
        ],
    },
    "major": {
        "priority": 4,
        "keywords": [
            "major", "overhaul", "rewrite", "rewritten", "revamped",
            "significant", "new architecture", "ga release", "generally available",
        ],
    },
    "added": {
        "priority": 5,
        "keywords": [
            "added", "add ", "new ", "introduce", "introduced", "introducing",
            "now supports", "now support", "enable", "support for",
        ],
    },
    "changed": {
        "priority": 6,
        "keywords": [
            "changed", "change ", "updated", "update ", "improved", "improve ",
            "renamed", "moved", "switched", "replaced", "now defaults",
            "default", "behavior", "performance", "faster", "optimized",
        ],
    },
    "fixed": {
        "priority": 7,
        "keywords": [
            "fixed", "fix ", "bug fix", "resolved", "resolves", "patched",
            "regression", "crash", "hang", "hanging", "deadlock", "race condition",
            "unexpectedly", "incorrect", "broken",
        ],
    },
}

# Order categories by priority once at import time.
_ORDERED_CATEGORIES = sorted(CATEGORY_KEYWORDS.items(), key=lambda kv: kv[1]["priority"])

TAG_RE = re.compile(r"^\s*\[([A-Za-z0-9 _.\-]+)\]\s*")
BULLET_RE = re.compile(r"^\s*[-*•]\s*")


def _strip_bullet(line):
    return BULLET_RE.sub("", line).strip()


def extract_tags(line):
    """Extract leading bracketed product tags, e.g. '[VSCode] Fixed ...'."""
    tags = []
    remainder = _strip_bullet(line)
    while True:
        m = TAG_RE.match(remainder)
        if not m:
            break
        tags.append(m.group(1))
        remainder = remainder[m.end():]
    return tags, remainder


def classify_line(line):
    """Classify a single changelog line.

    Returns a dict: {"text", "category", "confidence", "tags"}.
    """
    tags, remainder = extract_tags(line)
    text = remainder.strip() if remainder.strip() else _strip_bullet(line)
    lower = text.lower()

    matched_category = None
    match_count = 0
    for category_name, info in _ORDERED_CATEGORIES:
        hits = sum(1 for kw in info["keywords"] if kw in lower)
        if hits:
            matched_category = category_name
            match_count = hits
            break

    if matched_category is None:
        return {"text": text, "category": "other", "confidence": "low", "tags": tags}

    confidence = "high" if match_count >= 1 and len(text) >= 8 else "low"
    return {"text": text, "category": matched_category, "confidence": confidence, "tags": tags}


def classify_lines(lines):
    return [classify_line(line) for line in lines if line.strip()]


def main():
    text = sys.stdin.read()
    lines = [l for l in text.split("\n") if l.strip()]
    result = classify_lines(lines)
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
