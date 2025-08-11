#!/usr/bin/env python3
"""
SVG Text Box Wrapping Fix Script

This script fixes text wrapping issues in SVG files by modifying the CSS styles
of specific text boxes to prevent line breaks and handle overflow gracefully.

Usage:
    python svg_fix_text_wrap.py "text1,text2,text3" input.svg output.svg

Example:
    python svg_fix_text_wrap.py "Pass-Through Method,Consistent Names" inputs/Full.svg inputs/Full-2.svg
"""

import sys
import re
import argparse
from pathlib import Path


def parse_style_attribute(style_str):
    """Parse CSS style string into a dictionary."""
    styles = {}
    if not style_str:
        return styles
    
    # Split by semicolon and parse each property
    for item in style_str.split(';'):
        item = item.strip()
        if ':' in item:
            key, value = item.split(':', 1)
            styles[key.strip()] = value.strip()
    
    return styles


def serialize_style_dict(styles):
    """Convert style dictionary back to CSS string."""
    return '; '.join(f"{key}: {value}" for key, value in styles.items() if value)


def fix_ancestor_styles(style_str):
    """
    Fix problematic styles in ancestor elements that can cause wrapping.
    
    Removes or replaces:
    - white-space: pre-wrap → remove (defaults to normal)
    - text-wrap: wrap → remove  
    - overflow-wrap: break-word → set to normal
    """
    styles = parse_style_attribute(style_str)
    
    # Remove problematic white-space setting
    if styles.get('white-space') == 'pre-wrap':
        del styles['white-space']
    
    # Remove text-wrap: wrap
    if styles.get('text-wrap') == 'wrap':
        del styles['text-wrap']
    
    # Fix overflow-wrap
    if styles.get('overflow-wrap') == 'break-word':
        styles['overflow-wrap'] = 'normal'
    
    return serialize_style_dict(styles)


def create_no_wrap_style(original_style_str):
    """
    Create the new style for the <p> element to prevent wrapping.
    
    Preserves existing styles but adds no-wrap rules.
    """
    styles = parse_style_attribute(original_style_str)
    
    # Add no-wrap styles
    styles.update({
        'margin': '0',
        'white-space': 'nowrap',
        'overflow-wrap': 'normal',
        'word-break': 'normal', 
        'hyphens': 'none',
        'overflow': 'hidden',
        'text-overflow': 'ellipsis'
    })
    
    return serialize_style_dict(styles)


def fix_p_tag_style(p_start_tag):
    """Extract and modify the style attribute of a <p> tag to prevent wrapping."""
    style_match = re.search(r'style="([^"]*)"', p_start_tag)
    if style_match:
        original_style = style_match.group(1)
        new_style = create_no_wrap_style(original_style)
        return p_start_tag.replace(f'style="{original_style}"', f'style="{new_style}"')
    else:
        # No existing style, add our no-wrap style
        new_style = create_no_wrap_style('')
        return p_start_tag.replace('>', f' style="{new_style}">')


def fix_ancestor_divs_for_text_box(modified_content, first_p_start_tag, text_content, last_p_end_tag):
    """Find and fix ancestor div styles for a text box."""
    # Find the foreignObject that contains this text box
    parts = modified_content.split(first_p_start_tag)
    if len(parts) >= 2:
        # Look backwards from the <p> to find the start of foreignObject
        before_p = parts[0]
        foreign_obj_start_pos = before_p.rfind('<foreignObject')
        
        if foreign_obj_start_pos != -1:
            # Find the end of this foreignObject
            after_p_and_rest = first_p_start_tag + text_content + last_p_end_tag + parts[1]
            foreign_obj_end_pos = after_p_and_rest.find('</foreignObject>')
            
            if foreign_obj_end_pos != -1:
                # Extract the full foreignObject
                foreign_obj_content = before_p[foreign_obj_start_pos:] + after_p_and_rest[:foreign_obj_end_pos + len('</foreignObject>')]
                
                # Fix styles in all div elements within this foreignObject
                def fix_div_style(match):
                    full_tag = match.group(0)
                    style_attr_match = re.search(r'style="([^"]*)"', full_tag)
                    if style_attr_match:
                        original_style = style_attr_match.group(1)
                        fixed_style = fix_ancestor_styles(original_style)
                        return full_tag.replace(f'style="{original_style}"', f'style="{fixed_style}"')
                    return full_tag
                
                # Apply fixes to div elements in this foreignObject
                fixed_foreign_obj = re.sub(r'<div[^>]*style="[^"]*"[^>]*>', fix_div_style, foreign_obj_content)
                
                # Replace the original foreignObject with the fixed one
                return modified_content.replace(foreign_obj_content, fixed_foreign_obj)
    
    return modified_content


