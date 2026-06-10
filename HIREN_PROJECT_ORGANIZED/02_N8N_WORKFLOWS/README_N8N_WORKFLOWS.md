# N8N Workflows - Hiren Kumar Project

**Location**: This folder contains all n8n workflow JSON files for Hiren Kumar's digital transformation project.

---

## 📋 Workflow Categories

N8N workflows are automation sequences that connect different tools and systems. Place JSON files in this folder organized by category:

### 1. **E-Commerce Workflows**
- `ecommerce-order-sync.json` - Sync orders from Odoo to fulfillment
- `ecommerce-inventory-update.json` - Update inventory across all 7 websites
- `ecommerce-customer-sync.json` - Sync customers from websites to CRM
- `ecommerce-product-import.json` - Import products to Odoo

### 2. **CRM & Customer Management**
- `crm-lead-capture.json` - Capture leads from website forms
- `crm-email-sequence.json` - Automated email sequences
- `crm-customer-enrichment.json` - Add customer data from external sources
- `crm-followup-automation.json` - Follow-up tasks for salespeople

### 3. **Accounting & Finance**
- `accounting-invoice-generation.json` - Auto-generate invoices from orders
- `accounting-payment-reconciliation.json` - Reconcile payments
- `accounting-expense-tracking.json` - Track business expenses
- `accounting-financial-reports.json` - Generate financial reports

### 4. **Marketing Automation**
- `marketing-social-media-posting.json` - Auto-post to social media
- `marketing-email-campaigns.json` - Email marketing sequences
- `marketing-lead-scoring.json` - Score and rank leads
- `marketing-analytics-sync.json` - Sync analytics to dashboard

### 5. **Inventory & Warehouse**
- `inventory-stock-sync.json` - Sync stock across locations
- `inventory-reorder-alerts.json` - Alert when stock is low
- `inventory-supplier-orders.json` - Auto-create supplier orders
- `inventory-barcode-tracking.json` - Track items by barcode

### 6. **Mobile App Integration**
- `mobile-push-notifications.json` - Send push notifications
- `mobile-order-sync.json` - Sync orders from mobile app
- `mobile-user-registration.json` - Handle app registrations
- `mobile-payment-processing.json` - Process mobile payments

### 7. **Data Syncing & Backups**
- `data-backup-schedule.json` - Automated daily backups
- `data-sync-all-systems.json` - Master sync workflow
- `data-cleanup-archive.json` - Archive old data
- `data-error-reporting.json` - Log and report errors

### 8. **Reporting & Analytics**
- `reports-daily-summary.json` - Daily business summary
- `reports-sales-analytics.json` - Sales performance reports
- `reports-customer-analytics.json` - Customer behavior analytics
- `reports-inventory-analytics.json` - Inventory reports

---

## 🚀 How to Use This Folder

### Adding a New Workflow

1. **Export from N8N**:
   - In n8n, go to your workflow
   - Click Menu → Download → Workflow
   - Save as `workflow-name.json`

2. **Place in This Folder**:
   - Save JSON file to `02_N8N_WORKFLOWS/`
   - Name format: `category-workflow-name.json`
   - Example: `ecommerce-order-sync.json`

3. **Document the Workflow**:
   - Add entry to list above
   - Include brief description
   - Note any dependencies

### Importing a Workflow

1. **In N8N**:
   - Click "Open" or "Import"
   - Select the JSON file from this folder
   - Configure credentials/connections
   - Test and activate

2. **Update the List**:
   - Mark as "Imported" in documentation
   - Note the workflow ID
   - Record any custom configuration

---

## 📊 Workflow Structure

A typical n8n workflow JSON contains:

```json
{
  "nodes": [
    {
      "name": "Trigger",
      "type": "schedule",
      "parameters": {
        "interval": ["daily"],
        "triggerAtHour": 8
      }
    },
    {
      "name": "Fetch Data",
      "type": "http",
      "parameters": {
        "url": "https://api.example.com/data"
      }
    },
    {
      "name": "Process Data",
      "type": "code",
      "parameters": {
        "jsCode": "// JavaScript code here"
      }
    },
    {
      "name": "Send Result",
      "type": "email",
      "parameters": {
        "to": "admin@example.com"
      }
    }
  ],
  "connections": {
    "Trigger": {
      "main": [["Fetch Data"]]
    },
    "Fetch Data": {
      "main": [["Process Data"]]
    },
    "Process Data": {
      "main": [["Send Result"]]
    }
  }
}
```

---

## 🔗 N8N Connection Configuration

### Required Credentials Setup

