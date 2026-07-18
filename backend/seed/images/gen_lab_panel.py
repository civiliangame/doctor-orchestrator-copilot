"""Render lab_panel.png — synthetic demo lab panel for Beat C.

Run:  python gen_lab_panel.py   (from this directory)
Pure Pillow; no network, no PHI — every value is invented for the demo.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "lab_panel.png"

W, H = 1400, 900
MARGIN = 60
ROW_H = 96

BG = (250, 250, 248)
INK = (28, 32, 38)
MUTED = (110, 116, 124)
LINE = (208, 210, 214)
HEADER_BG = (36, 52, 84)
HEADER_INK = (255, 255, 255)
HIGH_BG = (253, 232, 232)
HIGH_INK = (178, 32, 32)

# (test, value, reference, flag)
ROWS = [
    ("Troponin I", "0.09 ng/mL", "ref < 0.04", "HIGH"),
    ("CK-MB", "6.8 ng/mL", "ref < 6.3", "HIGH"),
    ("D-dimer", "0.4 ug/mL FEU", "ref < 0.5", ""),
    ("Lipid panel — LDL", "132 mg/dL", "ref < 100", "HIGH"),
    ("CRP", "1.1 mg/L", "ref < 3.0", ""),
]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    names = ["arialbd.ttf" if bold else "arial.ttf", "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"]
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default(size)


def main() -> None:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    f_title = font(44, bold=True)
    f_sub = font(30)
    f_head = font(28, bold=True)
    f_cell = font(32)
    f_cell_b = font(32, bold=True)
    f_flag = font(30, bold=True)

    y = MARGIN
    d.text((MARGIN, y), "SYNTHETIC LAB PANEL — DEMO DATA", font=f_title, fill=INK)
    y += 64
    d.text((MARGIN, y), "Patient: Maria Alvarez    DOB 1968-03-12    Collected 2026-07-18 08:40", font=f_sub, fill=MUTED)
    y += 56

    # Column x-positions
    x_test, x_val, x_ref, x_flag = MARGIN + 20, 560, 900, 1200
    table_top = y
    table_w = W - 2 * MARGIN

    # Header row
    d.rectangle([MARGIN, y, MARGIN + table_w, y + 64], fill=HEADER_BG)
    for x, label in ((x_test, "TEST"), (x_val, "RESULT"), (x_ref, "REFERENCE"), (x_flag, "FLAG")):
        d.text((x, y + 16), label, font=f_head, fill=HEADER_INK)
    y += 64

    for test, val, ref, flag in ROWS:
        high = flag == "HIGH"
        if high:
            d.rectangle([MARGIN, y, MARGIN + table_w, y + ROW_H], fill=HIGH_BG)
        cy = y + (ROW_H - 32) // 2
        d.text((x_test, cy), test, font=f_cell_b if high else f_cell, fill=HIGH_INK if high else INK)
        d.text((x_val, cy), val, font=f_cell_b if high else f_cell, fill=HIGH_INK if high else INK)
        d.text((x_ref, cy), ref, font=f_cell, fill=MUTED)
        if high:
            # flag pill
            pad, tw = 14, d.textlength("HIGH", font=f_flag)
            d.rounded_rectangle([x_flag - pad, y + 22, x_flag + tw + pad, y + ROW_H - 22], radius=12, fill=HIGH_INK)
            d.text((x_flag, cy), "HIGH", font=f_flag, fill=(255, 255, 255))
        y += ROW_H
        d.line([MARGIN, y, MARGIN + table_w, y], fill=LINE, width=2)

    d.rectangle([MARGIN, table_top, MARGIN + table_w, y], outline=LINE, width=2)

    d.text((MARGIN, H - 70), "SYNTHETIC DATA — generated for the DOC hackathon demo. Not a real patient record.",
           font=f_sub, fill=MUTED)

    img.save(OUT)
    print(f"wrote {OUT} ({img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
