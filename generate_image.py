#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news front page (1024x1024 PNG).

Deterministic: no randomness, no timestamps, fixed layout and palette.
Run:  python3 generate_image.py   -> writes entry.png next to this file.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36

PAPER = (247, 243, 232)
INK = (18, 22, 32)
RED = (163, 22, 33)
DARKRED = (120, 16, 26)
NAVY = (16, 28, 52)
MIDNIGHT = (10, 18, 36)
GREY = (90, 88, 80)
LIGHT = (233, 227, 210)
CHART_BG = (238, 240, 244)
GREEN = (34, 120, 74)
TEAL = (18, 110, 120)
BROWN = (140, 96, 54)
BLUE = (40, 90, 170)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, text, x, y, size=24):
    fnt = font(SANS, size)
    draw.text((x, y), text, font=fnt, fill=RED)
    return y + size + 8


def story_block(draw, x, y, width, kick, headline, subhead,
                head_size=44, sub_size=25, head_leading=52, sub_leading=32):
    """Kicker + wrapped headline + wrapped subhead; returns bottom y."""
    y = kicker(draw, kick, x, y)
    hf = font(SERIF, head_size)
    lines = wrap(draw, headline, hf, width)
    y = draw_lines(draw, lines, x, y, hf, INK, head_leading)
    y += 6
    sf = font(SERIF_REG, sub_size)
    lines = wrap(draw, subhead, sf, width)
    y = draw_lines(draw, lines, x, y, sf, (52, 52, 52), sub_leading)
    return y


def draw_missile_panel(draw, x0, y0, x1, y1):
    """Night sky over a coastline: two missile trails, a blast glow,
    rooftops below and a small Polish flag. Pure vector shapes."""
    draw.rectangle([x0, y0, x1, y1], fill=MIDNIGHT)
    # Stars.
    stars = [(18, 26), (70, 60), (130, 24), (190, 74), (250, 30),
             (305, 66), (45, 110), (160, 120), (285, 130), (330, 40)]
    for sx, sy in stars:
        draw.ellipse([x0 + sx - 2, y0 + sy - 2, x0 + sx + 2, y0 + sy + 2],
                     fill=(220, 225, 240))
    # Moon.
    draw.ellipse([x0 + 300, y0 + 18, x0 + 340, y0 + 58], fill=(235, 232, 210))
    # Missile trails: bright diagonal streaks with glow.
    for (tx0, ty0, tx1, ty1) in [(30, 210, 210, 90), (90, 240, 300, 130)]:
        draw.line([x0 + tx0, y0 + ty0, x0 + tx1, y0 + ty1],
                  fill=(255, 150, 60), width=10)
        draw.line([x0 + tx0, y0 + ty0, x0 + tx1, y0 + ty1],
                  fill=(255, 240, 200), width=4)
        draw.ellipse([x0 + tx1 - 7, y0 + ty1 - 7, x0 + tx1 + 7, y0 + ty1 + 7],
                     fill=(255, 220, 120))
    # Blast glow near the ground.
    cx, cy = x0 + 120, y0 + 235
    for r, col in [(46, (255, 120, 40)), (30, (255, 180, 60)),
                   (16, (255, 235, 160))]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    # Rooftops silhouette.
    base = y1 - 34
    draw.rectangle([x0, base, x1, y1], fill=(6, 10, 22))
    roofs = [(0, 46, 60), (60, 30, 110), (110, 52, 170), (170, 34, 230),
             (230, 48, 290), (290, 30, 368)]
    for rx0, rh, rx1 in roofs:
        draw.rectangle([x0 + rx0, base - rh, x0 + rx1, base],
                       fill=(6, 10, 22))
        draw.polygon([(x0 + rx0, base - rh), (x0 + (rx0 + rx1) // 2,
                       base - rh - 18), (x0 + rx1, base - rh)],
                     fill=(6, 10, 22))
    # Lit windows.
    for wx in (20, 85, 145, 205, 255, 315):
        draw.rectangle([x0 + wx, base - 14, x0 + wx + 10, base - 4],
                       fill=(255, 200, 90))
    # Polish flag (white over red) on a pole.
    px, py = x0 + 300, base - 96
    draw.line([px, py, px, base], fill=(200, 200, 200), width=3)
    draw.rectangle([px, py, px + 44, py + 12], fill=(255, 255, 255))
    draw.rectangle([px, py + 12, px + 44, py + 24], fill=(220, 20, 60))
    # Caption inside the panel.
    cf = font(SANS, 19)
    draw.text((x0 + 14, y1 - 30), "MISSILES CROSS INTO POLAND",
              font=cf, fill=(255, 255, 255))


