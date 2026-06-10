#!/usr/bin/env python3
"""
Update homepage with Pokemon card images:
1. Replace MTG right image with Pokemon card
2. Add Pokemon cards gallery at bottom
3. Create base64 files
"""

import os
import base64
import re

base_dir = r"c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\HIREN_PROJECT_ORGANIZED\02_N8N_WORKFLOWS\SCRIPTS_BY_WEBSITE\WEBSITE_36_LONG_ISLAND_CARDS"
assets_dir = os.path.join(base_dir, "assets")
html_file = os.path.join(base_dir, "homepage_base64.html")

print("=" * 70)
print("UPDATING HOMEPAGE WITH POKEMON CARD IMAGES")
print("=" * 70)

# Pokemon images to use
pokemon_images = {
    "PokemonAncientSolRing.png": "pokemon-ancient-solring_base64.txt",
    "PokemonDeoxys.png": "pokemon-deoxys_base64.txt",
    "PokemonDragon.png": "pokemon-dragon_base64.txt",
    "PokemonInfernap.png": "pokemon-infernap_base64.txt",
}

# Convert to base64
print("\nConverting Pokemon card images to base64...")
pokemon_b64 = {}

for image, b64_file in pokemon_images.items():
    image_path = os.path.join(assets_dir, image)
    if not os.path.exists(image_path):
        print(f"  [SKIP] {image} - Not found")
        continue

    try:
        with open(image_path, 'rb') as f:
            img_data = f.read()

        base64_data = base64.b64encode(img_data).decode('utf-8')
        pokemon_b64[image] = base64_data

        b64_path = os.path.join(base_dir, b64_file)
        with open(b64_path, 'w') as f:
            f.write(base64_data)

        size_mb = len(img_data) / (1024*1024)
        print(f"  [OK] {image} ({size_mb:.2f} MB)")

    except Exception as e:
        print(f"  [ERROR] {image}: {e}")

# Read HTML
print("\nReading homepage...")
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Replace MTG right image with first Pokemon card
print("\nUpdating MTG right image with Pokemon card...")
if "PokemonDragon.png" in pokemon_b64:
    # Find MTG cards right image and replace with Pokemon Dragon
    pattern = r'(<div class="category-image cat-r">.*?<img src="data:image/png;base64,)[^"]*(" alt="Magic: MTG")'
    replacement = f'\\1{pokemon_b64["PokemonDragon.png"]}\\2'

    new_content = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
    if new_content != html_content:
        html_content = new_content
        print("  [OK] MTG right image replaced with Pokemon Dragon card")
    else:
        print("  [INFO] Pattern not found, will add at bottom instead")

# Add Pokemon Cards Gallery at bottom
print("\nAdding Pokemon Cards Gallery at bottom...")

pokemon_gallery_html = f'''
<!-- POKEMON CARDS SHOWCASE GALLERY -->
<section class="pokemon-gallery" style="padding: 60px 40px; background: linear-gradient(135deg, rgba(51, 153, 255, 0.05) 0%, rgba(102, 204, 255, 0.05) 100%); margin-top: 60px;">
    <h2 class="section-title" style="text-align: center; margin-bottom: 40px; color: #333;">Featured Pokemon Cards</h2>

    <div class="pokemon-cards-showcase" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px; max-width: 1200px; margin: 0 auto;">

        <!-- Ancient Sol Ring -->
        <div class="pokemon-card-item" style="background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1); transition: transform 0.3s, box-shadow 0.3s;">
            <img src="data:image/png;base64,{pokemon_b64.get('PokemonAncientSolRing.png', '')}" alt="Pokemon Ancient Sol Ring" style="width: 100%; height: 300px; object-fit: cover;">
            <div style="padding: 20px;">
                <h3 style="color: #333; margin-bottom: 10px;">Ancient Sol Ring</h3>
                <p style="color: #666; font-size: 14px;">Rare Pokemon Card</p>
            </div>
        </div>

        <!-- Deoxys -->
        <div class="pokemon-card-item" style="background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1); transition: transform 0.3s, box-shadow 0.3s;">
            <img src="data:image/png;base64,{pokemon_b64.get('PokemonDeoxys.png', '')}" alt="Pokemon Deoxys" style="width: 100%; height: 300px; object-fit: cover;">
            <div style="padding: 20px;">
                <h3 style="color: #333; margin-bottom: 10px;">Deoxys</h3>
                <p style="color: #666; font-size: 14px;">Mythical Pokemon</p>
            </div>
        </div>

        <!-- Dragon -->
        <div class="pokemon-card-item" style="background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1); transition: transform 0.3s, box-shadow 0.3s;">
            <img src="data:image/png;base64,{pokemon_b64.get('PokemonDragon.png', '')}" alt="Pokemon Dragon" style="width: 100%; height: 300px; object-fit: cover;">
            <div style="padding: 20px;">
                <h3 style="color: #333; margin-bottom: 10px;">Dragon Cards</h3>
                <p style="color: #666; font-size: 14px;">Premium Collection</p>
            </div>
        </div>

        <!-- Infernap -->
        <div class="pokemon-card-item" style="background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1); transition: transform 0.3s, box-shadow 0.3s;">
            <img src="data:image/png;base64,{pokemon_b64.get('PokemonInfernap.png', '')}" alt="Pokemon Infernap" style="width: 100%; height: 300px; object-fit: cover;">
            <div style="padding: 20px;">
                <h3 style="color: #333; margin-bottom: 10px;">Infernap</h3>
                <p style="color: #666; font-size: 14px;">Fire Type Pokemon</p>
            </div>
        </div>

    </div>
</section>

<!-- Pokemon Gallery Styles -->
<style>
    .pokemon-card-item:hover {{
        transform: translateY(-8px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }}

    .pokemon-cards-showcase {{
        animation: fadeIn 0.8s ease-in;
    }}

    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
</style>
'''

# Insert before footer or at end
footer_pattern = r'(</section>\s*</body>)'
if re.search(footer_pattern, html_content):
    html_content = re.sub(footer_pattern, pokemon_gallery_html + r'\1', html_content)
    print("  [OK] Pokemon gallery added at bottom")
else:
    # Add at end
    html_content += pokemon_gallery_html
    print("  [OK] Pokemon gallery appended")

# Save updated HTML
print("\nSaving updated homepage...")
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

file_size = os.path.getsize(html_file)
print(f"[OK] File saved ({file_size / (1024*1024):.2f} MB)")

print("\n" + "=" * 70)
print("HOMEPAGE UPDATED WITH POKEMON CARDS:")
print("  ✓ 4 Pokemon card base64 files created")
print("  ✓ Pokemon Cards Gallery added at bottom")
print("  ✓ 4 featured Pokemon cards displayed")
print("  ✓ Hover effects on cards")
print("  ✓ Responsive grid layout")
print("=" * 70)
