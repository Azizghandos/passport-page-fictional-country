#!/usr/bin/env python3
"""Draw an invented passport spread for the Republic of Kavora.

A North Atlantic island nation of lighthouse keepers and fishermen.
Open spread: left = data page (drawn portrait, bilingual Kavoran/English
field labels, machine-readable strip); right = visa page (Aldermark visa
sticker, arrival/departure stamps in plausible order, harbour-dues fee stamp).

Deterministic: no network, no randomness, no timestamps. Writes entry.png
1024x1024, well under 1 MiB.
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter

W = H = 1024

# ---------------------------------------------------------------- palette
DESK = (22, 33, 52)          # deep navy desk
PAGE_L = (246, 241, 227)     # cream, data page
PAGE_R = (248, 244, 233)     # cream, visa page (a touch lighter)
INK = (31, 58, 95)           # navy ink
INK_SOFT = (74, 92, 122)     # softer navy for labels
BURGUNDY = (122, 46, 46)
TEAL = (46, 107, 98)
PURPLE = (107, 78, 138)
RUST = (138, 59, 46)
RULE = (31, 58, 95)
SKIN = (232, 195, 154)
HAIR = (91, 46, 34)
SWEATER = (34, 64, 107)
PORTRAIT_BG = (199, 210, 218)

FDIR = "/usr/share/fonts/truetype"
SERIF = f"{FDIR}/liberation/LiberationSerif-Regular.ttf"
SERIF_B = f"{FDIR}/liberation/LiberationSerif-Bold.ttf"
SERIF_I = f"{FDIR}/liberation/LiberationSerif-Italic.ttf"
SANS = f"{FDIR}/liberation/LiberationSans-Regular.ttf"
SANS_B = f"{FDIR}/liberation/LiberationSans-Bold.ttf"
MONO = f"{FDIR}/dejavu/DejaVuSansMono.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def text(d, xy, s, font, fill, anchor="la"):
    d.text(xy, s, font=font, fill=fill, anchor=anchor)


def mrz_check(s):
    """ICAO MRZ check digit: values 0-9 digits, A=10..Z=35, '<'=0; weights 7,3,1."""
    total = 0
    for i, ch in enumerate(s):
        if ch == "<":
            v = 0
        elif ch.isdigit():
            v = int(ch)
        else:
            v = ord(ch) - ord("A") + 10
        total += v * (7, 3, 1)[i % 3]
    return str(total % 10)


def mrz_lines():
    line1 = "P<KAVVANN<<MARA<ILSA" + "<" * 24
    doc = "KV847291<"                       # 9 chars incl. filler
    cd_doc = mrz_check(doc)
    dob = "880314"
    cd_dob = mrz_check(dob)
    exp = "350212"
    cd_exp = mrz_check(exp)
    personal = "<" * 14
    cd_per = mrz_check(personal)
    body = doc + cd_doc + "KAV" + dob + cd_dob + "F" + exp + cd_exp + personal + cd_per
    line2 = body + mrz_check(body)
    assert len(line1) == 44 and len(line2) == 44, (len(line1), len(line2))
    return line1, line2


# ---------------------------------------------------------------- emblem
def draw_lighthouse(d, cx, cy, s, colour, alpha=255):
    """Small lighthouse emblem, s = height in px."""
    w = s * 0.42
    # rays
    for ang in (-38, -18, 0, 18, 38):
        import math
        x2 = cx + math.sin(math.radians(ang)) * s * 0.62
        y2 = cy - s * 0.52 - math.cos(math.radians(ang)) * s * 0.28
        d.line([(cx, cy - s * 0.42), (x2, y2)], fill=colour, width=max(1, s // 26))
    # tower: tapered, two bands
    top_y = cy - s * 0.44
    base_y = cy + s * 0.30
    d.polygon([(cx - w * 0.30, top_y), (cx + w * 0.30, top_y),
               (cx + w * 0.5, base_y), (cx - w * 0.5, base_y)], fill=colour)
    d.polygon([(cx - w * 0.34, top_y + s * 0.20), (cx + w * 0.34, top_y + s * 0.20),
               (cx + w * 0.40, top_y + s * 0.32), (cx - w * 0.40, top_y + s * 0.32)],
              fill=(246, 241, 227))
    # lamp room
    d.rectangle([cx - w * 0.22, top_y - s * 0.10, cx + w * 0.22, top_y], fill=colour)
    d.rectangle([cx - w * 0.30, top_y - s * 0.13, cx + w * 0.30, top_y - s * 0.10], fill=colour)
    # base + waves
    d.rectangle([cx - w * 0.62, base_y, cx + w * 0.62, base_y + s * 0.06], fill=colour)
    for k, wy in enumerate((base_y + s * 0.14, base_y + s * 0.22)):
        d.arc([cx - w * 0.85, wy - s * 0.05, cx + w * 0.85, wy + s * 0.05],
              200, 340, fill=colour, width=max(1, s // 30))


# ---------------------------------------------------------------- portrait
def draw_portrait(d, x0, y0, x1, y1):
    """Stylised flat-illustration portrait: Mara Ilsa Vann, 37, of Port Lumen.
    Dark auburn hair tied back, navy fisherman's sweater, cream collar."""
    cx = (x0 + x1) // 2
    # background: pale blue-grey with faint guilloche lines
    d.rectangle([x0, y0, x1, y1], fill=PORTRAIT_BG)
    for yy in range(y0 + 8, y1, 14):
        d.line([(x0, yy), (x1, yy)], fill=(214, 223, 229), width=1)
    # soft light from upper left (clipped to the portrait box)
    d.ellipse([x0, y0, x0 + 130, y0 + 120], fill=(210, 220, 228))
    # shoulders / sweater
    shoulder_top = y0 + (y1 - y0) * 0.62
    d.polygon([(x0 + 6, y1), (x0 + 6, shoulder_top + 26),
               (cx - 46, shoulder_top - 6), (cx + 46, shoulder_top - 6),
               (x1 - 6, shoulder_top + 26), (x1 - 6, y1)], fill=SWEATER)
    # sweater ribbing
    for yy in range(int(shoulder_top) + 34, y1 - 4, 12):
        d.line([(x0 + 10, yy), (x1 - 10, yy)], fill=(28, 52, 88), width=1)
    # cream collar (V)
    d.polygon([(cx - 30, shoulder_top + 2), (cx, shoulder_top + 34),
               (cx + 30, shoulder_top + 2), (cx + 22, shoulder_top - 8),
               (cx, shoulder_top + 12), (cx - 22, shoulder_top - 8)], fill=(240, 234, 214))
    # neck
    d.rectangle([cx - 15, shoulder_top - 34, cx + 15, shoulder_top + 4], fill=SKIN)
    # ears
    d.ellipse([cx - 52, y0 + 92, cx - 38, y0 + 118], fill=SKIN)
    d.ellipse([cx + 38, y0 + 92, cx + 52, y0 + 118], fill=SKIN)
    # head
    d.ellipse([cx - 44, y0 + 38, cx + 44, y0 + 142], fill=SKIN)
    # hair: cap over the top of the head + side locks + bun
    d.pieslice([cx - 48, y0 + 26, cx + 48, y0 + 122], 180, 360, fill=HAIR)
    d.polygon([(cx - 48, y0 + 60), (cx - 46, y0 + 150), (cx - 30, y0 + 150),
               (cx - 34, y0 + 70)], fill=HAIR)
    d.polygon([(cx + 48, y0 + 60), (cx + 46, y0 + 150), (cx + 30, y0 + 150),
               (cx + 34, y0 + 70)], fill=HAIR)
    d.ellipse([cx + 8, y0 + 2, cx + 44, y0 + 38], fill=HAIR)   # bun
    d.arc([cx + 8, y0 + 2, cx + 44, y0 + 38], 0, 360, fill=(70, 34, 25), width=2)
    # hairline fringe
    d.pieslice([cx - 44, y0 + 34, cx + 44, y0 + 96], 180, 360, fill=HAIR)
    # eyebrows
    d.arc([cx - 30, y0 + 82, cx - 8, y0 + 96], 200, 340, fill=(58, 30, 22), width=3)
    d.arc([cx + 8, y0 + 82, cx + 30, y0 + 96], 200, 340, fill=(58, 30, 22), width=3)
    # eyes
    for ex in (cx - 19, cx + 19):
        d.ellipse([ex - 5, y0 + 98, ex + 5, y0 + 106], fill=(38, 28, 24))
        d.arc([ex - 7, y0 + 94, ex + 7, y0 + 106], 180, 360, fill=(58, 30, 22), width=2)
    # nose
    d.line([(cx, y0 + 106), (cx - 2, y0 + 124), (cx + 4, y0 + 126)],
           fill=(198, 158, 118), width=2)
    # mouth, muted rose
    d.arc([cx - 12, y0 + 130, cx + 12, y0 + 146], 15, 165, fill=(150, 84, 78), width=3)
    # cheek shading, very light
    d.ellipse([cx - 40, y0 + 112, cx - 24, y0 + 124], fill=(228, 178, 138))
    d.ellipse([cx + 24, y0 + 112, cx + 40, y0 + 124], fill=(228, 178, 138))


