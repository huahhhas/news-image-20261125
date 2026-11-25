#!/usr/bin/env python3
"""Draw the 25 November 2026 world-news image (1024x1024 PNG).

Build-time script only: it renders entry.png with PIL. The submitted
entrypoint main.py is pure stdlib and just copies entry.png to the
output directory, so the graded run needs no Pillow.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- icons
def icon_cyber(d, x, y, s):
    # laptop + warning triangle
    d.rounded_rectangle([x, y + s * 0.12, x + s, y + s * 0.72], radius=8,
                        outline="#1f3a5f", width=5, fill="#dcebf7")
    d.rectangle([x - s * 0.08, y + s * 0.78, x + s * 1.08, y + s * 0.88],
                fill="#1f3a5f")
    d.polygon([(x + s * 0.5, y + s * 0.22), (x + s * 0.82, y + s * 0.62),
               (x + s * 0.18, y + s * 0.62)], fill="#d62728")
    d.rectangle([x + s * 0.47, y + s * 0.34, x + s * 0.53, y + s * 0.50],
                fill="white")
    d.rectangle([x + s * 0.47, y + s * 0.54, x + s * 0.53, y + s * 0.58],
                fill="white")


def icon_ship(d, x, y, s):
    # ship hull + waves + drone above
    d.polygon([(x, y + s * 0.45), (x + s, y + s * 0.45),
               (x + s * 0.82, y + s * 0.78), (x + s * 0.18, y + s * 0.78)],
              fill="#1f3a5f")
    d.rectangle([x + s * 0.42, y + s * 0.18, x + s * 0.58, y + s * 0.45],
                fill="#1f3a5f")
    d.rectangle([x + s * 0.30, y + s * 0.30, x + s * 0.70, y + s * 0.36],
                fill="#e8a33d")
    for i, wy in enumerate((0.84, 0.92)):
        d.arc([x - s * 0.05 + i * s * 0.1, y + s * wy, x + s * 0.25 + i * s * 0.1,
               y + s * wy + s * 0.12], 0, 180, fill="#2f7fc1", width=4)
        d.arc([x + s * 0.45 + i * s * 0.1, y + s * wy, x + s * 0.75 + i * s * 0.1,
               y + s * wy + s * 0.12], 0, 180, fill="#2f7fc1", width=4)
    # drone
    cx, cy = x + s * 0.78, y + s * 0.08
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill="#d62728")
    for dx in (-14, 14):
        d.ellipse([cx + dx - 7, cy - 7, cx + dx + 7, cy + 7],
                  outline="#d62728", width=3)


def icon_tower(d, x, y, s):
    # skyscraper with impact burst near the top
    d.rectangle([x + s * 0.30, y + s * 0.10, x + s * 0.70, y + s * 0.95],
                fill="#3a5a7c")
    d.rectangle([x + s * 0.42, y + s * 0.02, x + s * 0.58, y + s * 0.10],
                fill="#3a5a7c")
    for row in range(5):
        for col in range(2):
            d.rectangle([x + s * (0.36 + col * 0.14), y + s * (0.20 + row * 0.14),
                         x + s * (0.46 + col * 0.14), y + s * (0.28 + row * 0.14)],
                        fill="#ffd76a")
    cx, cy = x + s * 0.82, y + s * 0.30
    for ang in range(0, 360, 45):
        import math
        r1, r2 = s * 0.10, s * 0.24
        a = math.radians(ang)
        d.line([(cx + r1 * math.cos(a), cy + r1 * math.sin(a)),
                (cx + r2 * math.cos(a), cy + r2 * math.sin(a))],
               fill="#d62728", width=5)
    d.ellipse([cx - s * 0.09, cy - s * 0.09, cx + s * 0.09, cy + s * 0.09],
              fill="#e8a33d")


def icon_medical(d, x, y, s):
    # shield with a medical cross
    d.polygon([(x + s * 0.5, y), (x + s * 0.95, y + s * 0.18),
               (x + s * 0.95, y + s * 0.55), (x + s * 0.5, y + s * 0.98),
               (x + s * 0.05, y + s * 0.55), (x + s * 0.05, y + s * 0.18)],
              fill="#2e7d32")
    d.rectangle([x + s * 0.44, y + s * 0.28, x + s * 0.56, y + s * 0.68],
                fill="white")
    d.rectangle([x + s * 0.30, y + s * 0.42, x + s * 0.70, y + s * 0.54],
                fill="white")


def icon_quasar(d, x, y, s):
    # black hole glow + orbiting light
    import math
    d.ellipse([x + s * 0.08, y + s * 0.08, x + s * 0.92, y + s * 0.92],
              fill="#101828")
    d.ellipse([x + s * 0.36, y + s * 0.36, x + s * 0.64, y + s * 0.64],
              fill="#ffd76a")
    for ang in (30, 150, 270):
        a = math.radians(ang)
        d.line([(x + s * 0.5 + s * 0.34 * math.cos(a),
                 y + s * 0.5 + s * 0.34 * math.sin(a)),
                (x + s * 0.5 + s * 0.48 * math.cos(a),
                 y + s * 0.5 + s * 0.48 * math.sin(a))],
               fill="#ffd76a", width=5)
    d.ellipse([x + s * 0.72, y + s * 0.10, x + s * 0.86, y + s * 0.24],
              fill="#d62728")


def icon_chart(d, x, y, s):
    # falling market line over axes
    d.line([(x + s * 0.10, y + s * 0.12), (x + s * 0.10, y + s * 0.90),
            (x + s * 0.95, y + s * 0.90)], fill="#1f3a5f", width=5)
    pts = [(x + s * 0.14, y + s * 0.28), (x + s * 0.34, y + s * 0.38),
           (x + s * 0.52, y + s * 0.34), (x + s * 0.70, y + s * 0.58),
           (x + s * 0.90, y + s * 0.78)]
    d.line(pts, fill="#d62728", width=6, joint="curve")
    for px, py in pts:
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill="#d62728")
    d.polygon([(x + s * 0.90, y + s * 0.78), (x + s * 0.78, y + s * 0.76),
               (x + s * 0.86, y + s * 0.90)], fill="#d62728")


ICONS = {"cyber": icon_cyber, "ship": icon_ship, "tower": icon_tower,
         "medical": icon_medical, "quasar": icon_quasar, "chart": icon_chart}

STORIES = [
    ("USA  ·  CYBERATTACK", "America's spies hacked",
     "CIA and US intelligence hit by a cyber breach; unclassified data exposed.",
     "cyber", "#b3261e"),
    ("EUROPE  ·  WAR AT SEA", "War at sea widens",
     "Ukraine's drone strikes on Russian ships draw threats; NATO jets head to Poland.",
     "ship", "#1f3a5f"),
    ("MIDDLE EAST", "Riyadh tower struck",
     "Drone hits the Saudi capital's tallest tower; 11 people hurt, Houthis blamed.",
     "tower", "#8a5a00"),
    ("AFRICA  ·  HEALTH", "Ebola teams flee fighting",
     "WHO pulls health workers from a Congo hospital after days sheltering under fire.",
     "medical", "#2e7d32"),
    ("SCIENCE", "Oldest quasar found",
     "Euclid spots a black hole shining just 630m years after the Big Bang.",
     "quasar", "#4a2b7a"),
    ("ECONOMY", "Iran's rial at record low",
     "Currency plunges after US sanctions on Tehran's 'shadow banking' network.",
     "chart", "#0b6e4f"),
]

# ---------------------------------------------------------------- draw
img = Image.new("RGB", (W, H), "#f7f3ea")
d = ImageDraw.Draw(img)

# Header
d.rectangle([0, 0, W, 148], fill="#14263f")
d.rectangle([0, 148, W, 154], fill="#e8a33d")
d.text((28, 16), "THE WORLD IN ONE DAY  —  WORLD NEWS",
       font=font(BOLD, 25), fill="#ffd76a")
d.text((28, 50), "WEDNESDAY 25 NOVEMBER 2026",
       font=font(BOLD, 52), fill="white")
d.text((28, 112), "Six stories that defined the day, around the globe",
       font=font(REG, 24), fill="#c8d6e5")

# Grid of story panels
M, G = 16, 14
PW = (W - 2 * M - G) // 2
PH = 262
top = 168
for i, (tag, head, sub, icon, accent) in enumerate(STORIES):
    col, row = i % 2, i // 2
    x0 = M + col * (PW + G)
    y0 = top + row * (PH + G)
    x1, y1 = x0 + PW, y0 + PH
    d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill="white",
                        outline="#d8d2c4", width=2)
    d.rounded_rectangle([x0, y0, x1, y0 + 10], radius=5, fill=accent)
    d.rectangle([x0, y0 + 5, x1, y0 + 10], fill=accent)
    # icon box
    ix, iy, isz = x0 + 18, y0 + 26, 96
    ICONS[icon](d, ix, iy, isz)
    tx = x0 + 132
    d.text((tx, y0 + 24), tag, font=font(BOLD, 19), fill=accent)
    hl = wrap(d, head, font(BOLD, 30), PW - 150)
    yy = y0 + 52
    for line in hl:
        d.text((tx, yy), line, font=font(BOLD, 30), fill="#14263f")
        yy += 36
    sl = wrap(d, sub, font(REG, 21), PW - 36)
    sy = y0 + 148
    for line in sl[:3]:
        d.text((x0 + 18, sy), line, font=font(REG, 21), fill="#333333")
        sy += 28

# Footer
fy = top + 3 * PH + 2 * G + 6
d.rectangle([0, fy, W, H], fill="#14263f")
d.text((28, fy + 8), "Sources: Reuters · CNN · AP · ESA  —  reported 25 November 2026",
       font=font(REG, 20), fill="#c8d6e5")

img.save(OUT, "PNG", optimize=True)
print("wrote", OUT, os.path.getsize(OUT), "bytes", img.size)
