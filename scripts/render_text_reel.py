#!/usr/bin/env python3
"""Render a kinetic-text Reel (1080x1920, 30 fps) from a scenes JSON file, silent.

Usage: python3 render_text_reel.py scenes.json out.mp4
scenes.json: {"scenes": [{"dur": 2.4, "lines": [{"text": "It's 4 pm.", "style": "h1"}, ...]}, ...],
              "end": {"dur": 3.0}}   # end card with AKITA + url
Styles: h1 (white, large), accent (blue, large), dim (grey, large), small (white, medium).
Text stays inside Instagram's Reel safe zone (clear of the top bar, caption and side buttons).
"""
import json
import subprocess
import sys
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
FONT_DIR = "/usr/share/fonts/opentype/inter/"
F_DISPLAY = FONT_DIR + "InterDisplay-Bold.otf"
F_MED = FONT_DIR + "Inter-Medium.otf"
F_SEMI = FONT_DIR + "Inter-SemiBold.otf"
NAVY1, NAVY2 = (26, 51, 82), (33, 67, 108)
WHITE, ACCENT, DIM, MUTED, BLUE = (255, 255, 255), (109, 182, 230), (159, 179, 200), (201, 214, 227), (46, 134, 193)
LEFT, RIGHT_PAD = 96, 150          # right pad clears the Reel action buttons
SAFE_TOP, SAFE_BOTTOM = 330, 1420  # clears top bar and the caption area
STYLES = {
    "h1": (F_DISPLAY, 112, WHITE), "accent": (F_DISPLAY, 112, ACCENT),
    "dim": (F_DISPLAY, 112, DIM), "small": (F_MED, 56, MUTED),
}


def ease_out(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def background():
    import numpy as np
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    t = (yy / H)[..., None]
    base = np.array(NAVY1, np.float32) + (np.array(NAVY2, np.float32) - np.array(NAVY1, np.float32)) * t
    dist = np.sqrt((xx - (W - 180)) ** 2 + (yy - 140) ** 2)
    glow = np.clip(1 - dist / 820, 0, 1) ** 2
    base += np.array(BLUE, np.float32) * 0.30 * glow[..., None]
    grid = ((xx % 72) < 1) | ((yy % 72) < 1)
    base += grid[..., None] * 7.0
    return Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGB")


def wrap(draw, text, font, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def layout(draw, scene):
    blocks, y = [], 0
    width = W - LEFT - RIGHT_PAD
    for i, line in enumerate(scene["lines"]):
        path, size, color = STYLES[line.get("style", "h1")]
        font = ImageFont.truetype(path, size)
        gap = int(size * 0.28) if i else 0
        y += gap
        for txt in wrap(draw, line["text"], font, width):
            blocks.append((txt, font, color, y, i))
            y += int(size * 1.08)
    total = y
    top = SAFE_TOP + (SAFE_BOTTOM - SAFE_TOP - total) // 2
    return [(t, f, c, top + yy, i) for t, f, c, yy, i in blocks], top


def draw_scene(base, scene, t, dur):
    img = base.copy()
    d = ImageDraw.Draw(img, "RGBA")
    blocks, top = layout(d, scene)
    out_a = 1.0 if t < dur - 0.25 else max(0.0, (dur - t) / 0.25)
    rule_p = ease_out(t / 0.35)
    d.rectangle([LEFT, top - 64, LEFT + int(84 * rule_p), top - 56], fill=BLUE + (int(255 * out_a),))
    for txt, font, color, y, idx in blocks:
        start = 0.12 + idx * 0.42
        p = ease_out((t - start) / 0.45)
        a = int(255 * p * out_a)
        if a <= 0:
            continue
        d.text((LEFT, y + int(40 * (1 - p))), txt, font=font, fill=color + (a,))
    return img


def draw_end(base, t, dur):
    img = base.copy()
    d = ImageDraw.Draw(img, "RGBA")
    p = ease_out(t / 0.5)
    a = int(255 * p)
    big = ImageFont.truetype(F_DISPLAY, 190)
    sub = ImageFont.truetype(F_SEMI, 54)
    url = ImageFont.truetype(F_MED, 50)
    cy = 820
    d.text((LEFT, cy + int(30 * (1 - p))), "AKITA", font=big, fill=WHITE + (a,))
    d.rectangle([LEFT, cy + 240, LEFT + 84, cy + 248], fill=BLUE + (a,))
    p2 = ease_out((t - 0.35) / 0.5)
    d.text((LEFT, cy + 290), "Field sales software", font=sub, fill=ACCENT + (int(255 * p2),))
    d.text((LEFT, cy + 370), "akitasales.com", font=url, fill=MUTED + (int(255 * p2),))
    return img


def main():
    spec = json.load(open(sys.argv[1]))
    out = sys.argv[2]
    base = background()
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast",
                           "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for scene in spec["scenes"]:
        n = int(scene["dur"] * FPS)
        for f in range(n):
            ff.stdin.write(draw_scene(base, scene, f / FPS, scene["dur"]).tobytes())
    end = spec.get("end", {"dur": 3.0})
    for f in range(int(end["dur"] * FPS)):
        ff.stdin.write(draw_end(base, f / FPS, end["dur"]).tobytes())
    ff.stdin.close()
    ff.wait()
    print("wrote", out)


if __name__ == "__main__":
    main()
