#!/usr/bin/env python3
"""
MOCKUP GENERATOR WITH PROFESSIONAL FRAMING
- Adds white mat border around artwork
- Adds black frame around mat
- Composites onto lifestyle mockup templates
- Consistent sizing and placement
"""

import os
import sys
import pickle
from pathlib import Path
from PIL import Image, ImageDraw
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import time

# Google Drive folder for Death NYC Art
DEATH_NYC_ART_FOLDER_ID = '1oGtrD1326eBij2akelFn2nzEc5_OUckW'

# Google Sheets
SPREADSHEET_ID = "1qRRIA7rbW_JhDg20xXV1WrZ-yx8ndnlwQrLkapr65Hc"
PRODUCTS_SHEET = "PRODUCTS"

BASE_DIR = Path("/Users/johnshay/3DSELLERS")
CROPS_INPUT_DIR = BASE_DIR / "processed_crops"  # Where Photoroom crops are
MOCKUPS_OUTPUT_DIR = Path("/Users/johnshay/Desktop/framed_mockups")  # Output to Desktop
MOCKUP_TEMPLATES_DIR = Path("/Users/johnshay/Desktop/mockup_templates")  # User provides these

# Mockup columns in Google Sheets (AF, AG, AH, AI, AJ)
MOCKUP_COLUMNS = ['AF', 'AG', 'AH', 'AI', 'AJ']

def get_drive_service():
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    else:
        raise FileNotFoundError("token.pickle not found")
    return build('drive', 'v3', credentials=creds)

def get_sheets_service():
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    else:
        raise FileNotFoundError("token.pickle not found")
    return build('sheets', 'v4', credentials=creds)

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
    # Outer frame
    draw.rectangle(
        [(0, 0), (total_width-1, total_height-1)],
        outline='black',
        width=frame_width_px
    )

    # Paste artwork on white mat (centered)
    # Position: frame_width + mat_width from edges
    paste_x = frame_width_px + mat_width
    paste_y = frame_width_px + mat_width

    # Create white background for artwork area
    bg = Image.new('RGB', artwork_image.size, 'white')
    bg.paste(artwork_image, (0, 0), artwork_image)

    canvas.paste(bg, (paste_x, paste_y))

    return canvas

def create_mockup_on_template(framed_artwork, template_path, artwork_position):
    """
    Composite framed artwork onto mockup template

    Args:
        framed_artwork: PIL Image (artwork with mat and frame)
        template_path: Path to mockup template image
        artwork_position: dict with 'x', 'y', 'width', 'height' (normalized 0-1)

    Returns:
        PIL Image of final mockup
    """
    # Load template
    template = Image.open(template_path).convert('RGB')
    template_width, template_height = template.size

    # Calculate artwork dimensions on template
    # Position is given as percentage of template size
    target_width = int(template_width * artwork_position['width'])
    target_height = int(template_height * artwork_position['height'])
    target_x = int(template_width * artwork_position['x'])
    target_y = int(template_height * artwork_position['y'])

    # Resize framed artwork to fit target area (preserve aspect ratio)
    framed_artwork.thumbnail((target_width, target_height), Image.Resampling.LANCZOS)

    # Center within target area
    final_x = target_x + (target_width - framed_artwork.width) // 2
    final_y = target_y + (target_height - framed_artwork.height) // 2

    # Paste onto template
    result = template.copy()
    result.paste(framed_artwork, (final_x, final_y))

    return result