# ---------------------------------------------------------------- stamps
def stamp_rect(img, cx, cy, w, h, angle, colour, lines, font, small_font):
    """A rectangular ink stamp, rotated, on its own layer."""
    layer = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ox, oy = 20, 20
    ld.rounded_rectangle([ox, oy, ox + w, oy + h], radius=8,
                         outline=colour + (215,), width=3)
    ld.rounded_rectangle([ox + 5, oy + 5, ox + w - 5, oy + h - 5], radius=5,
                         outline=colour + (160,), width=1)
    n = len(lines)
    y = oy + (h - n * 17) // 2 + 2
    for i, ln in enumerate(lines):
        f = font if i == 1 else small_font
        ld.text((ox + w // 2, y), ln, font=f, fill=colour + (225,),
                anchor="ma")
        y += 17
    layer = layer.rotate(angle, resample=Image.BICUBIC, expand=False)
    img.paste(layer, (cx - (w + 40) // 2, cy - (h + 40) // 2), layer)


def stamp_oval(img, cx, cy, w, h, angle, colour, lines, font, small_font):
    layer = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ox, oy = 20, 20
    ld.ellipse([ox, oy, ox + w, oy + h], outline=colour + (215,), width=3)
    ld.ellipse([ox + 5, oy + 5, ox + w - 5, oy + h - 5],
               outline=colour + (160,), width=1)
    n = len(lines)
    y = oy + (h - n * 16) // 2 + 1
    for i, ln in enumerate(lines):
        f = font if i == 1 else small_font
        ld.text((ox + w // 2, y), ln, font=f, fill=colour + (225,), anchor="ma")
        y += 16
    layer = layer.rotate(angle, resample=Image.BICUBIC, expand=False)
    img.paste(layer, (cx - (w + 40) // 2, cy - (h + 40) // 2), layer)


# ---------------------------------------------------------------- pages
def main():
    img = Image.new("RGB", (W, H), DESK)
    d = ImageDraw.Draw(img)

    # soft shadow under the spread
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle([34, 106, 998, 932], radius=6, fill=(0, 0, 0, 110))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    img.paste(shadow, (0, 0), shadow)
    d = ImageDraw.Draw(img)

    # pages
    d.rounded_rectangle([28, 100, 500, 924], radius=4, fill=PAGE_L)
    d.rounded_rectangle([524, 100, 996, 924], radius=4, fill=PAGE_R)
    d.line([(512, 100), (512, 924)], fill=(120, 110, 88), width=2)  # spine
    d.line([(500, 100), (500, 924)], fill=(190, 180, 152), width=1)
    d.line([(524, 100), (524, 924)], fill=(190, 180, 152), width=1)

    # faint lighthouse watermarks, centred on each page
    wm = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(wm)
    draw_lighthouse(wd, 264, 560, 420, INK + (14,))
    draw_lighthouse(wd, 760, 560, 420, INK + (14,))
    img.paste(wm, (0, 0), wm)
    d = ImageDraw.Draw(img)

    # ================================================= LEFT: data page
    L, R = 54, 474          # inner content edges
    cx = (L + R) // 2

    draw_lighthouse(d, cx, 168, 46, INK)
    text(d, (cx, 196), "REPUBLIKA KAVORA", F(SERIF_B, 23), INK, anchor="ma")
    text(d, (cx, 224), "REPUBLIC OF KAVORA", F(SANS, 11), INK_SOFT, anchor="ma")
    d.line([(L, 246), (R, 246)], fill=RULE, width=2)
    d.line([(L, 250), (R, 250)], fill=RULE, width=1)

    # type / code / number row
    y = 262
    for x, lab, val in ((L, "TYPE / TYPE", "P"),
                        (L + 130, "COUNTRY CODE / LAND", "KAV"),
                        (L + 300, "PASSPORT NO. / NR.", "KV 847 291")):
        text(d, (x, y), lab, F(SANS, 9), INK_SOFT)
        text(d, (x, y + 13), val, F(SANS_B, 15), INK)
    d.line([(L, 296), (R, 296)], fill=RULE, width=1)

    # portrait
    px0, py0, px1, py1 = L, 312, L + 150, 542
    d.rectangle([px0 - 2, py0 - 2, px1 + 2, py1 + 2], outline=INK, width=2)
    draw_portrait(d, px0, py0, px1, py1)
    text(d, (px0 + 75, py1 + 8), "PORTRAIT / BILDE", F(SANS, 8), INK_SOFT, anchor="ma")

    # data fields, right of portrait
    fx = L + 168
    fields = [
        ("SURNAME / SLEKT", "VANN"),
        ("GIVEN NAMES / FORNAMN", "MARA ILSA"),
        ("NATIONALITY / NASJON", "KAVORAN"),
        ("SEX / KJØNN", "F"),
        ("DATE OF BIRTH / FØDD", "14 MAR 1988"),
        ("PLACE OF BIRTH / STAD", "PORT LUMEN, KAVORA"),
    ]
    fy = 312
    for lab, val in fields:
        text(d, (fx, fy), lab, F(SANS, 10), INK_SOFT)
        text(d, (fx, fy + 14), val, F(SANS_B, 16), INK)
        fy += 38
    # last field is long: keep it on one line at 15pt
    d.rectangle([fx, 312 + 5 * 38 + 14, R, 312 + 5 * 38 + 30], fill=PAGE_L)
    text(d, (fx, 312 + 5 * 38 + 14), "PORT LUMEN, KAVORA", F(SANS_B, 15), INK)

    # issue / expiry / authority
    y = 588
    d.line([(L, y), (R, y)], fill=RULE, width=1)
    y += 12
    text(d, (L, y), "DATE OF ISSUE / UTFERD", F(SANS, 10), INK_SOFT)
    text(d, (L, y + 14), "12 FEB 2025", F(SANS_B, 16), INK)
    text(d, (L + 170, y), "DATE OF EXPIRY / GYLDIG TIL", F(SANS, 10), INK_SOFT)
    text(d, (L + 170, y + 14), "12 FEB 2035", F(SANS_B, 16), INK)
    y += 56
    text(d, (L, y), "AUTHORITY / MYNDIGHEIT", F(SANS, 10), INK_SOFT)
    text(d, (L, y + 14), "PASSPORT OFFICE — PORT LUMEN", F(SANS_B, 15), INK)

    # signature
    y += 58
    text(d, (L, y), "MARA ILSA VANN", F(SERIF_I, 21), INK)
    d.line([(L, y + 30), (L + 230, y + 30)], fill=INK, width=1)
    text(d, (L, y + 36), "SIGNATURE / UNDERSKRIFT", F(SANS, 9), INK_SOFT)

    # machine-readable strip
    y = 800
    d.line([(L, y), (R, y)], fill=RULE, width=1)
    l1, l2 = mrz_lines()
    text(d, (L, y + 14), l1, F(MONO, 15), INK)
    text(d, (L, y + 38), l2, F(MONO, 15), INK)
    text(d, (L, y + 66), "P<KAV — KEEP THIS DOCUMENT SAFE — DETTE PASSET TILHØRER REPUBLIKKEN KAVORA",
         F(SANS, 8), INK_SOFT)

    # ================================================= RIGHT: visa page
    L2, R2 = 550, 970
    cx2 = (L2 + R2) // 2
    text(d, (L2, 128), "VISAS", F(SERIF_B, 17), INK)
    text(d, (L2, 150), "VISA — STAMPS / VISUM — STEMPLER", F(SANS, 9), INK_SOFT)
    text(d, (R2, 128), "PAGE 12", F(SANS, 10), INK_SOFT, anchor="ra")

    # ---- Aldermark visa sticker
    vx0, vy0, vx1, vy1 = L2, 176, R2, 306
    d.rectangle([vx0, vy0, vx1, vy1], fill=(238, 242, 236), outline=TEAL, width=3)
    d.rectangle([vx0 + 5, vy0 + 5, vx1 - 5, vy1 - 5], outline=TEAL, width=1)
    text(d, (vx0 + 14, vy0 + 12), "ALDERMARK", F(SERIF_B, 17), TEAL)
    text(d, (vx1 - 14, vy0 + 12), "No. AV-2025-1184", F(SANS, 10), INK_SOFT, anchor="ra")
    d.line([(vx0 + 14, vy0 + 38), (vx1 - 14, vy0 + 38)], fill=TEAL, width=1)
    visa_rows = [
        ("VISITOR VISA — SINGLE ENTRY", "90 DAYS"),
        ("CONDITION: NO EMPLOYMENT", "FEE PAID 25 ALD"),
        ("ISSUED 20 FEB 2025 — PORT LUMEN", "VALID UNTIL 20 MAY 2025"),
    ]
    yy = vy0 + 48
    for a, b in visa_rows:
        text(d, (vx0 + 14, yy), a, F(SANS_B, 12), INK)
        text(d, (vx1 - 14, yy), b, F(SANS, 12), INK, anchor="ra")
        yy += 22

    # ---- stamps
    sb = F(SANS_B, 13)
    ss = F(SANS, 11)
    # fee stamp: harbour dues (the telling detail)
    stamp_rect(img, 660, 348, 200, 62, -7, RUST,
               ["HARBOUR DUES PAID", "40 KVK — PORT LUMEN", "03 MAR 2025"], sb, ss)
    d = ImageDraw.Draw(img)
    # travel history, in order, all after the 12 FEB 2025 issue date
    stamp_rect(img, 650, 448, 196, 66, 5, INK,
               ["KAVORA — PORT LUMEN", "DEPARTURE", "03 MAR 2025"], sb, ss)
    stamp_oval(img, 868, 448, 190, 66, -5, TEAL,
               ["ALDERMARK", "ARRIVAL", "04 MAR 2025"], sb, ss)
    stamp_oval(img, 650, 542, 196, 66, -4, TEAL,
               ["ALDERMARK", "DEPARTURE", "18 MAR 2025"], sb, ss)
    stamp_rect(img, 868, 542, 190, 66, 6, PURPLE,
               ["SULAIRE", "ARRIVAL", "19 MAR 2025"], sb, ss)
    stamp_rect(img, 650, 636, 196, 66, -6, PURPLE,
               ["SULAIRE", "DEPARTURE", "02 APR 2025"], sb, ss)
    stamp_oval(img, 868, 636, 190, 66, 4, INK,
               ["KAVORA — PORT LUMEN", "ARRIVAL", "03 APR 2025"], sb, ss)
    d = ImageDraw.Draw(img)

    # footnote: the passport's owner, in both languages
    y = 700
    d.line([(L2, y), (R2, y)], fill=RULE, width=1)
    text(d, (L2, y + 14),
         "This passport remains the property of the Republic of Kavora.",
         F(SERIF_I, 12), INK_SOFT)
    text(d, (L2, y + 34),
         "Dette passet tilhører Republikken Kavora. Tap eller tyveri meldes straks",
         F(SERIF_I, 12), INK_SOFT)
    text(d, (L2, y + 54),
         "til nærmeste kavoranske havnemyndighet eller konsulat.",
         F(SERIF_I, 12), INK_SOFT)
    # small lighthouse sign-off
    draw_lighthouse(d, R2 - 24, y + 40, 34, INK_SOFT)
    text(d, (cx2, 892), "ISSUED AT PORT LUMEN — LYS HAVN — 12 FEB 2025",
         F(SANS, 9), INK_SOFT, anchor="ma")

    img.save("entry.png", optimize=True)


if __name__ == "__main__":
    main()
    print("wrote entry.png")
