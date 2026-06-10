# System Architecture — Hiren Kumar Digital Ecosystem
## SeekHowItHRua | Technical Blueprint

---

## High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                    HIREN KUMAR DIGITAL ECOSYSTEM                     │
│                                                                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │
│  │  Balloon    │  │  Greeting   │  │  Gift Card  │  │  Gift     │  │
│  │  E-Commerce │  │  Card Store │  │  Portal     │  │  Basket   │  │
│  │  (Odoo)     │  │  (Odoo)     │  │  (Odoo)     │  │  (Odoo)   │  │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └─────┬─────┘  │
│         │                │                │               │         │
│  ┌──────┴──────┐  ┌──────┴──────┐  ┌─────┴────────────────┘         │
│  │  Game Cards │  │ Sports Cards│  │  CyberConsulting.net            │
│  │  (Django)   │  │  (Django)   │  │  (Odoo/Hostinger)              │
│  └──────┬──────┘  └──────┬──────┘  └─────────────────────           │
│         └────────────────┘                                           │
│                  │                                                    │
│         ┌────────▼────────┐                                          │
│         │   ODOO ONE DB   │  ← Master ERP (CRM, POS, Accounting,    │
│         │  (Core Platform)│    Inventory, Email, WhatsApp)           │
│         └────────┬────────┘                                          │
│                  │                                                    │
│    ┌─────────────┼─────────────┐                                     │
│    │             │             │                                      │
│    ▼             ▼             ▼                                      │
│  ┌──────┐  ┌──────────┐  ┌──────────┐                               │
│  │ n8n  │  │  Mobile  │  │  VOIP    │                               │
│  │ Auto │  │  App     │  │  Twilio  │                               │
│  │ mation│  │ (RN)     │  │          │                               │
│  └──┬───┘  └──────────┘  └──────────┘                               │
│     │                                                                 │
│     ├── Instagram ── TikTok ── Facebook                              │
│     ├── YouTube ── Pinterest ── Twitter                              │
│     ├── Email Campaigns ── WhatsApp Broadcasts                       │
│     ├── Blog Auto-Publish                                            │
│     └── Lead CRM Auto-Entry                                          │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐   │
│  │              AI / RAG LAYER                                   │   │
│  │  Pinecone │ Claude API │ GPT-4 API │ ElevenLabs │ Runway ML  │   │
│  └───────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Infrastructure Map

### Hosting
| Service | Host | Purpose |
|---------|------|---------|
| Odoo One | Odoo Cloud | Main ERP + 5 Odoo sites |
| Custom Sites (5, 6) | Hostinger VPS | Django + React apps |
| n8n | Hostinger VPS | Automation engine |
| CyberConsulting.net | Hostinger | Static/Odoo site |
| CDN | Cloudflare | All domains |

### Domain Strategy
| Domain | Site | DNS |
|--------|------|-----|
| hirenballoons.com | Balloon E-Commerce | Cloudflare |
| hirengreetings.com | Greeting Cards | Cloudflare |
| hirengiftcards.com | Gift Card Portal | Cloudflare |
| hirengiftbaskets.com | Gift Basket Store | Cloudflare |
| hirengamecards.com | Game/Gambling Cards | Cloudflare |
| hirenspotscards.com | Sports Cards | Cloudflare |
| cyberconsulting.net | Cyber Consulting | Cloudflare (existing) |

*Note: Final domain names to be confirmed by Hiren.*

### Data Flow
```
Customer Action
     ↓
Website/App (Odoo or Django)
     ↓
Event published to n8n webhook
     ↓
n8n routes to: Email / WhatsApp / Social / CRM / Analytics
     ↓
Odoo CRM/Database updated
     ↓
Reporting Dashboard (Odoo + Metabase)
```

---

## Security Architecture

```
Internet ──→ Cloudflare WAF ──→ Load Balancer ──→ App Servers
                │                                      │
                ├── DDoS Protection                    ├── HTTPS Only (TLS 1.3)
                ├── Rate Limiting                      ├── JWT Authentication
                ├── Bot Protection                     ├── Input Sanitization
                └── Geo-Blocking (if needed)           └── SQL Injection Prevention
```

### Compliance
- **PCI-DSS:** Payment processing via Stripe/PayPal (they handle card data; we never store raw card numbers)
- **New York Sales Tax:** Automated via Odoo Tax module
- **GDPR/CCPA:** Privacy policy + cookie consent on all sites
- **SSL:** Wildcard SSL on all domains

---

## Database Architecture

### Odoo PostgreSQL
- Single Odoo instance with multi-website feature
- All 5 Odoo sites share one product/customer/inventory database
- Financial separation by website for reporting

### Custom Sites (Django)
- Separate PostgreSQL databases for Sites 5 & 6
- Redis for session management and caching
- Celery for async task processing
- Connection to Odoo via REST API for unified inventory

---
