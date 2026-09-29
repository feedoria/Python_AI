"""
slice_spritesheet.py

Automatically splits a spritesheet PNG (icons/frames on a transparent
background, like the SteampunkUI sheets) into separate PNG files, one per
element - detected via connected-component analysis on the alpha channel.
Same idea as Unity's Sprite Editor "Automatic" slicing, but produces
standalone files you can drop straight into Figma for mockups.

Requires: pip install pillow numpy scipy   (scipy is optional - falls back
to a pure-Python flood fill if it's missing, just slower on big images)

Usage:
    # one file
    python slice_spritesheet.py Steampunk_UI_Frames_3.png out/

    # a whole folder of spritesheets at once (each gets its own subfolder)
    python slice_spritesheet.py Art/ out/ --batch

Options:
    --min-size N        minimum pixel area to keep (filters tiny noise specks). Default 24.
    --padding N          transparent margin (px) kept around each crop. Default 2.
    --alpha-threshold N  alpha value above which a pixel counts as "element". Default 10.
"""
import argparse
import os

import numpy as np
from PIL import Image

try:
    from scipy import ndimage
    HAVE_SCIPY = True
except ImportError:
    HAVE_SCIPY = False
    from collections import deque


def _label_components_scipy(mask):
    # 8-connectivity (diagonals count too, so anti-aliased corners don't split an icon in two)
    structure = np.ones((3, 3), dtype=int)
    labeled, n = ndimage.label(mask, structure=structure)
    objects = ndimage.find_objects(labeled)
    boxes = []
    for i, sl in enumerate(objects, start=1):
        if sl is None:
            continue
        ys, xs = sl
        size = int((labeled[sl] == i).sum())
        boxes.append((ys.start, ys.stop, xs.start, xs.stop, size))
    return boxes


def _label_components_pure(mask):
    h, w = mask.shape
    visited = np.zeros_like(mask, dtype=bool)
    boxes = []
    for y in range(h):
        for x in range(w):
            if mask[y, x] and not visited[y, x]:
                q = deque([(y, x)])
                visited[y, x] = True
                min_x = max_x = x
                min_y = max_y = y
                size = 0
                while q:
                    cy, cx = q.popleft()
                    size += 1
                    min_x, max_x = min(min_x, cx), max(max_x, cx)
                    min_y, max_y = min(min_y, cy), max(max_y, cy)
                    for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)):
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not visited[ny, nx]:
                            visited[ny, nx] = True
                            q.append((ny, nx))
                boxes.append((min_y, max_y + 1, min_x, max_x + 1, size))
    return boxes


def slice_spritesheet(input_path, output_dir, min_size=24, padding=2, alpha_threshold=10, prefix=None):
    os.makedirs(output_dir, exist_ok=True)

    img = Image.open(input_path).convert("RGBA")
    arr = np.array(img)
    mask = arr[:, :, 3] > alpha_threshold
    h, w = mask.shape

    boxes = _label_components_scipy(mask) if HAVE_SCIPY else _label_components_pure(mask)

    if prefix is None:
        prefix = os.path.splitext(os.path.basename(input_path))[0]

    count = 0
    for (y0, y1, x0, x1, size) in boxes:
        if size < min_size:
            continue
        x0 = max(0, x0 - padding)
        y0 = max(0, y0 - padding)
        x1 = min(w, x1 + padding)
        y1 = min(h, y1 + padding)

        crop = img.crop((x0, y0, x1, y1))
        crop.save(os.path.join(output_dir, f"{prefix}_{count:03d}.png"))
        count += 1

    return count


def main():
    parser = argparse.ArgumentParser(description="Slice spritesheet PNG(s) into separate element PNGs.")
    parser.add_argument("input", help="A spritesheet PNG, or a folder of them (with --batch)")
    parser.add_argument("output", help="Folder to save results into")
    parser.add_argument("--batch", action="store_true", help="Treat 'input' as a folder and process every .png inside it")
    parser.add_argument("--min-size", type=int, default=24)
    parser.add_argument("--padding", type=int, default=2)
    parser.add_argument("--alpha-threshold", type=int, default=10)
    args = parser.parse_args()

    if not HAVE_SCIPY:
        print("(scipy not found - using the slower pure-Python fallback. `pip install scipy` for speed on big sheets.)")

    if args.batch:
        sheets = [f for f in os.listdir(args.input) if f.lower().endswith(".png")]
        if not sheets:
            print(f"No .png files found in {args.input}")
            return
        for fname in sheets:
            in_path = os.path.join(args.input, fname)
            out_subdir = os.path.join(args.output, os.path.splitext(fname)[0])
            n = slice_spritesheet(in_path, out_subdir, args.min_size, args.padding, args.alpha_threshold)
            print(f"{fname}: {n} elements -> {out_subdir}")
    else:
        n = slice_spritesheet(args.input, args.output, args.min_size, args.padding, args.alpha_threshold)
        print(f"Done - {n} elements saved to {args.output}")


if __name__ == "__main__":
    main()