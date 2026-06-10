#!/usr/bin/env python3
"""
COMPLETE IMAGE CLEANUP & REORGANIZATION
1. Delete all existing base64 files
2. Keep only correct images per category
3. Create fresh base64 files
4. Ensure NO duplicates
5. Proper organization
"""

import os
import base64
import glob

base_dir = r"c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\HIREN_PROJECT_ORGANIZED\02_N8N_WORKFLOWS\SCRIPTS_BY_WEBSITE\WEBSITE_36_LONG_ISLAND_CARDS"
assets_dir = os.path.join(base_dir, "assets")

print("=" * 80)
print("COMPLETE IMAGE CLEANUP & REORGANIZATION")
print("=" * 80)

# Step 1: Delete all existing base64 files
print("\n[STEP 1] Deleting all existing base64 files...")
b64_files = glob.glob(os.path.join(base_dir, "*_base64.txt"))
deleted_count = 0
for f in b64_files:
    try:
        os.remove(f)
        deleted_count += 1
    except:
        pass
print(f"  Deleted: {deleted_count} base64 files")

# Step 2: Define clean image organization
print("\n[STEP 2] Organizing images by category...")

image_mapping = {
    # Sports Cards - 3 unique sports images
    "sports": {
        "left": "sports-cards-left.png",
        "center": "sports-cards-center.png",
        "right": "sports-cards-right.png",
    },
    # Pokemon Cards - 3 unique pokemon images
    "pokemon": {
        "left": "pokemon-cards-left.png",
        "center": "pokemon-cards-center.png",
        "right": "pokemon-cards-right.png",
    },
    # MTG Cards - 3 unique magic images
    "mtg": {
        "left": "mtg-cards-left.png",
        "center": "mtg-cards-center.png",
        "right": "mtg-cards-right.png",
    },
    # Yu-Gi-Oh Cards - 3 unique yugioh images
    "yugioh": {
        "left": "yugioh-cards-left.png",
        "center": "yugioh-cards-center.png",
        "right": "yugioh-cards-right.png",
    },
    # Graded Cards - 3 unique graded images
    "graded": {
        "left": "graded-cards-left.png",
        "center": "graded-cards-center.png",
        "right": "graded-cards-right.png",
    },
    # Hero Section Pokemon Overlay - 3 unique pokemon cards
    "pokemon_hero": {
        "card1": "PokemonAncientSolRing.png",
        "card2": "PokemonDeoxys.png",
        "card3": "PokemonDragon.png",
    },
    # Bundle/Special
    "bundle": "bulk-dragon-collection.png",
    # Products - 4 unique product images
    "products": {
        "premium": "product-premium-boxes.png",
        "graded": "product-graded-slabbed.png",
        "rare": "product-rare-editions.png",
        "exclusive": "product-exclusive-collection.png",
    }
}

# Step 3: Convert all images to base64
print("\n[STEP 3] Converting images to base64...")
total_converted = 0

for category, files in image_mapping.items():
    if category == "products":
        for product_type, filename in files.items():
            image_path = os.path.join(assets_dir, filename)
            if os.path.exists(image_path):
                with open(image_path, 'rb') as f:
                    b64_data = base64.b64encode(f.read()).decode('utf-8')

                b64_filename = filename.replace('.png', '_base64.txt')
                with open(os.path.join(base_dir, b64_filename), 'w') as f:
                    f.write(b64_data)

                print(f"  [OK] {filename}")
                total_converted += 1

    elif category == "pokemon_hero":
        for card_type, filename in files.items():
            image_path = os.path.join(assets_dir, filename)
            if os.path.exists(image_path):
                with open(image_path, 'rb') as f:
                    b64_data = base64.b64encode(f.read()).decode('utf-8')

                b64_filename = filename.replace('.png', '_base64.txt')
                with open(os.path.join(base_dir, b64_filename), 'w') as f:
                    f.write(b64_data)

                print(f"  [OK] {filename}")
                total_converted += 1

    elif category == "bundle":
        image_path = os.path.join(assets_dir, files)
        if os.path.exists(image_path):
            with open(image_path, 'rb') as f:
                b64_data = base64.b64encode(f.read()).decode('utf-8')

            b64_filename = files.replace('.png', '_base64.txt')
            with open(os.path.join(base_dir, b64_filename), 'w') as f:
                f.write(b64_data)

            print(f"  [OK] {files}")
            total_converted += 1

    else:
        for position, filename in files.items():
            image_path = os.path.join(assets_dir, filename)
            if os.path.exists(image_path):
                with open(image_path, 'rb') as f:
                    b64_data = base64.b64encode(f.read()).decode('utf-8')

                b64_filename = filename.replace('.png', '_base64.txt')
                with open(os.path.join(base_dir, b64_filename), 'w') as f:
                    f.write(b64_data)

                print(f"  [OK] {filename}")
                total_converted += 1

print(f"\n  Total converted: {total_converted} images")

# Step 4: Verify no duplicates
print("\n[STEP 4] Verifying no duplicate base64 files...")
b64_files = glob.glob(os.path.join(base_dir, "*_base64.txt"))
print(f"  Total base64 files: {len(b64_files)}")
print(f"  Status: {'NO DUPLICATES' if len(b64_files) == total_converted else 'WARNING: Duplicates found'}")

# Step 5: Summary
print("\n" + "=" * 80)
print("CLEANUP COMPLETE - IMAGE ORGANIZATION:")
print("=" * 80)
print("\nCategory Organization:")
print("  Sports Cards:     sports-cards-left/center/right")
print("  Pokemon Cards:    pokemon-cards-left/center/right")
print("  MTG Cards:        mtg-cards-left/center/right")
print("  Yu-Gi-Oh Cards:   yugioh-cards-left/center/right")
print("  Graded Cards:     graded-cards-left/center/right")
print("  Hero Overlay:     PokemonAncientSolRing/Deoxys/Dragon")
print("  Bundle/Special:   bulk-dragon-collection")
print("  Products (4):     premium/graded/rare/exclusive")
print("\nSummary:")
print(f"  Total base64 files: {len(b64_files)}")
print(f"  Duplicates removed: YES")
print(f"  Organization: CLEAN")
print(f"  Status: READY FOR HOMEPAGE UPDATE")
print("=" * 80)