def draw_chart_panel(draw, x0, y0, x1, y1):
    """Falling market chart: grid, red plunge line, big -3.7% label."""
    draw.rectangle([x0, y0, x1, y1], fill=CHART_BG)
    draw.rectangle([x0, y0, x1, y1], outline=GREY, width=2)
    # Grid.
    for gx in range(x0 + 40, x1, 40):
        draw.line([gx, y0 + 12, gx, y1 - 44], fill=(210, 214, 222), width=1)
    for gy in range(y0 + 28, y1 - 40, 28):
        draw.line([x0 + 12, gy, x1 - 12, gy], fill=(210, 214, 222), width=1)
    # Falling line across the top half of the panel.
    pts = [(x0 + 20, y0 + 22), (x0 + 80, y0 + 30), (x0 + 130, y0 + 28),
           (x0 + 190, y0 + 48), (x0 + 240, y0 + 46), (x0 + 300, y0 + 70),
           (x0 + 350, y0 + 68), (x1 - 24, y0 + 92)]
    draw.line(pts, fill=RED, width=6, joint="curve")
    # Arrowhead at the end.
    ex, ey = pts[-1]
    draw.polygon([(ex, ey), (ex - 18, ey - 12), (ex - 4, ey - 20)],
                 fill=RED)
    # Big figure under the line, clear of the bottom label.
    bf = font(SANS, 52)
    draw.text((x0 + 18, y0 + 102), "-3.7%", font=bf, fill=RED)
    sf = font(SANS_REG, 20)
    draw.text((x0 + 190, y0 + 122), "US STOCKS, FRIDAY",
              font=sf, fill=INK)
    draw.text((x0 + 18, y1 - 30), "NVIDIA: RECORD WIPEOUT",
              font=font(SANS, 20), fill=GREY)


def draw_icon(draw, x, y, kind):
    """Small 76x76 story icon, drawn from primitives."""
    size = 76
    if kind == "quake":
        draw.rectangle([x, y, x + size, y + size], fill=BROWN)
        draw.line([x + 8, y + 58, x + 24, y + 40, x + 38, y + 54,
                   x + 54, y + 34, x + 68, y + 48], fill=(255, 235, 200),
                  width=5, joint="curve")
        draw.rectangle([x + 14, y + 12, x + 34, y + 36], fill=(255, 235, 200))
        draw.rectangle([x + 44, y + 18, x + 62, y + 36], fill=(255, 235, 200))
    elif kind == "climate":
        draw.rectangle([x, y, x + size, y + size], fill=GREEN)
        draw.ellipse([x + 14, y + 14, x + 62, y + 62],
                     outline=(230, 245, 230), width=5)
        draw.arc([x + 22, y + 24, x + 54, y + 52], 200, 340,
                 fill=(230, 245, 230), width=4)
        draw.line([x + 38, y + 14, x + 38, y + 62], fill=(230, 245, 230),
                  width=3)
    elif kind == "iran":
        draw.rectangle([x, y, x + size, y + size], fill=TEAL)
        draw.rounded_rectangle([x + 18, y + 12, x + 58, y + 50],
                               radius=6, fill=(220, 240, 240))
        draw.line([x + 18, y + 24, x + 58, y + 24], fill=TEAL, width=3)
        draw.line([x + 18, y + 38, x + 58, y + 38], fill=TEAL, width=3)
        draw.arc([x + 10, y + 52, x + 36, y + 68], 180, 360,
                 fill=(220, 240, 240), width=4)
        draw.arc([x + 40, y + 52, x + 66, y + 68], 180, 360,
                 fill=(220, 240, 240), width=4)
    elif kind == "cyclone":
        draw.rectangle([x, y, x + size, y + size], fill=BLUE)
        for r, start in [(28, 0), (20, 90), (12, 180)]:
            draw.arc([x + 38 - r, y + 34 - r, x + 38 + r, y + 34 + r],
                     start, start + 270, fill=(225, 238, 255), width=5)
        draw.ellipse([x + 33, y + 29, x + 43, y + 39], fill=(225, 238, 255))
        for rx in (14, 30, 46, 62):
            draw.line([x + rx, y + 62, x + rx - 4, y + 70],
                      fill=(225, 238, 255), width=3)


