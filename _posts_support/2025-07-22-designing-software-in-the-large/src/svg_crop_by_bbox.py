#!/usr/bin/env python3
"""
svg_crop_by_bbox.py

Set the SVG root viewBox to a given bbox and optionally hide orange viewport
strokes. Optionally export a PNG via CairoSVG if installed.

You can pass coordinates directly or point to a CSV row produced by
svg_find_viewports.py.

Usage examples:

  # From explicit coords:
  python svg_crop_by_bbox.py Full.svg --coords "-34.3374,91.9799,480.649,490.2719" \
      --pad 12 --hide-stroke "#e16919" --out Full_cropped_rect3.svg

  # From CSV row index:
  python svg_crop_by_bbox.py Full.svg --csv rectangles.csv --index 2 --pad 12 \
      --hide-stroke "#e16919" --out Full_cropped_rect3.svg

  # Also render PNG (requires cairosvg installed):
  python svg_crop_by_bbox.py Full.svg --csv rectangles.csv --index 2 \
      --png Full_cropped_rect3.png
"""

import argparse, csv, sys, xml.etree.ElementTree as ET

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("svg", help="Input SVG file")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--coords", help="x0,y0,x1,y1")
    src.add_argument("--csv", help="CSV from svg_find_viewports.py")
    ap.add_argument("--index", type=int, help="Row index in CSV (0-based) when using --csv")
    ap.add_argument("--pad", type=float, default=0.0, help="Padding (in SVG units) around bbox")
    ap.add_argument("--hide-stroke", default="#e16919",
                    help="Hide any element with this stroke color (use '' to skip)")
    ap.add_argument("--out", required=True, help="Output SVG path")
    ap.add_argument("--png", help="Optional PNG output (requires cairosvg)")
    return ap.parse_args()

import xml.etree.ElementTree as ET
import csv
import sys
from typing import Tuple

def read_csv_bbox(csv_path: str, index: int) -> Tuple[float, float, float, float]:
    with open(csv_path, newline="", encoding="utf-8") as f:
        r = list(csv.DictReader(f))
    if index < 0 or index >= len(r):
        raise SystemExit(f"Index {index} out of range (CSV has {len(r)} data rows).")
    row = r[index]
    return (float(row["x0"]), float(row["y0"]), float(row["x1"]), float(row["y1"]))

def parse_coords(s: str) -> Tuple[float, float, float, float]:
    parts = [p.strip() for p in s.split(",")]
    if len(parts) != 4:
        raise SystemExit("--coords must be 'x0,y0,x1,y1'")
    return tuple(map(float, parts))  # type: ignore

def hide_stroke(root, color: str):
    if not color:
        return
    for el in root.iter():
        if el.attrib.get("stroke", "").lower() == color.lower():
            el.set("display", "none")

def main():
    a = parse_args()
    if a.csv:
        if a.index is None:
            sys.exit("When using --csv you must also pass --index.")
        x0, y0, x1, y1 = read_csv_bbox(a.csv, a.index)
    else:
        x0, y0, x1, y1 = parse_coords(a.coords)

    pad = a.pad
    vx0, vy0 = x0 - pad, y0 - pad
    vw, vh = (x1 - x0) + 2 * pad, (y1 - y0) + 2 * pad

    tree = ET.parse(a.svg)
    root = tree.getroot()

    # Optionally hide orange viewports
    if a["hide_stroke"] if isinstance(a, dict) else a.hide_stroke:
        hide_stroke(root, a.hide_stroke)

    # Update viewBox (and width/height to match the box)
    root.set("viewBox", f"{vx0} {vy0} {vw} {vh}")
    root.set("width", str(vw))
    root.set("height", str(vh))

    tree.write(a.out, encoding="utf-8", xml_declaration=True)
    print(f"Wrote {a.out}")

    if a.png:
        try:
            import cairosvg
        except Exception:
            sys.exit("cairosvg not installed. `pip install cairosvg` to enable PNG export.")
        cairosvg.svg2png(url=a.out, write_to=a.png)
        print(f"Wrote {a.png}")

if __name__ == "__main__":
    main()
