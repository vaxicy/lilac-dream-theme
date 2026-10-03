#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate-variant-previews.py
Generate one high-fidelity VS Code window mockup per theme variant, used as
"real preview" screenshots in README.

The script reads the 5 theme JSON files directly (single source of truth),
so every mockup reflects the actual editor / sidebar / tab / status bar /
token colors of the variant.

Output:
  store-assets/screenshots/variants/preview-dawn.png
  store-assets/screenshots/variants/preview-dream.png
  store-assets/screenshots/variants/preview-bloom.png
  store-assets/screenshots/variants/preview-dusk.png
  store-assets/screenshots/variants/preview-night.png

Usage: python scripts/generate-variant-previews.py
Deps:  pip install pillow
"""

import os
import json
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "store-assets", "screenshots", "variants")
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 1200, 750
RADIUS = 12

VARIANTS = [
    ("lilac-dawn-color-theme.json", "Lilac Dawn", "晨薰", "dawn"),
    ("lilac-dream-color-theme.json", "Lilac Dream", "梦薰", "dream"),
    ("lilac-bloom-color-theme.json", "Lilac Bloom", "盛薰", "bloom"),
    ("lilac-dusk-color-theme.json", "Lilac Dusk", "暮薰", "dusk"),
    ("lilac-night-color-theme.json", "Lilac Night", "夜薰", "night"),
]

# ---------------------------------------------------------------- fonts
_font_cache = {}


def load_font(size, bold=False, mono=False):
    key = (size, bold, mono)
    if key in _font_cache:
        return _font_cache[key]
    if mono:
        candidates = [
            "C:/Windows/Fonts/consolab.ttf" if bold else "C:/Windows/Fonts/consola.ttf",
            "C:/Windows/Fonts/cour.ttf",
        ]
    else:
        candidates = [
            "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        ]
    font = None
    for path in candidates:
        if os.path.exists(path):
            try:
                font = ImageFont.truetype(path, size)
                break
            except Exception:
                pass
    if font is None:
        font = ImageFont.load_default()
    _font_cache[key] = font
    return font


# ---------------------------------------------------------------- colors
def parse_color(value, fallback=(0x2E, 0x2A, 0x36)):
    v = (value or "").strip()
    if v.startswith("#") and len(v) in (7, 9):
        try:
            r = int(v[1:3], 16)
            g = int(v[3:5], 16)
            b = int(v[5:7], 16)
            a = int(v[7:9], 16) if len(v) == 9 else 255
            return (r, g, b, a)
        except ValueError:
            pass
    return (fallback[0], fallback[1], fallback[2], 255)


def blend(fg, bg, t=None):
    r, g, b, a = fg
    if t is None:
        t = a / 255.0
    return (
        round(r * t + bg[0] * (1 - t)),
        round(g * t + bg[1] * (1 - t)),
        round(b * t + bg[2] * (1 - t)),
    )


def luminance(c):
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


# ---------------------------------------------------------------- theme
class Theme:
    def __init__(self, path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.colors = data.get("colors", {})
        self.tokens = {}
        for entry in data.get("tokenColors", []):
            scope = entry.get("scope")
            fg = (entry.get("settings") or {}).get("foreground")
            if not fg:
                continue
            scopes = [scope] if isinstance(scope, str) else scope
            for s in scopes:
                self.tokens.setdefault(s, parse_color(fg))

    def raw(self, key, fallback="#2E2A36"):
        return parse_color(self.colors.get(key, fallback))

    def rgb(self, key, fallback="#2E2A36"):
        return self.raw(key, fallback)[:3]

    def over(self, key, base, fallback="#00000000"):
        """color blended over base (for alpha colors)."""
        return blend(self.raw(key, fallback), base)

    def token(self, scope, fallback="#2E2A36"):
        c = self.tokens.get(scope)
        if c:
            return c[:3]
        return parse_color(fallback)[:3]


# ---------------------------------------------------------------- code sample
KW, FN, STR, VAR, COM, P, PROP, TXT = "kw", "fn", "str", "var", "comment", "punct", "prop", "text"

CODE = [
    [("import", KW), (" { ", P), ("createTheme", FN), (" } ", P), ("from", KW), (" ", TXT), ('"./theme"', STR)],
    [],
    [("// Lilac Dream - a soft lilac pastel theme", COM)],
    [("const", KW), (" ", TXT), ("palette", VAR), (" = {", P)],
    [("  accent", PROP), (": ", P), ('"#BE9FE1"', STR), (",", P)],
    [("  surface", PROP), (": ", P), ('"#F1F1F6"', STR), (",", P)],
    [("  text", PROP), (": ", P), ('"#2E2A36"', STR), (",", P)],
    [("}", P)],
    [],
    [("function", KW), (" ", TXT), ("greet", FN), ("(name) {", P)],
    [("  const", KW), (" ", TXT), ("message", VAR), (" = ", P), ("`Hello, ${name}!`", STR)],
    [("  return", KW), (" ", TXT), ("message", VAR)],
    [("}", P)],
    [],
    [("const", KW), (" ", TXT), ("variants", VAR), (" = [", P), ('"Dawn", "Dream", "Bloom",', STR), (" ", P), ('"Dusk", "Night"', STR), ("]", P)],
    [],
    [("export", KW), (" ", TXT), ("default", KW), (" ", TXT), ("createTheme", FN), ("({", P)],
    [("  palette,", PROP)],
    [("  variants,", PROP)],
    [("  greet,", PROP)],
    [("})", P)],
]
ACTIVE_LINE = 10  # 0-based index -> "const message" line

# ---------------------------------------------------------------- layout
TITLE_H = 36
AB_W = 48
SB_W = 224
TAB_H = 34
CRUMB_H = 22
STATUS_H = 34
MM_W = 62  # minimap width
GUTTER_X = 326  # right edge of line numbers
CODE_X = 344
LH = 26
CODE_TOP = 104


def draw_window(theme, name_en, name_zh):
    img = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    d = ImageDraw.Draw(img)

    eb = theme.rgb("editor.background", "#F3F1F8")
    text = theme.rgb("editor.foreground", "#2E2A36")
    sub = theme.token("comment", "#9B8CA7")

    tk = {
        "kw": theme.token("keyword", "#A67DD8"),
        "fn": theme.token("entity.name.function", "#7A6FA3"),
        "str": theme.token("string", "#8A6BBE"),
        "num": theme.token("constant.numeric", "#C9B6E4"),
        "var": theme.token("variable", "#2E2A36"),
    }

    # ============ title bar ============
    tb = theme.rgb("titleBar.activeBackground", "#F4F1F9")
    tbfg = theme.rgb("titleBar.activeForeground", "#2E2A36")
    d.rectangle([0, 0, W, TITLE_H], fill=tb)
    for i, col in enumerate([(0xE0, 0x88, 0x92), (0xE0, 0xA4, 0x58), (0x7B, 0xA8, 0x8F)]):
        cx = 22 + i * 22
        d.ellipse([cx - 6, TITLE_H // 2 - 6, cx + 6, TITLE_H // 2 + 6], fill=col)
    title = "lilac-dream-theme  —  Visual Studio Code"
    tf = load_font(12)
    d.text(((W - d.textlength(title, font=tf)) / 2, 11), title, font=tf,
           fill=blend((*tbfg, 255), tb, 0.85))

    # variant badge (top-right)
    accent = theme.rgb("focusBorder", "#BE9FE1")
    badge_txt = f"{name_en} · {name_zh}"
    bf = load_font(12, bold=True)
    bw = int(d.textlength(badge_txt, font=bf)) + 26
    d.rounded_rectangle([W - bw - 14, 8, W - 14, 30], radius=11, fill=accent)
    d.text((W - bw - 14 + 13, 12), badge_txt, font=bf, fill=(255, 255, 255))

    # ============ activity bar ============
    ab = theme.rgb("activityBar.background", "#EDE8F4")
    abfg = theme.rgb("activityBar.foreground", "#2E2A36")
    abdim = theme.rgb("activityBar.inactiveForeground", "#9B8CA7")
    d.rectangle([0, TITLE_H, AB_W, H - STATUS_H], fill=ab)
    # active item border
    d.rectangle([0, TITLE_H, 2, TITLE_H + 220], fill=accent)

    def draw_icon(idx, active):
        col = abfg if active else abdim
        cy = TITLE_H + 40 + idx * 56
        cx = AB_W // 2
        if idx == 0:  # explorer (two files)
            d.rectangle([cx - 10, cy - 9, cx + 3, cy + 3], fill=None, outline=col, width=2)
            d.rectangle([cx - 3, cy - 3, cx + 10, cy + 9], fill=ab, outline=col, width=2)
        elif idx == 1:  # search
            d.ellipse([cx - 9, cy - 9, cx + 5, cy + 5], outline=col, width=2)
            d.line([cx + 3, cy + 3, cx + 10, cy + 10], fill=col, width=2)
        elif idx == 2:  # source control
            d.ellipse([cx - 3, cy - 11, cx + 3, cy - 5], fill=col)
            d.ellipse([cx - 3, cy + 5, cx + 3, cy + 11], fill=col)
            d.line([cx, cy - 4, cx, cy + 5], fill=col, width=2)
            d.line([cx, cy - 8, cx + 8, cy - 8], fill=col, width=2)
            d.line([cx + 8, cy - 8, cx + 8, cy + 2], fill=col, width=2)
            d.ellipse([cx + 5, cy + 2, cx + 11, cy + 8], fill=col)
        elif idx == 3:  # run / debug
            d.polygon([(cx - 7, cy - 9), (cx + 9, cy), (cx - 7, cy + 9)], outline=col, fill=None, width=2)
        else:  # extensions
            s = 6
            for dx, dy in [(-8, -8), (2, -8), (-8, 2), (2, 2)]:
                d.rectangle([cx + dx, cy + dy, cx + dx + s, cy + dy + s], fill=col)

    for i in range(5):
        draw_icon(i, i == 0)
    # settings gear at bottom
    cy = H - STATUS_H - 30
    d.ellipse([AB_W // 2 - 7, cy - 7, AB_W // 2 + 7, cy + 7], outline=abdim, width=2)
    d.ellipse([AB_W // 2 - 2, cy - 2, AB_W // 2 + 2, cy + 2], fill=abdim)

    # ============ sidebar ============
    sb = theme.rgb("sideBar.background", "#F4F1F9")
    sbfg = theme.rgb("sideBar.foreground", "#2E2A36")
    sbtitle = theme.rgb("sideBarTitle.foreground", "#9B8CA7")
    d.rectangle([AB_W, TITLE_H, AB_W + SB_W, H - STATUS_H], fill=sb)
    sf = load_font(11, bold=True)
    d.text((AB_W + 12, TITLE_H + 12), "EXPLORER", font=sf, fill=sbtitle)

    # project row
    d.polygon([(AB_W + 14, TITLE_H + 38), (AB_W + 22, TITLE_H + 38), (AB_W + 18, TITLE_H + 44)],
              fill=sbfg)
    d.text((AB_W + 28, TITLE_H + 34), "LILAC-DREAM-THEME", font=sf, fill=sbfg)

    tree = [
        (0, "themes", "folder_open", None),
        (1, "lilac-dawn.json", "file", None),
        (1, "lilac-dream.json", "file", "selected"),
        (1, "lilac-night.json", "file", None),
        (0, "package.json", "file", None),
        (0, "README.md", "file", None),
        (0, "scripts", "folder", None),
        (0, "LICENSE.md", "file", None),
    ]
    row_y = TITLE_H + 62
    row_h = 26
    row_font = load_font(13)
    sel_bg = theme.over("list.activeSelectionBackground", sb, "#E1CCEC80")
    sel_fg = theme.rgb("list.activeSelectionForeground", "#2E2A36")

    for indent, label, kind, state in tree:
        y = row_y
        x = AB_W + 14 + indent * 16
        if state == "selected":
            d.rectangle([AB_W + 1, y - 4, AB_W + SB_W, y - 4 + row_h], fill=sel_bg)
        fg = sel_fg if state == "selected" else sbfg
        if kind in ("folder", "folder_open"):
            # chevron
            if kind == "folder_open":
                d.polygon([(x, y + 3), (x + 8, y + 3), (x + 4, y + 9)], fill=sub)
            else:
                d.polygon([(x + 1, y + 1), (x + 9, y + 5), (x + 1, y + 10)], fill=sub)
            # folder glyph
            d.rounded_rectangle([x + 14, y, x + 30, y + 12], radius=2,
                                fill=blend((*accent, 255), sb, 0.55))
        else:
            d.rectangle([x + 14, y, x + 24, y + 12], outline=blend((*sub, 255), sb, 0.9), width=1)
        d.text((x + 36, y - 2), label, font=row_font, fill=fg)
        row_y += row_h

    # sidebar border
    d.rectangle([AB_W + SB_W, TITLE_H, AB_W + SB_W + 1, H - STATUS_H],
                fill=theme.rgb("editorGroup.border", "#E1CCEC"))

    # ============ tabs ============
    ex0 = AB_W + SB_W + 1
    tabs_bg = theme.rgb("editorGroupHeader.tabsBackground", "#EDE8F4")
    d.rectangle([ex0, TITLE_H, W, TITLE_H + TAB_H], fill=tabs_bg)
    # active tab
    ta_bg = theme.rgb("tab.activeBackground", eb)
    ta_fg = theme.rgb("tab.activeForeground", text)
    tab_border = theme.raw("tab.activeBorderTop", "")
    if tab_border[3] == 255 and "tab.activeBorderTop" not in theme.colors:
        tab_border = theme.raw("tab.activeBorder", "#BE9FE1")
    d.rectangle([ex0, TITLE_H, ex0 + 168, TITLE_H + TAB_H], fill=ta_bg)
    d.rectangle([ex0, TITLE_H, ex0 + 168, TITLE_H + 2], fill=tab_border[:3])
    twf = load_font(12)
    d.text((ex0 + 16, TITLE_H + 10), "main.js", font=twf, fill=ta_fg)
    d.text((ex0 + 148, TITLE_H + 9), "×", font=load_font(13), fill=sub)
    # inactive tab
    ti_bg = theme.rgb("tab.inactiveBackground", "#E8E2F0")
    ti_fg = theme.rgb("tab.inactiveForeground", "#9B8CA7")
    d.rectangle([ex0 + 168, TITLE_H, ex0 + 300, TITLE_H + TAB_H], fill=ti_bg)
    d.text((ex0 + 184, TITLE_H + 10), "theme.json", font=twf, fill=ti_fg)
    d.text((ex0 + 280, TITLE_H + 9), "×", font=load_font(13), fill=ti_fg)

    # ============ breadcrumb ============
    crumb_y = TITLE_H + TAB_H
    crumb = "src  ›  main.js  ›  greet()"
    cf = load_font(11)
    d.text((ex0 + 18, crumb_y + 4), crumb, font=cf,
           fill=blend((*sub, 255), eb, 0.85))

    # ============ editor ============
    ed_top = crumb_y + CRUMB_H
    ed_bottom = H - STATUS_H
    d.rectangle([ex0, ed_top, W, ed_bottom], fill=eb)

    # active line highlight
    hl = theme.over("editor.lineHighlightBackground", eb, "#E1CCEC40")
    hl_y = CODE_TOP + ACTIVE_LINE * LH
    d.rectangle([ex0 + 1, hl_y - 2, W - MM_W, hl_y + LH - 2], fill=hl)

    # line numbers
    ln_fg = theme.rgb("editorLineNumber.foreground", "#9B8CA7")
    ln_act = theme.rgb("editorLineNumber.activeForeground", "#A67DD8")
    num_font = load_font(13, mono=True)
    code_font = load_font(15, mono=True)
    code_bold = load_font(15, bold=True, mono=True)

    for i, parts in enumerate(CODE):
        y = CODE_TOP + i * LH
        if i == ACTIVE_LINE:
            num_col = ln_act
        else:
            num_col = ln_fg
        num = str(i + 1)
        d.text((GUTTER_X - d.textlength(num, font=num_font), y + 1), num,
               font=num_font, fill=num_col)
        x = CODE_X
        for txt_, tone in parts:
            if tone == KW:
                col = tk["kw"]
                f = code_bold
            elif tone == FN:
                col = tk["fn"]
                f = code_font
            elif tone == STR:
                col = tk["str"]
                f = code_font
            elif tone == VAR:
                col = tk["var"]
                f = code_font
            elif tone == COM:
                col = sub
                f = code_font
            elif tone == PROP:
                col = text
                f = code_font
            else:
                col = blend((*sub, 255), eb, 0.95)
                f = code_font
            d.text((x, y), txt_, font=f, fill=col)
            x += d.textlength(txt_, font=f)

    # minimap
    mm_x = W - MM_W
    for i, parts in enumerate(CODE):
        if not parts:
            continue
        y = CODE_TOP + i * LH * 0.34 - 8
        chars = sum(len(t) for t, _ in parts)
        tone = parts[0][1]
        base_col = {
            KW: tk["kw"], FN: tk["fn"], STR: tk["str"],
            VAR: tk["var"], COM: sub, PROP: text,
        }.get(tone, sub)
        col = blend((*base_col, 255), eb, 0.42)
        d.rectangle([mm_x + 8, y, mm_x + 8 + min(MM_W - 16, chars * 1.15), y + 2.4], fill=col)

    # ============ status bar ============
    st = theme.rgb("statusBar.background", "#BE9FE1")
    stfg = theme.rgb("statusBar.foreground", "#FFFFFF")
    st_y = H - STATUS_H
    d.rectangle([0, st_y, W, H], fill=st)
    stf = load_font(12)
    # branch glyph drawn manually (font-safe)
    bx, by = 22, st_y + 17
    d.ellipse([bx - 2, by - 9, bx + 2, by - 5], fill=stfg)
    d.ellipse([bx - 2, by + 5, bx + 2, by + 9], fill=stfg)
    d.line([bx, by - 5, bx, by + 6], fill=stfg, width=1)
    d.line([bx, by - 3, bx + 6, by - 7], fill=stfg, width=1)
    d.ellipse([bx + 5, by - 10, bx + 9, by - 6], fill=stfg)
    d.text((bx + 16, st_y + 9), "main", font=stf, fill=stfg)
    d.text((bx + 66, st_y + 9), name_en, font=stf, fill=stfg)
    right = "Ln 12, Col 22    Spaces: 2    UTF-8    JavaScript"
    d.text((W - 16 - d.textlength(right, font=stf), st_y + 9), right, font=stf, fill=stfg)

    # ============ rounded window mask ============
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, W - 1, H - 1], radius=RADIUS, fill=255)
    img.putalpha(mask)

    # thin window border
    d.rounded_rectangle([0, 0, W - 1, H - 1], radius=RADIUS, outline=None)

    return img


def main():
    for fname, en, zh, slug in VARIANTS:
        theme = Theme(os.path.join(ROOT, "themes", fname))
        img = draw_window(theme, en, zh)
        out = os.path.join(OUT_DIR, f"preview-{slug}.png")
        img.save(out)
        print("saved:", out)


if __name__ == "__main__":
    main()
