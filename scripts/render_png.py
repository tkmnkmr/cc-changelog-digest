#!/usr/bin/env python3
"""Render out/<version>/card.html and report.html to PNG via Playwright.

Usage:
    python3 scripts/render_png.py <version>

Produces:
    out/<version>/card.png    (1200x675, device_scale_factor=2)
    out/<version>/report.png  (width 1000, full page)

Missing HTML files are skipped with a warning (exit code stays 0 unless
neither file exists, and even then we just warn — rendering is best
effort so publish can still proceed with a text-only fallback).
"""
import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def render(version):
    out_dir = os.path.join(ROOT_DIR, "out", version)
    card_html = os.path.join(out_dir, "card.html")
    report_html = os.path.join(out_dir, "report.html")
    card_png = os.path.join(out_dir, "card.png")
    report_png = os.path.join(out_dir, "report.png")

    if not os.path.isdir(out_dir):
        print(f"error: {out_dir} does not exist", file=sys.stderr)
        sys.exit(1)

    did_any = False

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("error: playwright is not importable; cannot render PNGs", file=sys.stderr)
        sys.exit(1)

    with sync_playwright() as p:
        browser = p.chromium.launch()

        if os.path.exists(card_html):
            page = browser.new_page(viewport={"width": 1200, "height": 675}, device_scale_factor=2)
            page.goto(f"file://{card_html}")
            page.screenshot(path=card_png)
            page.close()
            did_any = True
            print(f"wrote {card_png}")
        else:
            print(f"warning: {card_html} not found, skipping card.png", file=sys.stderr)

        if os.path.exists(report_html):
            page = browser.new_page(viewport={"width": 1000, "height": 800})
            page.goto(f"file://{report_html}")
            page.screenshot(path=report_png, full_page=True)
            page.close()
            did_any = True
            print(f"wrote {report_png}")
        else:
            print(f"warning: {report_html} not found, skipping report.png", file=sys.stderr)

        browser.close()

    if not did_any:
        print(f"error: neither card.html nor report.html found in {out_dir}", file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) != 2:
        print("usage: python3 scripts/render_png.py <version>", file=sys.stderr)
        sys.exit(1)
    render(sys.argv[1])


if __name__ == "__main__":
    main()
