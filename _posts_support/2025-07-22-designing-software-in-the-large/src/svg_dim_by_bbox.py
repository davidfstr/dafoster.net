#!/usr/bin/env python3
"""
SVG Element Dimmer/Remover by Bounding Box

Processes SVG elements that are not fully within a specified viewport rectangle.
By default, dims them to 25% opacity; with --mode remove, deletes them entirely.

Note: This script does NOT crop the SVG.
Use svg_crop_by_bbox.py for cropping functionality.

Usage:
    python svg_dim_by_bbox.py <input_svg> <output_svg> <rect_index> [--csv PATH] [--mode dim|remove]

The script:
1. Reads the specified rectangle bounds from rectangles.csv (or --csv path)
2. Parses the SVG and finds all top-level group elements
3. For each group, determines if it's fully within the viewport
4. If not fully within: dims to 25% opacity (dim mode) or removes it (remove mode)
5. Outputs the modified SVG

Elements are considered "fully within" if all their bounding box coordinates
are inside the viewport rectangle.
"""

import argparse
import sys
import csv
import xml.etree.ElementTree as ET
import re


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
    
    # Build a set of elements inside <defs> so we can skip them.
    # TLDraw exports clip-path rectangles inside <defs> that are much larger
    # than the visible content and would inflate the bounding box.
    defs_elements = set()
    for defs in element.iter():
        tag = defs.tag.split('}')[-1]
        if tag == 'defs':
            for child in defs.iter():
                defs_elements.add(child)
    
    # Look for path elements within this group, skipping invisible ones
    paths = []
    for el in element.iter():
        tag = el.tag.split('}')[-1]
        # Skip elements inside <defs> (clip paths)
        if el in defs_elements:
            continue
        # Skip invisible rects (TLDraw hit-test areas)
        if tag == 'rect' and el.get('opacity') == '0':
            continue
        if el.get('d'):
            paths.append(el)
    
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


def filter_elements_outside_viewport(svg_path, output_path, viewport, mode='dim'):
    """
    Process SVG file and handle elements that are not fully within viewport.

    Args:
        svg_path: Path to input SVG file
        output_path: Path to output SVG file
        viewport: Dict with viewport bounds (x0, y0, x1, y1)
        mode: 'dim' to set opacity 25%, or 'remove' to delete the element
    """
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    ET.register_namespace('html', 'http://www.w3.org/1999/xhtml')
    ET.register_namespace('sodipodi', 'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd')
    ET.register_namespace('inkscape', 'http://www.inkscape.org/namespaces/inkscape')

    tree = ET.parse(svg_path)
    root = tree.getroot()

    # Only top-level groups — avoids nested groups and opacity stacking
    groups = root.findall('./{http://www.w3.org/2000/svg}g')

    affected_count = 0
    total_groups = len(groups)

    for group in groups:
        bounds = get_element_bounds(group)
        if bounds and not is_fully_within_viewport(bounds, viewport):
            if mode == 'remove':
                root.remove(group)
            else:
                group.set('opacity', '0.25')
            affected_count += 1

    action = 'removed' if mode == 'remove' else 'dimmed'
    print(f"Processed {total_groups} groups, {action} {affected_count} elements")

    tree.write(output_path, encoding='utf-8', xml_declaration=True)
    print(f"Output written to: {output_path}")


# Keep the old name as an alias so existing callers still work
dim_elements_outside_viewport = filter_elements_outside_viewport


def main():
    ap = argparse.ArgumentParser(
        description='Dim or remove SVG top-level groups outside a viewport rectangle.')
    ap.add_argument('input_svg')
    ap.add_argument('output_svg')
    ap.add_argument('rect_index', type=int)
    ap.add_argument('--csv', default='outputs/rectangles.csv',
                    help='Path to rectangles CSV (default: outputs/rectangles.csv)')
    ap.add_argument('--mode', choices=['dim', 'remove'], default='dim',
                    help='dim: set opacity 25%%; remove: delete element (default: dim)')
    args = ap.parse_args()

    rectangles = load_rectangles(args.csv)

    viewport = next((r for r in rectangles if r['index'] == args.rect_index), None)
    if viewport is None:
        print(f"Error: Rectangle index {args.rect_index} not found in {args.csv}")
        sys.exit(1)

    print(f"Using viewport: {viewport}")
    filter_elements_outside_viewport(args.input_svg, args.output_svg, viewport, mode=args.mode)


if __name__ == '__main__':
    main()
