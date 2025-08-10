# SVG Viewport Processing Tools

This toolkit processes concept map diagrams to create zoomed-in views with dimmed elements outside the viewport.

## Overview

When writing articles about complex topics with concept map diagrams, you often want to show zoomed-in sections that focus on specific areas. This toolkit helps create those zoomed views by:

1. **Dimming** elements that extend outside the viewport to 25% opacity  
2. **Cropping** the SVG to the specific rectangular viewport

The workflow applies dimming first (to the full diagram), then crops to ensure proper visual focus on the main content area while maintaining context from partially visible elements.

## Workflow

### Quick Start (Recommended)

Use the complete workflow script for one-step processing:

```bash
# Process viewport 0 (first orange rectangle)
python3 src/svg_process_viewport.py inputs/Full.svg outputs/section0.svg 0

# Process viewport 1 (second orange rectangle)  
python3 src/svg_process_viewport.py inputs/Full.svg outputs/section1.svg 1
```

### Manual Steps (for debugging)

1. **Find viewport rectangles** (orange rectangles in your diagram):
```bash
python3 src/svg_find_viewports.py inputs/Full.svg --stroke "#e16919" --out outputs/rectangles.csv
```

2. **Dim elements outside viewport**:
```bash
python3 src/svg_dim_by_bbox.py inputs/Full.svg outputs/section1_dimmed.svg 0
```

3. **Crop to specific viewport**:
```bash
python3 src/svg_crop_by_bbox.py outputs/section1_dimmed.svg --csv outputs/rectangles.csv --index 0 --pad 0 --hide-stroke "#e16919" --out outputs/section1_final.svg
```

## Key Features

- **No opacity stacking**: Applies opacity only to top-level groups to avoid visual artifacts
- **Accurate bounds detection**: Parses SVG paths and transforms to determine element positions  
- **Viewport-aware dimming**: Only dims elements that extend outside the viewport boundary
- **Preserves element structure**: Maintains the original SVG structure and namespaces

## Files

- `svg_find_viewports.py` - Finds orange rectangle viewports in SVG
- `svg_dim_by_bbox.py` - Dims elements outside viewport (main dimming logic)
- `svg_crop_by_bbox.py` - Crops SVG to bounding box  
- `svg_process_viewport.py` - Complete workflow script (dimming + cropping)

## Output

The final SVGs will have:
- Cropped viewBox showing only the target area
- Elements fully within viewport at normal opacity (100%)
- Elements extending outside viewport dimmed to 25% opacity
- Proper visual focus on the main content area

## Workflow Details

The correct processing order is **dim first, then crop**:
1. Dimming is applied to the full diagram to identify which elements extend outside the viewport
2. Cropping is then applied to focus on the target area
3. This ensures that dimming decisions are based on the original element positions relative to the viewport
