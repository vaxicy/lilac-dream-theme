#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate-preview-website.py
Generate a wide landscape hero/preview image for the personal website themes page:
https://lilinhuang.site/themes/

Shows all 5 Lilac theme variants in a polished 3+2 grid collage with shadows,
rounded corners, and bilingual labels. Output is optimized for web hero use.

Output: store-assets/preview-website.png  (1600 x 900)
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "store-assets", "preview-website.png")


def load_font(size, bold=False):
    candidates = [
        ("C:/Windows/Fonts/msyhbd.ttc", 0),
        ("C:/Windows/Fonts/msyh.ttc", 0),
        ("C:/Windows/Fonts/arialbd.ttf", 0),
        ("C:/Windows/Fonts/arial.ttf", 0),
    ]
    for path, idx in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


# Theme palettes used in the mockups
DAWN = {
    "bg": (0xF7, 0xF6, 0xFA), "sidebar": (0xFA, 0xF9, 0xFD),
    "activitybar": (0xF5, 0xF3, 0xF9), "tab_active": (0xF7, 0xF6, 0xFA),
    "tab_inact": (0xF3, 0xF1, 0xF7), "widget": (0xFD, 0xFD, 0xFF),
    "titlebar": (0xFA, 0xF9, 0xFD), "statusbar": (0xBE, 0x9F, 0xE1),
    "accent": (0xBE, 0x9F, 0xE1), "hover": (0xDC, 0xD0, 0xEE),
    "select": (0xEF, 0xE8, 0xF6), "text": (0x33, 0x2F, 0x3C),
    "sub": (0xA6, 0x99, 0xB2), "keyword": (0xB3, 0x8F, 0xD9),
    "string": (0x97, 0x7A, 0xC9),
}

DREAM = {
    "bg": (0xF3, 0xF1, 0xF8), "sidebar": (0xF4, 0xF1, 0xF9),
    "activitybar": (0xED, 0xE8, 0xF4), "tab_active": (0xF3, 0xF1, 0xF8),
    "tab_inact": (0xE8, 0xE2, 0xF0), "widget": (0xFC, 0xFB, 0xFD),
    "titlebar": (0xF4, 0xF1, 0xF9), "statusbar": (0xBE, 0x9F, 0xE1),
    "accent": (0xBE, 0x9F, 0xE1), "hover": (0xC9, 0xB6, 0xE4),
    "select": (0xE1, 0xCC, 0xEC), "text": (0x2E, 0x2A, 0x36),
    "sub": (0x9B, 0x8C, 0xA7), "keyword": (0xA6, 0x7D, 0xD8),
    "string": (0x8A, 0x6B, 0xBE),
}

BLOOM = {
    "bg": (0xEF, 0xEC, 0xF6), "sidebar": (0xEC, 0xE7, 0xF4),
    "activitybar": (0xE3, 0xDA, 0xEF), "tab_active": (0xEF, 0xEC, 0xF6),
    "tab_inact": (0xDD, 0xD2, 0xEC), "widget": (0xF8, 0xF5, 0xFD),
    "titlebar": (0xEC, 0xE7, 0xF4), "statusbar": (0xA6, 0x7D, 0xD8),
    "accent": (0xA6, 0x7D, 0xD8), "hover": (0xBE, 0x9F, 0xE1),
    "select": (0xD2, 0xB9, 0xEA), "text": (0x2A, 0x26, 0x33),
    "sub": (0x8F, 0x7E, 0xA0), "keyword": (0x8E, 0x5F, 0xC8),
    "string": (0x78, 0x57, 0xAD),
}

DUSK = {
    "bg": (0xE4, 0xDF, 0xEE), "sidebar": (0xE0, 0xD9, 0xEC),
    "activitybar": (0xC9, 0xBE, 0xE0), "tab_active": (0xE4, 0xDF, 0xEE),
    "tab_inact": (0xCE, 0xC4, 0xDE), "widget": (0xF0, 0xEC, 0xF8),
    "titlebar": (0xE0, 0xD9, 0xEC), "statusbar": (0x7A, 0x4A, 0xB8),
    "accent": (0x7A, 0x4A, 0xB8), "hover": (0x9A, 0x72, 0xD0),
    "select": (0xB8, 0x9C, 0xDC), "text": (0x23, 0x1F, 0x2D),
    "sub": (0x7A, 0x6A, 0x8E), "keyword": (0x6A, 0x3C, 0xA8),
    "string": (0x57, 0x3A, 0x8E),
}

