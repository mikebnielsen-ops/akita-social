import html, json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
"""Render a 1200x630 blog cover from templates/card.html.

Usage: python3 scripts/render_hero.py '{"theme":"dark|light","eyebrow":"Topic","l1":"Line one","l2":"Line two"}' out.png
"""
ROOT = Path(__file__).resolve().parent.parent
tpl = (ROOT / "templates" / "card.html").read_text()
tpl = (tpl.replace("width:1080px;height:1350px", "width:1200px;height:630px")
          .replace("inset:104px 96px 96px", "inset:56px 72px 52px")
          .replace("font-size:92px", "font-size:64px")
          .replace("font-size:26px;font-weight:600;letter-spacing:.16em", "font-size:20px;font-weight:600;letter-spacing:.16em")
          .replace("margin-bottom:36px", "margin-bottom:22px")
          .replace("font-size:28px;color:var(--muted)", "font-size:22px;color:var(--muted)")
          .replace("font-size:34px", "font-size:26px"))
spec = json.loads(sys.argv[1]); out = Path(sys.argv[2]).resolve()
page = (tpl.replace("{{THEME}}", spec.get("theme","dark")).replace("{{EYEBROW}}", html.escape(spec.get("eyebrow","")))
           .replace("{{L1}}", html.escape(spec["l1"])).replace("{{L2}}", html.escape(spec.get("l2",""))))
tmp = out.with_suffix(".tmp.html"); tmp.write_text(page)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":1200,"height":630}, device_scale_factor=1)
    pg.goto(tmp.as_uri()); pg.wait_for_timeout(250); pg.screenshot(path=str(out)); b.close()
tmp.unlink(); print("wrote", out)
