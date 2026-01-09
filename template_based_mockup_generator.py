#!/usr/bin/env python3
"""
TEMPLATE-BASED MOCKUP GENERATOR
- Uses your professional mockup templates with perfect placement
- Detects artwork position in each template
- Replaces template artwork with YOUR Death NYC artwork
- Maintains perfect centering and spacing from templates
"""

import os
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
MOCKUPS_OUTPUT_DIR = Path("/Users/johnshay/Desktop/professional_mockups")
TEMPLATES_DIR = Path("/Users/johnshay/Desktop/mockup_templates")

# Mockup columns in Google Sheets (AF, AG, AH, AI, AJ, AK, AL)
MOCKUP_COLUMNS = ['AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL']

# Manual configuration based on visual analysis of templates
# Format: {x_center: 0-1, y_center: 0-1, width: 0-1, height: 0-1}
TEMPLATE_ARTWORK_POSITIONS = {
    'template_1.png': {
        'name': 'Desk_Office',
        'position': {'x': 0.35, 'y': 0.20, 'width': 0.22, 'height': 0.28},
        'description': 'Artwork above desk with lamp and turntable'
    },
    'template_2.png': {
        'name': 'Entryway_Bench',
        'position': {'x': 0.50, 'y': 0.35, 'width': 0.20, 'height': 0.30},
        'description': 'Artwork centered above wooden bench'
    },
    'template_3.png': {
        'name': 'Floor_Lean',
        'position': {'x': 0.30, 'y': 0.35, 'width': 0.35, 'height': 0.50},
        'description': 'Large artwork leaning against wall'
    },
    'template_4.png': {
        'name': 'Living_Room_Sofa',
        'position': {'x': 0.32, 'y': 0.22, 'width': 0.28, 'height': 0.32},
        'description': 'Artwork above tan leather couch'
    },
    'template_5.png': {
        'name': 'Rustic_Guitar',
        'position': {'x': 0.30, 'y': 0.35, 'width': 0.20, 'height': 0.25},
        'description': 'Black framed artwork on textured wall'
    },
    'template_6.png': {
        'name': 'Bedroom_Credenza',
        'position': {'x': 0.42, 'y': 0.22, 'width': 0.25, 'height': 0.28},
        'description': 'Artwork above bedroom credenza'
    },
    'template_7.png': {
        'name': 'Modern_Living',
        'position': {'x': 0.35, 'y': 0.28, 'width': 0.22, 'height': 0.26},
        'description': 'Artwork on white wall with mustard chair'
    }
}

def get_drive_service():
    token_path = Path("/Users/johnshay/3DSELLERS/token.pickle")
    if token_path.exists():
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    else:
        raise FileNotFoundError(f"token.pickle not found at {token_path}")
    return build('drive', 'v3', credentials=creds)

def get_sheets_service():
    token_path = Path("/Users/johnshay/3DSELLERS/token.pickle")
    if token_path.exists():
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    else:
        raise FileNotFoundError(f"token.pickle not found at {token_path}")
    return build('sheets', 'v4', credentials=creds)