NIGHT = {
    "bg": (0x1B, 0x16, 0x2A), "sidebar": (0x21, 0x1B, 0x33),
    "activitybar": (0x16, 0x12, 0x24), "tab_active": (0x1B, 0x16, 0x2A),
    "tab_inact": (0x24, 0x1E, 0x38), "widget": (0x2A, 0x23, 0x40),
    "titlebar": (0x21, 0x1B, 0x33), "statusbar": (0x8E, 0x5F, 0xC8),
    "accent": (0xB3, 0x8F, 0xE6), "hover": (0x33, 0x2A, 0x4E),
    "select": (0x3A, 0x2F, 0x57), "text": (0xE6, 0xDF, 0xF2),
    "sub": (0x9B, 0x8C, 0xB2), "keyword": (0xC4, 0x9B, 0xEE),
    "string": (0xA6, 0x7F, 0xD8),
}

CODE = [
    ("keyword", "function"), ("text", " greet"), ("punct", "() {"),
    ("", ""),
    ("keyword", "  const"), ("text", " name"), ("punct", " = "), ("string", '"Lilac Dream"'),
    ("keyword", "  return"), ("text", " name"), ("punct", " + "), ("string", '" says hi"'),
    ("punct", "}"),
    ("", ""),
    ("comment", "// A soft lilac pastel theme sample"),
    ("keyword", "const"), ("text", " palette"), ("punct", " = ["),
    ("string", '"#BE9FE1"'), ("punct", ", "), ("string", '"#F1F1F6"'),
    ("punct", "]"),
    ("", ""),
    ("keyword", "import"), ("text", " Theme"), ("punct", " from "), ("string", "'./theme'"),
]


def draw_rounded_rect(img, xy, radius, fill, outline=None, width=1):
    """Draw a rounded rectangle on an image."""
    d = ImageDraw.Draw(img)
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def draw_editor_mockup(pal, w, h, label):
    """Render a single VS Code-style editor mockup into an RGBA image."""
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # activity bar (left thin strip)
    ab_w = max(34, int(w * 0.10))
    ax = 0
    d.rectangle([ax, 0, ax + ab_w, h], fill=pal["activitybar"])
    d.rectangle([ax, 90, ax + ab_w, 124], fill=pal["accent"])

    # sidebar
    sb_w = int(w * 0.24)
    sbx = ax + ab_w
    d.rectangle([sbx, 0, sbx + sb_w, h], fill=pal["sidebar"])

    # sidebar header + tree
    d.text((sbx + 10, 10), "Explorer", font=load_font(12, True), fill=pal["text"])
    d.line([(sbx, 30), (sbx + sb_w, 30)], fill=pal["select"], width=1)
    fy = 44
    for f in ["package.json", "themes/", "README.md", "scripts/"]:
        col = pal["sub"] if f.endswith("/") else pal["text"]
        d.text((sbx + 10, fy), f, font=load_font(10), fill=col)
        fy += 18

    # editor column
    ex0 = sbx + sb_w + 4
    ex1 = w - 4

    # title bar
    tb_h = 24
    d.rectangle([ex0, 0, ex1, tb_h], fill=pal["titlebar"])
    d.text((ex0 + 8, 7), "Lilac Dream", font=load_font(9), fill=pal["sub"])

    # tab bar
    tab_y = tb_h
    tab_h = 22
    tab_w = min(90, int((ex1 - ex0) * 0.38))
    d.rectangle([ex0, tab_y, ex0 + tab_w, tab_y + tab_h], fill=pal["tab_active"])
    d.rectangle([ex0, tab_y + tab_h - 2, ex0 + tab_w, tab_y + tab_h], fill=pal["accent"])
    d.text((ex0 + 8, tab_y + 5), "main.js", font=load_font(9), fill=pal["text"])

    # editor background
    edy0 = tab_y + tab_h
    d.rectangle([ex0, edy0, ex1, h - 18], fill=pal["bg"])

    # code lines
    cx = ex0 + 10
    cy = edy0 + 12
    line_h = 15
    for scope, txt in CODE:
        if scope == "" and txt == "":
            cy += line_h * 0.6
            continue
        color = {
            "keyword": pal["keyword"], "string": pal["string"],
            "comment": pal["sub"], "text": pal["text"], "punct": pal["sub"],
        }.get(scope, pal["text"])
        fnt = load_font(10, bold=(scope == "keyword"))
        d.text((cx, cy), txt, font=fnt, fill=color)
        cy += line_h
        if cy > h - 60:
            break

    # suggest widget
    sw_w = min(140, ex1 - ex0 - 30)
    sw_h = 54
    sw_x = ex0 + 24
    sw_y = edy0 + 92
    if sw_x + sw_w < ex1 and sw_y + sw_h < h - 30:
        d.rectangle([sw_x, sw_y, sw_x + sw_w, sw_y + sw_h], fill=pal["widget"],
                    outline=pal["select"], width=1)
        d.text((sw_x + 8, sw_y + 4), "theme.list", font=load_font(9, True), fill=pal["text"])
        d.rectangle([sw_x, sw_y + 18, sw_x + sw_w, sw_y + 19], fill=pal["select"], width=1)
        d.text((sw_x + 8, sw_y + 24), "theme.load()", font=load_font(9), fill=pal["text"])
        d.text((sw_x + 8, sw_y + 38), "theme.store", font=load_font(9), fill=pal["text"])

    # status bar
    d.rectangle([0, h - 18, w, h], fill=pal["statusbar"])
    sb_fg = (255, 255, 255) if pal["statusbar"][0] > 0x80 else (0xE6, 0xDF, 0xF2)
    d.text((8, h - 15), "Lilac", font=load_font(9), fill=sb_fg)
    d.text((w - 70, h - 15), "Ln 1  Col 1", font=load_font(8), fill=sb_fg)

    # divider
    d.line([(sbx + sb_w, 0), (sbx + sb_w, h - 18)], fill=pal["select"], width=2)

    # label badge
    badge_h = 22
    badge_w = min(130, w - 20)
    d.rounded_rectangle([8, 8, 8 + badge_w, 8 + badge_h], radius=6,
                        fill=pal["accent"])
    d.text((16, 13), label, font=load_font(11, True), fill=(255, 255, 255))

    return img


