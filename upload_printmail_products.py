#!/usr/bin/env python3
"""
Upload Print & Mail products to Odoo Website 39.
Creates categories, products, and uploads images.
"""
import xmlrpc.client
import base64
import csv
import sys
import os

# Odoo Credentials
URL  = "https://country-cove-inc.odoo.com"
DB   = "country-cove-inc"
USER = "countrycoveinc@gmail.com"
PASS = "M@nhattan1234"

# CSV and Images paths
CSV_FILE = r"C:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\longislandprintmail\LONG_ISLAND_PRINTMAIL_PRODUCTS.csv"
IMAGES_DIR = r"C:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\longislandprintmail\images"
WEBSITE_ID = 41  # Print & Mail website

# Category mapping
CATEGORIES = {
    "Banners": "Banners",
    "Stands": "Display Stands",
    "Signs": "Signage",
    "Decals": "Vinyl Decals",
    "Flags": "Flags",
    "Table Covers": "Table Covers"
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

def get_or_create_category(m, uid, cat_name):
    """Get or create a product category"""
    print(f"   [*] Processing category: {cat_name}")

    # Search for existing category
    cats = execute(m, uid, 'product.category', 'search', [[['name', '=', cat_name]]])
    if cats:
        print(f"   [OK] Category exists: {cats[0]}")
        return cats[0]

    # Create new category (without website_id - not a valid field)
    cat_id = execute(m, uid, 'product.category', 'create', [{
        'name': cat_name,
    }])
    if cat_id:
        print(f"   [+] Created category: {cat_name} (ID: {cat_id})")
        return cat_id
    return None

def upload_product_image(m, uid, product_id, image_path):
    """Upload and set product image"""
    try:
        if not os.path.exists(image_path):
            print(f"   [!] Image not found: {image_path}")
            return False

        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')

        # Set main image
        result = execute(m, uid, 'product.template', 'write', [product_id, {
            'image_1920': image_data,
        }])

        if result:
            print(f"   [OK] Image uploaded")
            return True
    except Exception as e:
        print(f"   [!] Image upload error: {e}")
    return False

def create_product(m, uid, product_data, cat_id):
    """Create a product"""
    try:
        product_vals = {
            'name': product_data['Product Name'],
            'default_code': product_data['SKU'],
            'list_price': float(product_data['List Price']),
            'standard_price': float(product_data['Cost Price']),
            'categ_id': cat_id,
            'type': 'consu',
            'website_published': True,
            'description_sale': product_data['Description'],
        }

        product_id = execute(m, uid, 'product.template', 'create', [product_vals])

        if product_id:
            print(f"   [+] Created product: {product_data['Product Name']} (ID: {product_id})")

            # Upload image
            image_path = os.path.join(IMAGES_DIR, product_data['Image File'])
            upload_product_image(m, uid, product_id, image_path)

            return product_id
    except Exception as e:
        print(f"   [!] Error creating product: {e}")
    return None

def main():
    """Main execution"""
    print("=" * 70)
    print("LONG ISLAND PRINT & MAIL - PRODUCT IMPORTER")
    print("=" * 70)

    # Connect to Odoo
    m, uid = connect()

    # Create categories
    print("\n[*] Creating categories...")
    category_map = {}
    for csv_cat, odoo_cat in CATEGORIES.items():
        cat_id = get_or_create_category(m, uid, odoo_cat)
        if cat_id:
            category_map[csv_cat] = cat_id

    # Import products
    print("\n[*] Importing products from CSV...")
    products_created = 0
    products_failed = 0

    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not row.get('Product Name'):
                    continue

                print(f"\n[*] Processing: {row['Product Name']}")
                cat_key = row['Category']

                if cat_key not in category_map:
                    print(f"   [!] Category not found: {cat_key}")
                    products_failed += 1
                    continue

                product_id = create_product(m, uid, row, category_map[cat_key])
                if product_id:
                    products_created += 1
                else:
                    products_failed += 1

    except Exception as e:
        print(f"[!] CSV read error: {e}")
        return 1

    # Summary
    print("\n" + "=" * 70)
    print("IMPORT SUMMARY")
    print("=" * 70)
    print(f"[+] Created:  {products_created}")
    print(f"[-] Failed:   {products_failed}")
    print(f"Total:        {products_created + products_failed}")
    print("=" * 70)

    if products_created == 18:
        print("\n[OK] ALL PRODUCTS IMPORTED SUCCESSFULLY!")
        return 0
    else:
        print(f"\n[!] {products_failed} products failed to import")
        return 1

if __name__ == "__main__":
    sys.exit(main())