def grid_story(draw, x, y, width, icon, kick, headline, subhead):
    draw_icon(draw, x, y + 4, icon)
    tx = x + 92
    tw = width - 92
    kicker(draw, kick, tx, y, size=20)
    hf = font(SERIF, 24)
    lines = wrap(draw, headline, hf, tw)
    yy = draw_lines(draw, lines, tx, y + 26, hf, INK, 30)
    sf = font(SERIF_REG, 21)
    lines = wrap(draw, subhead, sf, tw)
    draw_lines(draw, lines, tx, yy + 3, sf, (52, 52, 52), 26)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # --- Masthead ---
    name = "THE WORLD TODAY"
    nf = font(SERIF, 82)
    nw = draw.textlength(name, font=nf)
    draw.text(((W - nw) / 2, 16), name, font=nf, fill=NAVY)
    draw.line([MARGIN, 116, W - MARGIN, 116], fill=RED, width=5)
    draw.line([MARGIN, 124, W - MARGIN, 124], fill=INK, width=2)

    # --- Date line ---
    date = "SATURDAY, 21 NOVEMBER 2026"
    df = font(SANS, 36)
    dw = draw.textlength(date, font=df)
    draw.text(((W - dw) / 2, 134), date, font=df, fill=DARKRED)
    draw.line([MARGIN, 178, W - MARGIN, 178], fill=INK, width=2)

    # --- Lead story: Poland ---
    story_block(draw, MARGIN, 190, 560,
                "WAR IN EUROPE  •  POLAND",
                "RUSSIAN MISSILES HIT POLAND",
                "Two missiles and a suspected drone come down in "
                "Poland. Warsaw calls it a deliberate provocation; "
                "NATO calls it a grave violation of its airspace.",
                head_size=56, sub_size=26, head_leading=60, sub_leading=32)
    draw_missile_panel(draw, 624, 190, W - MARGIN, 486)

    # --- Markets ---
    draw.line([MARGIN, 500, W - MARGIN, 500], fill=GREY, width=2)
    draw_chart_panel(draw, MARGIN, 512, 424, 700)
    story_block(draw, 452, 512, W - MARGIN - 452,
                "MARKETS  •  WALL STREET",
                "WALL STREET ENTERS CORRECTION",
                "US stocks fall about 3.7% as AI and chip shares plunge.",
                head_size=40, sub_size=24, head_leading=46, sub_leading=30)

    # --- Four more stories, 2 x 2 grid ---
    draw.line([MARGIN, 712, W - MARGIN, 712], fill=GREY, width=2)
    col_w = (W - 2 * MARGIN - 24) // 2
    grid_story(draw, MARGIN, 726, col_w, "quake", "PERU",
               "EARTHQUAKE SHAKES PERU",
               "Strong tremor widely reported; details still emerging.")
    grid_story(draw, MARGIN + col_w + 24, 726, col_w, "climate",
               "CLIMATE  •  COP31",
               "COP31 TALKS IN OVERTIME",
               "Fossil-fuel deadlock pushes talks past schedule.")
    grid_story(draw, MARGIN, 844, col_w, "iran", "MIDDLE EAST",
               "IRAN: TALKS VS BLOCKADE",
               "Tehran seeks talks to end the war; oil exports restart "
               "despite a US naval blockade.")
    grid_story(draw, MARGIN + col_w + 24, 844, col_w, "cyclone", "INDIA",
               "CYCLONE AKVAN AFTERMATH",
               "300,000 evacuated as the storm crosses the "
               "Odisha-Andhra coast.")

    # --- Footer briefs ---
    draw.line([MARGIN, 968, W - MARGIN, 968], fill=INK, width=2)
    ff = font(SERIF, 20)
    footer = ("ALSO TODAY:  Myanmar calls the ICJ genocide ruling "
              "\"unfair\"  •  UK signs three EU deals in Brussels  •  "
              "Trump-Xi-Putin summit ends with few results.")
    lines = wrap(draw, footer, ff, W - 2 * MARGIN)
    draw_lines(draw, lines, MARGIN, 976, ff, INK, 24)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
