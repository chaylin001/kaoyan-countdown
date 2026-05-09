from PIL import Image, ImageDraw
import os

SIZES = {
    "icon-192.png": 192,
    "icon-512.png": 512,
    "apple-touch-icon.png": 180,
}

INK = (26, 23, 20)
VERMILLION = (181, 52, 58)
PAPER = (250, 246, 240)
GOLD = (196, 164, 90)

def draw_icon(size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    r = size * 0.2  # corner radius approx

    # Rounded rect background (ink)
    draw.rounded_rectangle(
        [(0, 0), (size - 1, size - 1)],
        radius=int(r),
        fill=INK,
    )

    # Outer vermillion ring
    margin = size * 0.16
    ring_outer = size - margin * 2
    ring_thick = size * 0.06
    draw.arc(
        [margin, margin, margin + ring_outer, margin + ring_outer],
        start=0, end=360,
        fill=VERMILLION,
        width=int(ring_thick),
    )

    # Progress arc (about 60% filled, representing the study journey)
    progress = 215  # degrees
    draw.arc(
        [margin, margin, margin + ring_outer, margin + ring_outer],
        start=90, end=90 + progress,
        fill=GOLD,
        width=int(ring_thick),
    )

    # Center number: days remaining style
    cx, cy = size / 2, size / 2
    # Draw a simplified "天" concept: a small square grid
    cell = size * 0.10
    gap = size * 0.03

    # Simple abstract countdown blocks
    for col in range(3):
        x = cx - (1.5 * cell + gap) + col * (cell + gap)
        for row in range(2):
            y = cy - (cell + gap / 2) + row * (cell + gap)
            alpha = 255 if (col + row) < 4 else 80
            color = (*PAPER, alpha)
            draw.rounded_rectangle(
                [x, y, x + cell, y + cell],
                radius=int(cell * 0.3),
                fill=color,
            )

    return img

os.chdir(os.path.dirname(os.path.abspath(__file__)))
for filename, size in SIZES.items():
    img = draw_icon(size)
    img.save(filename)
    print(f"Saved {filename} ({size}x{size})")

print("Done.")
