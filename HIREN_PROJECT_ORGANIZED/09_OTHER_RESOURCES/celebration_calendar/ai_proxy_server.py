"""
VPS AI Proxy Server — deploy this on Hostinger VPS (or any Linux VPS).
Keeps the Anthropic API key server-side; browser never sees it.

Usage:
  pip install flask anthropic python-dotenv
  python ai_proxy_server.py

Then update AI_PROXY_URL in build_ai_widget.py to your VPS IP/domain.
Port 8765 — open this in your VPS firewall.

CORS is open to all 7 store domains only.
"""

import os, json, re
from datetime import date
from flask import Flask, request, jsonify
from flask_cors import CORS

try:
    import anthropic
except ImportError:
    raise SystemExit("pip install anthropic flask flask-cors")

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")  # set via .env or env var

ALLOWED_ORIGINS = [
    "https://longislandconvenience.com",
    "https://www.longislandconvenience.com",
    "https://longislandballoonsdecor.com",
    "https://www.longislandballoonsdecor.com",
    "https://ligiftbasket.com",
    "https://www.ligiftbasket.com",
    "https://longislandprintandmail.com",
    "https://www.longislandprintandmail.com",
    "https://longislandcards.com",
    "https://www.longislandcards.com",
    "https://jhdadvisor.com",
    "https://www.jhdadvisor.com",
    "https://consultcyber.net",
    "https://www.consultcyber.net",
    "http://localhost",
    "http://127.0.0.1",
]

STORE_CONTEXT = {
    "LongIslandConvenience": {
        "name": "Long Island Convenience",
        "products": "everyday essentials, snacks, drinks, household items, toiletries, candy, beverages",
        "tone": "friendly neighborhood store",
    },
    "LongIslandBalloons": {
        "name": "Long Island Balloons Decor",
        "products": "balloon arrangements, party decorations, custom balloon bouquets, event packages, mylar balloons",
        "tone": "festive and celebratory",
    },
    "LIGiftBasket": {
        "name": "LI Gift Basket",
        "products": "curated gift baskets from $35, gourmet food baskets, wine gift sets, baby shower baskets, corporate gifts",
        "tone": "warm and gift-giving",
    },
    "LongIslandPrintMail": {
        "name": "Long Island Print & Mail",
        "products": "custom invitations, greeting cards, banners, business cards, flyers, custom printing, mailing services",
        "tone": "professional and creative",
    },
    "LongIslandCards": {
        "name": "Long Island Card",
        "products": "sports cards, trading cards, collectibles, greeting cards, rare cards, card grading",
        "tone": "collector-savvy and enthusiastic",
    },
    "HirenKumar": {
        "name": "JHD Advisor",
        "products": "financial planning, business advisory, tax planning, investment guidance, free consultation",
        "tone": "professional and trustworthy",
    },
    "ConsultCyber": {
        "name": "Consult Cyber",
        "products": "cybersecurity assessment, IT consulting, network security, managed IT services, data protection",
        "tone": "expert and reassuring",
    },
}

app = Flask(__name__)
CORS(app, origins=ALLOWED_ORIGINS)


def get_system_prompt(store_key: str, celebration: str, celebration_emoji: str) -> str:
    ctx = STORE_CONTEXT.get(store_key, STORE_CONTEXT["LIGiftBasket"])
    today = date.today().strftime("%B %d, %Y")
    celebration_line = f"Today's special day: {celebration_emoji} {celebration}" if celebration else f"Today is {today}"

    return f"""You are a helpful, friendly shopping assistant for {ctx['name']} on Long Island, New York.

{celebration_line}

Your role:
- Greet visitors warmly in the spirit of today's celebration
- Suggest 2-3 specific products from the store that are perfect for this occasion
- Keep responses SHORT (2-4 sentences max) — this is a chat widget, not an essay
- Mention any available discounts or promo codes when relevant
- Be {ctx['tone']} in tone
- Always end with a clear call to action (browse shop, call, book, etc.)

Store products: {ctx['products']}
Store location: Long Island, New York

Never mention competitors. Keep it upbeat and concise."""


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "date": str(date.today())})


@app.route("/ai-greet", methods=["POST"])
def ai_greet():
    if not ANTHROPIC_API_KEY:
        return jsonify({"error": "API key not configured"}), 500

    data = request.get_json(silent=True) or {}
    store_key   = data.get("store", "LIGiftBasket")
    celebration = data.get("celebration", "")
    emoji       = data.get("emoji", "🎉")
    user_msg    = data.get("message", "Hello! What do you recommend today?")

    # Sanitize inputs
    store_key   = re.sub(r"[^A-Za-z]", "", store_key)[:30]
    celebration = celebration[:80]
    user_msg    = user_msg[:500]

    if store_key not in STORE_CONTEXT:
        store_key = "LIGiftBasket"

    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=200,
            system=get_system_prompt(store_key, celebration, emoji),
            messages=[{"role": "user", "content": user_msg}],
        )
        reply = message.content[0].text
        return jsonify({"reply": reply, "store": store_key, "celebration": celebration})

    except Exception as e:
        return jsonify({"error": str(e)[:200]}), 500


@app.route("/ai-chat", methods=["POST"])
def ai_chat():
    """Multi-turn chat endpoint."""
    if not ANTHROPIC_API_KEY:
        return jsonify({"error": "API key not configured"}), 500

    data = request.get_json(silent=True) or {}
    store_key   = data.get("store", "LIGiftBasket")
    celebration = data.get("celebration", "")
    emoji       = data.get("emoji", "🎉")
    history     = data.get("history", [])  # list of {role, content}
    user_msg    = data.get("message", "")

    store_key = re.sub(r"[^A-Za-z]", "", store_key)[:30]
    if store_key not in STORE_CONTEXT:
        store_key = "LIGiftBasket"

    # Trim history to last 6 turns (12 messages) to avoid token bloat
    history = history[-12:]

    messages = []
    for h in history:
        if h.get("role") in ("user", "assistant") and h.get("content"):
            messages.append({"role": h["role"], "content": str(h["content"])[:300]})
    messages.append({"role": "user", "content": user_msg[:500]})

    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        result = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=200,
            system=get_system_prompt(store_key, celebration, emoji),
            messages=messages,
        )
        reply = result.content[0].text
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)[:200]}), 500


if __name__ == "__main__":
    if not ANTHROPIC_API_KEY:
        print("WARNING: ANTHROPIC_API_KEY not set. Set it as env variable.")
        print("  export ANTHROPIC_API_KEY=sk-ant-...")
    print("Starting AI proxy on port 8765 ...")
    app.run(host="0.0.0.0", port=8765, debug=False)
