#!/usr/bin/env python3
"""
SVG Element Dimmer by Bounding Box

Dims SVG elements that are not fully within a specified viewport rectangle.
Elements extending outside the viewport are set to 25% opacity while elements
fully within the viewport maintain their original appearance.

Note: This script only applies dimming - it does NOT crop the SVG. 
Use svg_crop_by_bbox.py for cropping functionality.

Usage:
    python svg_dim_by_bbox.py <input_svg> <output_svg> <rect_index>

The script:
1. Reads the specified rectangle bounds from rectangles.csv
2. Parses the SVG and finds all top-level group elements
3. For each group, determines if it's fully within the viewport
4. If not fully within, adds opacity="0.25" to dim it
5. Outputs the modified SVG

Elements are considered "fully within" if all their bounding box coordinates
are inside the viewport rectangle.
"""

import sys
import csv
import xml.etree.ElementTree as ET
from pathlib import Path
import re
from typing import List, Tuple


def load_rectangles(csv_path):
    """Load rectangle definitions from CSV file."""
    rectangles = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rectangles.append({
                'index': int(row['index']),
                'x0': float(row['x0']),
                'y0': float(row['y0']),
                'x1': float(row['x1']),
                'y1': float(row['y1']),
                'width': float(row['width']),
                'height': float(row['height'])
            })
    return rectangles


def get_element_bounds(element):
    """
    Extract bounding box coordinates from an SVG element.
    Returns (min_x, min_y, max_x, max_y) or None if bounds can't be determined.
    """
    bounds = None
    
    # Check for transform matrix in the group
    transform = element.get('transform', '')
    translate_x, translate_y = 0, 0
    
    # Parse matrix transform: matrix(a, b, c, d, e, f) where e, f are translations
    matrix_match = re.search(r'matrix\(([^)]+)\)', transform)
    if matrix_match:
        values = [float(x.strip()) for x in matrix_match.group(1).split(',')]
        if len(values) >= 6:
            translate_x, translate_y = values[4], values[5]
    
    # Look for path elements within this group
    paths = element.findall('.//*[@d]')  # Find all elements with 'd' attribute (paths)
    
    if not paths:
        return None
    
    all_coords = []
    
    for path in paths:
        d_attr = path.get('d', '')
        # Extract coordinate pairs from path data
        # This is a simplified parser - may need enhancement for complex paths
        coords = re.findall(r'-?\d+(?:\.\d+)?', d_attr)
        coords = [float(c) for c in coords]
        
        # Group coordinates into (x, y) pairs
        for i in range(0, len(coords) - 1, 2):
            x, y = coords[i] + translate_x, coords[i + 1] + translate_y
            all_coords.append((x, y))
    
    if not all_coords:
        return None
    
    # Calculate bounding box
    min_x = min(coord[0] for coord in all_coords)
    max_x = max(coord[0] for coord in all_coords)
    min_y = min(coord[1] for coord in all_coords)
    max_y = max(coord[1] for coord in all_coords)
    
    return (min_x, min_y, max_x, max_y)


def is_fully_within_viewport(element_bounds, viewport):
    """
    Check if element bounds are fully within the viewport rectangle.
    
    Args:
        element_bounds: (min_x, min_y, max_x, max_y)
        viewport: dict with x0, y0, x1, y1
    
    Returns:
        True if element is fully within viewport, False otherwise
    """
    if element_bounds is None:
        return True  # If we can't determine bounds, don't dim
    
    min_x, min_y, max_x, max_y = element_bounds
    
    viewport_min_x = viewport['x0']
    viewport_max_x = viewport['x1']
    viewport_min_y = viewport['y0']
    viewport_max_y = viewport['y1']
    
    # Element is fully within viewport if all coordinates are inside
    return (min_x >= viewport_min_x and max_x <= viewport_max_x and
            min_y >= viewport_min_y and max_y <= viewport_max_y)


def dim_elements_outside_viewport(svg_path, output_path, viewport):
    """
    Process SVG file and dim elements that are not fully within viewport.
    
    Args:
        svg_path: Path to input SVG file
        output_path: Path to output SVG file
        viewport: Dict with viewport bounds (x, y, width, height)
    """
    # Register namespaces to preserve them
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    ET.register_namespace('html', 'http://www.w3.org/1999/xhtml')
    ET.register_namespace('sodipodi', 'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd')
    ET.register_namespace('inkscape', 'http://www.inkscape.org/namespaces/inkscape')
    
    # Parse the SVG
    tree = ET.parse(svg_path)
    root = tree.getroot()
    
    # Find only top-level group elements (direct children of root)
    # This avoids nested groups and prevents opacity stacking
    groups = root.findall('./{http://www.w3.org/2000/svg}g')
    
    dimmed_count = 0
    total_groups = len(groups)
    debug_count = 0
    
    for group in groups:
        debug_count += 1
        
        # Get the bounding box of this group
        bounds = get_element_bounds(group)
        
        # Check if it's fully within the viewport
        if bounds and not is_fully_within_viewport(bounds, viewport):
            # Dim this element by setting opacity to 25%
            group.set('opacity', '0.25')
            dimmed_count += 1
    
    print(f"Processed {total_groups} groups, dimmed {dimmed_count} elements")
    
    # Write the modified SVG
    tree.write(output_path, encoding='utf-8', xml_declaration=True)
    print(f"Output written to: {output_path}")


def main():
    if len(sys.argv) != 4:
        print("Usage: python svg_crop_and_dim.py <input_svg> <output_svg> <rect_index>")
        print("Example: python svg_crop_and_dim.py outputs/Full_cropped_rect0.svg outputs/Full_cropped_rect0_dimmed.svg 0")
        sys.exit(1)
    
    input_svg = sys.argv[1]
    output_svg = sys.argv[2]
    rect_index = int(sys.argv[3])
    
    # Load rectangle definitions
    rectangles = load_rectangles('outputs/rectangles.csv')
    
    # Find the specified rectangle
    viewport = None
    for rect in rectangles:
        if rect['index'] == rect_index:
            viewport = rect
            break
    
    if viewport is None:
        print(f"Error: Rectangle index {rect_index} not found in rectangles.csv")
        sys.exit(1)
    
    print(f"Using viewport: {viewport}")
    
    # Process the SVG
    dim_elements_outside_viewport(input_svg, output_svg, viewport)


if __name__ == '__main__':
    main()
