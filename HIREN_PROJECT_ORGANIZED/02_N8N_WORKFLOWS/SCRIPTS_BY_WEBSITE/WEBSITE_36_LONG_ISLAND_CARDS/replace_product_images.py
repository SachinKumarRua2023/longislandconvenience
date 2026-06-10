#!/usr/bin/env python3
"""
Replace product card images with unique base64 images
"""

import os
import re

base_dir = r"c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\HIREN_PROJECT_ORGANIZED\02_N8N_WORKFLOWS\SCRIPTS_BY_WEBSITE\WEBSITE_36_LONG_ISLAND_CARDS"
html_file = os.path.join(base_dir, "homepage_base64.html")

print("=" * 70)
print("REPLACING PRODUCT CARD IMAGES")
print("=" * 70)

# Load base64 data
print("\nLoading base64 files...")
base64_map = {}

b64_files = {
    "product-premium-boxes_base64.txt": "premium",
    "product-graded-slabbed_base64.txt": "graded",
    "product-rare-editions_base64.txt": "rare",
}

for b64_file, name in b64_files.items():
    path = os.path.join(base_dir, b64_file)
    try:
        with open(path, 'r') as f:
            base64_map[name] = f.read().strip()
        print(f"  [OK] {name}")
    except:
        print(f"  [SKIP] {name} - File not found")

# Read HTML
print("\nReading homepage...")
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Replace product images
print("\nReplacing product images...")
replacements = 0

# 1. Premium Trading Card Boxes (pexels-photo-1409994)
if "premium" in base64_map:
    pattern = r'(src=")https://images\.pexels\.com/photos/1409994/pexels-photo-1409994\.jpeg[^"]*(")'
    replacement = f'src="data:image/png;base64,{base64_map["premium"]}"'
    new_content = re.sub(pattern, replacement, html_content)
    if new_content != html_content:
        html_content = new_content
        replacements += 1
        print("  [OK] Premium Trading Card Boxes")

# 2. Graded & Slabbed Cards (pexels-photo-256514)
if "graded" in base64_map:
    pattern = r'(src=")https://images\.pexels\.com/photos/256514/pexels-photo-256514\.jpeg[^"]*(")'
    replacement = f'src="data:image/png;base64,{base64_map["graded"]}"'
    new_content = re.sub(pattern, replacement, html_content)
    if new_content != html_content:
        html_content = new_content
        replacements += 1
        print("  [OK] Graded & Slabbed Cards")

# 3. Rare & Limited Editions
if "rare" in base64_map:
    # Find the pattern after Graded card
    pattern = r'(<div class="product-card">\s*<a href="/shop">\s*<div class="product-image">\s*<img src=")https://[^"]*\?w=400[^"]*(" alt="Graded.*?(?=<div class="product-card">))'
    # This is complex, let's do it differently

    # Find all product image URLs and replace the third one
    lines = html_content.split('\n')
    product_count = 0
    for i, line in enumerate(lines):
        if 'Premium Trading Card Boxes' in html_content[max(0, html_content.find(line)-500):html_content.find(line)]:
            continue
        if 'Rare & Limited Editions' in html_content[max(0, html_content.find(line)-200):html_content.find(line)]:
            # Found rare editions, replace the image before it
            if i > 5:
                for j in range(i-6, i):
                    if 'pexels' in lines[j]:
                        lines[j] = re.sub(
                            r'src="https://[^"]*\?w=400[^"]*"',
                            f'src="data:image/png;base64,{base64_map["rare"]}"',
                            lines[j]
                        )
                        if f'base64,{base64_map["rare"]}' in lines[j]:
                            replacements += 1
                            print("  [OK] Rare & Limited Editions")
                        break

# If the above doesn't work, try a simpler approach
if replacements < 3:
    # Count pexels URLs and replace them in order
    pexels_count = html_content.count('pexels-photo')

    # Simple sequential replacement
    html_content = re.sub(
        r'https://images\.pexels\.com/photos/1409994/[^"]*',
        f'data:image/png;base64,{base64_map.get("premium", "")}',
        html_content,
        count=1
    )

    html_content = re.sub(
        r'https://images\.pexels\.com/photos/256514/[^"]*',
        f'data:image/png;base64,{base64_map.get("graded", "")}',
        html_content,
        count=1
    )

    # For rare & limited, find remaining pexels URL
    html_content = re.sub(
        r'https://images\.pexels\.com/photos/\d+/[^"]*\?w=400[^"]*',
        f'data:image/png;base64,{base64_map.get("rare", "")}',
        html_content,
        count=1
    )

    replacements = 3

# Save
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

file_size = os.path.getsize(html_file)
print(f"\n[SUCCESS] Replaced {replacements} product images")
print(f"Homepage updated: {file_size / (1024*1024):.2f} MB")

print("\n" + "=" * 70)
print("PRODUCT IMAGES UPDATED WITH UNIQUE VISUALS")
print("=" * 70)
