#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate-preview-four.py
Generate a 2x2 VS Code editor mockup grid previewing four lilac-themed variants:
  (0,0) Lilac Dawn   - lightest, dawn glow, near-white + faint lilac
  (0,1) Lilac Dream  - baseline optimized, lavender skeleton
  (1,0) Lilac Bloom  - medium saturation, lilac "in bloom"
  (1,1) Lilac Dusk   - deepest light theme, dusk purple, stronger skeleton

Output: store-assets/preview-four.png  (1280 x 1000)
"""

import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "store-assets", "preview-four.png")


def load_font(size, bold=False):
    candidates = [
        ("C:/Windows/Fonts/msyh.ttc", 0),
        ("C:/Windows/Fonts/arial.ttf", 0),
    ]
    for path, idx in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


# Each palette: bg, sidebar, activitybar, tab_active, tab_inact, widget,
# titlebar, statusbar, accent, hover, select, text, sub, keyword, string
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
    "bg": (0xE9, 0xE5, 0xF1), "sidebar": (0xE5, 0xDF, 0xEF),
    "activitybar": (0xD8, 0xCD, 0xE8), "tab_active": (0xE9, 0xE5, 0xF1),
    "tab_inact": (0xD2, 0xC6, 0xE2), "widget": (0xF4, 0xF0, 0xFB),
    "titlebar": (0xE5, 0xDF, 0xEF), "statusbar": (0x8E, 0x5F, 0xC8),
    "accent": (0x8E, 0x5F, 0xC8), "hover": (0xA6, 0x7D, 0xD8),
    "select": (0xC4, 0xA9, 0xE2), "text": (0x26, 0x22, 0x30),
    "sub": (0x84, 0x72, 0x96), "keyword": (0x7A, 0x4A, 0xB8),
    "string": (0x68, 0x47, 0x9B),
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


def draw_editor(img, pal, x0, y0, w, h, label):
    d = ImageDraw.Draw(img)
    # activity bar (thin)
    ab_w = 42
    ax = x0
    d.rectangle([ax, y0, ax + ab_w, y0 + h], fill=pal["activitybar"])
    d.rectangle([ax, y0 + 120, ax + ab_w, y0 + 162], fill=pal["accent"])

    # side bar
    sb_w = int(w * 0.20)
    sbx = ax + ab_w
    d.rectangle([sbx, y0, sbx + sb_w, y0 + h], fill=pal["sidebar"])

    # side bar header + tree
    d.text((sbx + 12, y0 + 14), "资源管理器", font=load_font(15, True), fill=pal["text"])
    d.line([(sbx, y0 + 40), (sbx + sb_w, y0 + 40)], fill=pal["select"], width=1)
    fy = y0 + 56
    for f in ["package.json", "themes/", "README.md", "scripts/"]:
        col = pal["sub"] if f.endswith("/") else pal["text"]
        d.text((sbx + 14, fy), f, font=load_font(12), fill=col)
        fy += 24

    # editor column
    ex0 = sbx + sb_w + 6
    ex1 = x0 + w - 6

    # title bar
    d.rectangle([ex0, y0, ex1, y0 + 32], fill=pal["titlebar"])
    d.text((ex0 + 10, y0 + 10), "Lilac Dream", font=load_font(11), fill=pal["sub"])

    # tab bar
    tab_x = ex0
    tab_y = y0 + 32
    tab_w = 130
    tab_h = 30
    d.rectangle([tab_x, tab_y, tab_x + tab_w, tab_y + tab_h], fill=pal["tab_active"])
    d.rectangle([tab_x, tab_y + tab_h - 3, tab_x + tab_w, tab_y + tab_h], fill=pal["accent"])
    d.text((tab_x + 10, tab_y + 8), "main.js", font=load_font(11), fill=pal["text"])

    # editor background
    edy0 = tab_y + tab_h
    d.rectangle([ex0, edy0, ex1, y0 + h - 22], fill=pal["bg"])

    # code lines
    cx = ex0 + 16
    cy = edy0 + 18
    line_h = 22
    for scope, txt in CODE:
        if scope == "" and txt == "":
            cy += line_h * 0.6
            continue
        color = {
            "keyword": pal["keyword"], "string": pal["string"],
            "comment": pal["sub"], "text": pal["text"], "punct": pal["sub"],
        }.get(scope, pal["text"])
        fnt = load_font(13, bold=(scope == "keyword"))
        d.text((cx, cy), txt, font=fnt, fill=color)
        cy += line_h

    # suggest widget
    sw_w = 190
    sw_h = 78
    sw_x = ex0 + 34
    sw_y = edy0 + 130
    d.rectangle([sw_x, sw_y, sw_x + sw_w, sw_y + sw_h], fill=pal["widget"],
                outline=pal["select"], width=1)
    d.text((sw_x + 10, sw_y + 6), "theme.list", font=load_font(12, True), fill=pal["text"])
    d.rectangle([sw_x, sw_y + 26, sw_x + sw_w, sw_y + 27], fill=pal["select"], width=1)
    d.text((sw_x + 10, sw_y + 34), "theme.load()", font=load_font(12), fill=pal["text"])
    d.text((sw_x + 10, sw_y + 54), "theme.apply", font=load_font(12), fill=pal["text"])

    # status bar
    d.rectangle([x0, y0 + h - 22, x0 + w, y0 + h], fill=pal["statusbar"])
    d.text((x0 + 10, y0 + h - 17), "Lilac", font=load_font(11), fill=(255, 255, 255))
    d.text((x0 + w - 108, y0 + h - 17), "Ln 1  Col 1  JS",
           font=load_font(10), fill=(255, 255, 255))

    # vertical divider between sidebar and editor (drawn last, on top)
    d.line([(sbx + sb_w, y0), (sbx + sb_w, y0 + h - 22)], fill=pal["select"], width=2)

    # label badge (drawn last, on top of everything)
    d.rounded_rectangle([x0 + 8, y0 + 8, x0 + 8 + 130, y0 + 8 + 26], radius=7,
                        fill=pal["accent"])
    d.text((x0 + 18, y0 + 14), label, font=load_font(13, True), fill=(255, 255, 255))


def main():
    W, H = 1280, 1000
    img = Image.new("RGB", (W, H), (0xE6, 0xE2, 0xEF))
    d = ImageDraw.Draw(img)

    gap_x, gap_y = 24, 24
    pad = 24
    col_w = (W - pad * 2 - gap_x) // 2
    row_h = (H - pad * 2 - gap_y) // 2

    cells = [
        (DAWN,  pad,            pad,            "Lilac Dawn · 晨薰"),
        (DREAM, pad + col_w + gap_x, pad,      "Lilac Dream · 梦薰"),
        (BLOOM, pad,            pad + row_h + gap_y, "Lilac Bloom · 盛薰"),
        (DUSK,  pad + col_w + gap_x, pad + row_h + gap_y, "Lilac Dusk · 暮薰"),
    ]
    for pal, x0, y0, label in cells:
        draw_editor(img, pal, x0, y0, col_w, row_h, label)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT)
    print("saved:", OUT)


if __name__ == "__main__":
    main()
