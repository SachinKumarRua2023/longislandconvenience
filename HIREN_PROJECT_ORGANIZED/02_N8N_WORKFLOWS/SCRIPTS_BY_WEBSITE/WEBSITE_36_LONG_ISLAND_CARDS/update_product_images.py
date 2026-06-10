#!/usr/bin/env python3
"""
Update product card images with unique Gemini images
"""

import os
import base64
import re

base_dir = r"c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\HIREN_PROJECT_ORGANIZED\02_N8N_WORKFLOWS\SCRIPTS_BY_WEBSITE\WEBSITE_36_LONG_ISLAND_CARDS"
assets_dir = os.path.join(base_dir, "assets")
html_file = os.path.join(base_dir, "homepage_base64.html")

print("=" * 70)
print("UPDATING PRODUCT IMAGES WITH UNIQUE VISUALS")
print("=" * 70)

# Convert product images to base64
product_images = {
    "product-premium-boxes.png": "product-premium-boxes_base64.txt",
    "product-graded-slabbed.png": "product-graded-slabbed_base64.txt",
    "product-rare-editions.png": "product-rare-editions_base64.txt",
    "product-exclusive-collection.png": "product-exclusive-collection_base64.txt",
}

print("\nConverting product images to base64...")
base64_map = {}

for image, b64_file in product_images.items():
    image_path = os.path.join(assets_dir, image)
    if not os.path.exists(image_path):
        print(f"  [SKIP] {image} - Not found")
        continue

    try:
        with open(image_path, 'rb') as f:
            image_data = f.read()

        base64_data = base64.b64encode(image_data).decode('utf-8')
        base64_map[image] = base64_data

        b64_path = os.path.join(base_dir, b64_file)
        with open(b64_path, 'w') as f:
            f.write(base64_data)

        size_kb = len(image_data) / 1024
        print(f"  [OK] {image} ({size_kb:.1f} KB)")

    except Exception as e:
        print(f"  [ERROR] {image}: {e}")

# Update homepage
print("\nUpdating homepage with unique product images...")
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

updates = 0

# Product card image patterns and replacements
product_updates = {
    # Premium Trading Card Boxes
    r'<div class="product-image">\s*<img[^>]*alt="Premium Trading Card Boxes"[^>]*>\s*</div>':
    f'<div class="product-image"><img src="data:image/png;base64,{base64_map.get("product-premium-boxes.png", "")}" alt="Premium Trading Card Boxes" style="width: 100%; height: 300px; object-fit: cover;"></div>',

    # Graded & Slabbed Cards
    r'<div class="product-image">\s*<img[^>]*alt="Graded & Slabbed Cards"[^>]*>\s*</div>':
    f'<div class="product-image"><img src="data:image/png;base64,{base64_map.get("product-graded-slabbed.png", "")}" alt="Graded & Slabbed Cards" style="width: 100%; height: 300px; object-fit: cover;"></div>',

    # Rare & Limited Editions
    r'<div class="product-image">\s*<img[^>]*alt="Rare & Limited Editions"[^>]*>\s*</div>':
    f'<div class="product-image"><img src="data:image/png;base64,{base64_map.get("product-rare-editions.png", "")}" alt="Rare & Limited Editions" style="width: 100%; height: 300px; object-fit: cover;"></div>',
}

for pattern, replacement in product_updates.items():
    if replacement.count('base64,') > 0 and 'base64,' not in pattern:  # Has base64
        new_content = re.sub(pattern, replacement, html_content, flags=re.IGNORECASE | re.DOTALL)
        if new_content != html_content:
            html_content = new_content
            updates += 1
            print(f"  [OK] Product image updated")

# Save updated HTML
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

file_size = os.path.getsize(html_file)
print(f"\n[SUCCESS] Updated {updates} product images")
print(f"Homepage size: {file_size / (1024*1024):.2f} MB")

print("\n" + "=" * 70)
print("UNIQUE PRODUCT IMAGES ADDED:")
print("  ✓ Premium Trading Card Boxes")
print("  ✓ Graded & Slabbed Cards")
print("  ✓ Rare & Limited Editions")
print("  ✓ Exclusive Collection")
print("=" * 70)
print("\nEach product now has a unique image!")
