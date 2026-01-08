#!/usr/bin/env python3
"""
Mockup Generator Demo
Creates sample mockups without needing any API keys.

Run: python demo.py
"""

import os
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
except ImportError:
    print("Installing Pillow...")
    os.system("pip install Pillow")
    from PIL import Image, ImageDraw, ImageFilter, ImageEnhance


def print_header(text):
    print(f"\n{'='*60}")
    print(f" {text}")
    print(f"{'='*60}\n")


def create_sample_artwork():
    """Create a sample artwork image"""
    # Create colorful abstract art
    img = Image.new('RGB', (800, 1000), '#F5F5F5')
    draw = ImageDraw.Draw(img)

    # Background gradient effect (simplified)
    for i in range(100):
        y = i * 10
        color = f'#{hex(200 + i // 2)[2:]:0>2}{hex(180 + i // 3)[2:]:0>2}{hex(220 - i // 2)[2:]:0>2}'
        try:
            draw.rectangle([0, y, 800, y + 10], fill=color)
        except:
            draw.rectangle([0, y, 800, y + 10], fill='#C8B4DC')

    # Add abstract shapes
    draw.ellipse([100, 150, 400, 450], fill='#E74C3C', outline='#C0392B', width=5)
    draw.rectangle([350, 400, 700, 800], fill='#3498DB', outline='#2980B9', width=5)
    draw.polygon([(400, 100), (650, 350), (200, 400)], fill='#F1C40F', outline='#F39C12', width=3)

    # Add some texture lines
    for i in range(20):
        x = 50 + i * 40
        draw.line([(x, 850), (x + 100, 950)], fill='#2C3E50', width=2)

    # Signature area
    draw.text((650, 950), "Artist", fill='#2C3E50')

    return img


