#!/usr/bin/env python3
import os

# Read original HTML
html_file = r"c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\HIREN_PROJECT_ORGANIZED\02_N8N_WORKFLOWS\SCRIPTS_BY_WEBSITE\WEBSITE_36_LONG_ISLAND_CARDS\homepage_real_images.html"
base_dir = r"c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\HIREN_PROJECT_ORGANIZED\02_N8N_WORKFLOWS\SCRIPTS_BY_WEBSITE\WEBSITE_36_LONG_ISLAND_CARDS"

# Mapping of image filenames to base64 file paths
images = {
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
    "bulk-dragon-collection.png": "bulk-dragon-collection_base64.txt",
}

print("Reading base64 files...")
base64_map = {}
for filename, b64_file in images.items():
    path = os.path.join(base_dir, b64_file)
    try:
        with open(path, 'r') as f:
            base64_map[filename] = f.read().strip()
        print(f"[OK] {filename}")
    except Exception as e:
        print(f"[ERROR] {filename}: {e}")

print("\nReading HTML file...")
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

print("\nReplacing image URLs with base64...")
replacements = 0

for filename, base64_data in base64_map.items():
    old_url = f'/web/image/34015/{filename}' if 'sports-cards-left' in filename else f'/web/image/*/{filename}'
    # More flexible replacement - match any /web/image/.../{filename}
    import re
    pattern = rf'/web/image/\d+/{re.escape(filename)}'
    base64_url = f'data:image/png;base64,{base64_data}'
    
    # Replace all occurrences
    new_content = re.sub(pattern, base64_url, html_content)
    if new_content != html_content:
        replacements += 1
        html_content = new_content
        print(f"[OK] Replaced {filename}")

print(f"\n[SUCCESS] Made {replacements} replacements")

print("\nSaving updated HTML...")
output_file = os.path.join(base_dir, "homepage_base64.html")
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"[OK] Saved to: {output_file}")
print("\nFile ready to deploy to Odoo!")
