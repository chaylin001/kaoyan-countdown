from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

W, H = 1200, 630
PAPER = (250, 246, 240)
INK = (26, 23, 20)
INK_LIGHT = (74, 69, 64)
INK_MUTED = (138, 128, 118)
VERMILLION = (181, 52, 58)
VERMILLION_GLOW = (212, 74, 80)
GOLD = (196, 164, 90)
BORDER = (224, 216, 202)

img = Image.new("RGBA", (W, H), PAPER)
draw = ImageDraw.Draw(img)

# ── Background ink-wash blobs ──
for cx, cy, rx, ry, alpha in [
    (240, 180, 480, 360, 30),
    (960, 420, 360, 480, 20),
    (600, 315, 600, 500, 12),
]:
    blob = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(blob)
    bdraw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(180, 160, 130, alpha))
    blob = blob.filter(ImageFilter.GaussianBlur(80))
    img = Image.alpha_composite(img, blob)
    draw = ImageDraw.Draw(img)

# ── Seal border corners ──
corner = 50
for x, y, dx, dy in [
    (corner, corner, 1, 1),
    (W - corner, corner, -1, 1),
    (corner, H - corner, 1, -1),
    (W - corner, H - corner, -1, -1),
]:
    draw.line([(x + dx * 60, y), (x, y), (x, y + dy * 60)], fill=VERMILLION, width=4)

# ── Border rect ──
border_margin = 40
draw.rectangle(
    [border_margin, border_margin, W - border_margin, H - border_margin],
    outline=BORDER, width=1,
)

# ── Try to load a Chinese font ──
def find_font(size):
    candidates = [
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/msyhbd.ttc",
        "C:/Windows/Fonts/simsun.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/STKAITI.TTF",
        "C:/Windows/Fonts/STSONG.TTF",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

font_title = find_font(72)
font_sub = find_font(28)
font_footer = find_font(22)
font_quote = find_font(24)

# ── Top label ──
label = "全国硕士研究生招生考试"
lw = draw.textlength(label, font=font_sub)
lx = (W - lw) / 2
draw.text((lx, 120), label, fill=INK_MUTED, font=font_sub)

# ── Title ──
title = "考 研 倒 计 时"
tw = draw.textlength(title, font=font_title)
tx = (W - tw) / 2
# Draw title with slight vermillion shadow
draw.text((tx + 3, 178), title, fill=VERMILLION_GLOW, font=font_title)
draw.text((tx, 175), title, fill=INK, font=font_title)

# ── Vermillion underline ──
draw.line([(W / 2 - 80, 270), (W / 2 + 80, 270)], fill=VERMILLION, width=3)

# ── Exam date ──
date_str = "2026 年 12 月 26 日  ·  上午 8:30"
dw = draw.textlength(date_str, font=font_sub)
dx = (W - dw) / 2
draw.ellipse([dx - 24, 308, dx - 12, 320], fill=VERMILLION)
draw.ellipse([dx + dw + 12, 308, dx + dw + 24, 320], fill=VERMILLION)
draw.text((dx, 300), date_str, fill=INK_LIGHT, font=font_sub)

# ── Decorative line ──
draw.line([(200, 380), (W - 200, 380)], fill=BORDER, width=1)

# ── Quote area ──
quote = '"星光不问赶路人，时光不负有心人。"'
qw = draw.textlength(quote, font=font_quote)
draw.text(((W - qw) / 2, 430), quote, fill=INK_MUTED, font=font_quote)

# ── Footer ──
footer = "研途漫漫 · 功不唐捐"
fw = draw.textlength(footer, font=font_footer)
draw.text(((W - fw) / 2, 520), footer, fill=INK_MUTED, font=font_footer)

# ── Bottom gold line ──
draw.line([(W / 2 - 60, 568), (W / 2 + 60, 568)], fill=GOLD, width=1)

# ── Save ──
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "og-image.png")
img = img.convert("RGB")
img.save(out, "PNG")
print(f"Saved {out} ({W}x{H})")
