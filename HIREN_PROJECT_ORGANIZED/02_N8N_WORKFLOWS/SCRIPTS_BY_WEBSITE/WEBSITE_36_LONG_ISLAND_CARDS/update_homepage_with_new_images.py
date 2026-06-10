#!/usr/bin/env python3
"""
Update the homepage_base64.html with new base64 images
- Replaces existing card images with new real card images
- Adds bulk-dragon-collection to the hero section
"""

import os
import re

base_dir = r"c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\HIREN_PROJECT_ORGANIZED\02_N8N_WORKFLOWS\SCRIPTS_BY_WEBSITE\WEBSITE_36_LONG_ISLAND_CARDS"

# Read all base64 files
print("=" * 70)
print("UPDATING HOMEPAGE WITH NEW IMAGES")
print("=" * 70)

base64_map = {}
b64_files = [
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

print("\nLoading base64 files...")
for b64_file in b64_files:
    path = os.path.join(base_dir, b64_file)
    try:
        with open(path, 'r') as f:
            base64_map[b64_file] = f.read().strip()
        print(f"  [OK] {b64_file}")
    except Exception as e:
        print(f"  [ERROR] {b64_file}: {e}")

# Read homepage
print("\nReading homepage_base64.html...")
html_file = os.path.join(base_dir, "homepage_base64.html")
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()
print(f"  [OK] Loaded ({len(html_content)} chars)")

# Replace all image URLs with base64
print("\nReplacing images with base64 data...")
replacements = 0

# Mapping of cards to their base64
card_mappings = {
    "sports-cards-left.png": base64_map.get("sports-cards-left_base64.txt"),
    "sports-cards-center.png": base64_map.get("sports-cards-center_base64.txt"),
    "sports-cards-right.png": base64_map.get("sports-cards-right_base64.txt"),
    "pokemon-cards-left.png": base64_map.get("pokemon-cards-left_base64.txt"),
    "pokemon-cards-center.png": base64_map.get("pokemon-cards-center_base64.txt"),
    "pokemon-cards-right.png": base64_map.get("pokemon-cards-right_base64.txt"),
    "mtg-cards-left.png": base64_map.get("mtg-cards-left_base64.txt"),
    "mtg-cards-center.png": base64_map.get("mtg-cards-center_base64.txt"),
    "mtg-cards-right.png": base64_map.get("mtg-cards-right_base64.txt"),
    "yugioh-cards-left.png": base64_map.get("yugioh-cards-left_base64.txt"),
    "yugioh-cards-center.png": base64_map.get("yugioh-cards-center_base64.txt"),
    "yugioh-cards-right.png": base64_map.get("yugioh-cards-right_base64.txt"),
    "graded-cards-left.png": base64_map.get("graded-cards-left_base64.txt"),
    "graded-cards-center.png": base64_map.get("graded-cards-center_base64.txt"),
    "graded-cards-right.png": base64_map.get("graded-cards-right_base64.txt"),
}

for filename, base64_data in card_mappings.items():
    if not base64_data:
        print(f"  [SKIP] {filename} - No base64 data")
        continue

    # Replace all image paths with base64
    pattern = rf'/web/image/\d+/{re.escape(filename)}'
    base64_url = f'data:image/png;base64,{base64_data}'

    new_content = re.sub(pattern, base64_url, html_content)
    if new_content != html_content:
        replacements += 1
        html_content = new_content
        print(f"  [OK] {filename}")
    else:
        print(f"  [SKIP] {filename} - No match found")

# Add bulk-dragon-collection to hero section
print("\nAdding bulk-dragon-collection to hero section...")
bulk_dragon_b64 = base64_map.get("bulk-dragon-collection_base64.txt")
if bulk_dragon_b64:
    # Find and replace the hero image
    hero_pattern = r'<div class="hero-image">.*?</div>'
    hero_replacement = f'''<div class="hero-image">
        <img src="data:image/png;base64,{bulk_dragon_b64}" alt="Bulk Dragon Collection" style="max-width: 100%; height: auto; object-fit: cover;">
    </div>'''

    new_content = re.sub(hero_pattern, hero_replacement, html_content, flags=re.DOTALL)
    if new_content != html_content:
        html_content = new_content
        print("  [OK] Hero image updated with bulk-dragon-collection")
        replacements += 1
    else:
        print("  [SKIP] Hero section - Pattern not found")
else:
    print("  [ERROR] bulk-dragon-collection base64 data not available")

print(f"\n[SUCCESS] Made {replacements} replacements")

# Save updated HTML
print("\nSaving updated homepage_base64.html...")
output_file = os.path.join(base_dir, "homepage_base64.html")
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

file_size = os.path.getsize(output_file)
print(f"  [OK] Saved ({file_size} bytes)")

print("\n" + "=" * 70)
print("UPDATE COMPLETE!")
print("=" * 70)
print("\nThe homepage is ready to deploy to Odoo.")
print("Run: python deploy_homepage_odoo.py")
print("\n")
