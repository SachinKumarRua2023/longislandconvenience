#!/usr/bin/env python3
import os
import base64
import re

base_dir = r"c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\HIREN_PROJECT_ORGANIZED\02_N8N_WORKFLOWS\SCRIPTS_BY_WEBSITE\WEBSITE_36_LONG_ISLAND_CARDS"
assets_dir = os.path.join(base_dir, "assets")

# List of all images to convert to base64
images = [
    "sports-cards-left.png",
    "sports-cards-center.png",
    "sports-cards-right.png",
    "pokemon-cards-left.png",
    "pokemon-cards-center.png",
    "pokemon-cards-right.png",
    "mtg-cards-left.png",
    "mtg-cards-center.png",
    "mtg-cards-right.png",
    "yugioh-cards-left.png",
    "yugioh-cards-center.png",
    "yugioh-cards-right.png",
    "graded-cards-left.png",
    "graded-cards-center.png",
    "graded-cards-right.png",
    "bulk-dragon-collection.png",
]

print("=" * 60)
print("CONVERTING IMAGES TO BASE64")
print("=" * 60)

for image in images:
    image_path = os.path.join(assets_dir, image)
    if not os.path.exists(image_path):
        print(f"[SKIP] {image} - File not found")
        continue

    try:
        with open(image_path, 'rb') as f:
            image_data = f.read()

        base64_data = base64.b64encode(image_data).decode('utf-8')

        # Save base64 to file
        b64_filename = image.replace('.png', '_base64.txt')
        b64_path = os.path.join(base_dir, b64_filename)

        with open(b64_path, 'w') as f:
            f.write(base64_data)

        print(f"[OK] {image} -> {b64_filename} ({len(base64_data)} chars)")

    except Exception as e:
        print(f"[ERROR] {image}: {e}")

print("\n" + "=" * 60)
print("BASE64 CONVERSION COMPLETE")
print("=" * 60)
print("\nBase64 files saved in:")
print(base_dir)
