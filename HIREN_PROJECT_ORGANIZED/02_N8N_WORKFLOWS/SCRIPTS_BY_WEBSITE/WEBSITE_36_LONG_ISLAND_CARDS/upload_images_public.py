#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Upload card images to Odoo as PUBLIC
"""

import os
import sys
import base64
import xmlrpc.client

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# ===== ODOO CREDENTIALS =====
ODOO_URL = "https://country-cove-inc.odoo.com"
ODOO_DB = "country-cove-inc"
ODOO_USER = "countrycoveinc@gmail.com"
ODOO_PASSWORD = "M@nhattan1234"
WEBSITE_ID = 36

# ===== IMAGE PATHS =====
ASSETS_FOLDER = r"c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\HIREN_PROJECT_ORGANIZED\02_N8N_WORKFLOWS\SCRIPTS_BY_WEBSITE\WEBSITE_36_LONG_ISLAND_CARDS\assets"

IMAGE_FILES = [
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
]

def upload_images():
    """Upload all card images to Odoo as PUBLIC"""

    print("[INFO] Connecting to Odoo...")
    common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
    uid = common.authenticate(ODOO_DB, ODOO_USER, ODOO_PASSWORD, {})

    if not uid:
        print("[ERROR] Authentication failed!")
        return False

    print(f"[OK] Authenticated as user {uid}")

    models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')

    uploaded_images = {}

    for image_file in IMAGE_FILES:
        image_path = os.path.join(ASSETS_FOLDER, image_file)

        if not os.path.exists(image_path):
            print(f"[ERROR] File not found: {image_path}")
            continue

        try:
            # Read image and encode to base64
            with open(image_path, 'rb') as f:
                image_data = base64.b64encode(f.read()).decode()

            # Upload to Odoo with PUBLIC access
            image_id = models.execute_kw(
                ODOO_DB, uid, ODOO_PASSWORD,
                'ir.attachment',
                'create',
                [{
                    'name': image_file,
                    'datas': image_data,
                    'res_model': 'website',
                    'res_id': WEBSITE_ID,
                    'type': 'binary',
                    'public': True,  # Make PUBLIC
                }]
            )

            image_url = f"/web/image/{image_id}/{image_file}"
            uploaded_images[image_file] = image_url

            print(f"[OK] Uploaded: {image_file} > {image_url}")

        except Exception as e:
            print(f"[ERROR] Failed to upload {image_file}: {str(e)}")
            continue

    # Save mapping to file
    print("\n[INFO] Saving URLs...")
    with open(os.path.join(ASSETS_FOLDER, 'image_urls_public.txt'), 'w') as f:
        for filename, url in uploaded_images.items():
            f.write(f"{filename}={url}\n")

    print(f"\n[OK] Successfully uploaded {len(uploaded_images)} images!")
    print(f"[INFO] Check Odoo to verify images are VISIBLE")

    return True

if __name__ == '__main__':
    print("=" * 60)
    print("LONG ISLAND CARDS - PUBLIC IMAGE UPLOAD")
    print("=" * 60)
    print()

    success = upload_images()

    if success:
        print("\n[SUCCESS] Images uploaded as PUBLIC!")
        print("[NEXT] Test URLs in browser - they should load now")
    else:
        print("\n[FAILED] Some images failed to upload")