def create_frame(artwork, frame_style='black_metal', frame_width=40):
    """Add a frame around the artwork"""
    aw, ah = artwork.size

    # Frame colors by style
    frame_colors = {
        'black_metal': ('#1a1a1a', '#333333'),
        'white_wood': ('#F5F5F5', '#E0E0E0'),
        'gold_ornate': ('#D4AF37', '#B8860B'),
        'natural_oak': ('#DEB887', '#D2691E'),
    }

    outer_color, inner_color = frame_colors.get(frame_style, ('#1a1a1a', '#333333'))

    # Create framed image
    framed_width = aw + frame_width * 2
    framed_height = ah + frame_width * 2

    framed = Image.new('RGB', (framed_width, framed_height), outer_color)
    draw = ImageDraw.Draw(framed)

    # Inner frame border
    draw.rectangle(
        [frame_width // 4, frame_width // 4,
         framed_width - frame_width // 4, framed_height - frame_width // 4],
        fill=inner_color
    )

    # Mat/mount (white border around artwork)
    mat_width = 20
    draw.rectangle(
        [frame_width - mat_width, frame_width - mat_width,
         frame_width + aw + mat_width, frame_width + ah + mat_width],
        fill='#FAFAFA'
    )

    # Paste artwork
    framed.paste(artwork, (frame_width, frame_width))

    return framed


def create_room_scene(width=1600, height=1200):
    """Create a simple room scene background"""
    room = Image.new('RGB', (width, height), '#E8E4E0')
    draw = ImageDraw.Draw(room)

    # Wall (upper 2/3)
    draw.rectangle([0, 0, width, height * 2 // 3], fill='#F5F2EF')

    # Floor (lower 1/3)
    draw.rectangle([0, height * 2 // 3, width, height], fill='#D4C4B5')

    # Baseboard
    draw.rectangle([0, height * 2 // 3 - 20, width, height * 2 // 3], fill='#FFFFFF')

    # Add subtle wall texture (horizontal lines)
    for i in range(0, height * 2 // 3, 100):
        draw.line([(0, i), (width, i)], fill='#EBE7E3', width=1)

    # Add a simple plant silhouette on the right
    plant_x = width - 200
    plant_y = height * 2 // 3 - 50
    draw.ellipse([plant_x, plant_y - 150, plant_x + 100, plant_y + 50], fill='#228B22')
    draw.rectangle([plant_x + 40, plant_y, plant_x + 60, plant_y + 100], fill='#8B4513')

    return room


def create_mockup(artwork, room, position='center'):
    """Composite artwork onto room scene"""
    room_copy = room.copy()
    aw, ah = artwork.size
    rw, rh = room_copy.size

    # Calculate position (centered on wall)
    if position == 'center':
        x = (rw - aw) // 2
        y = (rh * 2 // 3 - ah) // 2 - 50  # Centered on wall, slightly up

    # Add shadow
    shadow = Image.new('RGBA', (aw + 40, ah + 40), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rectangle([20, 20, aw + 20, ah + 20], fill=(0, 0, 0, 80))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=15))

    # Paste shadow
    room_copy.paste(Image.new('RGB', (aw + 40, ah + 40), '#F5F2EF'), (x - 10, y - 10))
    shadow_rgb = Image.new('RGB', shadow.size, '#F5F2EF')
    shadow_rgb.paste(shadow, mask=shadow.split()[3])
    room_copy.paste(shadow_rgb, (x - 10, y + 10), mask=shadow.split()[3])

    # Paste framed artwork
    room_copy.paste(artwork, (x, y))

    return room_copy


def demo_single_mockup():
    """Create a single mockup demonstration"""
    print_header("CREATING SINGLE MOCKUP")

    output_dir = Path("demo_output")
    output_dir.mkdir(exist_ok=True)

    # Create artwork
    print("1. Creating sample artwork...")
    artwork = create_sample_artwork()
    artwork.save(output_dir / "original_artwork.jpg", quality=95)
    print(f"   Saved: original_artwork.jpg ({artwork.size[0]}x{artwork.size[1]})")

    # Create framed version
    print("\n2. Adding black metal frame...")
    framed = create_frame(artwork, 'black_metal')
    framed.save(output_dir / "framed_artwork.jpg", quality=95)
    print(f"   Saved: framed_artwork.jpg ({framed.size[0]}x{framed.size[1]})")

    # Create room scene
    print("\n3. Creating room scene...")
    room = create_room_scene()
    room.save(output_dir / "room_scene.jpg", quality=95)
    print(f"   Saved: room_scene.jpg ({room.size[0]}x{room.size[1]})")

    # Create final mockup
    print("\n4. Compositing final mockup...")
    mockup = create_mockup(framed, room)
    mockup.save(output_dir / "final_mockup.jpg", quality=95)
    print(f"   Saved: final_mockup.jpg ({mockup.size[0]}x{mockup.size[1]})")

    return output_dir


def demo_multiple_frames():
    """Create mockups with different frame styles"""
    print_header("CREATING MULTIPLE FRAME STYLES")

    output_dir = Path("demo_output")
    artwork = create_sample_artwork()
    room = create_room_scene()

    frame_styles = ['black_metal', 'white_wood', 'gold_ornate', 'natural_oak']

    for style in frame_styles:
        print(f"Creating {style} frame mockup...")
        framed = create_frame(artwork, style)
        mockup = create_mockup(framed, room)
        filename = f"mockup_{style}.jpg"
        mockup.save(output_dir / filename, quality=95)
        print(f"   Saved: {filename}")


def demo_export_sizes():
    """Export mockup in multiple sizes"""
    print_header("EXPORTING MULTIPLE SIZES")

    output_dir = Path("demo_output")
    artwork = create_sample_artwork()
    framed = create_frame(artwork, 'black_metal')
    room = create_room_scene(1920, 1440)  # Larger base for quality
    mockup = create_mockup(framed, room)

    sizes = [
        ("square_1200", (1200, 1200)),
        ("landscape_1600x1200", (1600, 1200)),
        ("hero_1920x1080", (1920, 1080)),
        ("thumbnail_800", (800, 800)),
    ]

    for name, size in sizes:
        resized = mockup.copy()
        # Crop to aspect ratio then resize
        target_ratio = size[0] / size[1]
        current_ratio = resized.size[0] / resized.size[1]

        if current_ratio > target_ratio:
            # Too wide, crop width
            new_width = int(resized.size[1] * target_ratio)
            left = (resized.size[0] - new_width) // 2
            resized = resized.crop((left, 0, left + new_width, resized.size[1]))
        else:
            # Too tall, crop height
            new_height = int(resized.size[0] / target_ratio)
            top = (resized.size[1] - new_height) // 2
            resized = resized.crop((0, top, resized.size[0], top + new_height))

        resized = resized.resize(size, Image.Resampling.LANCZOS)
        filename = f"mockup_{name}.jpg"
        resized.save(output_dir / filename, quality=95)
        print(f"Saved: {filename} ({size[0]}x{size[1]})")


def main():
    print_header("MOCKUP GENERATOR - DEMO")

    print("This demo creates professional product mockups.")
    print("No API keys required!\n")

    # Demo 1: Single mockup
    output_dir = demo_single_mockup()

    # Demo 2: Multiple frames
    demo_multiple_frames()

    # Demo 3: Multiple sizes
    demo_export_sizes()

    print_header("DEMO COMPLETE")
    print(f"All mockups saved to: {output_dir}/")
    print("\nFiles created:")
    for f in sorted(output_dir.glob("*.jpg")):
        size = Image.open(f).size
        print(f"  - {f.name} ({size[0]}x{size[1]})")

    print("\nNext steps:")
    print("  1. Try with your own artwork images")
    print("  2. Customize frame styles in the code")
    print("  3. Add PhotoRoom API key for background removal")


if __name__ == "__main__":
    main()
