#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate-store-assets.py
Generate VS Code Marketplace store assets for Lilac Dream Theme:
  - store-assets/icon.png                128x128 transparent icon (lilac gradient + moon)
  - store-assets/screenshots/zh/*.png    Chinese store screenshots (single-language)
  - store-assets/screenshots/en/*.png    English store screenshots (single-language)
  - store-assets/promo/440x280.png       bilingual small promo (zh + en in one image)
  - store-assets/promo/1400x560.png      bilingual large promo (zh + en in one image)

Palette:
  BG      #F1F1F6
  SIDEBAR #F8F8FC
  ACCENT  #BE9FE1
  HOVER   #C9B6E4
  SELECT  #E1CCEC
  TEXT    #2E2A36
  SUB     #9B8CA7
  KEYWORD #A67DD8
  STRING  #8A6BBE

Usage: python scripts/generate-store-assets.py
Deps:  pip install pillow
"""

import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "store-assets")
SCREEN_ZH = os.path.join(ASSETS, "screenshots", "zh")
SCREEN_EN = os.path.join(ASSETS, "screenshots", "en")
PROMO = os.path.join(ASSETS, "promo")
ICON = os.path.join(ASSETS, "icon.png")

for d in (SCREEN_ZH, SCREEN_EN, PROMO):
    os.makedirs(d, exist_ok=True)

# ---- palette ----
BG = (0xF1, 0xF1, 0xF6)
SIDEBAR = (0xF8, 0xF8, 0xFC)
ACCENT = (0xBE, 0x9F, 0xE1)
HOVER = (0xC9, 0xB6, 0xE4)
SELECT = (0xE1, 0xCC, 0xEC)
TEXT = (0x2E, 0x2A, 0x36)
SUB = (0x9B, 0x8C, 0xA7)
KEYWORD = (0xA6, 0x7D, 0xD8)
STRING = (0x8A, 0x6B, 0xBE)
WHITE = (0xFF, 0xFF, 0xFF)
CARD = (0xFF, 0xFF, 0xFF)

# ---- mockup code samples (lang-aware) ----
CODE_SAMPLES = {
    "zh": [
        ("keyword", "function"), ("text", " 问候"), ("punct", "() {"),
        ("", ""),
        ("keyword", "  const"), ("text", " 名字"), ("punct", " = "), ("string", '"紫色梦境"'),
        ("keyword", "  return"), ("text", " 名字"), ("punct", " + "), ("string", '"，你好"'),
        ("}", ""),
        ("", ""),
        ("comment", "// 这是一段淡紫柔和的主题示例"),
        ("keyword", "const"), ("text", " 色板"), ("punct", " = ["),
        ("string", '"#BE9FE1"'), ("punct", ", "), ("string", '"#F1F1F6"'),
        ("punct", "]"),
    ],
    "en": [
        ("keyword", "function"), ("text", " greet"), ("punct", "() {"),
        ("", ""),
        ("keyword", "  const"), ("text", " name"), ("punct", " = "), ("string", '"Lilac Dream"'),
        ("keyword", "  return"), ("text", " name"), ("punct", " + "), ("string", '" says hi"'),
        ("}", ""),
        ("", ""),
        ("comment", "// A soft lilac pastel theme sample"),
        ("keyword", "const"), ("text", " palette"), ("punct", " = ["),
        ("string", '"#BE9FE1"'), ("punct", ", "), ("string", '"#F1F1F6"'),
        ("punct", "]"),
    ],
}

SCREEN_TITLES = {
    "zh": "紫色梦境 主题预览",
    "en": "Lilac Dream Theme Preview",
}
SCREEN_SUB = {
    "zh": "柔和淡紫 · 浅色护眼 · 全界面配色",
    "en": "Soft lilac · Light & easy on eyes · Full UI theming",
}


def load_font(size, bold=False):
    candidates = [
        ("C:/Windows/Fonts/msyh.ttc", 0),          # Microsoft YaHei (zh)
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


def draw_text_center(draw, box, text, font, fill):
    l, t, r, b = box
    w = draw.textlength(text, font=font)
    x = l + (r - l - w) / 2
    # vertical center
    ascent, descent = font.getmetrics()
    h = ascent + descent
    y = t + (b - t - h) / 2
    draw.text((x, y), text, font=font, fill=fill)


def make_screenshot(lang, width=1280, height=800):
    img = Image.new("RGB", (width, height), BG)
    d = ImageDraw.Draw(img)

    # side bar (left)
    sb_w = int(width * 0.20)
    d.rectangle([0, 0, sb_w, height], fill=SIDEBAR)
    d.line([(sb_w, 0), (sb_w, height)], fill=SELECT, width=2)

    # activity bar (far left thin)
    ab_w = 48
    d.rectangle([0, 0, ab_w, height], fill=WHITE)
    # active border on activity bar
    d.rectangle([0, 120, ab_w, 168], fill=ACCENT)

    # side bar header
    d.text((ab_w + 14, 18), SCREEN_TITLES[lang], font=load_font(20, True), fill=TEXT)
    d.line([(ab_w, 52), (sb_w, 52)], fill=SELECT, width=1)

    # file tree rows
    fy = 70
    files = ["package.json", "themes/", "README.md", "scripts/"] if lang == "en" \
        else ["package.json", "themes/", "README.md", "scripts/"]
    for f in files:
        d.text((ab_w + 16, fy), f, font=load_font(15), fill=SUB if f.endswith("/") else TEXT)
        fy += 30

    # editor area
    ex0 = sb_w + 10
    ey0 = 70
    # tab bar
    tab_w = 180
    d.rectangle([ex0, 56, ex0 + tab_w, 90], fill=BG)
    d.rectangle([ex0, 87, ex0 + tab_w, 90], fill=ACCENT)
    d.text((ex0 + 14, 64), "main.js" if lang == "en" else "main.js", font=load_font(14), fill=TEXT)

    # code area card
    code_x = ex0 + 14
    code_y = ey0 + 40
    line_h = 30
    for scope, txt in CODE_SAMPLES[lang]:
        if scope == "" and txt == "":
            code_y += line_h
            continue
        color = {
            "keyword": KEYWORD, "string": STRING, "comment": SUB,
            "text": TEXT, "punct": SUB,
        }.get(scope, TEXT)
        font = load_font(16, bold=(scope == "keyword"))
        d.text((code_x, code_y), txt, font=font, fill=color)
        code_y += line_h

    # status bar
    d.rectangle([0, height - 28, width, height], fill=ACCENT)
    d.text((14, height - 22), "Lilac Dream" if lang == "en" else "Lilac Dream",
           font=load_font(14), fill=WHITE)
    st = "行 1, 列 1  UTF-8  JavaScript" if lang == "zh" else "Ln 1, Col 1  UTF-8  JavaScript"
    d.text((width - 260, height - 22), st, font=load_font(13), fill=WHITE)

    # bottom banner with title + subtitle
    banner_h = 120
    by = height - 28 - banner_h
    d.rectangle([0, by, width, height - 28], fill=WHITE)
    d.rectangle([0, by, width, by + 6], fill=ACCENT)
    draw_text_center(d, (0, by + 20, width, by + 64), SCREEN_TITLES[lang],
                     load_font(34, True), TEXT)
    draw_text_center(d, (0, by + 72, width, by + 104), SCREEN_SUB[lang],
                     load_font(18), SUB)

    out = os.path.join(SCREEN_ZH if lang == "zh" else SCREEN_EN,
                       f"preview-{lang}.png")
    img.save(out)
    return out


def make_promo(w, h, zh_title, en_title, zh_sub, en_sub):
    img = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(img)

    # left lilac gradient band
    band = int(w * 0.42)
    for x in range(band):
        t = x / band
        r = int(ACCENT[0] + (HOVER[0] - ACCENT[0]) * t)
        g = int(ACCENT[1] + (HOVER[1] - ACCENT[1]) * t)
        b = int(ACCENT[2] + (HOVER[2] - ACCENT[2]) * t)
        d.line([(x, 0), (x, h)], fill=(r, g, b))

    # decorative circle (moon) on band
    cx, cy = int(band * 0.55), int(h * 0.5)
    rad = int(min(w, h) * 0.18)
    d.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=SELECT)

    # right side text block (bilingual)
    scale = w / 1400.0
    tx = band + int(40 * scale)
    title_y = int(h * 0.26)
    # title zh
    d.text((tx, title_y), zh_title, font=load_font(int(40 * scale), True), fill=TEXT)
    # title en (just below, smaller, dark accent — gap >= 8 px)
    en_title_y = title_y + int(48 * scale) + int(10 * scale)
    d.text((tx, en_title_y), en_title,
           font=load_font(int(24 * scale), True), fill=TEXT)
    # subtitle zh
    sub_y = int(h * 0.62)
    d.text((tx, sub_y), zh_sub, font=load_font(int(20 * scale)), fill=TEXT)
    # subtitle en (gap >= 8 px)
    en_sub_y = sub_y + int(28 * scale) + int(10 * scale)
    d.text((tx, en_sub_y), en_sub,
           font=load_font(int(16 * scale)), fill=SUB)

    # CTA button (bilingual, separated by middle dot)
    btn_w = int(200 * scale)
    btn_h = int(48 * scale)
    btn_x = tx
    btn_y = int(h * 0.80)
    d.rounded_rectangle([btn_x, btn_y, btn_x + btn_w, btn_y + btn_h],
                        radius=int(10 * scale), fill=ACCENT)
    cta_zh, cta_en = "立即体验", "Try It Now"
    cta = f"{cta_zh} · {cta_en}"
    fnt = load_font(int(18 * scale), True)
    # vertical center inside button
    ascent, descent = fnt.getmetrics()
    th = ascent + descent
    tw = d.textlength(cta, font=fnt)
    d.text((btn_x + (btn_w - tw) / 2, btn_y + (btn_h - th) / 2),
           cta, font=fnt, fill=WHITE)

    return img


def make_icon():
    size = 128
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # rounded square lilac bg
    d.rounded_rectangle([4, 4, size - 4, size - 4], radius=28, fill=ACCENT)
    # moon (crescent-ish circle) using SELECT
    d.ellipse([34, 30, 86, 82], fill=SELECT)
    # small dot accent
    d.ellipse([54, 50, 66, 62], fill=HOVER)
    img.save(ICON)
    return ICON


def main():
    # screenshots (single language each)
    zh = make_screenshot("zh")
    en = make_screenshot("en")
    print("screenshot zh:", zh)
    print("screenshot en:", en)

    # promo bilingual
    p_small = make_promo(440, 280, "紫色梦境主题", "Lilac Dream Theme",
                          "柔和淡紫 · 浅色护眼", "Soft lilac light theme")
    p_small.save(os.path.join(PROMO, "440x280.png"))
    p_big = make_promo(1400, 560, "紫色梦境主题", "Lilac Dream Theme",
                        "柔和淡紫 · 浅色护眼 · 完整界面配色",
                        "Soft lilac · light & eye-friendly · full UI")
    p_big.save(os.path.join(PROMO, "1400x560.png"))
    print("promo 440x280 + 1400x560 saved")

    # icon
    ic = make_icon()
    print("icon:", ic)


if __name__ == "__main__":
    main()
