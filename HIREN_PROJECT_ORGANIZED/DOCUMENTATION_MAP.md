# 📍 Documentation Map - Where to Find Everything

**Quick Reference: Which File Contains What**

---

## 🌐 Website Information

### All 14 Website IDs
**Files**:
1. `02_N8N_WORKFLOWS/PRODUCT_UPDATE_GUIDE_BY_WEBSITE.md` - **⭐ MAIN REFERENCE**
2. `01_DOCUMENTATION/ODOO_WEBSITE_IDS.md` - Website ID list
3. `01_DOCUMENTATION/ODOO_WEBSITES_AND_SCRIPTS_DOCUMENTATION.md` - Website architecture

**Contents**:
```
Website 1: Long Island Convenience
Website 18: Country Cove Balloons
Website 27: Country Cove Gift Baskets
Website 29: Long Island Print & Copy
Website 33: Long Island Card Shop
Website 36-46: Expansion websites (9 more)
```

---

## 📦 Product Management

### How to Add Products Manually (UI)
**File**: `02_N8N_WORKFLOWS/PRODUCT_UPDATE_GUIDE_BY_WEBSITE.md` 
**Section**: "Method 1: Manual Update Via UI"
**Steps**: Step-by-step guide with images

### How to Add Products Via Python Script
**File**: `02_N8N_WORKFLOWS/PRODUCT_UPDATE_GUIDE_BY_WEBSITE.md`
**Section**: "Method 2: Update Via Python Script"
**Scripts**: 4 ready-to-use examples

### How to Add Products Via N8N Automation
**File**: `02_N8N_WORKFLOWS/PRODUCT_UPDATE_GUIDE_BY_WEBSITE.md`
**Section**: "Method 3: Update Via n8n Workflow"
**Template**: JSON workflow ready to use

---

## 🔗 Product-Website Assignment

### Assign Product to Specific Website
**File**: `02_N8N_WORKFLOWS/PRODUCT_UPDATE_GUIDE_BY_WEBSITE.md`
**Script**: Script 1 - "Add Product to Specific Website"
**Website IDs to Use**: 1, 18, 27, 29, 33, 36-46

### Assign Product to Multiple Websites
**File**: `02_N8N_WORKFLOWS/PRODUCT_UPDATE_GUIDE_BY_WEBSITE.md`
**Script**: Script 2 - "Add Product to Multiple Websites"
**Example**: Websites [1, 18, 27]

### Assign Product to ALL Websites
**File**: `02_N8N_WORKFLOWS/PRODUCT_UPDATE_GUIDE_BY_WEBSITE.md`
**Script**: Script 3 - "Update Product for All Websites"
**Result**: Product appears on all 14 websites

### Bulk Update Multiple Products
**File**: `02_N8N_WORKFLOWS/PRODUCT_UPDATE_GUIDE_BY_WEBSITE.md`
**Script**: Script 4 - "Bulk Update Multiple Products"
**Use Case**: Update 10+ products at once

---

## 🛠️ Technical Information

### XML-RPC API Reference
**File**: `01_DOCUMENTATION/ODOO_WEBSITES_AND_SCRIPTS_DOCUMENTATION.md`
**Section**: "🐍 Python Scripts - How They Work"
**Methods**: search(), read(), write(), unlink(), create()

### Odoo Authentication
**File**: `01_DOCUMENTATION/ODOO_WEBSITES_AND_SCRIPTS_DOCUMENTATION.md`
**Section**: "Connection Architecture"
**Details**: How to connect and authenticate

### Database Fields for Products
**File**: `02_N8N_WORKFLOWS/PRODUCT_UPDATE_GUIDE_BY_WEBSITE.md`
**Section**: "📊 Field Reference"
**Fields**: All product fields explained

---

## 🏗️ System Architecture

### How Odoo Websites Work
**File**: `01_DOCUMENTATION/ODOO_WEBSITES_AND_SCRIPTS_DOCUMENTATION.md`
**Section**: "🌐 Website IDs & Information"
**Diagram**: Shows how all 14 websites share one database

### How Product Images Display
**File**: `01_DOCUMENTATION/ODOO_WEBSITES_AND_SCRIPTS_DOCUMENTATION.md`
**Section**: "🖼️ Product Images & Display System"
**Details**: Image storage and display flow

