#!/usr/bin/env python3
"""
PHOTOROOM MOCK-UP GENERATOR WITH BLACK FRAME BORDER
====================================================

This script:
1. Loads artwork images from a folder
2. Adds a black border frame + white mat around each image
3. Sends framed artwork to PhotoRoom API
4. Saves the mock-up results

Usage:
    python3 photoroom_mockup.py

Requirements:
    pip3 install Pillow requests
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageOps
import requests
import io
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# =============================================================================
# CONFIGURATION - EDIT THESE
# =============================================================================

CONFIG = {
    # PhotoRoom API
    'API_KEY': os.getenv('PHOTOROOM_API_KEY', ''),  # Get from .env file

    # Folders
    'INPUT_FOLDER': '/Users/johnshay/Desktop/artwork_input',   # Source artwork
    'OUTPUT_FOLDER': '/Users/johnshay/Desktop/mockup_output',  # Output mock-ups

    # Frame Settings (in pixels) - for 13"x18" art at ~90 DPI
    # 3" mat = ~270 pixels, 0.5" frame = ~45 pixels
    'FRAME_BORDER_WIDTH': 45,      # Black border thickness (0.5 inch frame)
    'FRAME_BORDER_COLOR': (0, 0, 0),  # RGB black
    'MAT_WIDTH': 270,              # White mat thickness (3 inches)
    'MAT_COLOR': (255, 255, 255),  # RGB white

    # PhotoRoom API Settings
    'MODEL': 'background-studio-beta-2025-03-17',  # Best quality model
    'OUTPUT_SIZE': '4000x4000',
    'PADDING': '0.40',             # Artwork size (0.40 = ~30% of image)
    'GUIDANCE_SCALE': '0.90',
    'SEED': '117879368',
    'REFERENCE_BOX': 'originalImage',  # Use entire image (includes frame)
    'VERTICAL_ALIGNMENT': 'center',
    'HORIZONTAL_ALIGNMENT': 'center',
    'ENABLE_SHADOWS': True,
}

# Mock-up scenes - each will generate a separate output
PROMPTS = [
    {
        'name': 'CHAIR',
        'prompt': 'Clean white wall in modern minimalist living room. Stylish designer armchair below. Natural daylight from windows, contemporary decor.',
        'seed': '117879368',
        'guidance_image': None,
    },
    {
        'name': 'COUCH',
        'prompt': 'Clean wall above contemporary leather sofa in elegant living room. Plant nearby. Natural light, neutral colors.',
        'seed': '65080068',
        'guidance_image': None,
    },
    {
        'name': 'DESK',
        'prompt': 'Clean wall in stylish home office. Wooden desk with lamp below. Modern professional atmosphere.',
        'seed': '55994449',
        'guidance_image': None,
    },
    {
        'name': 'FLOOR',
        'prompt': 'Clean white wall with beautiful hardwood flooring in minimalist interior. Soft diffused lighting.',
        'seed': '117879368',
        'guidance_image': None,
        'vertical_alignment': 'bottom',
        'padding': '0.38',
    },
]

# =============================================================================
# FRAME FUNCTIONS
# =============================================================================

def add_frame_to_image(image_path, config):
    """
    Add black border frame and white mat to artwork image.

    Returns PIL Image with frame added.
    """
    print(f"  Adding frame to: {os.path.basename(image_path)}")

    # Load image
    img = Image.open(image_path)

    # Convert to RGB if necessary (handles PNG with transparency)
    if img.mode in ('RGBA', 'P'):
        # Create white background
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'RGBA':
            background.paste(img, mask=img.split()[3])  # Use alpha channel as mask
        else:
            background.paste(img)
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')

    # Get frame settings
    border_width = config['FRAME_BORDER_WIDTH']
    border_color = config['FRAME_BORDER_COLOR']
    mat_width = config['MAT_WIDTH']
    mat_color = config['MAT_COLOR']

    # Step 1: Add white mat around artwork
    img_with_mat = ImageOps.expand(img, border=mat_width, fill=mat_color)

    # Step 2: Add black border around mat
    img_with_frame = ImageOps.expand(img_with_mat, border=border_width, fill=border_color)

    print(f"    Original size: {img.size}")
    print(f"    With frame: {img_with_frame.size}")
    print(f"    Border: {border_width}px black, Mat: {mat_width}px white")

    return img_with_frame


def image_to_bytes(pil_image, format='PNG'):
    """Convert PIL Image to bytes."""
    buffer = io.BytesIO()
    pil_image.save(buffer, format=format)
    buffer.seek(0)
    return buffer.getvalue()


# =============================================================================
# PHOTOROOM API
# =============================================================================

def call_photoroom_api(image_bytes, prompt_config, config):
    """
    Call PhotoRoom API to generate mock-up with AI background.
    """
    api_url = 'https://image-api.photoroom.com/v2/edit'

    # Build form data
    files = {
        'imageFile': ('artwork.png', image_bytes, 'image/png'),
    }

    data = {
        'referenceBox': config['REFERENCE_BOX'],
        'background.prompt': prompt_config['prompt'],
        'outputSize': config['OUTPUT_SIZE'],
        'scaling': 'fit',
        'padding': prompt_config.get('padding', config['PADDING']),
        'verticalAlignment': prompt_config.get('vertical_alignment', config['VERTICAL_ALIGNMENT']),
        'horizontalAlignment': prompt_config.get('horizontal_alignment', config['HORIZONTAL_ALIGNMENT']),
        'background.seed': prompt_config.get('seed', config['SEED']),
    }

    if config['ENABLE_SHADOWS']:
        data['shadow.mode'] = 'ai.soft'

    # Add guidance image if provided
    if prompt_config.get('guidance_image') and os.path.exists(prompt_config['guidance_image']):
        with open(prompt_config['guidance_image'], 'rb') as f:
            files['background.guidance.imageFile'] = ('guidance.jpg', f.read(), 'image/jpeg')
        data['background.guidance.scale'] = config['GUIDANCE_SCALE']

    headers = {
        'x-api-key': config['API_KEY'],
        'pr-ai-background-model-version': config['MODEL'],
    }

    print(f"  Calling PhotoRoom API...")
    print(f"    Model: {config['MODEL']}")
    print(f"    Prompt: {prompt_config['prompt'][:80]}...")

    response = requests.post(api_url, headers=headers, files=files, data=data, timeout=120)

    if response.status_code == 200:
        print(f"    Success! Received {len(response.content)} bytes")
        return response.content
    else:
        print(f"    ERROR: {response.status_code}")
        print(f"    {response.text[:500]}")
        return None


# =============================================================================
# MAIN PROCESSING
# =============================================================================

def composite_frame_onto_mockup(mockup_image, framed_artwork, position='center', scale=0.25):
    """
    Composite the framed artwork onto the mockup background.

    Args:
        mockup_image: PIL Image of the room background
        framed_artwork: PIL Image of artwork with frame
        position: 'center', 'center-upper', or tuple (x, y)
        scale: Size of artwork relative to mockup (0.25 = 25% of width)

    Returns:
        PIL Image with artwork composited
    """
    mockup_w, mockup_h = mockup_image.size

    # Calculate target size for framed artwork
    target_width = int(mockup_w * scale)
    aspect_ratio = framed_artwork.height / framed_artwork.width
    target_height = int(target_width * aspect_ratio)

    # Resize framed artwork
    framed_resized = framed_artwork.resize((target_width, target_height), Image.LANCZOS)

    # Calculate position
    if position == 'center':
        x = (mockup_w - target_width) // 2
        y = (mockup_h - target_height) // 2
    elif position == 'center-upper':
        x = (mockup_w - target_width) // 2
        y = int(mockup_h * 0.15)  # 15% from top
    elif position == 'floor':
        x = (mockup_w - target_width) // 2
        y = int(mockup_h * 0.55)  # Lower position for floor lean
    else:
        x, y = position

    # Create composite
    result = mockup_image.copy()

    # If framed artwork has alpha, use it as mask
    if framed_resized.mode == 'RGBA':
        result.paste(framed_resized, (x, y), framed_resized)
    else:
        result.paste(framed_resized, (x, y))

    return result


def process_artwork(image_path, config, prompts):
    """
    Process a single artwork image through all prompts.

    APPROACH:
    1. Create framed artwork (black border + white mat)
    2. Send FRAMED artwork to PhotoRoom
    3. Save the result directly (PhotoRoom should preserve the frame)
    """
    filename = os.path.basename(image_path)
    name_without_ext = os.path.splitext(filename)[0]

    print(f"\n{'='*60}")
    print(f"Processing: {filename}")
    print(f"{'='*60}")

    # Step 1: Create framed version
    framed_image = add_frame_to_image(image_path, config)

    # Save framed version for inspection
    framed_path = os.path.join(config['OUTPUT_FOLDER'], f"{name_without_ext}_FRAMED.png")
    framed_image.save(framed_path)
    print(f"  Saved framed artwork: {framed_path}")

    # Convert to bytes for API
    framed_bytes = image_to_bytes(framed_image)

    # Step 2: Generate mock-up for each prompt
    results = []
    for prompt_config in prompts:
        prompt_name = prompt_config['name']
        print(f"\n  Generating mock-up: {prompt_name}")

        # Call PhotoRoom API with FRAMED image
        result_bytes = call_photoroom_api(framed_bytes, prompt_config, config)

        if result_bytes:
            # Save result directly
            output_filename = f"{name_without_ext}_{prompt_name}.png"
            output_path = os.path.join(config['OUTPUT_FOLDER'], output_filename)

            with open(output_path, 'wb') as f:
                f.write(result_bytes)

            print(f"    Saved: {output_path}")
            results.append({'name': prompt_name, 'path': output_path, 'success': True})
        else:
            results.append({'name': prompt_name, 'path': None, 'success': False})

    return results


def main():
    """Main entry point."""
    print("\n" + "="*60)
    print("PHOTOROOM MOCK-UP GENERATOR WITH FRAME")
    print("="*60)

    # Validate config
    if not CONFIG['API_KEY']:
        print("\nERROR: Please set your API_KEY in the CONFIG section!")
        print("Get your key at: https://www.photoroom.com/api")
        sys.exit(1)

    # Create output folder if needed
    os.makedirs(CONFIG['OUTPUT_FOLDER'], exist_ok=True)

    # Create input folder if needed (for user to add files)
    os.makedirs(CONFIG['INPUT_FOLDER'], exist_ok=True)

    # Find all images in input folder
    input_folder = Path(CONFIG['INPUT_FOLDER'])
    image_extensions = {'.png', '.jpg', '.jpeg', '.webp'}
    images = [f for f in input_folder.iterdir() if f.suffix.lower() in image_extensions]

    if not images:
        print(f"\nNo images found in: {CONFIG['INPUT_FOLDER']}")
        print("Please add artwork images to this folder and run again.")
        sys.exit(0)

    print(f"\nFound {len(images)} artwork images")
    print(f"Will generate {len(PROMPTS)} mock-ups per image")
    print(f"Total outputs: {len(images) * len(PROMPTS)}")

    # Process each image
    all_results = []
    for image_path in images:
        results = process_artwork(str(image_path), CONFIG, PROMPTS)
        all_results.extend(results)

    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    success_count = sum(1 for r in all_results if r['success'])
    print(f"Successful: {success_count}/{len(all_results)}")
    print(f"Output folder: {CONFIG['OUTPUT_FOLDER']}")

    # Open output folder
    if sys.platform == 'darwin':
        os.system(f'open "{CONFIG["OUTPUT_FOLDER"]}"')


if __name__ == '__main__':
    main()
