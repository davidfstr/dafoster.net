#!/usr/bin/env python3
"""
svg_find_viewports.py

Scan an SVG for orange "viewport" rectangles and emit a CSV of their bboxes.

We detect any <path> or <rect> whose *stroke* equals the target color.
For <rect>, bbox = transformed corners. For <path>, we approximate bbox by
taking min/max over all numeric (x,y) pairs found in the 'd' attribute and then
applying any parent/own translation (matrix(1,0,0,1,tx,ty) or translate).

This is tuned for the provided file where the viewports are orange stroked
paths with only translations in ancestor <g> transforms.

Usage:
  python svg_find_viewports.py Full.svg --stroke "#e16919" --out rectangles.csv
  # or omit --out to print CSV to stdout
"""

import argparse, csv, re, sys, xml.etree.ElementTree as ET
from typing import List, Tuple, Optional

Pair = Tuple[float, float]
BBox = Tuple[float, float, float, float]

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("svg", help="Input SVG file")
    ap.add_argument("--stroke", default="#e16919", help="Stroke color to match (e.g. #e16919)")
    ap.add_argument("--out", help="Output CSV path (default: stdout)")
    return ap.parse_args()

def parse_translate_only(transform: str) -> Tuple[float, float]:
    """Extract translation (tx,ty) from either translate(x[,y]) or matrix(1,0,0,1,tx,ty)."""
    if not transform:
        return 0.0, 0.0
    tx = ty = 0.0
    m = re.search(r"matrix\(\s*([^)]+)\)", transform)
    if m:
        parts = [float(x) for x in re.split(r"[ ,]+", m.group(1).strip()) if x]
        if len(parts) == 6:
            # a,b,c,d,e,f; we only honor e,f (translation)
            tx += parts[4]; ty += parts[5]
    t = re.search(r"translate\(\s*([^)]+)\)", transform)
    if t:
        parts = [float(x) for x in re.split(r"[ ,]+", t.group(1).strip()) if x]
        if len(parts) == 1:
            tx += parts[0]
        elif len(parts) >= 2:
            tx += parts[0]; ty += parts[1]
    return tx, ty

def build_parent_map(root):
    return {c: p for p in root.iter() for c in p}

def total_translation(node, parent_map) -> Tuple[float, float]:
    tx = ty = 0.0
    n = node
    while n is not None:
        t = n.attrib.get("transform", "")
        dx, dy = parse_translate_only(t)
        tx += dx; ty += dy
        n = parent_map.get(n)
    return tx, ty

def rect_bbox(node, parent_map) -> Optional[BBox]:
    try:
        x = float(node.attrib.get("x", "0"))
        y = float(node.attrib.get("y", "0"))
        w = float(node.attrib.get("width", "0"))
        h = float(node.attrib.get("height", "0"))
    except ValueError:
        return None
    x0, y0, x1, y1 = x, y, x + w, y + h
    tx, ty = total_translation(node, parent_map)
    return (x0 + tx, y0 + ty, x1 + tx, y1 + ty)

def path_bbox(node, parent_map) -> Optional[BBox]:
    """Approximate bbox by min/max over (x,y) numeric pairs in 'd' then apply translation."""
    d = node.attrib.get("d", "")
    if not d:
        return None
    # capture float pairs (x y). This ignores command letters and works well for your rounded-rect paths.
    pairs: List[Pair] = []
    # Find all floats then fold into pairs
    floats = [float(n) for n in re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", d)]
    if len(floats) < 2:
        return None
    # Best-effort: treat them as x,y,x,y,...; this matches your viewport paths.
    xs = floats[0::2]
    ys = floats[1::2]
    if not xs or not ys:
        return None
    x0, y0, x1, y1 = min(xs), min(ys), max(xs), max(ys)
    tx, ty = total_translation(node, parent_map)
    return (x0 + tx, y0 + ty, x1 + tx, y1 + ty)

def main():
    args = parse_args()
    tree = ET.parse(args.svg)
    root = tree.getroot()
    parent_map = build_parent_map(root)

    targets = []
    for el in root.iter():
        if el.attrib.get("stroke", "").lower() != args.stroke.lower():
            continue
        bbox = None
        tag = el.tag.split("}")[-1]
        if tag == "rect":
            bbox = rect_bbox(el, parent_map)
        elif tag == "path":
            bbox = path_bbox(el, parent_map)
        if bbox:
            x0, y0, x1, y1 = bbox
            targets.append((x0, y0, x1, y1))

    # Write CSV
    out_f = open(args.out, "w", newline="", encoding="utf-8") if args.out else sys.stdout
    w = csv.writer(out_f)
    w.writerow(["index", "x0", "y0", "x1", "y1", "width", "height"])
    for i, (x0, y0, x1, y1) in enumerate(targets):
        w.writerow([i, x0, y0, x1, y1, x1 - x0, y1 - y0])
    if args.out:
        out_f.close()

if __name__ == "__main__":
    main()
