#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate-store-assets.py
Generate VS Code Marketplace store screenshots for Lilac Dream Theme (5-variant family).

Output:
  - store-assets/screenshots/zh/preview-1.png   Chinese screenshot
  - store-assets/screenshots/en/preview-1.png   English screenshot

Each screenshot shows:
  - Top banner with title + subtitle (lang-aware)
  - 5 theme swatches (Dawn/Dream/Bloom/Dusk/Night) as mini editor mockups
  - A main editor mockup (lang-aware code) using the base Lilac Dream palette

No promo images (VS Code themes do not need them).

Usage: python scripts/generate-store-assets.py
Deps:  pip install pillow
"""

import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "store-assets")
SCREEN_ZH = os.path.join(ASSETS, "screenshots", "zh")
SCREEN_EN = os.path.join(ASSETS, "screenshots", "en")

for d in (SCREEN_ZH, SCREEN_EN):
    os.makedirs(d, exist_ok=True)

# ---- 5 theme palettes (HEX tuples) ----
# order: Dawn, Dream, Bloom, Dusk, Night
PALETTES = {
    "Dawn":   {"bg": (0xF7, 0xF6, 0xFA), "sb": (0xFA, 0xF9, 0xFD), "accent": (0xBE, 0x9F, 0xE1),
               "text": (0x33, 0x2F, 0x3C), "sub": (0xA6, 0x99, 0xB2), "kw": (0xB3, 0x8F, 0xD9),
               "str": (0x97, 0x7A, 0xC9), "status": (0xBE, 0x9F, 0xE1)},
    "Dream":  {"bg": (0xF3, 0xF1, 0xF8), "sb": (0xF4, 0xF1, 0xF9), "accent": (0xBE, 0x9F, 0xE1),
               "text": (0x2E, 0x2A, 0x36), "sub": (0x9B, 0x8C, 0xA7), "kw": (0xA6, 0x7D, 0xD8),
               "str": (0x8A, 0x6B, 0xBE), "status": (0xBE, 0x9F, 0xE1)},
    "Bloom":  {"bg": (0xEF, 0xEC, 0xF6), "sb": (0xEC, 0xE7, 0xF4), "accent": (0xA6, 0x7D, 0xD8),
               "text": (0x2A, 0x26, 0x33), "sub": (0x8F, 0x7E, 0xA0), "kw": (0x8E, 0x5F, 0xC8),
               "str": (0x78, 0x57, 0xAD), "status": (0xA6, 0x7D, 0xD8)},
    "Dusk":   {"bg": (0xE4, 0xDF, 0xEE), "sb": (0xE0, 0xD9, 0xEC), "accent": (0x7A, 0x4A, 0xB8),
               "text": (0x23, 0x1F, 0x2D), "sub": (0x7A, 0x6A, 0x8E), "kw": (0x6A, 0x3C, 0xA8),
               "str": (0x57, 0x3A, 0x8E), "status": (0x7A, 0x4A, 0xB8)},
    "Night":  {"bg": (0x1B, 0x16, 0x2A), "sb": (0x21, 0x1B, 0x33), "accent": (0xB3, 0x8F, 0xE6),
               "text": (0xE6, 0xDF, 0xF2), "sub": (0x9B, 0x8C, 0xB2), "kw": (0xC4, 0x9B, 0xEE),
               "str": (0xA6, 0x7F, 0xD8), "status": (0x8E, 0x5F, 0xC8)},
}
ORDER = ["Dawn", "Dream", "Bloom", "Dusk", "Night"]
LABELS = {
    "zh": {"Dawn": "晨薰", "Dream": "梦薰", "Bloom": "盛薰", "Dusk": "暮薰", "Night": "夜薰",
           "title": "Lilac Dream 紫调主题家族", "sub": "五款淡紫变体 · 从最浅到深色 · 护眼柔和",
           "desc": "一套紫调主题，五档明度任你选"},
    "en": {"Dawn": "Dawn", "Dream": "Dream", "Bloom": "Bloom", "Dusk": "Dusk", "Night": "Night",
           "title": "Lilac Dream Theme Family", "sub": "Five lilac variants · lightest to dark · soft & calm",
           "desc": "One lilac palette, five brightness levels"},
}

CODE_LINES = {
    "zh": [
        "function 问候() {",
        "",
        "  const 名字 = \"紫色梦境\"",
        "  return 名字 + \"，你好\"",
        "}",
        "",
        "// 淡紫柔和主题示例",
        "const 色板 = [",
        "  \"#BE9FE1\",",
        "  \"#F1F1F6\"",
        "]",
    ],
    "en": [
        "function greet() {",
        "",
        "  const name = \"Lilac Dream\"",
        "  return name + \" says hi\"",
        "}",
        "",
        "// A soft lilac pastel theme sample",
        "const palette = [",
        "  \"#BE9FE1\",",
        "  \"#F1F1F6\"",
        "]",
    ],
}


def load_font(size, bold=False):
    candidates = [
        ("C:/Windows/Fonts/msyh.ttc", 0),
        ("C:/Windows/Fonts/seguiemj.ttf", 0),
        ("C:/Windows/Fonts/arial.ttf", 0),
    ]
    for path, idx in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


def wrap_text(draw, text, font, max_w):
    """break text into lines that fit max_w (for ascii). Chinese handled per-char."""
    lines = []
    cur = ""
    for ch in text:
        test = cur + ch
        if draw.textlength(test, font=font) > max_w and cur:
            lines.append(cur)
            cur = ch
        else:
            cur = test
    if cur:
        lines.append(cur)
    return lines


def draw_mini(draw, x, y, w, h, pal, label, lang):
    """Draw a mini editor mockup for one theme swatch."""
    # window bg
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=pal["bg"])
    # title bar
    draw.rectangle([x, y, x + w, y + int(h * 0.18)], fill=pal["sb"])
    draw.ellipse([x + 12, y + int(h * 0.06), x + 22, y + int(h * 0.16)], fill=(0xD6, 0x6F, 0x8B))
    draw.ellipse([x + 28, y + int(h * 0.06), x + 38, y + int(h * 0.16)], fill=(0xE0, 0xA4, 0x58))
    draw.ellipse([x + 44, y + int(h * 0.06), x + 54, y + int(h * 0.16)], fill=(0x7B, 0xA8, 0x8F))
    # code lines
    ly = y + int(h * 0.24)
    lh = int(h * 0.10)
    for _ in range(4):
        lw = int(w * (0.5 + 0.35 * ((ly // 7) % 3) / 3.0))
        col = pal["sub"] if (_ % 2) else pal["kw"]
        draw.rectangle([x + 14, ly + int(lh * 0.3), x + 14 + lw, ly + int(lh * 0.55)], fill=col)
        ly += lh
    # status bar
    draw.rectangle([x, y + h - int(h * 0.14), x + w, y + h], fill=pal["status"])
    # label below
    fnt = load_font(16, True)
    tw = draw.textlength(label, font=fnt)
    draw.text((x + (w - tw) / 2, y + h + 8), label, font=fnt, fill=(0x2E, 0x2A, 0x36))


def make_screenshot(lang, width=1280, height=800):
    img = Image.new("RGB", (width, height), (0xF3, 0xF1, 0xF8))
    d = ImageDraw.Draw(img)
    L = LABELS[lang]

    # top banner
    d.rectangle([0, 0, width, 96], fill=(0xED, 0xE8, 0xF4))
    d.rectangle([0, 0, width, 6], fill=(0xBE, 0x9F, 0xE1))
    d.text((40, 22), L["title"], font=load_font(34, True), fill=(0x2E, 0x2A, 0x36))
    d.text((40, 64), L["sub"], font=load_font(18), fill=(0x9B, 0x8C, 0xA7))

    # 5 mini swatches
    sw_w = 200
    gap = (width - 80 - sw_w * 5) / 4.0
    sy = 130
    sh = 150
    for i, key in enumerate(ORDER):
        sx = 40 + i * (sw_w + gap)
        label = key if lang == "en" else f"{L[key]}（{key}）"
        draw_mini(d, int(sx), sy, sw_w, sh, PALETTES[key], label, lang)

    # main editor mockup (base Lilac Dream) on the left-bottom
    ex, ey, ew, eh = 40, 360, int(width * 0.52), 420
    pal = PALETTES["Dream"]
    d.rounded_rectangle([ex, ey, ex + ew, ey + eh], radius=12, fill=pal["bg"])
    # title bar
    d.rectangle([ex, ey, ex + ew, ey + 40], fill=pal["sb"])
    d.ellipse([ex + 16, ey + 12, ex + 28, ey + 24], fill=(0xD6, 0x6F, 0x8B))
    d.ellipse([ex + 34, ey + 12, ex + 46, ey + 24], fill=(0xE0, 0xA4, 0x58))
    d.ellipse([ex + 52, ey + 12, ex + 64, ey + 24], fill=(0x7B, 0xA8, 0x8F))
    d.text((ex + 80, ey + 10), "main.js", font=load_font(15), fill=pal["text"])

    # code area (stop before status bar)
    code_x = ex + 24
    code_y = ey + 64
    lh = 24
    code_max_y = ey + eh - 46  # leave room for status bar
    def line_color(line):
        if line.startswith("//"):
            return pal["sub"]
        if any(line.lstrip().startswith(k) for k in ("function", "const", "return")):
            return pal["kw"]
        if '"' in line:
            return pal["str"]
        return pal["text"]
    for line in CODE_LINES[lang]:
        if code_y > code_max_y:
            break
        if line == "":
            code_y += lh
            continue
        font = load_font(16, bold=any(line.lstrip().startswith(k) for k in ("function", "const", "return")))
        d.text((code_x, code_y), line, font=font, fill=line_color(line))
        code_y += lh

    # status bar
    d.rounded_rectangle([ex, ey + eh - 32, ex + ew, ey + eh], radius=12, fill=pal["status"])
    d.text((ex + 16, ey + eh - 22), "Lilac Dream", font=load_font(14), fill=(0xFF, 0xFF, 0xFF))

    # right side: description card
    rx, ry, rw, rh = ex + ew + 30, 360, int(width - (ex + ew + 30) - 40), 420
    d.rounded_rectangle([rx, ry, rx + rw, ry + rh], radius=12, fill=(0xFA, 0xF9, 0xFD))
    d.rectangle([rx, ry, rx + rw, ry + 6], fill=(0xBE, 0x9F, 0xE1))
    d.text((rx + 24, ry + 30), L["desc"], font=load_font(20, True), fill=(0x2E, 0x2A, 0x36))
    # feature bullets
    feats = (["五款明度梯度", "统一淡紫骨架", "完整界面配色", "语法高亮优化", "深色夜薰可选"]
             if lang == "zh" else
             ["Five brightness levels", "Unified lilac chrome", "Full UI token coverage",
              "Tuned syntax colors", "Dark Night variant"])
    fy = ry + 80
    for f in feats:
        d.ellipse([rx + 28, fy + 6, rx + 36, fy + 14], fill=(0xBE, 0x9F, 0xE1))
        d.text((rx + 48, fy), f, font=load_font(17), fill=(0x2E, 0x2A, 0x36))
        fy += 40

    out = os.path.join(SCREEN_ZH if lang == "zh" else SCREEN_EN, "preview-1.png")
    img.save(out)
    return out


def main():
    zh = make_screenshot("zh")
    en = make_screenshot("en")
    print("screenshot zh:", zh)
    print("screenshot en:", en)


if __name__ == "__main__":
    main()