def fix_text_box_wrapping(svg_content, text_identifiers):
    """
    Fix text wrapping for specified text boxes in SVG content.
    
    Args:
        svg_content: The SVG file content as a string
        text_identifiers: List of text strings that identify the text boxes to fix
        
    Returns:
        Modified SVG content with fixed text wrapping
    """
    modified_content = svg_content
    
    for text_id in text_identifiers:
        text_id = text_id.strip()
        if not text_id:
            continue
            
        # Check if this is a 2-line text box (contains \n)
        if '\\n' in text_id:
            # Handle 2-line text box - split on the literal \n sequence
            lines = text_id.split('\\n')
            if len(lines) != 2:
                print(f"  Warning: Expected 2 lines but got {len(lines)} for '{text_id}'")
                continue
                
            line1, line2 = lines
            
            # Find both <p> tags in sequence
            # Look for pattern: <p...>line1</p><p...>line2</p> (adjacent p tags)
            pattern = rf'(<p[^>]*>){re.escape(line1)}(</p><p[^>]*>){re.escape(line2)}(</p>)'
            match = re.search(pattern, modified_content, re.DOTALL)
            
            if not match:
                print(f"  Warning: Could not find 2-line text box for '{text_id}'")
                continue
                
            p1_start_tag = match.group(1)
            middle_content = match.group(2)  # </p><p...> (direct connection)
            p2_end_tag = match.group(3)
            
            # Extract the second <p> start tag from middle_content
            # middle_content is "</p><p...>" so we need to extract "<p...>"
            p2_start_match = re.search(r'(<p[^>]*>)$', middle_content)
            if not p2_start_match:
                print(f"  Warning: Could not parse second <p> tag for '{text_id}'")
                continue
                
            p2_start_tag = p2_start_match.group(1)
            p1_end_tag = middle_content[:-len(p2_start_tag)]  # Should be "</p>"
            
            # Fix both <p> tags
            new_p1_start_tag = fix_p_tag_style(p1_start_tag)
            new_p2_start_tag = fix_p_tag_style(p2_start_tag)
            
            # Replace the entire matched section
            original_section = p1_start_tag + line1 + middle_content + line2 + p2_end_tag
            new_section = new_p1_start_tag + line1 + p1_end_tag + new_p2_start_tag + line2 + p2_end_tag
            
            modified_content = modified_content.replace(original_section, new_section)
            
            # Fix ancestor div styles (same logic as single-line)
            modified_content = fix_ancestor_divs_for_text_box(modified_content, new_p1_start_tag, line1, p2_end_tag)
            
        else:
            # Handle single-line text box (existing logic)
            # Find the <p> tag containing this text (minified SVG format)
            p_pattern = rf'(<p[^>]*>){re.escape(text_id)}(</p>)'
            p_match = re.search(p_pattern, modified_content, re.DOTALL)
            
            if not p_match:
                print(f"  Warning: Could not find text box for '{text_id}'")
                continue
                
            p_start_tag = p_match.group(1)
            p_end_tag = p_match.group(2)
            
            # Extract and modify the <p> style
            new_p_start_tag = fix_p_tag_style(p_start_tag)
            
            # Replace the <p> tag
            modified_content = modified_content.replace(p_start_tag, new_p_start_tag)
            
            # Fix ancestor div styles
            modified_content = fix_ancestor_divs_for_text_box(modified_content, new_p_start_tag, text_id, p_end_tag)
        
        print(f"  ✓ Fixed text box: '{text_id}'")
    
    return modified_content


def main():
    parser = argparse.ArgumentParser(
        description='Fix text wrapping in SVG text boxes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python svg_fix_text_wrap.py "Pass-Through Method" input.svg output.svg
  python svg_fix_text_wrap.py "Method 1,Method 2,Method 3" input.svg output.svg
        """)
    
    parser.add_argument('text_identifiers', 
                        help='Comma-separated list of text box identifiers to fix')
    parser.add_argument('input_file', 
                        help='Input SVG file path')
    parser.add_argument('output_file', 
                        help='Output SVG file path')
    
    args = parser.parse_args()
    
    # Parse text identifiers
    text_identifiers = [text.strip() for text in args.text_identifiers.split(',')]
    text_identifiers = [text for text in text_identifiers if text]  # Remove empty strings
    
    if not text_identifiers:
        print("Error: No valid text identifiers provided")
        sys.exit(1)
    
    # Check input file exists
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: Input file '{args.input_file}' does not exist")
        sys.exit(1)
    
    # Read input SVG
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            svg_content = f.read()
    except Exception as e:
        print(f"Error reading input file: {e}")
        sys.exit(1)
    
    print(f"Processing {len(text_identifiers)} text box(es)...")
    
    # Fix text wrapping
    try:
        modified_content = fix_text_box_wrapping(svg_content, text_identifiers)
    except Exception as e:
        print(f"Error processing SVG: {e}")
        sys.exit(1)
    
    # Write output SVG
    try:
        output_path = Path(args.output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)
    
    print(f"✓ Successfully processed SVG and saved to '{args.output_file}'")


if __name__ == '__main__':
    main()
