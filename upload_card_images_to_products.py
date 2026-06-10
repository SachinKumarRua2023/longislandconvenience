#!/usr/bin/env python3
"""
Upload card images to Long Island Cards products in Odoo.
Automatically links images to products by SKU matching.
"""
import xmlrpc.client
import base64
import sys
import os

# Odoo Credentials
URL  = "https://country-cove-inc.odoo.com"
DB   = "country-cove-inc"
USER = "countrycoveinc@gmail.com"
PASS = "M@nhattan1234"

# Image folder path
IMAGES_DIR = r"C:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\longislandcards\images"

# Image to SKU mapping
IMAGE_MAPPING = {
    "sports-cards-left.png": "LIC-SPC-001",
    "sports-cards-center.png": "LIC-SPC-002",
    "sports-cards-right.png": "LIC-SPC-003",
    "pokemon-cards-left.png": "LIC-PKM-001",
    "pokemon-cards-center.png": "LIC-PKM-002",
    "pokemon-cards-right.png": "LIC-PKM-003",
    "mtg-cards-left.png": "LIC-MTG-001",
    "mtg-cards-center.png": "LIC-MTG-002",
    "mtg-cards-right.png": "LIC-MTG-003",
    "yugioh-cards-left.png": "LIC-YGO-001",
    "yugioh-cards-center.png": "LIC-YGO-002",
    "yugioh-cards-right.png": "LIC-YGO-003",
    "graded-cards-left.png": "LIC-GRD-001",
    "graded-cards-center.png": "LIC-GRD-002",
    "graded-cards-right.png": "LIC-GRD-003",
    "bulk-dragon-collection.png": "LIC-BDL-001",
}

def connect():
    """Connect to Odoo via XML-RPC"""
    print("[*] Connecting to Odoo...")
    try:
        uid = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common').authenticate(DB, USER, PASS, {})
        if not uid:
            print("[!] Authentication failed")
            sys.exit(1)
        m = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
        print(f"[OK] Connected! UID: {uid}")
        return m, uid
    except Exception as e:
        print(f"[!] Connection error: {e}")
        sys.exit(1)

def execute(m, uid, model, method, args, kwargs={}):
    """Execute Odoo method via XML-RPC"""
    try:
        return m.execute_kw(DB, uid, PASS, model, method, args, kwargs)
    except Exception as e:
        print(f"[!] Odoo Error: {e}")
        return None

def find_product_by_sku(m, uid, sku):
    """Find product by internal reference (SKU)"""
    try:
        products = execute(m, uid, 'product.product', 'search', [[['default_code', '=', sku]]])
        if products:
            return products[0]
        return None
    except Exception as e:
        print(f"[!] Error searching for SKU {sku}: {e}")
        return None

def upload_image(m, uid, product_id, image_path, image_name):
    """Upload image to product and set as main image"""
    try:
        if not os.path.exists(image_path):
            print(f"[!] Image file not found: {image_path}")
            return False

        # Read and encode image to base64
        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')

        # Step 1: Set as main product image on product.template
        template_update = execute(m, uid, 'product.template', 'write', [product_id, {
            'image_1920': image_data,
        }])

        if not template_update:
            print(f"[!] Failed to set main image for product ID {product_id}")
            return False

        # Step 2: Also create image record for gallery
        image_record = {
            'name': image_name,
            'image_1920': image_data,
            'product_tmpl_id': product_id,
        }

        result = execute(m, uid, 'product.image', 'create', [image_record])

        if result:
            print(f"[OK] Uploaded {image_name} to product ID {product_id}")
            return True
        else:
            print(f"[OK] Main image set (gallery creation skipped) for product ID {product_id}")
            return True

    except Exception as e:
        print(f"[!] Error uploading image {image_name}: {e}")
        return False

def main():
    """Main execution"""
    print("=" * 70)
    print("LONG ISLAND CARDS - IMAGE UPLOADER")
    print("=" * 70)

    # Connect to Odoo
    m, uid = connect()

    # Upload images
    uploaded = 0
    failed = 0
    not_found = 0

    print(f"\n[*] Starting image upload for {len(IMAGE_MAPPING)} products...\n")

    for image_name, sku in IMAGE_MAPPING.items():
        image_path = os.path.join(IMAGES_DIR, image_name)

        print(f"[*] Processing {image_name} (SKU: {sku})")

        # Find product by SKU
        product_id = find_product_by_sku(m, uid, sku)

        if not product_id:
            print(f"   [!] Product not found with SKU {sku}")
            not_found += 1
            continue

        # Upload image
        if upload_image(m, uid, product_id, image_path, image_name):
            uploaded += 1
        else:
            failed += 1

    # Summary
    print("\n" + "=" * 70)
    print("UPLOAD SUMMARY")
    print("=" * 70)
    print(f"[+] Uploaded:    {uploaded}")
    print(f"[-] Failed:      {failed}")
    print(f"[?] Not Found:   {not_found}")
    print(f"Total:         {len(IMAGE_MAPPING)}")
    print("=" * 70)

    if uploaded == len(IMAGE_MAPPING):
        print("\n[OK] ALL IMAGES UPLOADED SUCCESSFULLY!")
        return 0
    else:
        print(f"\n[!] {failed + not_found} images could not be uploaded")
        return 1

if __name__ == "__main__":
    sys.exit(main())
