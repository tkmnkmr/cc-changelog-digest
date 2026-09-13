#!/usr/bin/env python3
"""Publish out/<version>/ to site/<version>/, update site/index.html,
commit, and (unless --no-push) push to the git remote.

Usage:
    python3 scripts/publish.py <version> [--no-push]

On success prints JSON: {"report_url", "card_url", "index_url"}.

Exit codes:
    0 - success
    1 - usage / missing files error
    3 - commit succeeded but push failed, or no remote configured
        (caller should fall back to a text-only email and retry the
        push later; state was still committed locally)
"""
import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT_DIR, "out")
SITE_DIR = os.path.join(ROOT_DIR, "site")
STATE_DIR = os.path.join(ROOT_DIR, "state")

PAGES_BASE_URL = "https://tkmnkmr.github.io/cc-changelog-digest"

PUBLISH_FILES = ["report.html", "card.png", "report.png", "summary.md"]

VERSION_SORT_RE = re.compile(r"(\d+)")


def version_sort_key(v):
    parts = VERSION_SORT_RE.findall(v)
    return tuple(int(p) for p in parts) if parts else (0,)


def copy_version_dir(version):
    src_dir = os.path.join(OUT_DIR, version)
    if not os.path.isdir(src_dir):
        print(f"error: {src_dir} does not exist", file=sys.stderr)
        sys.exit(1)

    dst_dir = os.path.join(SITE_DIR, version)
    os.makedirs(dst_dir, exist_ok=True)

    copied = []
    for filename in PUBLISH_FILES:
        src = os.path.join(src_dir, filename)
        if os.path.exists(src):
            dst = os.path.join(dst_dir, filename)
            shutil.copyfile(src, dst)
            copied.append(filename)
        else:
            print(f"warning: {src} not found, skipping", file=sys.stderr)

    if "report.html" not in copied:
        print(f"error: report.html missing for {version}; cannot publish", file=sys.stderr)
        sys.exit(1)

    return copied


def list_published_versions():
    if not os.path.isdir(SITE_DIR):
        return []
    versions = []
    for name in os.listdir(SITE_DIR):
        path = os.path.join(SITE_DIR, name)
        if os.path.isdir(path) and os.path.exists(os.path.join(path, "report.html")):
            versions.append(name)
    versions.sort(key=version_sort_key, reverse=True)
    return versions


def build_index_html(versions):
    rows = []
    for v in versions:
        card_path = os.path.join(SITE_DIR, v, "card.png")
        thumb = (
            f'<img src="{html.escape(v)}/card.png" alt="v{html.escape(v)} card" class="thumb">'
            if os.path.exists(card_path)
            else '<div class="thumb thumb-empty"></div>'
        )
        rows.append(
            f'''<li class="entry">
  <a href="{html.escape(v)}/report.html">
    {thumb}
    <span class="version">v{html.escape(v)}</span>
  </a>
</li>'''
        )

    rows_html = "\n".join(rows) if rows else "<li>まだ配信履歴がありません。</li>"

    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>Claude Code Changelog Digest</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #0d1117; color: #e6edf3; margin: 0; padding: 2rem; }}
  h1 {{ font-size: 1.4rem; margin-bottom: 1.5rem; }}
  ul {{ list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 1rem; }}
  .entry a {{ display: block; text-decoration: none; color: inherit; background: #161b22; border: 1px solid #30363d; border-radius: 8px; overflow: hidden; transition: border-color 0.15s; }}
  .entry a:hover {{ border-color: #58a6ff; }}
  .thumb {{ width: 100%; aspect-ratio: 1200 / 675; object-fit: cover; display: block; background: #21262d; }}
  .thumb-empty {{ display: flex; }}
  .version {{ display: block; padding: 0.6rem 0.8rem; font-weight: 600; }}
</style>
</head>
<body>
<h1>Claude Code Changelog Digest</h1>
<ul>
{rows_html}
</ul>
</body>
</html>
"""


def update_index():
    versions = list_published_versions()
    index_html = build_index_html(versions)
    with open(os.path.join(SITE_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)


def run(cmd, **kwargs):
    return subprocess.run(cmd, cwd=ROOT_DIR, capture_output=True, text=True, **kwargs)


def git_commit(version):
    run(["git", "add", "site", "out", "state"])
    result = run(["git", "commit", "-m", f"digest: v{version}"])
    if result.returncode != 0:
        combined = (result.stdout or "") + (result.stderr or "")
        if "nothing to commit" in combined:
            print("note: nothing new to commit", file=sys.stderr)
            return True
        print(f"error: git commit failed: {combined}", file=sys.stderr)
        return False
    return True


def git_has_remote():
    result = run(["git", "remote"])
    return bool(result.stdout.strip())


def git_push():
    result = run(["git", "push"])
    if result.returncode != 0:
        print(f"error: git push failed: {result.stderr}", file=sys.stderr)
        return False
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("version")
    parser.add_argument("--no-push", action="store_true")
    args = parser.parse_args()

    copy_version_dir(args.version)
    update_index()

    committed = git_commit(args.version)
    if not committed:
        sys.exit(3)

    urls = {
        "report_url": f"{PAGES_BASE_URL}/{args.version}/report.html",
        "card_url": f"{PAGES_BASE_URL}/{args.version}/card.png",
        "index_url": f"{PAGES_BASE_URL}/",
    }

    if args.no_push:
        print(json.dumps(urls, ensure_ascii=False))
        return

    if not git_has_remote():
        print("error: no git remote configured", file=sys.stderr)
        print(json.dumps(urls, ensure_ascii=False))
        sys.exit(3)

    if not git_push():
        print(json.dumps(urls, ensure_ascii=False))
        sys.exit(3)

    print(json.dumps(urls, ensure_ascii=False))


if __name__ == "__main__":
    main()
