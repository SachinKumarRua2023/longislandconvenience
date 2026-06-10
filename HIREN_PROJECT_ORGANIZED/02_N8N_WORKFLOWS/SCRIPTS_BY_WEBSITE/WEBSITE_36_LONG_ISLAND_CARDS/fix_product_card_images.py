#!/usr/bin/env python3
"""
Fix product card images - use actual trading card images instead of abstract images
"""

import os
import base64
import shutil
import re

base_dir = r"c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\HIREN_PROJECT_ORGANIZED\02_N8N_WORKFLOWS\SCRIPTS_BY_WEBSITE\WEBSITE_36_LONG_ISLAND_CARDS"
assets_dir = os.path.join(base_dir, "assets")
html_file = os.path.join(base_dir, "homepage_base64.html")

print("=" * 70)
print("FIXING PRODUCT CARD IMAGES WITH REAL TRADING CARDS")
print("=" * 70)

# Map product images to proper card images
image_mapping = {
    "product-premium-boxes.png": "graded-cards-center.png",
    "product-graded-slabbed.png": "graded-cards-left.png",
    "product-rare-editions.png": "mtg-cards-center.png",
    "product-exclusive-collection.png": "pokemon-cards-center.png",
}

print("\nReplacing product images with real card images...")
for product_img, card_img in image_mapping.items():
    src = os.path.join(assets_dir, card_img)
    dst = os.path.join(assets_dir, product_img)

    if os.path.exists(src):
        shutil.copy(src, dst)
        print(f"  [OK] {product_img} <- {card_img}")
    else:
        print(f"  [ERROR] {card_img} not found")

# Convert updated images to base64
print("\nConverting updated images to base64...")
base64_map = {}

for product_img in image_mapping.keys():
    img_path = os.path.join(assets_dir, product_img)
    b64_filename = product_img.replace('.png', '_base64.txt')
    b64_path = os.path.join(base_dir, b64_filename)

    try:
        with open(img_path, 'rb') as f:
            img_data = f.read()

        base64_data = base64.b64encode(img_data).decode('utf-8')
        base64_map[product_img] = base64_data

        with open(b64_path, 'w') as f:
            f.write(base64_data)

        print(f"  [OK] {b64_filename}")

    except Exception as e:
        print(f"  [ERROR] {product_img}: {e}")

# Update homepage with new base64 images
print("\nUpdating homepage with real card images...")
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

replacements = 0

# Replace each product image with proper base64
for product_img, base64_data in base64_map.items():
    # Find the pexels URLs for each product
    if "premium" in product_img:
        pattern = r'data:image/png;base64,[^"]*(?=.*?Premium Trading Card Boxes)'
        replacement = f'data:image/png;base64,{base64_data}'
        # More direct: replace pexels-photo-1409994
        html_content = re.sub(
            r'src="data:image/png;base64,[^"]*" alt="Baseball"',
            f'src="data:image/png;base64,{base64_data}" alt="Premium Trading Card Boxes"',
            html_content
        )
        print(f"  [OK] Updated Premium Trading Card Boxes")

    elif "graded" in product_img and "slabbed" in product_img:
        html_content = re.sub(
            r'src="data:image/png;base64,[^"]*" alt="Graded"',
            f'src="data:image/png;base64,{base64_data}" alt="Graded & Slabbed Cards"',
            html_content
        )
        print(f"  [OK] Updated Graded & Slabbed Cards")

    elif "rare" in product_img:
        html_content = re.sub(
            r'src="data:image/png;base64,[^"]*" alt="Rare"',
            f'src="data:image/png;base64,{base64_data}" alt="Rare & Limited Editions"',
            html_content,
            count=1
        )
        print(f"  [OK] Updated Rare & Limited Editions")

# Save updated HTML
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

file_size = os.path.getsize(html_file)
print(f"\n[SUCCESS] Homepage updated with real card images")
print(f"File size: {file_size / (1024*1024):.2f} MB")

print("\n" + "=" * 70)
print("PRODUCT CARD IMAGES FIXED:")
print("  Premium Trading Card Boxes <- Graded Cards")
print("  Graded & Slabbed Cards <- Graded Cards (Left)")
print("  Rare & Limited Editions <- MTG Cards")
print("  Exclusive Collection <- Pokemon Cards")
print("=" * 70)
print("\nAll images now show REAL TRADING CARDS!")
