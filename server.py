

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
import os
import datetime
import logging
import traceback
from typing import Tuple, Dict

# ------------------------------------------------------------------------------
# Flask Setup
# ------------------------------------------------------------------------------
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# ------------------------------------------------------------------------------
# Logging Setup
# ------------------------------------------------------------------------------
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

log_file = os.path.join(LOG_DIR, f"server_{datetime.date.today()}.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("translation_app")

# ------------------------------------------------------------------------------
# API Key Setup
# ------------------------------------------------------------------------------
API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBcil4TZYlDHxihw3wAzttx9dM2igba5b4")

if not API_KEY:
    logger.error("No Gemini API key found. Please set GEMINI_API_KEY env variable.")
else:
    genai.configure(api_key=API_KEY)

# ------------------------------------------------------------------------------
# Utility Functions
# ------------------------------------------------------------------------------

def build_prompt(text: str) -> str:
    """
    Build the translation prompt for Gemini.
    """
    return (
        f"Translate the following text into Hindi and Spanish.\n\n"
        f"Text: {text}\n\n"
        "Return output exactly in this format (no extra commentary, no quotes):\n"
        "Hindi: <hindi translation>\n"
        "Spanish: <spanish translation>\n"
    )


def parse_translation(raw_text: str) -> Tuple[str, str]:
    """
    Parse Gemini output to extract Hindi and Spanish translations.
    Returns (hindi, spanish). Empty strings if parsing fails.
    """
    hindi = ""
    spanish = ""

    for line in raw_text.splitlines():
        line = line.strip()
        if line.lower().startswith("hindi"):
            hindi = line.split(":", 1)[1].strip() if ":" in line else ""
        elif line.lower().startswith("spanish"):
            spanish = line.split(":", 1)[1].strip() if ":" in line else ""

    return hindi, spanish


def make_error_response(message: str, code: int = 400) -> Tuple[Dict, int]:
    """
    Helper to return standardized error responses.
    """
    return jsonify({"error": message}), code


# ------------------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------------------

@app.route("/")
def home():
    """
    Root route. Returns a simple message or template if available.
    """
    try:
        return render_template("index.html")
    except Exception:
        return "<h1>Translation API is running</h1>", 200


@app.route("/translate", methods=["POST"])
def translate():
    """
    Translate text into Hindi and Spanish.
    Expected JSON body: {"text": "some text"}
    """
    try:
        data = request.json
        if not data or "text" not in data:
            return make_error_response("Missing 'text' field in request", 400)

        text = data.get("text", "").strip()
        if not text:
            return make_error_response("Text cannot be empty", 400)

        logger.info(f"Received translation request: {text[:60]}...")

        # Initialize model
        model = genai.GenerativeModel("gemini-2.5-flash")

        # Build prompt
        prompt = build_prompt(text)

        # Generate response
        response = model.generate_content(prompt)
        raw_output = response.text.strip() if hasattr(response, "text") else ""

        logger.info(f"Raw Gemini output: {raw_output}")

        # Parse translations
        hindi, spanish = parse_translation(raw_output)

        if hindi or spanish:
            return jsonify({
                "hindi": hindi,
                "spanish": spanish,
                "raw": raw_output
            }), 200
        else:
            return jsonify({
                "warning": "Parsing failed. Returning raw output only.",
                "raw": raw_output
            }), 200

    except Exception as e:
        tb = traceback.format_exc()
        logger.error(f"Exception in /translate: {e}\n{tb}")
        return make_error_response(str(e), 500)


@app.route("/health", methods=["GET"])
def health_check():
    """
    Health check endpoint.
    """
    return jsonify({
        "status": "ok",
        "timestamp": datetime.datetime.utcnow().isoformat()
    }), 200


@app.route("/about", methods=["GET"])
def about():
    """
    About endpoint: provides service metadata.
    """
    return jsonify({
        "app": "Flask Translation API",
        "version": "1.0.0",
        "author": "Your Name",
        "description": "Translates English text into Hindi and Spanish using Google Gemini."
    }), 200


@app.route("/languages", methods=["GET"])
def languages():
    """
    Returns supported languages.
    """
    return jsonify({
        "supported_languages": ["English (input)", "Hindi (output)", "Spanish (output)"]
    }), 200


@app.route("/time", methods=["GET"])
def time_info():
    """
    Returns server time.
    """
    return jsonify({
        "server_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "utc_time": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    }), 200


# ------------------------------------------------------------------------------
# Main Entrypoint
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    logger.info("🚀 Starting Flask Translation API service...")
    app.run(host="0.0.0.0", port=5000, debug=True)
