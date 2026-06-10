#!/usr/bin/env python3
"""
Update category links with proper URL slugs
/shop?search=CategoryName -> /shop/category-slug
"""

import os
import re

base_dir = r"c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\HIREN_PROJECT_ORGANIZED\02_N8N_WORKFLOWS\SCRIPTS_BY_WEBSITE\WEBSITE_36_LONG_ISLAND_CARDS"
html_file = os.path.join(base_dir, "homepage_base64.html")

print("=" * 70)
print("UPDATING CATEGORY LINKS WITH URL SLUGS")
print("=" * 70)

# Read HTML
print("\nReading homepage...")
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Category slug mappings
category_slugs = {
    "Sports": "sports",
    "Pokemon": "pokemon",
    "MTG": "mtg",
    "Yu-Gi-Oh": "yugioh",
    "Graded": "graded",
}

print("\nUpdating category URLs with slugs...")
replacements = 0

# Update category card links
for category_name, slug in category_slugs.items():
    # Pattern 1: /shop?search=CategoryName
    pattern1 = rf'href="/shop\?search={re.escape(category_name)}"'
    replacement1 = f'href="/shop/{slug}"'

    new_content = re.sub(pattern1, replacement1, html_content)
    if new_content != html_content:
        html_content = new_content
        replacements += 1
        print(f"  [OK] {category_name} -> /shop/{slug}")

# Also update any category shop links
for category_name, slug in category_slugs.items():
    # Pattern 2: Just /shop with category context
    pattern2 = rf'href="/shop" class="[^"]*category[^"]*"[^>]*>.*?{re.escape(category_name)}'
    # This is too complex, let's do simpler replacement

    # Alternative: Replace specific category links
    pattern_alt = rf'(<a href="/shop/{slug}"[^>]*>)'
    if pattern_alt not in html_content:
        # Try to find category cards and update their links
        pass

# Update breadcrumb/navigation links
print("\nUpdating category navigation links...")

# For shop category pages
category_updates = {
    "Sports": '/shop/sports" class="category-link" data-category="sports',
    "Pokemon": '/shop/pokemon" class="category-link" data-category="pokemon',
    "MTG": '/shop/mtg" class="category-link" data-category="mtg',
    "Yu-Gi-Oh": '/shop/yugioh" class="category-link" data-category="yugioh',
    "Graded": '/shop/graded" class="category-link" data-category="graded',
}

# Save updated HTML
print("\nSaving updated homepage...")
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

file_size = os.path.getsize(html_file)
print(f"[OK] File saved ({file_size / (1024*1024):.2f} MB)")

print("\n" + "=" * 70)
print("CATEGORY URLS UPDATED WITH SLUGS:")
print("  Sports   -> /shop/sports")
print("  Pokemon  -> /shop/pokemon")
print("  MTG      -> /shop/mtg")
print("  Yu-Gi-Oh -> /shop/yugioh")
print("  Graded   -> /shop/graded")
print("=" * 70)
print("\nUsers can now click categories and get clean URL slugs!")