def make_shadow(w, h, radius, opacity=0.18):
    """Create a soft shadow layer."""
    shadow = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(shadow)
    d.rounded_rectangle([10, 10, 10 + w, 10 + h], radius=radius, fill=(0, 0, 0, int(255 * opacity)))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=10))
    return shadow


def main():
    W, H = 1600, 900
    img = Image.new("RGB", (W, H), (0xF8, 0xF6, 0xFB))
    d = ImageDraw.Draw(img)

    # Soft gradient-ish background: large radial wash at top center
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for r in range(700, 0, -10):
        alpha = int(14 * (1 - r / 700))
        od.ellipse([(W // 2 - r, -100 - r), (W // 2 + r, 300 + r)],
                   fill=(0xBE, 0x9F, 0xE1, alpha))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    d = ImageDraw.Draw(img)

    # Title
    title = "Lilac Dream Theme"
    subtitle = "A soft lilac-inspired VS Code theme family · 淡紫丁香主题系列"
    d.text((W // 2, 64), title, font=load_font(42, True), fill=(0x4A, 0x3F, 0x5C),
           anchor="mm")
    d.text((W // 2, 112), subtitle, font=load_font(18), fill=(0x7A, 0x6A, 0x8E),
           anchor="mm")

    # Layout: 3 on top row, 2 on bottom row (centered)
    pad_x = 60
    pad_y_top = 150
    gap = 24
    card_w = (W - pad_x * 2 - gap * 2) // 3
    card_h = 290

    cells = [
        (DAWN,  "Lilac Dawn · 晨薰",   0, 0),
        (DREAM, "Lilac Dream · 梦薰",  1, 0),
        (BLOOM, "Lilac Bloom · 盛薰",  2, 0),
        (DUSK,  "Lilac Dusk · 暮薰",   0, 1),
        (NIGHT, "Lilac Night · 夜薰",  1, 1),
    ]

    for pal, label, col, row in cells:
        if row == 0:
            x = pad_x + col * (card_w + gap)
            y = pad_y_top
        else:
            # center the two bottom cards in the 3-column width
            total_w = card_w * 2 + gap
            start_x = (W - total_w) // 2
            x = start_x + col * (card_w + gap)
            y = pad_y_top + card_h + gap

        mock = draw_editor_mockup(pal, card_w, card_h, label)
        shadow = make_shadow(card_w, card_h, radius=12)
        img.paste(shadow, (x - 10, y - 10), shadow)
        # card background rounded frame
        draw_rounded_rect(img, [x, y, x + card_w, y + card_h], 12,
                          fill=(255, 255, 255), outline=(0xE1, 0xCC, 0xEC), width=1)
        img.paste(mock, (x, y), mock)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, "PNG")
    print("saved:", OUT)


if __name__ == "__main__":
    main()
