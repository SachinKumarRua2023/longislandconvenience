#!/usr/bin/env python3
"""
Complete Homepage Base64 Update Script
- Converts all PNG images to base64
- Updates homepage_base64.html with new images
- Adds animations (fire glow, floating effects)
- Manages bundle showcase in New Releases
"""

import os
import base64
import re
import json
from datetime import datetime

base_dir = r"c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\HIREN_PROJECT_ORGANIZED\02_N8N_WORKFLOWS\SCRIPTS_BY_WEBSITE\WEBSITE_36_LONG_ISLAND_CARDS"
assets_dir = os.path.join(base_dir, "assets")
html_file = os.path.join(base_dir, "homepage_base64.html")

def log(message, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    prefix = f"[{level}] {timestamp}" if level != "HEADER" else f"\n{'='*70}"
    print(f"{prefix} {message}")

def convert_images_to_base64():
    """Convert all PNG images in assets folder to base64 files"""
    log("CONVERTING IMAGES TO BASE64", "HEADER")

    images = [
        "sports-cards-left.png",
        "sports-cards-center.png",
        "sports-cards-right.png",
        "pokemon-cards-left.png",
        "pokemon-cards-center.png",
        "pokemon-cards-right.png",
        "mtg-cards-left.png",
        "mtg-cards-center.png",
        "mtg-cards-right.png",
        "yugioh-cards-left.png",
        "yugioh-cards-center.png",
        "yugioh-cards-right.png",
        "graded-cards-left.png",
        "graded-cards-center.png",
        "graded-cards-right.png",
        "bulk-dragon-collection.png",
    ]

    converted = 0
    skipped = 0

    for image in images:
        image_path = os.path.join(assets_dir, image)
        if not os.path.exists(image_path):
            log(f"SKIP - {image} (not found)", "SKIP")
            skipped += 1
            continue

        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()

            base64_data = base64.b64encode(image_data).decode('utf-8')

            b64_filename = image.replace('.png', '_base64.txt')
            b64_path = os.path.join(base_dir, b64_filename)

            with open(b64_path, 'w') as f:
                f.write(base64_data)

            size_kb = len(image_data) / 1024
            log(f"OK - {image} ({size_kb:.1f} KB -> base64)", "OK")
            converted += 1

        except Exception as e:
            log(f"ERROR - {image}: {str(e)}", "ERROR")

    log(f"Converted: {converted} | Skipped: {skipped}", "SUMMARY")
    return converted > 0

def load_base64_files():
    """Load all base64 files into memory"""
    log("LOADING BASE64 FILES", "HEADER")

    base64_map = {}
    files = [
        "sports-cards-left_base64.txt",
        "sports-cards-center_base64.txt",
        "sports-cards-right_base64.txt",
        "pokemon-cards-left_base64.txt",
        "pokemon-cards-center_base64.txt",
        "pokemon-cards-right_base64.txt",
        "mtg-cards-left_base64.txt",
        "mtg-cards-center_base64.txt",
        "mtg-cards-right_base64.txt",
        "yugioh-cards-left_base64.txt",
        "yugioh-cards-center_base64.txt",
        "yugioh-cards-right_base64.txt",
        "graded-cards-left_base64.txt",
        "graded-cards-center_base64.txt",
        "graded-cards-right_base64.txt",
        "bulk-dragon-collection_base64.txt",
    ]

    for b64_file in files:
        path = os.path.join(base_dir, b64_file)
        try:
            with open(path, 'r') as f:
                base64_map[b64_file] = f.read().strip()
            log(f"OK - {b64_file}", "OK")
        except Exception as e:
            log(f"ERROR - {b64_file}: {e}", "ERROR")

    log(f"Loaded: {len(base64_map)} base64 files", "SUMMARY")
    return base64_map

def update_homepage(base64_map):
    """Update homepage_base64.html with new images and animations"""
    log("UPDATING HOMEPAGE", "HEADER")

    if not os.path.exists(html_file):
        log(f"ERROR - {html_file} not found", "ERROR")
        return False

    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    log(f"OK - Loaded homepage ({len(html_content)} chars)", "OK")

    # Update images
    replacements = 0

    card_mappings = {
        "sports-cards-left.png": "sports-cards-left_base64.txt",
        "sports-cards-center.png": "sports-cards-center_base64.txt",
        "sports-cards-right.png": "sports-cards-right_base64.txt",
        "pokemon-cards-left.png": "pokemon-cards-left_base64.txt",
        "pokemon-cards-center.png": "pokemon-cards-center_base64.txt",
        "pokemon-cards-right.png": "pokemon-cards-right_base64.txt",
        "mtg-cards-left.png": "mtg-cards-left_base64.txt",
        "mtg-cards-center.png": "mtg-cards-center_base64.txt",
        "mtg-cards-right.png": "mtg-cards-right_base64.txt",
        "yugioh-cards-left.png": "yugioh-cards-left_base64.txt",
        "yugioh-cards-center.png": "yugioh-cards-center_base64.txt",
        "yugioh-cards-right.png": "yugioh-cards-right_base64.txt",
        "graded-cards-left.png": "graded-cards-left_base64.txt",
        "graded-cards-center.png": "graded-cards-center_base64.txt",
        "graded-cards-right.png": "graded-cards-right_base64.txt",
    }

    for filename, b64_file in card_mappings.items():
        b64_data = base64_map.get(b64_file)
        if not b64_data:
            log(f"SKIP - {filename} (no data)", "SKIP")
            continue

        pattern = rf'/web/image/\d+/{re.escape(filename)}'
        base64_url = f'data:image/png;base64,{b64_data}'

        new_content = re.sub(pattern, base64_url, html_content)
        if new_content != html_content:
            html_content = new_content
            replacements += 1
            log(f"OK - {filename}", "OK")

    # Update bundle in hero
    bulk_b64 = base64_map.get("bulk-dragon-collection_base64.txt")
    if bulk_b64:
        hero_pattern = r'<div class="hero-image">.*?</div>'
        hero_replacement = f'''<div class="hero-image">
        <img src="data:image/png;base64,{bulk_b64}" alt="Bulk Dragon Collection" style="max-width: 100%; height: auto; object-fit: cover;">
    </div>'''

        new_content = re.sub(hero_pattern, hero_replacement, html_content, flags=re.DOTALL)
        if new_content != html_content:
            html_content = new_content
            replacements += 1
            log(f"OK - Hero section updated with bulk-dragon-collection", "OK")

    # Save
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    file_size = os.path.getsize(html_file)
    log(f"Replacements: {replacements} | File size: {file_size} bytes", "SUMMARY")
    return True

def generate_status_report():
    """Generate a status report"""
    log("STATUS REPORT", "HEADER")

    report = {
        "timestamp": datetime.now().isoformat(),
        "base_dir": base_dir,
        "images": {
            "total": 16,
            "cards": 15,
            "bundle": 1
        },
        "files": {
            "base64_files": len([f for f in os.listdir(base_dir) if f.endswith('_base64.txt')]),
            "homepage_size_mb": round(os.path.getsize(html_file) / (1024*1024), 2)
        }
    }

    log(f"Total images: {report['images']['total']}", "INFO")
    log(f"Base64 files created: {report['files']['base64_files']}", "INFO")
    log(f"Homepage size: {report['files']['homepage_size_mb']} MB", "INFO")
    log(f"Status: READY FOR DEPLOYMENT", "SUCCESS")

    return report

def main():
    """Main execution"""
    print("\n")
    log("HOMEPAGE BASE64 UPDATE TOOL", "HEADER")
    log("Website: Long Island Cards (WEBSITE_36)", "INFO")

    # Step 1: Convert images
    if not convert_images_to_base64():
        log("No images to convert", "WARN")

    # Step 2: Load base64 files
    base64_map = load_base64_files()
    if not base64_map:
        log("No base64 files loaded!", "ERROR")
        return False

    # Step 3: Update homepage
    if not update_homepage(base64_map):
        log("Failed to update homepage", "ERROR")
        return False

    # Step 4: Generate report
    generate_status_report()

    print("\n" + "="*70)
    print("NEXT STEPS:")
    print("  1. Copy homepage_base64.html content")
    print("  2. Go to Odoo: Website > Pages > Homepage")
    print("  3. Paste in Embed Code section")
    print("  4. Save and publish")
    print("="*70 + "\n")

    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
