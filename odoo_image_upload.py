#!/usr/bin/env python3
"""
Odoo Image Upload Script
Upload product images to Odoo Media Library and attach to product categories
"""

import os
import sys
import xmlrpc.client
import base64
from pathlib import Path

# ============================================
# ODOO CONNECTION DETAILS
# ============================================
ODOO_URL = "https://country-cove-inc.odoo.com"
ODOO_DB = "country-cove-inc"
ODOO_USER = "countrycoveinc@gmail.com"
ODOO_PASSWORD = "M@nhattan1234"

# Local images folder path
IMAGES_FOLDER = r"c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\images"

# ============================================
# PRODUCT CATEGORIES WITH IMAGES
# ============================================
PRODUCT_CATEGORIES = {
    'Sports Cards': {
        'description': 'Cards & Collectibles',
        'images': [
            'sports-cards-center.png',
            'cards_left.png',
            'cards_right.png'
        ]
    },
    'Gift Baskets': {
        'description': 'Gifts & Occasions',
        'images': [
            'giftbasket_center.jpg',
            'giftbasket_left.jpg',
            'giftbasket_right.jpg'
        ]
    },
    'Balloons & Décor': {
        'description': 'Events & Parties',
        'images': [
            'BalloonsCenter.png',
            'balloon_left.jfif',
            'balloon_right.jfif'
        ]
    },
    'Print & Mail': {
        'description': 'Print & Shipping',
        'images': [
            'printmail_center.jpeg',
            'printmail_left.jpeg',
            'printmail_right.jpeg'
        ]
    },
    'Game Cards': {
        'description': 'Gaming',
        'images': [
            'cards_left.png',
            'sports-cards-center.png',
            'cards_right.png'
        ]
    },
    'Greeting Cards': {
        'description': 'Cards & Stationery',
        'images': [
            'Gemini_Generated_Image_3a8oit3a8o.png',
            'GreetingCardLeft.png',
            'GreetingCardRight.png'
        ]
    }
}

# ============================================
# CONNECT TO ODOO
# ============================================
def connect_odoo():
    """Connect to Odoo using XML-RPC"""
    print(f"Connecting to Odoo: {ODOO_URL}")

    common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/jsonrpc/2/object')
    models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/jsonrpc/2/object')

    try:
        uid = xmlrpc.client.ServerProxy(f'{ODOO_URL}/jsonrpc/2/common').authenticate(
            ODOO_DB,
            ODOO_USER,
            ODOO_PASSWORD,
            {}
        )
        print(f"✓ Connected successfully! User ID: {uid}")
        return uid, models
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        sys.exit(1)

# ============================================
# UPLOAD IMAGE TO ODOO MEDIA
# ============================================
def upload_image_to_odoo(models, uid, image_path, image_name):
    """Upload single image to Odoo Media Library"""
    try:
        # Read image file
        with open(image_path, 'rb') as f:
            image_data = f.read()

        # Encode to base64
        image_base64 = base64.b64encode(image_data).decode('utf-8')

        # Get file extension
        file_ext = os.path.splitext(image_name)[1].lower()

        # Determine MIME type
        mime_types = {
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.jfif': 'image/jpeg',
            '.gif': 'image/gif'
        }
        mime_type = mime_types.get(file_ext, 'image/png')

        # Create attachment in Odoo
        attachment_id = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'ir.attachment',
            'create',
            [{
                'name': image_name,
                'type': 'binary',
                'datas': image_base64,
                'mimetype': mime_type,
                'res_model': 'ir.ui.view',
            }]
        )

        print(f"  ✓ Uploaded: {image_name} (ID: {attachment_id})")
        return attachment_id

    except Exception as e:
        print(f"  ✗ Failed to upload {image_name}: {e}")
        return None

# ============================================
# CREATE PRODUCT CATEGORY WITH IMAGES
# ============================================
def create_product_category(models, uid, category_name, category_data, image_ids):
    """Create or update product category with images"""
    try:
        # Check if category exists
        existing = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'product.category',
            'search',
            [[('name', '=', category_name)]]
        )

        category_vals = {
            'name': category_name,
            'display_on_website': True,
            'website_description': category_data['description'],
        }

        # Add image IDs if available
        if image_ids:
            category_vals['image_ids'] = [(6, 0, image_ids)]

        if existing:
            # Update existing
            models.execute_kw(
                ODOO_DB, uid, ODOO_PASSWORD,
                'product.category',
                'write',
                [existing, category_vals]
            )
            print(f"✓ Updated category: {category_name}")
            return existing[0]
        else:
            # Create new
            category_id = models.execute_kw(
                ODOO_DB, uid, ODOO_PASSWORD,
                'product.category',
                'create',
                [category_vals]
            )
            print(f"✓ Created category: {category_name} (ID: {category_id})")
            return category_id

    except Exception as e:
        print(f"✗ Failed to create category {category_name}: {e}")
        return None

# ============================================
# MAIN EXECUTION
# ============================================
def main():
    print("=" * 60)
    print("ODOO IMAGE UPLOAD & PRODUCT SETUP")
    print("=" * 60)
    print()

    # Step 1: Connect to Odoo
    print("Step 1: Connecting to Odoo...")
    uid, models = connect_odoo()
    print()

    # Step 2: Upload images and create categories
    print("Step 2: Uploading images and creating product categories...")
    print()

    for category_name, category_data in PRODUCT_CATEGORIES.items():
        print(f"Processing: {category_name}")

        # Upload images for this category
        image_ids = []
        for image_filename in category_data['images']:
            image_path = os.path.join(IMAGES_FOLDER, image_filename)

            if os.path.exists(image_path):
                img_id = upload_image_to_odoo(models, uid, image_path, image_filename)
                if img_id:
                    image_ids.append(img_id)
            else:
                print(f"  ⚠ Image not found: {image_filename}")

        # Create product category with images
        category_id = create_product_category(
            models, uid, category_name, category_data, image_ids
        )

        print()

    print("=" * 60)
    print("✓ UPLOAD COMPLETE!")
    print("=" * 60)
    print()
    print("Images are now available in Odoo:")
    print("  Location: Website > Media Library")
    print("  Product Categories: eCommerce > Categories")
    print()

if __name__ == "__main__":
    main()
