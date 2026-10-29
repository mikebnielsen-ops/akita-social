#!/usr/bin/env python3
"""Render a branded AKITA post card (1080x1350 PNG) from templates/card.html.

Usage: python3 render_card.py '{"theme":"dark","eyebrow":"Live sales","l1":"It\'s 4 pm.","l2":"Do you know what your team sold today?"}' out.png
theme: "dark" (navy) or "light" (grey). l1 = hook line (white/navy), l2 = second line (accent blue).
Keep l1 + l2 under about 90 characters so the text stays large.
"""
import html, json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
spec = json.loads(sys.argv[1])
out = Path(sys.argv[2]).resolve()
tpl = (ROOT / "templates" / "card.html").read_text()
page_html = (tpl.replace("{{THEME}}", spec.get("theme", "dark"))
             .replace("{{EYEBROW}}", html.escape(spec.get("eyebrow", "")))
             .replace("{{L1}}", html.escape(spec["l1"]))
             .replace("{{L2}}", html.escape(spec.get("l2", ""))))
tmp = out.with_suffix(".tmp.html")
tmp.write_text(page_html)
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
    pg.goto(tmp.as_uri())
    pg.wait_for_timeout(250)
    pg.screenshot(path=str(out), clip={"x": 0, "y": 0, "width": 1080, "height": 1350})
    b.close()
tmp.unlink()
print("wrote", out)