def add_mat_and_frame(artwork_image, mat_width_pct=0.08, frame_width_px=20):
    """
    Add white mat border and black frame around artwork

    Args:
        artwork_image: PIL Image (RGBA, background removed)
        mat_width_pct: Mat width as % of artwork width (default 8%)
        frame_width_px: Frame width in pixels (default 20px)

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

def composite_artwork_on_template(artwork_crop, template_path, template_filename):
    """
    Replace template artwork with user's actual artwork

    Args:
        artwork_crop: Path to artwork crop (PNG with transparent background)
        template_path: Path to mockup template
        template_filename: Filename of template (to look up position)

    Returns:
        PIL Image of final mockup
    """
    # Load template
    template = Image.open(template_path).convert('RGB')
    template_width, template_height = template.size

    # Load artwork
    artwork = Image.open(artwork_crop).convert('RGBA')

    # Get position config for this template
    config = TEMPLATE_ARTWORK_POSITIONS.get(template_filename)
    if not config:
        print(f"  ⚠️  No position config for template: {template_filename}")
        return template

    pos = config['position']

    # Calculate target artwork area (leaving room for mat and frame)
    target_width = int(template_width * pos['width'])
    target_height = int(template_height * pos['height'])
    center_x = int(template_width * pos['x'])
    center_y = int(template_height * pos['y'])

    # Resize artwork to fit target area (preserve aspect ratio)
    # Account for mat and frame that will be added
    max_art_width = int(target_width * 0.7)  # Artwork is 70% of target (rest is mat+frame)
    max_art_height = int(target_height * 0.7)

    artwork_copy = artwork.copy()
    artwork_copy.thumbnail((max_art_width, max_art_height), Image.Resampling.LANCZOS)

    # Add white mat and black frame
    framed_artwork = add_mat_and_frame(artwork_copy, mat_width_pct=0.08, frame_width_px=20)

    # Calculate paste position (centered at target point)
    paste_x = center_x - (framed_artwork.width // 2)
    paste_y = center_y - (framed_artwork.height // 2)

    # Create result by compositing framed artwork onto template
    result = template.copy()
    result.paste(framed_artwork, (paste_x, paste_y))

    return result

def generate_mockups_for_sku(sku_dir):
    """
    Generate mockups for all templates using SKU's main crop

    Args:
        sku_dir: Path to SKU directory (e.g., processed_crops/10/)

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

    print(f"  Using artwork: {crop_1_path.name}")
    artwork = Image.open(crop_1_path)
    print(f"  Artwork size: {artwork.size}")

    # Create output directory
    output_dir = MOCKUPS_OUTPUT_DIR / sku
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate mockup for each template
    mockup_files = []

    for template_file in sorted(TEMPLATES_DIR.glob("*.png")):
        template_filename = template_file.name
        config = TEMPLATE_ARTWORK_POSITIONS.get(template_filename)

        if not config:
            print(f"  ⚠️  Skipping unknown template: {template_filename}")
            continue

        print(f"\n  Creating: {config['name']}")
        print(f"    {config['description']}")

        try:
            mockup = composite_artwork_on_template(
                crop_1_path,
                template_file,
                template_filename
            )

            # Save mockup
            output_filename = f"{sku}_mockup_{config['name'].lower().replace(' ', '_').replace('/', '_')}.jpg"
            output_path = output_dir / output_filename

            mockup.save(output_path, 'JPEG', quality=95)
            mockup_files.append(output_path)

            print(f"    ✅ Saved: {output_filename}")

        except Exception as e:
            print(f"    ❌ Error: {e}")
            import traceback
            traceback.print_exc()

    print(f"\n  ✅ Generated {len(mockup_files)} mockups total")
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
    print("TEMPLATE-BASED MOCKUP GENERATOR")
    print("Professional placement • Your actual artwork")
    print(f"{'='*70}\n")

    MOCKUPS_OUTPUT_DIR.mkdir(exist_ok=True)

    # Check for templates
    if not TEMPLATES_DIR.exists() or not list(TEMPLATES_DIR.glob("*.png")):
        print(f"❌ No mockup templates found in {TEMPLATES_DIR}")
        return

    templates = list(TEMPLATES_DIR.glob("*.png"))
    print(f"Found {len(templates)} mockup templates:\n")
    for template in templates:
        config = TEMPLATE_ARTWORK_POSITIONS.get(template.name)
        if config:
            print(f"  ✅ {config['name']}")
            print(f"     {config['description']}")
        else:
            print(f"  ⚠️  {template.name} (no position config)")
    print()

    # Test mode - process 2 SKUs first
    test_mode = True

    # Check for crops
    if not CROPS_INPUT_DIR.exists():
        print(f"❌ Crops directory not found: {CROPS_INPUT_DIR}")
        print(f"   Please run CROP_WITH_PHOTOROOM_BG_REMOVAL.py first")
        return

    # Only process numeric SKU directories (not old directories with long names)
    sku_dirs = sorted([d for d in CROPS_INPUT_DIR.glob("*") if d.is_dir() and d.name.isdigit()])

    if not sku_dirs:
        print(f"❌ No SKU directories found in {CROPS_INPUT_DIR}")
        return

    print(f"Found {len(sku_dirs)} SKU directories (numeric SKUs only)\n")

    test_count = 2 if test_mode else len(sku_dirs)

    if test_mode:
        print(f"🔴 TEST MODE: Processing first {test_count} SKUs\n")
        print("Authenticating with Google...")
        drive_service = get_drive_service()
        sheets_service = get_sheets_service()
        print("✅ Authenticated\n")
    else:
        print("Authenticating with Google...")
        drive_service = get_drive_service()
        sheets_service = get_sheets_service()
        print("✅ Authenticated\n")

    successful = 0
    failed = 0

    for idx, sku_dir in enumerate(sku_dirs[:test_count], 1):
        sku = sku_dir.name
        print(f"\n[{idx}/{test_count}] Processing SKU: {sku}")

        try:
            # Generate mockups
            mockup_files = generate_mockups_for_sku(sku_dir)

            if not mockup_files:
                print(f"  ❌ No mockups generated")
                failed += 1
                continue

            # Upload to Google Drive
            print(f"\n  Uploading {len(mockup_files)} mockups to Google Drive...")
            mockup_links = []

            for i, mockup_path in enumerate(mockup_files, 1):
                print(f"    [{i}/{len(mockup_files)}] Uploading {mockup_path.name}...")
                link = upload_file_to_drive(drive_service, mockup_path, DEATH_NYC_ART_FOLDER_ID)

                if link:
                    mockup_links.append(link)
                    print(f"      ✅ Uploaded")
                else:
                    mockup_links.append("")

                time.sleep(0.5)

            # Update Google Sheets
            print(f"\n  Updating Google Sheets...")
            if update_sheet_with_mockups(sheets_service, sku, mockup_links):
                print(f"  ✅ Sheet updated with {len(mockup_links)} mockup links")
                successful += 1
            else:
                failed += 1

        except Exception as e:
            print(f"\n  ❌ Error: {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    print(f"\n\n{'='*70}")
    if test_mode:
        print("TEST RUN COMPLETE - REVIEW MOCKUPS")
        print(f"{'='*70}")
        print(f"✅ Successful: {successful}/{test_count}")
        print(f"❌ Failed: {failed}")
        print(f"\n📁 Mockups: {MOCKUPS_OUTPUT_DIR}")
        print(f"\nREVIEW THE MOCKUPS:")
        print(f"  • Check artwork is properly positioned")
        print(f"  • Verify no overlap with furniture")
        print(f"  • Confirm artwork looks natural in each scene")
        print(f"\nIf mockups look good:")
        print(f"  1. Edit line 210: Change test_mode = False")
        print(f"  2. Re-run to process all {len(sku_dirs)} SKUs")
    else:
        print("PROCESSING COMPLETE")
        print(f"{'='*70}")
        print(f"✅ Successful: {successful}/{len(sku_dirs)}")
        print(f"❌ Failed: {failed}")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