### Category System
**File**: `01_DOCUMENTATION/ODOO_WEBSITES_AND_SCRIPTS_DOCUMENTATION.md`
**Section**: "📂 Product Categories System"
**Info**: 230 categories and their use

---

## 💾 Odoo Credentials

### Login Information
**File**: `03_PROJECT_ACCOUNTS/00_Accounts_Passwords/`
**Type**: Secured folder
**Contains**: All credentials

**Quick Reference**:
```
URL: https://country-cove-inc.odoo.com/
Email: countrycoveinc@gmail.com
Password: M@nhattan1234
Database: country-cove-inc
```

---

## 📋 Product Upload Instructions

### Step-by-Step Manual Process
**File**: `02_N8N_WORKFLOWS/PRODUCT_UPDATE_GUIDE_BY_WEBSITE.md`
**Section**: "📝 Method 1: Manual Update Via UI"
**Steps**: 
1. Login
2. Navigate to Products
3. Create new product
4. Enter details
5. Upload images
6. Assign to websites
7. Publish
8. Save

### Automated Process (Python)
**File**: `02_N8N_WORKFLOWS/PRODUCT_UPDATE_GUIDE_BY_WEBSITE.md`
**Section**: "🐍 Method 2: Update Via Python Script"
**Time**: Run once, done

### Automated Process (N8N)
**File**: `02_N8N_WORKFLOWS/PRODUCT_UPDATE_GUIDE_BY_WEBSITE.md`
**Section**: "🤖 Method 3: Update Via n8n Workflow"
**Schedule**: Run daily/weekly/on demand

---

## 🎯 Use Cases & Examples

### Add Balloon Products to Website 18 Only
**File**: `02_N8N_WORKFLOWS/PRODUCT_UPDATE_GUIDE_BY_WEBSITE.md`
**Section**: "🎯 Common Use Cases"
**Use Case**: #2 - Balloon Products

### Add Gift Baskets to Multiple Websites
**File**: `02_N8N_WORKFLOWS/PRODUCT_UPDATE_GUIDE_BY_WEBSITE.md`
**Section**: "🎯 Common Use Cases"
**Use Case**: #3 - Gift Baskets

### Sync Product to All 14 Websites
**File**: `02_N8N_WORKFLOWS/PRODUCT_UPDATE_GUIDE_BY_WEBSITE.md`
**Section**: "🎯 Common Use Cases"
**Use Case**: #4 - All Websites

---

## 🔍 Querying Products

### Check Which Websites a Product is On
**File**: `02_N8N_WORKFLOWS/PRODUCT_UPDATE_GUIDE_BY_WEBSITE.md`
**Section**: "🔍 Query: Check Product Website Assignment"
**Code**: Python script to query

### Find All Products in a Category
**File**: `01_DOCUMENTATION/ODOO_WEBSITES_AND_SCRIPTS_DOCUMENTATION.md`
**Section**: "🔄 Python Script Workflow Diagram"
**Method**: Use search() with category domain

---

## 🚨 Troubleshooting

### Product Not Showing on Website
**File**: `02_N8N_WORKFLOWS/PRODUCT_UPDATE_GUIDE_BY_WEBSITE.md`
**Section**: "🚨 Common Issues & Solutions"
**Solution**: Set `website_published = True`

### Product on Wrong Website
**File**: `02_N8N_WORKFLOWS/PRODUCT_UPDATE_GUIDE_BY_WEBSITE.md`
**Section**: "🚨 Common Issues & Solutions"
**Solution**: Use replace method `(6, False, [list])`

### Image Not Displaying
**File**: `02_N8N_WORKFLOWS/PRODUCT_UPDATE_GUIDE_BY_WEBSITE.md`
**Section**: "🚨 Common Issues & Solutions"
**Solution**: Add `image_1920` field with base64 image

---

## 📚 Project Documentation Files

