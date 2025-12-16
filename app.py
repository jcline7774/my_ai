# app.py
import os
from flask import Flask, request, jsonify, render_template
import requests
try:
    from dotenv import load_dotenv
    load_dotenv()  # Load .env file for local development
except ImportError:
    pass  # dotenv not available in production

app = Flask(__name__)

# Environment configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.2-1b-instruct")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"


def call_openrouter(messages, model=None, max_tokens=512, temperature=0.7):
    """Send request to OpenRouter and log full debug info."""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://your-service.com",  # optional but recommended
        "X-Title": "AI Microservice",
    }

    final_model = model if model and model.strip() else OPENROUTER_MODEL

    body = {
        "model": final_model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    try:
        r = requests.post(OPENROUTER_URL, headers=headers, json=body, timeout=60)

        print("DEBUG status:", r.status_code, flush=True)
        print("DEBUG text:", r.text[:500], flush=True)  # first 500 chars for safety

        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": "OpenRouter call failed", "details": str(e)}


def call_groq(messages, model=None, max_tokens=512, temperature=0.7):
    """Send request to Groq (free and fast)."""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    final_model = model if model and model.strip() else GROQ_MODEL

    body = {
        "model": final_model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    try:
        r = requests.post(GROQ_URL, headers=headers, json=body, timeout=60)
        print("DEBUG Groq status:", r.status_code, flush=True)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": "Groq call failed", "details": str(e)}


def call_deepseek(messages, model=None, max_tokens=512, temperature=0.7):
    """Send request to DeepSeek (truly free)."""
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }

    final_model = model if model and model.strip() else DEEPSEEK_MODEL

    body = {
        "model": final_model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    try:
        r = requests.post(DEEPSEEK_URL, headers=headers, json=body, timeout=60)
        print("DEBUG DeepSeek status:", r.status_code, flush=True)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": "DeepSeek call failed", "details": str(e)}


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/api", methods=["GET"])
def api_info():
    return jsonify({"status": "running", "message": "Welcome to my-ai-tiger"})


@app.route("/health", methods=["GET"])
def health():
    print("Health check called", flush=True)
    return jsonify({"status": "ok"}), 200


@app.route("/generate", methods=["POST"])
def generate():
    provider = request.headers.get(
        "X-Provider", request.args.get("provider", "groq")
    ).lower()

    payload = request.get_json(force=True, silent=True) or {}
    print("DEBUG /generate payload:", payload, flush=True)

    if "messages" in payload:
        messages = payload["messages"]
    else:
        prompt = payload.get("prompt", "")
        messages = [{"role": "user", "content": prompt}]

    model = payload.get("model")
    max_tokens = payload.get("max_tokens", 512)
    temperature = payload.get("temperature", 0.7)

    try:
        if provider == "groq":
            model = model or GROQ_MODEL
            if not GROQ_API_KEY:
                return jsonify({"error": "GROQ_API_KEY not configured"}), 500
            print("DEBUG Calling Groq with model:", model, flush=True)
            result = call_groq(messages, model, max_tokens, temperature)
        elif provider == "deepseek":
            model = model or DEEPSEEK_MODEL
            if not DEEPSEEK_API_KEY:
                return jsonify({"error": "DEEPSEEK_API_KEY not configured"}), 500
            print("DEBUG Calling DeepSeek with model:", model, flush=True)
            result = call_deepseek(messages, model, max_tokens, temperature)
        else:
            model = model or OPENROUTER_MODEL
            if not OPENROUTER_API_KEY:
                return jsonify({"error": "OPENROUTER_API_KEY not configured"}), 500
            print("DEBUG Calling OpenRouter with model:", model, flush=True)
            result = call_openrouter(messages, model, max_tokens, temperature)
        
        print("DEBUG API response:", result, flush=True)

        # Extract assistant reply
        content = None
        if isinstance(result, dict):
            choices = result.get("choices", [])
            if choices:
                first = choices[0]
                if "message" in first and "content" in first["message"]:
                    content = first["message"]["content"]
                elif "text" in first:
                    content = first["text"]

        return jsonify({"response": content, "raw": result}), 200

    except requests.HTTPError as e:
        try:
            return (
                jsonify({"error": "upstream_error", "details": e.response.json()}),
                e.response.status_code,
            )
        except Exception:
            return jsonify({"error": "upstream_error", "details": str(e)}), 502
    except Exception as e:
        return jsonify({"error": "internal_error", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
