#!/usr/bin/env python3
"""
Fix hero section to have Pokemon cards overlaid on top
- Pokemon cards should float over the hero section
- Not below it, but integrated into the hero display
"""

import os
import re

base_dir = r"c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\HIREN_PROJECT_ORGANIZED\02_N8N_WORKFLOWS\SCRIPTS_BY_WEBSITE\WEBSITE_36_LONG_ISLAND_CARDS"
html_file = os.path.join(base_dir, "homepage_base64.html")

print("=" * 70)
print("FIXING HERO SECTION - POKEMON CARDS OVERLAY")
print("=" * 70)

# Read HTML
print("\nReading homepage...")
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Load Pokemon card base64
print("\nLoading Pokemon card base64 files...")
pokemon_b64 = {}
pokemon_files = [
    "pokemon-ancient-solring_base64.txt",
    "pokemon-deoxys_base64.txt",
    "pokemon-dragon_base64.txt",
]

for img_file in pokemon_files:
    path = os.path.join(base_dir, img_file)
    if os.path.exists(path):
        with open(path, 'r') as f:
            pokemon_b64[img_file] = f.read().strip()
        print(f"  [OK] {img_file}")

# Create hero section with Pokemon cards overlay
hero_html = f'''<!-- HERO SECTION WITH POKEMON CARDS OVERLAY -->
<section class="hero" style="position: relative; overflow: visible;">
    <div class="hero-content">
        <h1>Trading Card Paradise</h1>
        <p>Explore premium collectibles from your favorite brands</p>
        <a href="/shop" class="hero-btn">Shop Now</a>
    </div>

    <!-- Pokemon Cards Overlay -->
    <div class="pokemon-cards-overlay" style="position: absolute; right: 60px; top: 50%; transform: translateY(-50%); display: flex; gap: 20px; align-items: center; z-index: 10;">
        <!-- Card 1 -->
        <div style="background: white; border-radius: 12px; padding: 10px; box-shadow: 0 8px 24px rgba(0,0,0,0.3); transform: perspective(1000px) rotateY(-15deg); max-width: 150px;">
            <img src="data:image/png;base64,{pokemon_b64.get('pokemon-ancient-solring_base64.txt', '')}" alt="Pokemon Card" style="width: 100%; height: auto; border-radius: 8px; display: block;">
        </div>

        <!-- Card 2 (Center - Highlighted) -->
        <div style="background: white; border-radius: 12px; padding: 10px; box-shadow: 0 12px 32px rgba(0,0,0,0.4); max-width: 160px; transform: scale(1.1);">
            <img src="data:image/png;base64,{pokemon_b64.get('pokemon-deoxys_base64.txt', '')}" alt="Pokemon Card" style="width: 100%; height: auto; border-radius: 8px; display: block;">
        </div>

        <!-- Card 3 -->
        <div style="background: white; border-radius: 12px; padding: 10px; box-shadow: 0 8px 24px rgba(0,0,0,0.3); transform: perspective(1000px) rotateY(15deg); max-width: 150px;">
            <img src="data:image/png;base64,{pokemon_b64.get('pokemon-dragon_base64.txt', '')}" alt="Pokemon Card" style="width: 100%; height: auto; border-radius: 8px; display: block;">
        </div>
    </div>
</section>
'''

# Find and replace hero section
hero_pattern = r'<!-- HERO SECTION.*?</section>'
html_content = re.sub(hero_pattern, hero_html, html_content, flags=re.DOTALL)

print("\nUpdating hero section...")
print("  [OK] Hero section updated with Pokemon card overlay")

# Remove duplicate Pokemon gallery that was added separately
print("\nRemoving duplicate Pokemon gallery section...")
pokemon_gallery_pattern = r'<!-- POKEMON CARDS SHOWCASE GALLERY -->.*?</style>\s*'
html_content = re.sub(pokemon_gallery_pattern, '', html_content, flags=re.DOTALL)
print("  [OK] Duplicate gallery removed")

# Save updated HTML
print("\nSaving updated homepage...")
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

file_size = os.path.getsize(html_file)
print(f"[OK] File saved ({file_size / (1024*1024):.2f} MB)")

print("\n" + "=" * 70)
print("HERO SECTION FIXED:")
print("=" * 70)
print("\nHero Section Structure:")
print("  • Title: 'Trading Card Paradise'")
print("  • Description text")
print("  • 'Shop Now' button")
print("  • OVERLAID: 3 Pokemon cards on right side")
print("    - Left card: Rotated perspective")
print("    - Center card: Highlighted (scaled up)")
print("    - Right card: Rotated perspective")
print("\nResult: Pokemon cards float over hero with 3D effect!")
print("=" * 70)
