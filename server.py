from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# API key provided by the user
genai.configure(api_key="0000000000000000000000000000")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/translate", methods=["POST"])
def translate():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text received"}), 400

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = (
            f"Translate the following text into Hindi and Spanish.\n\n"
            f"Text: {text}\n\n"
            "Return output exactly in this format (no extra commentary):\n"
            "Hindi: <hindi translation>\n"
            "Spanish: <spanish translation>\n"
        )

        response = model.generate_content(prompt)
        raw = response.text.strip()

        hindi = ""
        spanish = ""
        for line in raw.splitlines():
            if line.lower().startswith("hindi"):
                hindi = line.split(":", 1)[1].strip()
            elif line.lower().startswith("spanish"):
                spanish = line.split(":", 1)[1].strip()

        # fallback: if not parsed, return raw under 'raw' key
        if not hindi and not spanish:
            return jsonify({"raw": raw}), 200

        return jsonify({"hindi": hindi, "spanish": spanish}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
