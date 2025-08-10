#!/usr/bin/env python3
"""
Comprehensive SVG viewport processor.
Crops SVG to a specific viewport rectangle and dims elements outside the viewport.
"""

import sys
import subprocess
import os

def main():
    if len(sys.argv) != 4:
        print("Usage: python svg_process_viewport.py <input_svg> <output_svg> <rect_index>")
        print("Example: python svg_process_viewport.py inputs/Full.svg outputs/Full_rect0_processed.svg 0")
        sys.exit(1)
    
    input_svg = sys.argv[1]
    output_svg = sys.argv[2]
    rect_index = sys.argv[3]
    
    # Check if input file exists
    if not os.path.exists(input_svg):
        print(f"Error: Input file '{input_svg}' not found")
        sys.exit(1)
    
    # Create intermediate filename for dimmed version
    base_name = os.path.splitext(output_svg)[0]
    dimmed_svg = f"{base_name}_dimmed.svg"
    
    print(f"Processing viewport {rect_index} from {input_svg}")
    print(f"Step 1: Dimming elements outside viewport...")
    
    # Step 1: Apply dimming to elements outside viewport
    dim_cmd = [
        "python3", "src/svg_dim_by_bbox.py",
        input_svg, dimmed_svg, rect_index
    ]
    
    result = subprocess.run(dim_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error during dimming: {result.stderr}")
        sys.exit(1)
    
    print(f"Step 2: Cropping to viewport...")
    
    # Step 2: Crop the dimmed SVG to the viewport
    crop_cmd = [
        "python3", "src/svg_crop_by_bbox.py",
        dimmed_svg,
        "--csv", "outputs/rectangles.csv",
        "--index", rect_index,
        "--out", output_svg
    ]
    
    result = subprocess.run(crop_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error during cropping: {result.stderr}")
        sys.exit(1)
    
    # Clean up intermediate file
    if os.path.exists(dimmed_svg):
        os.remove(dimmed_svg)
    
    print(f"✅ Successfully processed viewport {rect_index}")
    print(f"   Input:  {input_svg}")
    print(f"   Output: {output_svg}")
    print(f"   Dimmed outside elements, then cropped to viewport")

if __name__ == "__main__":
    main()
