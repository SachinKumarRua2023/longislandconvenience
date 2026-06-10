# 🚀 Homepage Deployment Checklist

## Complete Odoo Homepage Redesign for Long Island Cards

---

## ✅ What You Get

A professional homepage matching **Dave & Adam's Card World** with:

- ✓ Professional header with navigation
- ✓ Hero section with featured product image
- ✓ Features showcase (Free Gifts, Shipping, Buying)
- ✓ 5 Category cards (Sports, Pokemon, MTG, Yu-Gi-Oh!, Graded)
- ✓ Special sections (Live Breaks, Deals, Hit Parade, etc.)
- ✓ New Releases product grid
- ✓ Professional footer with links
- ✓ Mobile responsive design
- ✓ Real images from Unsplash (free, copyright-free)

---

## 📋 Deployment Steps (DO IN THIS ORDER)

### Step 1️⃣: Check Website ID ⚠️ **CRITICAL**

```bash
python check_websites.py
```

**Output shows all websites in Odoo:**
```
Website ID: 1
  Name: Long Island Cards
  Domain: longislandcards.com
```

📌 **Write down the Website ID for Long Island Cards** (e.g., 1, 2, 3, etc.)

---

### Step 2️⃣: Update Deploy Script

Open `deploy_homepage_odoo.py`

Find this line:
```python
WEBSITE_ID = 1  # ← CHANGE THIS
```

Replace with your actual ID from Step 1:
```python
WEBSITE_ID = 2  # ← Example: if your ID is 2
```

**Save the file**

---

### Step 3️⃣: Deploy Homepage

```bash
python deploy_homepage_odoo.py
```

**Wait for success message:**
```
================================================================================
SUCCESS!
================================================================================

Your custom homepage is now live!
```

---

### Step 4️⃣: Verify on Website

1. Go to **https://longislandcards.com**
2. **Clear cache:** Ctrl+Shift+Delete
3. **Hard refresh:** Ctrl+Shift+R
4. ✅ You should see the new professional homepage!

---

### Step 5️⃣ (Optional): Update Category Images

To add real card images to the category circles:

```bash
python add_images_homepage.py
```

This fetches card images from Unsplash and updates each category.

---

## 📁 Files Created

| File | Purpose |
|------|---------|
| `homepage.html` | Complete homepage (HTML + CSS + JavaScript) |
| `check_websites.py` | **Find correct Website ID** |
| `deploy_homepage_odoo.py` | Deploy to Odoo |
| `add_images_homepage.py` | Add category images |
| `DEPLOYMENT_GUIDE.md` | Detailed deployment guide |
| `HOMEPAGE_DEPLOYMENT_CHECKLIST.md` | This file |

---

## ⚠️ MOST IMPORTANT

**Before running `deploy_homepage_odoo.py`:**

1. ✅ Run `check_websites.py`
2. ✅ Find Long Island Cards Website ID
3. ✅ Update WEBSITE_ID in `deploy_homepage_odoo.py`
4. ✅ Then run the deploy script

**If you don't do this, it might deploy to the wrong website!**

---

## 🎯 Quick Reference

```bash
# Step 1: Find Website ID
python check_websites.py

# Step 2: Update deploy_homepage_odoo.py with correct WEBSITE_ID

# Step 3: Deploy
python deploy_homepage_odoo.py

# Step 4: Go to https://longislandcards.com and verify

# Step 5 (Optional): Add category images
python add_images_homepage.py
```

---

## ✨ Features Deployed

**Header:**
- Logo + Brand
- Navigation links
- Search bar
- Professional styling

**Hero:**
- Large featured image
- Headline
- Call-to-action button
- Gradient background

**Features:**
- 🎁 Free Gifts
- 🚚 Same-Day Dispatch
- 💰 Always Buying

**Categories:**
- Sports (with image)
- Pokemon (with image)
- MTG (with image)
- Yu-Gi-Oh! (with image)
- Graded (with image)

**Special Sections:**
- 📺 Live Box Breaks
- 💰 Reed Buys
- 📅 Daily Deals
- ⭐ Best Deals List
- #P Hit Parade

**New Releases:**
- Product grid (3 columns on desktop)
- Product images
- Prices
- Add to Cart buttons
- Responsive layout

**Footer:**
- Products links
- Customer service links
- About us links
- Contact info

---

## 🔧 Customization

### Change colors:
Edit `homepage.html` color values:
```css
#ff8c00 = Orange
#003d5c = Dark blue
#667eea = Purple
```

### Change text:
Edit HTML content directly in `homepage.html`

### Change products:
Edit the `loadProducts()` function in script tag

### Add/Remove sections:
Find `<section>` tags and add/remove them

---

## ❓ Troubleshooting

| Problem | Solution |
|---------|----------|
| "Website ID not found" | Run `check_websites.py` to find correct ID |
| Homepage doesn't appear | Clear cache (Ctrl+Shift+Delete) + Hard refresh (Ctrl+Shift+R) |
| Images not showing | Unsplash might be slow; wait 1-2 minutes and refresh |
| Wrong website updated | Check Website ID! Run Step 1 again |
| Connection error | Verify Odoo is running and credentials are correct |

---

## 📞 Next Steps

1. **Run:** `python check_websites.py`
2. **Note:** Long Island Cards Website ID
3. **Edit:** `deploy_homepage_odoo.py` with correct ID
4. **Run:** `python deploy_homepage_odoo.py`
5. **Verify:** Go to longislandcards.com
6. **Done!** Share with your team 🎉

---

**Status:** ✅ Ready to Deploy

**Last Updated:** 2026-06-07

---

## Quick Start

```bash
# Just run these 2 commands:
python check_websites.py
# Then after updating the Website ID:
python deploy_homepage_odoo.py
```

That's it! Your professional homepage is deployed! 🚀
