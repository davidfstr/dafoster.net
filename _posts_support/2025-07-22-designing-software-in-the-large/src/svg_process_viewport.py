#!/usr/bin/env python3
"""
Comprehensive SVG viewport processor.
Crops SVG to a specific viewport rectangle and dims or removes elements outside it.

Usage:
    python svg_process_viewport.py <input_svg> <output_svg> <rect_index> [--mode dim|remove] [--csv PATH]

Examples:
    python svg_process_viewport.py inputs/Full.svg outputs/section0.svg 0
    python svg_process_viewport.py inputs/Full.svg outputs/section0.svg 0 --mode remove
"""

import argparse
import sys
import subprocess
import os
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent


def main():
    ap = argparse.ArgumentParser(description='Crop SVG to a viewport rectangle.')
    ap.add_argument('input_svg')
    ap.add_argument('output_svg')
    ap.add_argument('rect_index', type=int)
    ap.add_argument('--mode', choices=['dim', 'remove'], default='dim',
                    help='How to handle out-of-viewport elements: dim (25%% opacity) or remove (default: dim)')
    ap.add_argument('--csv',
                    help='Path to rectangles CSV. Defaults to rectangles.csv in the output directory.')
    args = ap.parse_args()

    input_svg = args.input_svg
    output_svg = args.output_svg
    rect_index = str(args.rect_index)

    if not os.path.exists(input_svg):
        print(f"Error: Input file '{input_svg}' not found")
        sys.exit(1)

    csv_path = args.csv or str(Path(output_svg).parent / 'rectangles.csv')

    base_name = os.path.splitext(output_svg)[0]
    dimmed_svg = f"{base_name}_dimmed.svg"

    print(f"Processing viewport {rect_index} from {input_svg} (mode: {args.mode})")
    print(f"Step 1: Filtering elements outside viewport...")

    dim_cmd = [
        "python3", str(SCRIPT_DIR / "svg_dim_by_bbox.py"),
        input_svg, dimmed_svg, rect_index,
        "--csv", csv_path,
        "--mode", args.mode,
    ]

    result = subprocess.run(dim_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error during filtering: {result.stderr}")
        sys.exit(1)
    print(result.stdout.strip())

    print(f"Step 2: Cropping to viewport...")

    crop_cmd = [
        "python3", str(SCRIPT_DIR / "svg_crop_by_bbox.py"),
        dimmed_svg,
        "--csv", csv_path,
        "--index", rect_index,
        "--pad", "0",
        "--hide-stroke", "#e16919",
        "--out", output_svg,
    ]

    result = subprocess.run(crop_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error during cropping: {result.stderr}")
        sys.exit(1)
    print(result.stdout.strip())

    if os.path.exists(dimmed_svg):
        os.remove(dimmed_svg)

    print(f"✅ Successfully processed viewport {rect_index}")
    print(f"   Input:  {input_svg}")
    print(f"   Output: {output_svg}")


if __name__ == "__main__":
    main()
