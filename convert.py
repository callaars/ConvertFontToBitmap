import sys
import json
from PIL import Image, ImageDraw, ImageFont

if len(sys.argv) != 3:
    print("Usage: python font_to_bitmap.py path/to/font.ttf output_prefix")
    sys.exit(1)

FONT_PATH = sys.argv[1]
OUT_PREFIX = sys.argv[2]

FONT_SIZE = 16
CHARS = [chr(i) for i in range(32, 127)]
COLUMNS = 16
PADDING = 2

try:
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
except IOError:
    print(f"Error: Failed to load font from {FONT_PATH}")
    sys.exit(1)

bbox = font.getbbox("W")
max_width = bbox[2] - bbox[0]
max_height = bbox[3] - bbox[1]
cell_w, cell_h = max_width + PADDING, max_height + PADDING
rows = (len(CHARS) + COLUMNS - 1) // COLUMNS

atlas = Image.new("L", (COLUMNS * cell_w, rows * cell_h), color=0)
draw = ImageDraw.Draw(atlas)
metrics = {}

for i, char in enumerate(CHARS):
    x = (i % COLUMNS) * cell_w
    y = (i // COLUMNS) * cell_h
    draw.text((x, y), char, fill=255, font=font)
    bbox = font.getbbox(char)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    metrics[char] = {"x": x, "y": y, "w": w, "h": h}

atlas_path = f"{OUT_PREFIX}_atlas.png"
metrics_path = f"{OUT_PREFIX}_metrics.json"

atlas.save(atlas_path)
with open(metrics_path, "w") as f:
    json.dump(metrics, f, indent=2)

print(f"✅ Saved: {atlas_path}, {metrics_path}")