def generate_mockups_for_artwork(sku_dir):
    """
    Generate framed mockups for all crops in SKU directory

    Args:
        sku_dir: Path to SKU directory containing crops (e.g., processed_crops/10/)

    Returns:
        List of generated mockup file paths
    """
    sku = sku_dir.name
    print(f"\n{'='*70}")
    print(f"Generating Mockups: {sku}")
    print(f"{'='*70}")

    # Find crop_1 (main full artwork with background removed)
    crop_1_path = sku_dir / f"{sku}_crop_1.png"

    if not crop_1_path.exists():
        print(f"  ❌ Main crop not found: {crop_1_path}")
        return []

    print(f"  Loading main crop: {crop_1_path.name}")
    artwork = Image.open(crop_1_path).convert('RGBA')
    print(f"  Original crop size: {artwork.size}")

    # Step 1: Add mat and frame
    print(f"  Step 1: Adding white mat and black frame...")
    framed_artwork = add_mat_and_frame(artwork, mat_width_pct=0.08, frame_width_px=30)
    print(f"  Framed artwork size: {framed_artwork.size}")

    # Step 2: Check for mockup templates
    if not MOCKUP_TEMPLATES_DIR.exists():
        print(f"  ⚠️  No mockup templates found at {MOCKUP_TEMPLATES_DIR}")
        print(f"  Creating just the framed artwork without template compositing")

        # Save just the framed artwork
        output_dir = MOCKUPS_OUTPUT_DIR / sku
        output_dir.mkdir(parents=True, exist_ok=True)

        framed_path = output_dir / f"{sku}_framed_main.jpg"
        framed_artwork.save(framed_path, 'JPEG', quality=95)
        print(f"  ✅ Saved framed artwork: {framed_path.name}")

        return [framed_path]

    # Step 3: Generate mockups with templates
    mockup_configs = [
        {
            'name': 'living_room_wall',
            'template': 'living_room.jpg',
            'position': {'x': 0.25, 'y': 0.15, 'width': 0.35, 'height': 0.45}
        },
        {
            'name': 'gallery_wall',
            'template': 'gallery.jpg',
            'position': {'x': 0.3, 'y': 0.2, 'width': 0.4, 'height': 0.5}
        },
        {
            'name': 'bedroom_wall',
            'template': 'bedroom.jpg',
            'position': {'x': 0.28, 'y': 0.18, 'width': 0.38, 'height': 0.48}
        },
        {
            'name': 'office_wall',
            'template': 'office.jpg',
            'position': {'x': 0.32, 'y': 0.22, 'width': 0.36, 'height': 0.46}
        },
        {
            'name': 'modern_interior',
            'template': 'modern.jpg',
            'position': {'x': 0.27, 'y': 0.16, 'width': 0.42, 'height': 0.52}
        }
    ]

    output_dir = MOCKUPS_OUTPUT_DIR / sku
    output_dir.mkdir(parents=True, exist_ok=True)

    mockup_files = []

    # First, always save the framed artwork (no template)
    framed_path = output_dir / f"{sku}_framed_main.jpg"
    framed_artwork.save(framed_path, 'JPEG', quality=95)
    mockup_files.append(framed_path)
    print(f"  ✅ [1/6] Saved framed artwork: {framed_path.name}")

    # Generate template-based mockups
    for i, config in enumerate(mockup_configs, 2):
        template_path = MOCKUP_TEMPLATES_DIR / config['template']

        if not template_path.exists():
            print(f"  ⚠️  [{i}/6] Template not found: {config['template']}")
            continue

        print(f"  [{i}/6] Creating mockup: {config['name']}...")
        mockup = create_mockup_on_template(
            framed_artwork.copy(),
            template_path,
            config['position']
        )

        mockup_path = output_dir / f"{sku}_mockup_{config['name']}.jpg"
        mockup.save(mockup_path, 'JPEG', quality=95)
        mockup_files.append(mockup_path)
        print(f"      ✅ Saved: {mockup_path.name}")

    print(f"  ✅ Generated {len(mockup_files)} mockups")
    return mockup_files

def upload_file_to_drive(service, file_path, folder_id):
    """Upload file to Google Drive"""
    file_metadata = {'name': file_path.name, 'parents': [folder_id]}
    media = MediaFileUpload(str(file_path), mimetype='image/jpeg', resumable=True)

    try:
        file = service.files().create(
            body=file_metadata, media_body=media,
            fields='id, webViewLink, webContentLink'
        ).execute()

        permission = {'type': 'anyone', 'role': 'reader'}
        service.permissions().create(fileId=file['id'], body=permission).execute()

        return f"https://drive.google.com/uc?export=view&id={file['id']}"
    except Exception as e:
        print(f"    ❌ Upload failed: {e}")
        return None

def get_sheet_row_for_sku(sheets_service, sku):
    """Find row number for SKU"""
    result = sheets_service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID, range=f"{PRODUCTS_SHEET}!A:A"
    ).execute()

    values = result.get('values', [])
    for i, row in enumerate(values):
        if row and row[0].startswith(f"{sku}_"):
            return i + 1
    return None

