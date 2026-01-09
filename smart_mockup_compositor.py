#!/usr/bin/env python3
"""
SMART MOCKUP COMPOSITOR WITH SCENE-SPECIFIC RULES
- Adds white mat and black frame to artwork
- Uses scene-specific placement rules (no overlapping)
- Each scene type has custom positioning
- Preview mode before batch processing
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw
import sys

# Scene-specific positioning rules
SCENE_CONFIGS = {
    'living_room': {
        'name': 'Living Room (Above Sofa)',
        'art_position': {
            'x': 0.5,      # Center horizontally
            'y': 0.20,     # Higher up (well above sofa)
            'max_width': 0.20,   # SMALLER - 20% of scene width (was 35%)
            'max_height': 0.25   # SMALLER - 25% of scene height (was 40%)
        },
        'rules': [
            'Centered horizontally on wall',
            'Positioned in upper third (above furniture)',
            'No overlap with sofa or other furniture',
            'Maintains proper wall spacing'
        ]
    },
    'gallery': {
        'name': 'Gallery Wall',
        'art_position': {
            'x': 0.5,      # Center
            'y': 0.35,     # Slightly above center
            'max_width': 0.4,
            'max_height': 0.5
        },
        'rules': [
            'Centered on blank wall section',
            'No overlap with other artwork',
            'Gallery-standard height (eye level)',
            'Proper spacing from other pieces'
        ]
    },
    'office': {
        'name': 'Office (Behind Desk)',
        'art_position': {
            'x': 0.5,      # Center
            'y': 0.3,      # Upper section (wall behind desk)
            'max_width': 0.3,
            'max_height': 0.35
        },
        'rules': [
            'On wall BEHIND desk (not on furniture)',
            'Centered above workspace',
            'Does not overlap with computer/monitor',
            'Professional height positioning'
        ]
    },
    'bedroom': {
        'name': 'Bedroom (Above Headboard)',
        'art_position': {
            'x': 0.5,      # Center
            'y': 0.28,     # Above headboard
            'max_width': 0.38,
            'max_height': 0.42
        },
        'rules': [
            'Centered above bed headboard',
            'Not too low (must clear headboard)',
            'Balanced with room proportions',
            'Standard bedroom art placement'
        ]
    },
    'modern_interior': {
        'name': 'Modern Interior',
        'art_position': {
            'x': 0.48,     # Slightly off-center for modern look
            'y': 0.32,
            'max_width': 0.36,
            'max_height': 0.45
        },
        'rules': [
            'Clean, minimalist placement',
            'Slightly asymmetric for modern aesthetic',
            'No overlap with design elements',
            'Breathing room around artwork'
        ]
    }
}

def add_mat_and_frame(artwork_image, mat_width_pct=0.08, frame_width_px=30):
    """
    Add white mat border and black frame around artwork

    Args:
        artwork_image: PIL Image (RGBA, background removed)
        mat_width_pct: Mat width as % of artwork width (default 8%)
        frame_width_px: Frame width in pixels (default 30px)

    Returns:
        PIL Image with mat and frame
    """
    # Ensure RGBA
    if artwork_image.mode != 'RGBA':
        artwork_image = artwork_image.convert('RGBA')

    art_width, art_height = artwork_image.size

    # Calculate mat size
    mat_width = int(art_width * mat_width_pct)

    # Total canvas size (artwork + mat + frame)
    total_width = art_width + (mat_width * 2) + (frame_width_px * 2)
    total_height = art_height + (mat_width * 2) + (frame_width_px * 2)

    # Create canvas with white background (mat color)
    canvas = Image.new('RGB', (total_width, total_height), 'white')

    # Add black frame border
    draw = ImageDraw.Draw(canvas)
    draw.rectangle(
        [(0, 0), (total_width-1, total_height-1)],
        outline='black',
        width=frame_width_px
    )

    # Paste artwork on white mat (centered)
    paste_x = frame_width_px + mat_width
    paste_y = frame_width_px + mat_width

    # Create white background for artwork area
    bg = Image.new('RGB', artwork_image.size, 'white')
    bg.paste(artwork_image, (0, 0), artwork_image)

    canvas.paste(bg, (paste_x, paste_y))

    return canvas

def composite_artwork_on_scene(framed_artwork, template_path, scene_type):
    """
    Composite framed artwork onto scene with scene-specific rules

    Args:
        framed_artwork: PIL Image (artwork with mat and frame)
        template_path: Path to mockup template image
        scene_type: Key from SCENE_CONFIGS

    Returns:
        PIL Image of final mockup
    """
    # Load template
    template = Image.open(template_path).convert('RGB')
    template_width, template_height = template.size

    # Get scene config
    config = SCENE_CONFIGS.get(scene_type)
    if not config:
        print(f"  ⚠️  Unknown scene type: {scene_type}")
        return template

    pos = config['art_position']

    # Calculate maximum artwork dimensions based on scene
    max_art_width = int(template_width * pos['max_width'])
    max_art_height = int(template_height * pos['max_height'])

    # Resize framed artwork to fit constraints (preserve aspect ratio)
    framed_artwork.thumbnail((max_art_width, max_art_height), Image.Resampling.LANCZOS)

    # Calculate centered position based on scene config
    center_x = int(template_width * pos['x'])
    center_y = int(template_height * pos['y'])

    # Final position (centered at target point)
    final_x = center_x - (framed_artwork.width // 2)
    final_y = center_y - (framed_artwork.height // 2)

    # Create result
    result = template.copy()
    result.paste(framed_artwork, (final_x, final_y))

    return result

def generate_test_mockup(crop_path, template_path, scene_type, output_path):
    """Generate single test mockup"""
    print(f"\n  Testing: {scene_type}")
    config = SCENE_CONFIGS[scene_type]

    # Load artwork
    artwork = Image.open(crop_path).convert('RGBA')
    print(f"    Artwork size: {artwork.size}")

    # Add mat and frame
    framed = add_mat_and_frame(artwork, mat_width_pct=0.08, frame_width_px=30)
    print(f"    Framed size: {framed.size}")

    # Composite onto scene
    mockup = composite_artwork_on_scene(framed, template_path, scene_type)

    # Save
    mockup.save(output_path, 'JPEG', quality=95)
    print(f"    ✅ Saved: {output_path.name}")

    # Print rules
    print(f"    Placement rules for {config['name']}:")
    for rule in config['rules']:
        print(f"      • {rule}")

    return output_path

def main():
    print(f"\n{'='*70}")
    print("SMART MOCKUP COMPOSITOR - TEST MODE")
    print("Scene-specific placement rules • No overlapping")
    print(f"{'='*70}\n")

    # Check for templates directory
    templates_dir = Path("/Users/johnshay/Desktop/mockup_templates")
    if not templates_dir.exists():
        print(f"⚠️  Templates directory not found: {templates_dir}")
        print(f"\nTo use this system:")
        print(f"1. Create directory: {templates_dir}")
        print(f"2. Add mockup template images:")
        print(f"   • living_room.jpg - Living room with sofa")
        print(f"   • gallery.jpg - Gallery wall")
        print(f"   • office.jpg - Office with desk")
        print(f"   • bedroom.jpg - Bedroom with headboard")
        print(f"   • modern_interior.jpg - Modern minimalist space")
        print(f"\n3. Re-run this script to generate test mockups\n")
        templates_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created templates directory")
        return

    # Find available templates
    templates = {
        'living_room': templates_dir / 'living_room.jpg',
        'gallery': templates_dir / 'gallery.jpg',
        'office': templates_dir / 'office.jpg',
        'bedroom': templates_dir / 'bedroom.jpg',
        'modern_interior': templates_dir / 'modern_interior.jpg'
    }

    available_templates = {k: v for k, v in templates.items() if v.exists()}

    if not available_templates:
        print(f"❌ No template images found in {templates_dir}")
        print(f"\nExpected files:")
        for name, path in templates.items():
            print(f"  • {path.name}")
        return

    print(f"Found {len(available_templates)} mockup templates:\n")
    for scene_type, path in available_templates.items():
        config = SCENE_CONFIGS[scene_type]
        print(f"  ✅ {config['name']}: {path.name}")
    print()

    # Find test crop (use SKU 10 crop_1 from Photoroom processing)
    crops_dir = Path("/Users/johnshay/3DSELLERS/processed_crops")
    test_crop = crops_dir / "10" / "10_crop_1.png"

    if not test_crop.exists():
        print(f"❌ Test crop not found: {test_crop}")
        print(f"   Looking for alternative crops...")

        # Find any crop_1.png
        all_crop_1s = list(crops_dir.glob("*/\*_crop_1.png"))
        if all_crop_1s:
            test_crop = all_crop_1s[0]
            print(f"   ✅ Using: {test_crop}")
        else:
            print(f"   ❌ No crops found. Please run CROP_WITH_PHOTOROOM_BG_REMOVAL.py first")
            return

    print(f"\nTest artwork: {test_crop.name}\n")

    # Create output directory
    output_dir = Path("/Users/johnshay/Desktop/mockup_tests")
    output_dir.mkdir(exist_ok=True)

    # Generate test mockup for each available template
    print(f"Generating test mockups...\n")

    for scene_type, template_path in available_templates.items():
        output_path = output_dir / f"test_{scene_type}.jpg"

        try:
            generate_test_mockup(test_crop, template_path, scene_type, output_path)
        except Exception as e:
            print(f"  ❌ Error: {e}")
            import traceback
            traceback.print_exc()

    print(f"\n{'='*70}")
    print("TEST MOCKUPS GENERATED")
    print(f"{'='*70}")
    print(f"\n📁 Review mockups in: {output_dir}")
    print(f"\nCheck each mockup for:")
    print(f"  ✓ Artwork is properly centered")
    print(f"  ✓ No overlap with furniture or other elements")
    print(f"  ✓ White mat and black frame look professional")
    print(f"  ✓ Size is appropriate for the scene")
    print(f"\nIf positioning needs adjustment:")
    print(f"  1. Edit SCENE_CONFIGS in this script")
    print(f"  2. Adjust 'x', 'y', 'max_width', 'max_height' values")
    print(f"  3. Re-run to test again")
    print(f"\nWhen satisfied, batch process all SKUs with full script\n")

if __name__ == "__main__":
    main()
