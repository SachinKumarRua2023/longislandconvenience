# Long Island Cards - Homepage Deployment Guide

## ⚠️ IMPORTANT: Check Website ID First!

Before deploying the homepage, you MUST verify the correct **Website ID** for Long Island Cards in Odoo.

## Step-by-Step Deployment

### Step 1: Check Website ID

```bash
python check_websites.py
```

**Output will show:**
```
Website ID: 1
  Name: Long Island Cards
  Domain: longislandcards.com

Website ID: 2
  Name: Another Site
  Domain: othersite.com
```

**Note the Long Island Cards Website ID** (e.g., 1, 2, 3, etc.)

### Step 2: Update Website ID in Deploy Script

Open `deploy_homepage_odoo.py` and find this line:

```python
WEBSITE_ID = 1  # ← UPDATE THIS
```

Change it to your actual website ID:

```python
WEBSITE_ID = 2  # ← Your Long Island Cards ID
```

### Step 3: Deploy Homepage

```bash
python deploy_homepage_odoo.py
```

**Expected output:**
```
================================================================================
DEPLOY CUSTOM HOMEPAGE TO ODOO
================================================================================

[1/3] Reading homepage.html...
[OK] Loaded

[2/3] Connecting to Odoo...
[OK] Connected

[3/3] Deploying homepage...

  → Checking if homepage page exists...
  ✓ Homepage page found, updating...
  ✓ Homepage updated successfully!

================================================================================
SUCCESS!
================================================================================

Your custom homepage is now live!

NEXT STEPS:
  1. Go to https://longislandcards.com
  2. Clear browser cache (Ctrl+Shift+Delete)
  3. Hard refresh (Ctrl+Shift+R)
  4. Check the new homepage design
```

### Step 4: Verify on Website

1. Go to **https://longislandcards.com**
2. Clear browser cache: **Ctrl+Shift+Delete**
3. Hard refresh: **Ctrl+Shift+R**
4. You should see the new professional homepage design!

---

## What's Deployed

✅ **Professional Header**
- Long Island Cards logo
- Navigation menu (Shop, Sports, Pokemon, MTG, Contact)
- Search bar

✅ **Hero Section**
- Large featured image (trading cards from Unsplash)
- Headline and call-to-action button
- Eye-catching gradient background

✅ **Features Section**
- Free Gifts on orders $100+
- Same-Day Dispatch by 3 PM EST
- Always Buying (paid within 48 hours)

✅ **Category Showcase**
- 5 circular category cards with images:
  - Sports (baseball, basketball, football, hockey, soccer)
  - Pokemon
  - MTG
  - Yu-Gi-Oh!
  - Graded

✅ **Special Sections**
- Live Box Breaks
- Reed Buys
- Daily Deals
- Best Deals List
- Hit Parade

✅ **New Releases**
- Product grid (3 columns)
- Real product images from Unsplash
- Prices and "Add to Cart" buttons

✅ **Professional Footer**
- Links to products, customer service, about us
- Contact info and social media

✅ **Responsive Design**
- Works perfectly on desktop, tablet, and mobile
- Automatically adjusts layout for smaller screens

✅ **Real Images**
- All images auto-fetched from Unsplash (free, copyright-free)
- Dynamic content - different images each time

---

## Customization

### Change Colors

Edit `homepage.html` and find the color values:

```css
/* Change orange (#ff8c00) to any color */
background: #ff8c00;  /* Orange */
background: #e74c3c;  /* Red */
background: #27ae60;  /* Green */
```

### Change Text

Find and edit these sections:

```html
<h1>Trading Card Paradise</h1>  <!-- Hero title -->
<p>Explore premium collectibles</p>  <!-- Hero subtitle -->
<div class="category-name">Sports</div>  <!-- Category names -->
```

### Add/Remove Sections

To remove a section, find the `<section>` tag and delete it:

```html
<!-- Remove this entire section -->
<section class="special-sections">
    ...
</section>
```

### Change Product List

Edit the `loadProducts()` function in `<script>` tag:

```javascript
const products = [
    { name: 'Product Name 1', price: '$99.95', query: 'search term' },
    { name: 'Product Name 2', price: '$199.95', query: 'search term' },
    { name: 'Product Name 3', price: '$299.95', query: 'search term' }
];
```

### Change Image Search Keywords

Edit category image queries:

```javascript
{ id: 'cat-sports', query: 'baseball basketball cards' },  // Change this
{ id: 'cat-pokemon', query: 'pokemon trading cards' },     // Or this
```

---

## Troubleshooting

### "Website not found" error

**Solution:** The Website ID is wrong. Run `check_websites.py` again to find the correct ID.

### Homepage doesn't appear after deployment

1. **Clear cache:**
   - Ctrl+Shift+Delete (browser cache)
   - Ctrl+Shift+R (hard refresh)

2. **Check Odoo:**
   - Go to Odoo admin panel
   - Products → Website Pages
   - Look for "Homepage" page
   - Make sure it's Published (checkbox enabled)

3. **Wait for CDN:**
   - Sometimes images/cache take 1-5 minutes to update
   - Wait a few minutes and refresh again

### Images not showing

**Cause:** Unsplash API might be rate limited or temporarily unavailable

**Solution:**
- Wait a few minutes and reload
- Or manually set image URLs in `homepage.html`
- Or use local image files instead of Unsplash

### Some sections look broken on mobile

1. Ensure you're using a mobile viewport
2. Check CSS media queries in `<style>` section
3. Test on actual mobile device

---

## Files Reference

| File | Purpose |
|------|---------|
| `homepage.html` | Complete custom homepage design (HTML + CSS) |
| `deploy_homepage_odoo.py` | Deploys homepage.html to Odoo |
| `check_websites.py` | Lists all websites in Odoo (find Website ID) |
| `DEPLOYMENT_GUIDE.md` | This file - deployment instructions |

---

## Update Existing Homepage

If you need to make changes:

1. **Edit `homepage.html`** with your changes
2. **Run deployment again:**
   ```bash
   python deploy_homepage_odoo.py
   ```
3. **Clear cache and refresh**

The script will automatically update the existing homepage page in Odoo.

---

## Security Notes

✅ No Python code in Odoo  
✅ Only HTML/CSS deployed (static content)  
✅ Images fetched from Unsplash (external, safe)  
✅ No database manipulation  
✅ Safe to update anytime  

---

## Support

**If something goes wrong:**

1. Check `check_websites.py` output - verify Website ID
2. Verify Odoo connection and credentials
3. Check Odoo is running and accessible
4. Look for error messages in script output
5. Try manual deployment (go to Odoo → Website Pages → Create)

---

## Next Steps

After deployment:

1. ✅ Deploy homepage with correct Website ID
2. ✅ Verify on longislandcards.com
3. ✅ Update category images (run `add_images_homepage.py`)
4. ✅ Customize colors/text if desired
5. ✅ Test on mobile devices
6. ✅ Share with team!

---

**Ready to deploy? Start with:** `python check_websites.py`

---

Last Updated: 2026-06-07