def update_sheet_with_mockups(sheets_service, sku, mockup_links):
    """Update Google Sheets with mockup links"""
    row_num = get_sheet_row_for_sku(sheets_service, sku)
    if not row_num:
        print(f"    ⚠️  SKU {sku} not found in sheet")
        return False

    updates = []
    for i, link in enumerate(mockup_links):
        if i < len(MOCKUP_COLUMNS):
            col = MOCKUP_COLUMNS[i]
            updates.append({
                'range': f"{PRODUCTS_SHEET}!{col}{row_num}",
                'values': [[link]]
            })

    body = {'valueInputOption': 'USER_ENTERED', 'data': updates}

    try:
        sheets_service.spreadsheets().values().batchUpdate(
            spreadsheetId=SPREADSHEET_ID, body=body
        ).execute()
        return True
    except Exception as e:
        print(f"    ❌ Sheet update failed: {e}")
        return False

def main():
    print(f"\n{'='*70}")
    print("MOCKUP GENERATOR WITH PROFESSIONAL FRAMING")
    print("White mat + Black frame + Template compositing")
    print(f"{'='*70}\n")

    MOCKUPS_OUTPUT_DIR.mkdir(exist_ok=True)

    # Check for mockup templates
    if not MOCKUP_TEMPLATES_DIR.exists():
        print(f"⚠️  Mockup templates directory not found: {MOCKUP_TEMPLATES_DIR}")
        print(f"   Creating directory - you can add template images later")
        print(f"   Template images should be named: living_room.jpg, gallery.jpg, etc.")
        MOCKUP_TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
        print(f"   For now, I'll generate framed artworks without template compositing\n")

    print("Authenticating with Google...")
    drive_service = get_drive_service()
    sheets_service = get_sheets_service()
    print("✅ Authenticated\n")

    # Find all SKU directories with crops
    sku_dirs = sorted([d for d in CROPS_INPUT_DIR.glob("*") if d.is_dir()])
    print(f"Found {len(sku_dirs)} SKU directories to process\n")

    successful = 0
    failed = 0

    # Test mode - process first 2 SKUs for review
    test_mode = True
    test_count = 2 if test_mode else len(sku_dirs)

    if test_mode:
        print(f"🔴 TEST MODE: Processing first {test_count} SKUs for review\n")

    for idx, sku_dir in enumerate(sku_dirs[:test_count], 1):
        sku = sku_dir.name
        print(f"\n[{idx}/{test_count}] Processing SKU: {sku}")

        try:
            # Generate mockups
            mockup_files = generate_mockups_for_artwork(sku_dir)

            if not mockup_files:
                print(f"  ❌ No mockups generated")
                failed += 1
                continue

            # Upload to Google Drive
            print(f"  Uploading {len(mockup_files)} mockups to Google Drive...")
            mockup_links = []

            for i, mockup_path in enumerate(mockup_files, 1):
                print(f"    [{i}/{len(mockup_files)}] Uploading {mockup_path.name}...")
                link = upload_file_to_drive(drive_service, mockup_path, DEATH_NYC_ART_FOLDER_ID)

                if link:
                    mockup_links.append(link)
                    print(f"      ✅ Uploaded: {link[:80]}...")
                else:
                    mockup_links.append("")

                time.sleep(0.5)

            # Update Google Sheets
            print(f"  Updating Google Sheets...")
            if update_sheet_with_mockups(sheets_service, sku, mockup_links):
                print(f"  ✅ Sheet updated with {len(mockup_links)} mockup links")
                successful += 1
            else:
                print(f"  ❌ Failed to update sheet")
                failed += 1

        except Exception as e:
            print(f"\n  ❌ Error: {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    print(f"\n\n{'='*70}")
    if test_mode:
        print("TEST RUN COMPLETE - REVIEW MOCKUPS BEFORE CONTINUING")
        print(f"{'='*70}")
        print(f"✅ Successful: {successful}/{test_count}")
        print(f"❌ Failed: {failed}")
        print(f"\n📁 Mockups location: {MOCKUPS_OUTPUT_DIR}")
        print(f"\nPLEASE REVIEW THE MOCKUPS:")
        print(f"  - Check that white mat border looks good (8% of artwork width)")
        print(f"  - Check that black frame looks professional")
        print(f"  - If you have template images, place them in: {MOCKUP_TEMPLATES_DIR}")
        print(f"    Template names: living_room.jpg, gallery.jpg, bedroom.jpg, office.jpg, modern.jpg")
        print(f"\nIf mockups look good:")
        print(f"  1. Edit line 246: Change test_mode = False")
        print(f"  2. Re-run script to process all {len(sku_dirs)} SKUs")
    else:
        print("PROCESSING COMPLETE")
        print(f"{'='*70}")
        print(f"✅ Successful: {successful}/{len(sku_dirs)}")
        print(f"❌ Failed: {failed}")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
