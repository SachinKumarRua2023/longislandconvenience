# Blog Automation - Technical Reference

**For:** Developers, System Administrators, Integration Engineers  
**Level:** Advanced  
**Date:** June 9, 2026

---

## 📖 Table of Contents

1. [API Integration](#api-integration)
2. [Workflow Nodes](#workflow-nodes)
3. [Python Scripts](#python-scripts)
4. [Configuration Reference](#configuration-reference)
5. [Data Structures](#data-structures)
6. [Error Codes](#error-codes)
7. [Performance Tuning](#performance-tuning)

---

## API Integration

### Odoo JSON-RPC API

**Endpoint:** `https://country-cove-inc.odoo.com/jsonrpc`

#### Authentication

```json
{
  "jsonrpc": "2.0",
  "method": "call",
  "params": {
    "service": "common",
    "method": "authenticate",
    "args": [
      "country-cove-inc",
      "countrycoveinc@gmail.com",
      "M@nhattan1234",
      {}
    ]
  },
  "id": 1
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": 2,
  "id": 1
}
```

**Returns:** `uid` (integer) - User ID for authenticated session

---

#### Fetch Products

```json
{
  "jsonrpc": "2.0",
  "method": "call",
  "params": {
    "service": "object",
    "method": "execute",
    "args": [
      "country-cove-inc",
      2,
      "M@nhattan1234",
      "product.product",
      "search_read",
      [
        [
          ["sale_ok", "=", true],
          ["website_id", "=", 1]
        ]
      ],
      ["id", "name", "description", "list_price", "category_id", "image_1920"]
    ]
  },
  "id": 2
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": [
    {
      "id": 1234,
      "name": "Pokemon Cards Booster Box",
      "description": "Official Pokemon Trading Card Set",
      "list_price": 39.99,
      "category_id": [8, "Trading Cards"],
      "image_1920": "base64_encoded_image_data"
    }
  ],
  "id": 2
}
```

**Query Parameters:**
- `sale_ok = true` - Only saleable products
- `website_id = {id}` - Specific website
- Add `limit=50` to limit results

---

#### Create Blog Post

```json
{
  "jsonrpc": "2.0",
  "method": "call",
  "params": {
    "service": "object",
    "method": "execute",
    "args": [
      "country-cove-inc",
      2,
      "M@nhattan1234",
      "blog.post",
      "create",
      [
        {
          "name": "Pokemon Cards Long Island: Buying Guide",
          "subtitle": "Complete guide to trading cards on Long Island",
          "content": "<h2>Introduction</h2><p>Content here...</p>",
          "blog_id": 3,
          "website_id": 1,
          "author_id": 1,
          "is_published": true,
          "seo_description": "Learn about Pokemon cards trading Long Island",
          "teaser_include": true,
          "post_category_ids": [[6, false, []]]
        }
      ]
    ]
  },
  "id": 3
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": 42,
  "id": 3
}
```

**Returns:** `post_id` (integer) - ID of created blog post

---

### Claude API Integration

**Endpoint:** `https://api.anthropic.com/v1/messages`

#### Request Format

```json
{
  "model": "claude-3-5-sonnet-20241022",
  "max_tokens": 2000,
  "messages": [
    {
      "role": "user",
      "content": "Generate a professional SEO blog post about [product] for [website]..."
    }
  ],
  "temperature": 0.7
}
```

**Headers:**
```
Authorization: Bearer sk-ant-{api_key}
Content-Type: application/json
anthropic-version: 2023-06-01
```

#### Response Format

```json
{
  "id": "msg_...",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "{\n  \"title\": \"Pokemon Cards...\",\n  \"meta_description\": \"...\",\n  \"body_html\": \"<h2>...</h2>...\"\n}"
    }
  ],
  "model": "claude-3-5-sonnet-20241022",
  "stop_reason": "end_turn",
  "usage": {
    "input_tokens": 287,
    "output_tokens": 524
  }
}
```

---

## Workflow Nodes

### 1. Schedule Trigger

**Type:** `n8n-nodes-base.scheduleTrigger`  
**Version:** 1

**Configuration:**
```json
{
  "interval": ["days"],
  "triggerAtHour": 10,
  "triggerAtMinute": 0,
  "timezone": "America/New_York"
}
```

**Outputs:** Empty (triggers workflow)

**Cron Expression:** `0 10 * * *` (10 AM every day)

---

### 2. HTTP Request (Authenticate)

**Type:** `n8n-nodes-base.httpRequest`  
**Version:** 4.1

**Configuration:**
```json
{
  "method": "POST",
  "url": "https://country-cove-inc.odoo.com/jsonrpc",
  "authentication": "none",
  "sendBody": true,
  "bodyParameters": {
    "parameters": [
      {
        "name": "body",
        "value": "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"common\",\"method\":\"authenticate\",...}}"
      }
    ]
  },
  "sendHeaders": true,
  "headerParameters": {
    "parameters": [
      {
        "name": "Content-Type",
        "value": "application/json"
      }
    ]
  }
}
```

**Timeout:** 30000ms

---

### 3. Code Node (Extract UID)

**Type:** `n8n-nodes-base.code`  
**Version:** 2  
**Language:** JavaScript

```javascript
// Extract UID from Odoo auth response
const authResponse = $input.first().json;
return {
  uid: authResponse.result,
  db: 'country-cove-inc',
  url: 'https://country-cove-inc.odoo.com',
  timestamp: new Date().toISOString()
};
```

**Input:** HTTP response from auth
**Output:** Object with `uid`, `db`, `url`, `timestamp`

---

### 4. Split In Batches (Loop Products)

**Type:** `n8n-nodes-base.splitInBatches`  
**Version:** 3

**Configuration:**
```json
{
  "resource": "loop",
  "mode": "each",
  "loopCharacteristics": {
    "isSequential": true
  }
}
```

**Processes:** Each product individually through loop

---

### 5. OpenAI/Claude (Generate Blog)

**Type:** `n8n-nodes-base.openAi`  
**Version:** 3

**Configuration:**
```json
{
  "model": "claude-3-5-sonnet-20241022",
  "messages": {
    "messageValues": [
      {
        "content": "Generate a professional SEO blog post about {{$json.name}} for Long Island e-commerce..."
      }
    ]
  },
  "temperature": 0.7,
  "maxTokens": 2000
}
```

**Input Variables:**
- `$json.name` - Product name
- `$json.description` - Product details
- `$json.category` - Product category

---

### 6. Code Node (Format Blog Data)

**Type:** `n8n-nodes-base.code`  
**Version:** 2

```javascript
const content = $input.first().json.choices[0].message.content;
let blogData;

try {
  blogData = JSON.parse(content);
} catch(e) {
  // Parse failed, use content as body
  blogData = {
    title: `${$json.name} - Long Island Guide`,
    body_html: content,
    meta_description: `Discover ${$json.name} at Long Island Convenience.`
  };
}

return {
  ...blogData,
  product_id: $json.id,
  product_name: $json.name,
  website_id: 1,
  website_name: 'Long Island Convenience',
  domain: 'https://www.longislandconvenience.com',
  publish_date: new Date().toISOString().split('T')[0]
};
```

---

### 7. HTTP Request (Publish to Odoo)

**Type:** `n8n-nodes-base.httpRequest`  
**Version:** 4.1

**Dynamic Body:**
```json
{
  "jsonrpc": "2.0",
  "method": "call",
  "params": {
    "service": "object",
    "method": "execute",
    "args": [
      "country-cove-inc",
      {{$node["extract-auth"].json.uid}},
      "M@nhattan1234",
      "blog.post",
      "create",
      [{
        "name": "{{$json.title}}",
        "subtitle": "{{$json.meta_description}}",
        "content": "{{$json.body_html}}",
        "blog_id": 3,
        "website_id": 1,
        "author_id": 1,
        "is_published": true
      }]
    ]
  },
  "id": 3
}
```

---

## Python Scripts

### odoo_blog_automation_engine.py

**Main Class:** `OdooBlogAutomation`

#### Methods

##### `__init__(odoo_config: Dict = None)`
Initializes engine with Odoo configuration. Automatically authenticates.

```python
engine = OdooBlogAutomation()
if not engine.uid:
    print("Authentication failed")
```

---

##### `_authenticate() -> bool`
Authenticates with Odoo JSON-RPC. Sets `self.uid`.

```python
if engine._authenticate():
    print(f"Authenticated as UID: {engine.uid}")
```

---

##### `fetch_products(website_id: int, limit: int = 50) -> List[Dict]`
Fetches products from Odoo for specific website.

```python
products = engine.fetch_products(website_id=1, limit=10)
for product in products:
    print(f"Product: {product['name']} (${product['list_price']})")
```

**Returns:**
```python
[
  {
    "id": 1234,
    "name": "Pokemon Cards",
    "description": "...",
    "list_price": 39.99,
    "category_id": [8, "Cards"],
    "image_1920": "base64_data"
  }
]
```

---

##### `generate_seo_blog_content(website_id: int, product: Dict, blog_category: str) -> Dict`
Generates SEO-optimized blog content for a product.

```python
blog_data = engine.generate_seo_blog_content(
    website_id=1,
    product={"id": 123, "name": "Pokemon Cards"},
    blog_category="pokemon"
)

print(f"Title: {blog_data['title']}")
print(f"Words: {len(blog_data['body_html'].split())}")
print(f"SEO Score: {engine._calculate_seo_score(blog_data)}/100")
```

**Returns:**
```python
{
  "title": "Pokemon Cards Long Island: Complete Guide 2026",
  "meta_description": "Discover Pokemon cards at Long Island...",
  "body_html": "<h2>...</h2>...",
  "meta_tags": {...},
  "schema_org": {...},
  "product_id": 123,
  "website_id": 1,
  "author": "Hiren Kumar Digital",
  "publish_date": "2026-06-09"
}
```

---

##### `publish_blog_to_odoo(website_id: int, blog_section_id: int, blog_data: Dict) -> Tuple[bool, str]`
Publishes blog post to Odoo.

```python
success, post_url = engine.publish_blog_to_odoo(
    website_id=1,
    blog_section_id=3,
    blog_data=blog_data
)

if success:
    print(f"Published: {post_url}")
```

**Returns:** `(True, "https://..."), (False, "")`

---

##### `submit_to_google_search_console(blog_url: str) -> bool`
Logs blog URL for GSC submission.

```python
engine.submit_to_google_search_console("https://www.longislandconvenience.com/blog/...")
```

---

##### `log_blog_metrics(blog_data: Dict, post_url: str) -> Dict`
Logs metrics for monitoring.

```python
metrics = engine.log_blog_metrics(blog_data, post_url)
print(f"SEO Score: {metrics['seo_score']}/100")
print(f"Word Count: {metrics['word_count']}")
```

---

### odoo_blog_automation_config.py

#### ODOO_CONFIG
```python
ODOO_CONFIG = {
    "url": "https://country-cove-inc.odoo.com",
    "db": "country-cove-inc",
    "user": "countrycoveinc@gmail.com",
    "password": "M@nhattan1234",
    "api_endpoint": "/jsonrpc"
}
```

#### WEBSITES
```python
WEBSITES = {
    1: {
        "name": "Long Island Convenience",
        "domain": "https://www.longislandconvenience.com",
        "blog_sections": {3: "Balloons & Party", 5: "Gift Baskets", 7: "Convenience"},
        "product_categories": {...},
        "geo_keywords": ["Long Island", "Plainview NY", "Nassau County"]
    },
    36: {...},
    37: {...},
    38: {...},
    39: {...}
}
```

---

## Configuration Reference

### SCHEDULE

```python
SCHEDULE = {
    "frequency": "daily",           # daily, weekly, manual
    "time": "10:00",               # HH:MM format (ET)
    "timezone": "America/New_York",
    "posts_per_website_per_day": 1,
    "batch_size": 5                # Products per batch
}
```

### SEO_CONFIG

```python
SEO_CONFIG = {
    "min_word_count": 750,
    "max_word_count": 1200,
    "min_headings": 4,
    "include_faq": True,
    "include_schema": True,
    "internal_links": True,
    "meta_description_length": 155,
    "focus_keywords": True,
    "include_cta": True
}
```

### IMAGE_CONFIG

```python
IMAGE_CONFIG = {
    "width": 1200,
    "height": 630,
    "brand_colors": {
        "primary": "#6b3e4a",   # Burgundy
        "accent": "#d4af37",    # Gold
        "secondary": "#e94b7f"  # Pink
    }
}
```

---

## Data Structures

### Product Object

```python
{
    "id": int,
    "name": str,
    "description": str,
    "list_price": float,
    "category_id": [int, str],
    "image_1920": str  # Base64 encoded
}
```

---

### Blog Data Object

```python
{
    "product_id": int,
    "product_name": str,
    "website_id": int,
    "website_name": str,
    "website_domain": str,
    "category": str,
    "publish_date": str,  # YYYY-MM-DD
    "author": str,
    "title": str,
    "meta_description": str,  # ~155 chars
    "body_html": str,  # HTML formatted
    "meta_tags": {
        "keywords": str,
        "robots": str,
        "og:title": str,
        "og:description": str,
        "og:type": str,
        "article:author": str,
        "article:published_time": str
    },
    "schema_org": {
        "@context": str,
        "@type": str,
        "headline": str,
        "description": str,
        "author": {...},
        "publisher": {...},
        "datePublished": str,
        "url": str
    }
}
```

---

### Metrics Object

```python
{
    "timestamp": str,  # ISO format
    "website": str,
    "product": str,
    "title": str,
    "url": str,
    "seo_score": int,  # 0-100
    "word_count": int,
    "meta_description_length": int
}
```

---

## Error Codes

### Odoo Errors

| Code | Message | Solution |
|------|---------|----------|
| 401 | Unauthorized | Verify credentials |
| 404 | Method not found | Check model/method name |
| 500 | Server error | Check Odoo instance |
| Request timeout | Connection failed | Check network/URL |

### Claude API Errors

| Code | Message | Solution |
|------|---------|----------|
| 401 | Invalid API key | Verify API key |
| 429 | Rate limit exceeded | Wait before retrying |
| 500 | Internal server error | Retry in 60 seconds |
| 503 | Service unavailable | Check API status |

### N8N Errors

| Code | Message | Solution |
|------|---------|----------|
| Node failed | See error details | Check node configuration |
| Timeout | Operation too slow | Increase timeout setting |
| Memory exceeded | Too much data | Reduce batch size |

---

## Performance Tuning

### Optimize Product Fetch

**Default:** Fetches all fields for all products
**Optimized:** Fetch only needed fields

```python
# In odoo_blog_automation_engine.py, modify fetch_products():
fields = ["id", "name", "description", "list_price"]  # Remove image for speed
```

### Optimize Blog Generation

**Default:** Full 800-900 word blog per product
**Fast:** 400-500 word blog

```python
# Modify prompt in workflow:
"Generate a 500-word SEO blog post..."  # Changed from 750-900
```

### Batch Processing

**Default:** Process 5 products sequentially
**Parallel:** Process multiple at once

```json
{
  "resource": "loop",
  "mode": "batch",
  "loopCharacteristics": {"batchSize": 5}
}
```

### Caching

**Add Redis cache for product data:**

```python
import redis
cache = redis.Redis(host='localhost', port=6379)

# Cache products for 1 hour
cache.set(f"products_{website_id}", json.dumps(products), ex=3600)
```

---

## Monitoring & Logging

### Enable Detailed Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.info(f"Fetched {len(products)} products")
logger.warning(f"Product {id} has no description")
logger.error(f"Failed to publish blog post: {error}")
```

### Monitor N8N Execution

**Check execution logs:**
```bash
n8n list-workflows
n8n get-workflow --id <workflow-id>
```

**Monitor database:**
```sql
SELECT * FROM execution_entity 
WHERE workflow_id = <workflow-id> 
ORDER BY createdAt DESC 
LIMIT 10;
```

---

## Advanced Customization

### Custom Blog Template

```python
BLOG_TEMPLATES["custom"] = {
    "title_template": "Your Custom Title {location} {year}",
    "keywords": ["key1", "key2", "key3"],
    "sections": [
        "Section 1",
        "Section 2",
        "Section 3"
    ]
}
```

### Custom Product Filter

```python
# Modify search criteria in fetch_products():
domain = [
    ["sale_ok", "=", True],
    ["website_id", "=", website_id],
    ["list_price", ">", 10],  # Only products > $10
    ["categ_id.name", "=", "Cards"]  # Only specific category
]
```

### Custom Image Generation

Integrate with image API (Canva, Cloudinary):

```python
def generate_cover_image(blog_data: Dict) -> str:
    """Generate cover image via API"""
    image_data = create_image_api_request(
        title=blog_data["title"],
        subtitle=blog_data["meta_description"],
        colors=IMAGE_CONFIG["brand_colors"]
    )
    return upload_to_odoo(image_data)
```

---

## Testing

### Unit Tests

```python
import pytest

def test_fetch_products():
    engine = OdooBlogAutomation()
    products = engine.fetch_products(website_id=1, limit=5)
    assert len(products) > 0
    assert "id" in products[0]
    assert "name" in products[0]

def test_generate_blog():
    engine = OdooBlogAutomation()
    blog_data = engine.generate_seo_blog_content(
        website_id=1,
        product={"id": 123, "name": "Test Product"},
        blog_category="balloons"
    )
    assert blog_data["title"]
    assert len(blog_data["body_html"]) > 500
    assert blog_data["meta_description"]
```

### Integration Tests

```bash
# Test full workflow
python odoo_blog_automation_engine.py \
    --website-id 1 \
    --limit 3 \
    --dry-run
```

---

## Deployment

### Docker

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "odoo_blog_automation_engine.py"]
```

### Requirements.txt

```
requests>=2.28.0
python-dotenv>=0.19.0
Pillow>=9.0.0
redis>=4.0.0
```

---

**Document Version:** 1.0  
**Last Updated:** June 9, 2026  
**Maintainer:** Sachin Kumar