| File | Purpose | Location |
|------|---------|----------|
| **PROJECT_INDEX.md** | Master project overview | Root folder |
| **COMPLETION_SUMMARY.md** | What was completed | Root folder |
| **FINAL_ORGANIZATION_REPORT.md** | Organization details | Root folder |
| **PRODUCT_UPDATE_GUIDE_BY_WEBSITE.md** | ⭐ Product updates | 02_N8N_WORKFLOWS/ |
| **ODOO_WEBSITES_AND_SCRIPTS_DOCUMENTATION.md** | Technical reference | 01_DOCUMENTATION/ |
| **README_N8N_WORKFLOWS.md** | N8N automation guide | 02_N8N_WORKFLOWS/ |
| **ODOO_WEBSITE_IDS.md** | Website ID list | 01_DOCUMENTATION/ |
| **ODOO_WEBSITE45_SETUP.md** | Website configuration | 01_DOCUMENTATION/ |

---

## 🎯 Quick Start Path

### If You Want to...

**Add one product manually**
→ File: `02_N8N_WORKFLOWS/PRODUCT_UPDATE_GUIDE_BY_WEBSITE.md`
→ Section: "Method 1: Manual Update Via UI"

**Add 10 products at once**
→ File: `02_N8N_WORKFLOWS/PRODUCT_UPDATE_GUIDE_BY_WEBSITE.md`
→ Section: "Method 2: Update Via Python Script"

**Automate product updates**
→ File: `02_N8N_WORKFLOWS/PRODUCT_UPDATE_GUIDE_BY_WEBSITE.md`
→ Section: "Method 3: Update Via n8n Workflow"

**Learn the system**
→ File: `01_DOCUMENTATION/ODOO_WEBSITES_AND_SCRIPTS_DOCUMENTATION.md`
→ Read entire document

**Understand architecture**
→ File: `PROJECT_INDEX.md`
→ Then: `01_DOCUMENTATION/ODOO_WEBSITES_AND_SCRIPTS_DOCUMENTATION.md`

**Create custom automation**
→ File: `02_N8N_WORKFLOWS/README_N8N_WORKFLOWS.md`
→ Use Python scripts as templates

---

## 📊 File Organization Structure

```
HIREN_PROJECT_ORGANIZED/
├── 01_DOCUMENTATION/
│   ├── ODOO_WEBSITES_AND_SCRIPTS_DOCUMENTATION.md ← Architecture
│   ├── ODOO_WEBSITE_IDS.md ← Website list
│   ├── ODOO_WEBSITE45_SETUP.md ← Configuration
│   └── ... (50+ more guides)
│
├── 02_N8N_WORKFLOWS/
│   ├── PRODUCT_UPDATE_GUIDE_BY_WEBSITE.md ⭐ ← START HERE
│   ├── README_N8N_WORKFLOWS.md ← N8N guide
│   ├── template-schedule-http-email.json
│   ├── template-webhook-slack-notification.json
│   └── 69 JSON workflow files
│
├── 03_PROJECT_ACCOUNTS/ ← Credentials
├── 04_PROJECT_ARCHITECTURE/ ← System design
├── 05_TEAM_STRUCTURE/ ← Team info
├── 06_ROADMAP/ ← Timeline
├── 07_IMAGES_ASSETS/ ← Product images
├── 08_WORKFLOWS_DATA/ ← Scripts
├── 09_OTHER_RESOURCES/ ← Additional files
│
├── PROJECT_INDEX.md ← Master reference
├── COMPLETION_SUMMARY.md ← What was done
├── FINAL_ORGANIZATION_REPORT.md ← Full report
└── DOCUMENTATION_MAP.md ← This file
```

---

## 🚀 Recommended Reading Order

1. **First**: `PROJECT_INDEX.md` (5 min)
2. **Second**: `PRODUCT_UPDATE_GUIDE_BY_WEBSITE.md` (20 min)
3. **Third**: Choose your method and start building!

---

## 💡 Key Points

✅ All 14 websites in one file: `PRODUCT_UPDATE_GUIDE_BY_WEBSITE.md`
✅ How to update manually: Section "Method 1"
✅ How to update via script: Section "Method 2" + Scripts 1-4
✅ How to automate: Section "Method 3" + JSON template
✅ All credentials in: `03_PROJECT_ACCOUNTS/`

---

**Last Updated**: June 7, 2026
**Status**: Complete Documentation Ready
**Next Step**: Open `PRODUCT_UPDATE_GUIDE_BY_WEBSITE.md` and start!
