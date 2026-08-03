#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate-preview-compare.py
Generate a side-by-side VS Code editor mockup preview comparing:
  LEFT  = current Lilac Dream theme (too white)
  RIGHT = proposed optimization (lavender-tinted UI skeleton)
So the user can decide whether to apply the optimization.

Output: store-assets/preview-compare.png  (1260 x 820)
"""

import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "store-assets", "preview-compare.png")

# ---- fonts ----
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

# ---- two palettes ----
# (bg, sidebar, activitybar, tab_active_bg, tab_inactive_bg, widget, titlebar,
#  statusbar, accent, hover, select, text, sub, keyword, string)
CURRENT = {
    "bg":          (0xF1, 0xF1, 0xF6),
    "sidebar":     (0xF8, 0xF8, 0xFC),
    "activitybar": (0xFF, 0xFF, 0xFF),
    "tab_active":  (0xF1, 0xF1, 0xF6),
    "tab_inact":   (0xF8, 0xF8, 0xFC),
    "widget":      (0xFF, 0xFF, 0xFF),
    "titlebar":    (0xFF, 0xFF, 0xFF),
    "statusbar":   (0xBE, 0x9F, 0xE1),
    "accent":      (0xBE, 0x9F, 0xE1),
    "hover":       (0xC9, 0xB6, 0xE4),
    "select":      (0xE1, 0xCC, 0xEC),
    "text":        (0x2E, 0x2A, 0x36),
    "sub":         (0x9B, 0x8C, 0xA7),
    "keyword":     (0xA6, 0x7D, 0xD8),
    "string":      (0x8A, 0x6B, 0xBE),
}

PROPOSED = {
    "bg":          (0xF3, 0xF1, 0xF8),   # slightly lavender vs pure-ish white
    "sidebar":     (0xF4, 0xF1, 0xF9),   # lavender tint instead of near-white
    "activitybar": (0xED, 0xE8, 0xF4),   # lilac-grey skeleton
    "tab_active":  (0xF3, 0xF1, 0xF8),
    "tab_inact":   (0xE8, 0xE2, 0xF0),   # deeper lavender for inactive tabs
    "widget":      (0xFC, 0xFB, 0xFD),   # off-white with lavender hue
    "titlebar":    (0xF4, 0xF1, 0xF9),
    "statusbar":   (0xBE, 0x9F, 0xE1),
    "accent":      (0xBE, 0x9F, 0xE1),
    "hover":       (0xC9, 0xB6, 0xE4),
    "select":      (0xE1, 0xCC, 0xEC),
    "text":        (0x2E, 0x2A, 0x36),
    "sub":         (0x9B, 0x8C, 0xA7),
    "keyword":     (0xA6, 0x7D, 0xD8),
    "string":      (0x8A, 0x6B, 0xBE),
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


def draw_editor(img, pal, x0, w, label):
    d = ImageDraw.Draw(img)
    h = img.height
    y_top = 0

    # activity bar (far left, thin)
    ab_w = 46
    ax = x0
    d.rectangle([ax, y_top, ax + ab_w, h], fill=pal["activitybar"])
    # active item highlight
    d.rectangle([ax, 130, ax + ab_w, 176], fill=pal["accent"])

    # side bar
    sb_w = int(w * 0.20)
    sbx = ax + ab_w
    d.rectangle([sbx, y_top, sbx + sb_w, h], fill=pal["sidebar"])
    d.line([(sbx + sb_w, y_top), (sbx + sb_w, h)], fill=pal["select"], width=2)

    # side bar header + file tree
    d.text((sbx + 14, 18), "资源管理器", font=load_font(18, True), fill=pal["text"])
    d.line([(sbx, 50), (sbx + sb_w, 50)], fill=pal["select"], width=1)
    fy = 70
    for f in ["package.json", "themes/", "README.md", "scripts/"]:
        col = pal["sub"] if f.endswith("/") else pal["text"]
        d.text((sbx + 16, fy), f, font=load_font(14), fill=col)
        fy += 28

    # editor column
    ex0 = sbx + sb_w + 8
    ex1 = x0 + w - 8

    # title bar
    d.rectangle([ex0, y_top, ex1, 38], fill=pal["titlebar"])
    d.text((ex0 + 12, 12), "Lilac Dream", font=load_font(13), fill=pal["sub"])

    # tab bar
    tab_x = ex0
    tab_y = 38
    tab_w = 150
    tab_h = 34
    d.rectangle([tab_x, tab_y, tab_x + tab_w, tab_y + tab_h], fill=pal["tab_active"])
    d.rectangle([tab_x, tab_y + tab_h - 3, tab_x + tab_w, tab_y + tab_h], fill=pal["accent"])
    d.text((tab_x + 12, tab_y + 9), "main.js", font=load_font(13), fill=pal["text"])

    # editor background
    edy0 = tab_y + tab_h
    d.rectangle([ex0, edy0, ex1, h - 26], fill=pal["bg"])

    # code lines
    cx = ex0 + 18
    cy = edy0 + 22
    line_h = 26
    for scope, txt in CODE:
        if scope == "" and txt == "":
            cy += line_h * 0.6
            continue
        color = {
            "keyword": pal["keyword"], "string": pal["string"],
            "comment": pal["sub"], "text": pal["text"], "punct": pal["sub"],
        }.get(scope, pal["text"])
        fnt = load_font(15, bold=(scope == "keyword"))
        d.text((cx, cy), txt, font=fnt, fill=color)
        cy += line_h

    # suggest widget (mockup dropdown)
    sw_w = 220
    sw_h = 90
    sw_x = ex0 + 40
    sw_y = edy0 + 150
    d.rectangle([sw_x, sw_y, sw_x + sw_w, sw_y + sw_h], fill=pal["widget"],
                outline=pal["select"], width=1)
    d.text((sw_x + 10, sw_y + 8), "theme.list", font=load_font(13, True), fill=pal["text"])
    d.rectangle([sw_x, sw_y + 30, sw_x + sw_w, sw_y + 31], fill=pal["select"], width=1)
    d.text((sw_x + 10, sw_y + 38), "theme.load()", font=load_font(13), fill=pal["text"])
    d.text((sw_x + 10, sw_y + 60), "theme.apply", font=load_font(13), fill=pal["text"])

    # status bar
    d.rectangle([x0, h - 26, x0 + w, h], fill=pal["statusbar"])
    d.text((x0 + 12, h - 20), "Lilac Dream", font=load_font(13), fill=(255, 255, 255))
    d.text((x0 + w - 230, h - 20), "Ln 1, Col 1  UTF-8  JS",
           font=load_font(12), fill=(255, 255, 255))

    # label badge
    d.rounded_rectangle([x0 + 10, 10, x0 + 10 + 150, 10 + 30], radius=8,
                        fill=pal["accent"])
    d.text((x0 + 22, 18), label, font=load_font(15, True), fill=(255, 255, 255))


def main():
    W, H = 1260, 820
    img = Image.new("RGB", (W, H), (0xE9, 0xE6, 0xF0))
    d = ImageDraw.Draw(img)

    gap = 20
    col_w = (W - gap * 3) // 2
    draw_editor(img, CURRENT, gap, col_w, "当前：偏白")
    draw_editor(img, PROPOSED, gap * 2 + col_w, col_w, "优化：淡紫骨架")

    # center divider label
    d.text((W // 2 - 30, H - 16), "VS", font=load_font(14, True),
           fill=(0x9B, 0x8C, 0xA7))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT)
    print("saved:", OUT)


if __name__ == "__main__":
    main()
