# Universal — Real Products & Images
Scripts for managing products, inventory, and images across all Odoo sites.

## Scripts

| Script | What It Does |
|--------|-------------|
| `check_products.py` | List all products categorized by website |
| `count_all_products.py` | Count products across all stores |
| `find_shop_products.py` | Search for specific products in shop |
| `direct_image_update.py` | Update product/page images in Odoo views |
| `fix_all_real_images.py` | Fix broken image references across all sites |
| `fix_all_images_social.py` | Update social media og:image tags |
| `check_images.py` | Validate images and favicons across all sites |
| `fix_images_and_css.py` | Combined image + CSS fixes |
| `fix_shop_categories.py` | Fix product category structure |
| `fix_shop_images.py` | Fix shop product images |
| `test_one_product.py` | Test single product creation |
| `test_product_categ.py` | Test product category setup |
| `upload_images_v2.py` | Upload images to Odoo v2 |
| `upload_product_images.py` | Bulk upload product images |
| `patch_missing_images.py` | Find and fill in missing product images |
| `patch_section_images.py` | Patch homepage section images |
| `patch_final_images.py` | Final pass image patches |
| `pure_real_images.py` | Replace placeholder images with real photos |
| `fix_real_images_final.py` | Final real image fixes |
| `test_odoo_image_route.py` | Test Odoo image serving routes |
| `product_hover_v2.py` | Product card hover effects |
| `setup_payments.py` | Configure payment providers |

## ⚠️ IMPORTANT: cover_properties safety rule
Never set external URLs (e.g. Unsplash) in `cover_properties`.
This causes Odoo's `get_website_meta()` og:image to crash with a 500 error.
Always use:
```python
cover_properties = json.dumps({
    "background-image": "none",  # ← always none for external images
    "background_color_class": "o_cc3",
    "opacity": "0.2",
    "resize_class": ""
})
```
Use `<img src="https://images.unsplash.com/...">` inside post content HTML instead.
