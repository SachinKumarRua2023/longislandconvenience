# AI Proxy VPS Setup Guide

## What This Does
A lightweight Flask server on your Hostinger VPS receives requests from all 7 store chat widgets
and calls the Claude AI API — so the API key stays server-side, never exposed in the browser.

## Step 1 — Deploy on Hostinger VPS

SSH into your VPS, then:

```bash
# Install Python deps
pip install flask flask-cors anthropic

# Upload the proxy file
# Copy ai_proxy_server.py to /home/hiren/ai_proxy/

mkdir -p /home/hiren/ai_proxy
# (upload file via SFTP or paste content)

# Set your API key
export ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE

# Run (test first)
python /home/hiren/ai_proxy/ai_proxy_server.py
```

## Step 2 — Keep It Running (systemd)

```bash
sudo nano /etc/systemd/system/ai-proxy.service
```

Paste:
```ini
[Unit]
Description=AI Proxy for Hiren Kumar stores
After=network.target

[Service]
User=hiren
WorkingDirectory=/home/hiren/ai_proxy
Environment=ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE
ExecStart=/usr/bin/python3 ai_proxy_server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable ai-proxy
sudo systemctl start ai-proxy
sudo systemctl status ai-proxy
```

## Step 3 — Open Port 8765

In Hostinger VPS firewall / control panel:
- Allow inbound TCP on port **8765**

Or via UFW:
```bash
sudo ufw allow 8765/tcp
```

## Step 4 — Update AI_PROXY_URL

Edit `build_ai_widget.py`:
```python
AI_PROXY_URL = "https://YOUR_VPS_IP:8765"
# e.g. AI_PROXY_URL = "https://142.93.12.34:8765"
```

Then re-run the injector to push the updated URL to all homepages:
```bash
python inject_ai_widget.py
```

## Step 5 — HTTPS (Recommended)

Use Caddy for easy HTTPS reverse proxy:
```bash
sudo apt install -y caddy
sudo nano /etc/caddy/Caddyfile
```

Paste (replace with your domain):
```
ai.longislandconvenience.com {
    reverse_proxy localhost:8765
}
```

Then update `AI_PROXY_URL = "https://ai.longislandconvenience.com"`.

## Test the Proxy

```bash
curl -X POST https://YOUR_VPS_IP:8765/ai-greet \
  -H "Content-Type: application/json" \
  -d '{"store":"LIGiftBasket","celebration":"Memorial Day","emoji":"🎖️","message":"What should I buy?"}'
```

Expected response:
```json
{"reply": "Happy Memorial Day! ...", "store": "LIGiftBasket", "celebration": "Memorial Day"}
```

## What Happens Without VPS

The chat widget still appears on all 7 homepages, but the AI chat will show:
> "Sorry, the assistant is temporarily unavailable. Please call us or browse the shop!"

The celebration toast notification, countdown banners, and email/WhatsApp automation
all continue working regardless of whether the VPS proxy is running.

## Cost

- Claude Haiku API: ~$0.00025 per message (250 messages = $0.06)
- Typical monthly cost for all 7 stores: **under $5/month**
