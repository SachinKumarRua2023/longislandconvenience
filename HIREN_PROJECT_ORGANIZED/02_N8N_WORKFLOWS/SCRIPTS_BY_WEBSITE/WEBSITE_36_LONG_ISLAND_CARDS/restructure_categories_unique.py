#!/usr/bin/env python3
"""
Restructure category cards to show ONE unique image per category (no duplicates)
Instead of: Sports (left/center/right), Pokemon (left/center/right), etc.
Use: Sports (unique), Pokemon (unique), MTG (unique), Yu-Gi-Oh (unique), Graded (unique)
"""

import os
import re

base_dir = r"c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\HIREN_PROJECT_ORGANIZED\02_N8N_WORKFLOWS\SCRIPTS_BY_WEBSITE\WEBSITE_36_LONG_ISLAND_CARDS"
html_file = os.path.join(base_dir, "homepage_base64.html")

print("=" * 70)
print("RESTRUCTURING CATEGORIES WITH UNIQUE IMAGES (NO DUPLICATES)")
print("=" * 70)

# Read the base64 file to get the images
base64_map = {}
category_images = {
    "sports-cards-center": "sports-cards-center_base64.txt",
    "pokemon-cards-center": "pokemon-cards-center_base64.txt",
    "mtg-cards-center": "mtg-cards-center_base64.txt",
    "yugioh-cards-center": "yugioh-cards-center_base64.txt",
    "graded-cards-center": "graded-cards-center_base64.txt",
}

print("\nLoading base64 images...")
for name, filename in category_images.items():
    path = os.path.join(base_dir, filename)
    try:
        with open(path, 'r') as f:
            base64_map[name] = f.read().strip()
        print(f"  [OK] {name}")
    except Exception as e:
        print(f"  [ERROR] {name}: {e}")

# Read HTML
print("\nReading homepage...")
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Find the categories section
print("\nRestructuring categories section...")

# Create new category structure - 5 unique images instead of 15
new_categories = '''<!-- CATEGORIES -->
<section class="categories">
    <h2 class="section-title">Popular Categories</h2>
    <div class="category-grid">
        <!-- SPORTS CARDS - UNIQUE -->
        <div class="category-card">
            <a href="/shop?search=Sports">
                <div class="category-stage">
                    <div class="category-glow"></div>
                    <div class="category-image cat-center" style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
                        <img src="data:image/png;base64,{sports}" alt="Sports Cards" style="max-width: 90%; height: auto; object-fit: contain;">
                    </div>
                </div>
                <h3>Sports Cards</h3>
                <p>Baseball, Basketball & Football</p>
            </a>
        </div>

        <!-- POKEMON CARDS - UNIQUE -->
        <div class="category-card">
            <a href="/shop?search=Pokemon">
                <div class="category-stage">
                    <div class="category-glow"></div>
                    <div class="category-image cat-center" style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
                        <img src="data:image/png;base64,{pokemon}" alt="Pokemon Cards" style="max-width: 90%; height: auto; object-fit: contain;">
                    </div>
                </div>
                <h3>Pokemon Cards</h3>
                <p>Booster Packs & Sealed Sets</p>
            </a>
        </div>

        <!-- MTG CARDS - UNIQUE -->
        <div class="category-card">
            <a href="/shop?search=MTG">
                <div class="category-stage">
                    <div class="category-glow"></div>
                    <div class="category-image cat-center" style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
                        <img src="data:image/png;base64,{mtg}" alt="Magic: MTG" style="max-width: 90%; height: auto; object-fit: contain;">
                    </div>
                </div>
                <h3>Magic: MTG</h3>
                <p>The Gathering Cards & Sets</p>
            </a>
        </div>

        <!-- YU-GI-OH CARDS - UNIQUE -->
        <div class="category-card">
            <a href="/shop?search=Yu-Gi-Oh">
                <div class="category-stage">
                    <div class="category-glow"></div>
                    <div class="category-image cat-center" style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
                        <img src="data:image/png;base64,{yugioh}" alt="Yu-Gi-Oh Cards" style="max-width: 90%; height: auto; object-fit: contain;">
                    </div>
                </div>
                <h3>Yu-Gi-Oh!</h3>
                <p>Trading Card Game</p>
            </a>
        </div>

        <!-- GRADED CARDS - UNIQUE -->
        <div class="category-card">
            <a href="/shop?search=Graded">
                <div class="category-stage">
                    <div class="category-glow"></div>
                    <div class="category-image cat-center" style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
                        <img src="data:image/png;base64,{graded}" alt="Graded Cards" style="max-width: 90%; height: auto; object-fit: contain;">
                    </div>
                </div>
                <h3>Graded Cards</h3>
                <p>PSA & CGC Certified</p>
            </a>
        </div>
    </div>
</section>'''

# Replace base64 placeholders
new_categories = new_categories.format(
    sports=base64_map.get('sports-cards-center', ''),
    pokemon=base64_map.get('pokemon-cards-center', ''),
    mtg=base64_map.get('mtg-cards-center', ''),
    yugioh=base64_map.get('yugioh-cards-center', ''),
    graded=base64_map.get('graded-cards-center', '')
)

# Find and replace the categories section
pattern = r'<!-- CATEGORIES -->.*?</section>\s*(?=<!-- EXPLORE MORE|<!-- SPECIAL|<section class="special)'
replacement = new_categories

html_content = re.sub(pattern, replacement, html_content, flags=re.DOTALL)

# Save updated HTML
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

file_size = os.path.getsize(html_file)
print(f"\n[SUCCESS] Categories restructured with UNIQUE images only")
print(f"File size: {file_size / (1024*1024):.2f} MB")

print("\n" + "=" * 70)
print("CATEGORY STRUCTURE CHANGED:")
print("  OLD: 15 images (5 categories x 3 duplicates each)")
print("  NEW: 5 unique images (1 per category)")
print("=" * 70)
print("\nWhen users click categories, they'll see UNIQUE images!")