Before importing workflows, ensure these credentials are configured in N8N:

| Service | Credential Type | Purpose |
|---------|-----------------|---------|
| **Odoo** | Odoo API | Product/Order/Customer sync |
| **Gmail** | OAuth 2.0 | Email automation |
| **Slack** | Webhook | Notifications |
| **Twilio** | API Key | SMS notifications |
| **Stripe** | API Key | Payment processing |
| **Shopify** | OAuth 2.0 | E-commerce sync |
| **Google Sheets** | OAuth 2.0 | Data storage |
| **Zapier** | Webhook | Integration hub |
| **Airtable** | API Key | Database sync |
| **Facebook** | OAuth 2.0 | Social media posting |

### Configuration Steps

1. Go to N8N Settings → Credentials
2. Click "Create New"
3. Select credential type
4. Enter API key/token
5. Save and test connection
6. Use in workflows

---

## 📈 Common Workflow Patterns

### Pattern 1: Schedule + Fetch + Process + Send

```
[Schedule Trigger] 
    ↓
[HTTP Request - Fetch Data]
    ↓
[Code Node - Transform]
    ↓
[Email - Send Result]
```

### Pattern 2: Webhook + Database + Notification

```
[Webhook Trigger]
    ↓
[Database Query]
    ↓
[Slack Message]
```

### Pattern 3: Multi-App Sync

```
[Odoo Webhook]
    ↓
[Get Product Details]
    ↓
[Split into Website Updates]
    ├─ [Update Website 1]
    ├─ [Update Website 2]
    └─ [Update Website 3]
    ↓
[Send Confirmation Email]
```

---

## 🔧 Troubleshooting N8N Workflows

### Common Issues

| Issue | Solution |
|-------|----------|
| Workflow not triggering | Check trigger configuration, verify credentials |
| API errors | Validate API endpoints, check rate limits |
| Missing data | Check node mapping, verify field names |
| Timeout errors | Increase timeout in HTTP nodes |
| Authentication failed | Re-verify credentials, check API keys |

### Debug Techniques

1. **Enable Debug Mode**:
   - In N8N, click "Debug" button
   - Run workflow manually
   - Check each node's output

2. **Add Logging**:
   - Use Code nodes to log data
   - Check N8N logs for errors
   - Test each connection separately

3. **Test Individually**:
   - Disable downstream nodes
   - Test trigger first
   - Add nodes one at a time

---

## 📁 Folder Structure

```
02_N8N_WORKFLOWS/
├── README_N8N_WORKFLOWS.md (this file)
├── TEMPLATES/
│   ├── template-schedule-http-email.json
│   ├── template-webhook-database-notify.json
│   └── template-multi-app-sync.json
├── ECOMMERCE/
│   ├── ecommerce-order-sync.json
│   ├── ecommerce-inventory-update.json
│   └── ecommerce-product-import.json
├── CRM/
│   ├── crm-lead-capture.json
│   ├── crm-email-sequence.json
│   └── crm-customer-enrichment.json
├── ACCOUNTING/
│   ├── accounting-invoice-generation.json
│   └── accounting-payment-reconciliation.json
├── MARKETING/
│   ├── marketing-social-media-posting.json
│   ├── marketing-email-campaigns.json
│   └── marketing-lead-scoring.json
├── INVENTORY/
│   ├── inventory-stock-sync.json
│   └── inventory-reorder-alerts.json
├── MOBILE/
│   ├── mobile-push-notifications.json
│   └── mobile-order-sync.json
├── DATA_SYNC/
│   ├── data-backup-schedule.json
│   └── data-sync-all-systems.json
├── REPORTING/
│   ├── reports-daily-summary.json
│   └── reports-sales-analytics.json
└── ARCHIVE/
    └── (old/deprecated workflows)
```

---

## 🎯 Project Workflows Summary

**For Hiren Kumar's Project**, the key workflows are:

1. **Order Management** - Sync orders across 7 websites to Odoo
2. **Inventory Sync** - Keep stock levels updated across all channels
3. **Customer Data** - Consolidate customer info from multiple sources
4. **Email Automation** - Marketing sequences and notifications
5. **Reporting** - Daily/weekly business summaries
6. **Backup** - Automated data backups every night

---

## 📞 Support & Resources

- **N8N Docs**: https://docs.n8n.io/
- **N8N Community**: https://community.n8n.io/
- **API Documentation**: Check individual service docs
- **Project Manager**: Sachin (kahpk1933@gmail.com)

---

**Last Updated**: June 7, 2026
**Status**: Ready for workflow implementation
**Next Step**: Create and test workflows for each business process
