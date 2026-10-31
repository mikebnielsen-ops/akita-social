#!/usr/bin/env python3
"""Render a branded 1080x1350 card with an AKITA demo screenshot (phone) under a headline.

Usage: python3 render_screen_card.py '{"theme":"dark","eyebrow":"My stats","l1":"How am I doing?","l2":"Every rep can see it.","screen":"library/screens/phone-12-my-stats.png","step":"1/6"}' out.png
theme: "dark" or "light". screen: path relative to the repo. step (optional): small label top right, for carousels.
The phone sits at the bottom and bleeds off the lower edge, so the top of the screen is what people see.
"""
import base64, html, json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
spec = json.loads(sys.argv[1])
out = Path(sys.argv[2]).resolve()
img = base64.b64encode((ROOT / spec["screen"]).read_bytes()).decode()
e = lambda k: html.escape(spec.get(k, ""))

page = f"""<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1350px;overflow:hidden}}
body{{font-family:"Inter",sans-serif;position:relative}}
body.dark{{--bg1:#1A3352;--bg2:#1E3A5F;--bg3:#21436C;--ink:#FFFFFF;--acc:#6DB6E6;--eye:#8CC4E8;--muted:#C9D6E3;--grid:rgba(255,255,255,.045);--glow:rgba(46,134,193,.35);--frame:#0E1B2C}}
body.light{{--bg1:#F4F6F8;--bg2:#EEF2F6;--bg3:#E6ECF2;--ink:#1E3A5F;--acc:#2E86C1;--eye:#2E86C1;--muted:#5B6B7E;--grid:rgba(30,58,95,.06);--glow:rgba(46,134,193,.14);--frame:#1E3A5F}}
.bg{{position:absolute;inset:0;background:radial-gradient(ellipse 70% 50% at 88% 8%,var(--glow),transparent 70%),linear-gradient(160deg,var(--bg1) 0%,var(--bg2) 60%,var(--bg3) 100%)}}
.grid{{position:absolute;inset:0;background-image:repeating-linear-gradient(90deg,var(--grid) 0 1px,transparent 1px 72px),repeating-linear-gradient(0deg,var(--grid) 0 1px,transparent 1px 72px)}}
.top{{position:absolute;left:96px;right:96px;top:88px;color:var(--ink)}}
.row{{display:flex;justify-content:space-between;align-items:center}}
.eyebrow{{font-size:26px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--eye)}}
.step{{font-size:26px;font-weight:600;color:var(--muted)}}
h1{{margin-top:30px;font-weight:700;letter-spacing:-.02em;line-height:1.08;font-size:64px}}
h1 .l2{{display:block;color:var(--acc);margin-top:10px}}
.phone{{position:absolute;left:50%;transform:translateX(-50%);top:470px;width:560px;border-radius:64px 64px 0 0;background:var(--frame);padding:18px 18px 0;box-shadow:0 30px 80px rgba(0,0,0,.35)}}
.phone img{{display:block;width:100%;border-radius:48px 48px 0 0}}
.brand{{position:absolute;right:56px;bottom:40px;font-weight:800;letter-spacing:.06em;font-size:30px;color:var(--ink);background:var(--bg1);padding:8px 16px;border-radius:10px}}
</style></head><body class="{e('theme') or 'dark'}"><div class="bg"></div><div class="grid"></div>
<div class="top"><div class="row"><div class="eyebrow">{e('eyebrow')}</div><div class="step">{e('step')}</div></div>
<h1>{e('l1')}<span class="l2">{e('l2')}</span></h1></div>
<div class="phone"><img src="data:image/png;base64,{img}"></div>
<div class="brand">AKITA</div></body></html>"""
tmp = out.with_suffix(".tmp.html")
tmp.write_text(page)
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1350})
    pg.goto(tmp.as_uri())
    pg.wait_for_timeout(300)
    pg.screenshot(path=str(out), clip={"x": 0, "y": 0, "width": 1080, "height": 1350})
    b.close()
tmp.unlink()
print("wrote", out)
