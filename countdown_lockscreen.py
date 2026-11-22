from datetime import datetime, date
from PIL import Image, ImageDraw, ImageFont
import os

TARGET_DATE = date(2027, 5, 22)
TODAY = date.today()
DAYS_LEFT = max((TARGET_DATE - TODAY).days, 0)

MILESTONES = [
    (90, "FINALIZE POST-GRAD PLANS"),
    (60, "SECURE CAP & GOWN"),
    (45, "SUBMIT DEGREE APPLICATION"),
    (30, "COMPLETE FINAL THESIS DRAFT"),
    (14, "FINAL PROJECT SUBMISSION"),
    (0,  "CCNY GRADUATION CEREMONY"),
]

def get_font(size):
    # Try standard macOS system fonts
    font_paths = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf"
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()

def generate_lockscreen(output_path="graduation_lockscreen.png"):
    width, height = 1170, 2532
    img = Image.new("RGB", (width, height), color=(11, 15, 25))
    draw = ImageDraw.Draw(img)

    # Fonts
    font_header = get_font(36)
    font_sub = get_font(26)
    font_body = get_font(32)
    font_box_title = get_font(40)
    font_box_sub = get_font(28)

    # Subtle HUD grid
    grid_color = (22, 33, 55)
    for x in range(0, width, 90):
        draw.line([(x, 0), (x, height)], fill=grid_color, width=1)
    for y in range(0, height, 90):
        draw.line([(0, y), (width, y)], fill=grid_color, width=1)

    top_margin = 600
    accent_cyan = (56, 189, 248)
    text_white = (241, 245, 249)
    text_muted = (148, 163, 184)

    # Header
    draw.text((100, top_margin), "T-MINUS COUNTDOWN: GRADUATION", fill=accent_cyan, font=font_header)
    draw.text((100, top_margin + 50), f"CCNY B.E. COMPUTER ENGINEERING  |  T-{DAYS_LEFT} DAYS", fill=text_muted, font=font_sub)
    draw.line([(100, top_margin + 100), (width - 100, top_margin + 100)], fill=accent_cyan, width=3)

    # Milestones
    y_cursor = top_margin + 170
    for t_minus, label in MILESTONES:
        completed = DAYS_LEFT < t_minus
        box_color = (34, 197, 94) if completed else accent_cyan
        
        # Checkbox circle
        draw.ellipse([100, y_cursor, 145, y_cursor + 45], outline=box_color, width=4)
        if completed:
            draw.ellipse([110, y_cursor + 10, 135, y_cursor + 35], fill=box_color)

        draw.text((175, y_cursor + 4), f"{label} (T-{t_minus} DAYS)", fill=text_white if not completed else text_muted, font=font_body)
        y_cursor += 130

    # Bottom Readout Box
    box_top = height - 520
    draw.rectangle([100, box_top, width - 100, box_top + 220], outline=accent_cyan, width=3)
    draw.text((150, box_top + 55), f"T - {DAYS_LEFT:03d} DAYS REMAINING", fill=accent_cyan, font=font_box_title)
    draw.text((150, box_top + 125), f"TARGET: {TARGET_DATE.strftime('%B %d, %Y').upper()}", fill=text_muted, font=font_box_sub)

    img.save(output_path)
    print(f"Updated {output_path} with scalable fonts ({DAYS_LEFT} days remaining)")

if __name__ == "__main__":
    generate_lockscreen()
