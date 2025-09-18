# 🌎 Real-Time Translator

A simple **Flask + Google Gemini AI** powered web application that:  
- Records your speech (🎤 Voice input).  
- Transcribes it into text.  
- Translates it into **Hindi** 🇮🇳 and **Spanish** 🇪🇸 in real-time.  
- Reads translations aloud (🔊 Text-to-Speech).  

---

## ✨ Features
- 🎤 **Speech Recognition**: Speak and see live transcription.  
- 🌍 **AI Translation**: Get instant translations into **Hindi** and **Spanish**.  
- 🔊 **Text-to-Speech**: Listen to the translated results.  
- ⚡ **Flask Backend**: Handles API calls to Gemini AI.  
- 🖥️ **Simple Frontend**: Clean HTML + JavaScript interface.  

---

## 📂 Project Structure
```
real-time-translator/
│
├── server.py                # Flask backend
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html        # Frontend page
├── static/
│   ├── style.css         # Styling
│   └── script.js         # Speech + translation logic
└── README.md             # Documentation
```

---

## 🛠️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/real-time-translator-.git
cd translator-app
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set your Gemini API key
```bash
# Linux/Mac
export GEMINI_API_KEY="your_api_key_here"

# Windows (cmd)
set GEMINI_API_KEY="your_api_key_here"

# Windows (PowerShell)
$env:GEMINI_API_KEY="your_api_key_here"
```

---

## ▶️ Run the App
```bash
python server.py
```

App runs at 👉 **http://127.0.0.1:5000/**  

---

## 🎮 How to Use
1. Open the app in your browser.  
2. Click **Start Listening** and speak (in English or another language).  
3. The app will:  
   - Show your **speech transcript**.  
   - Translate into **Hindi** and **Spanish**.  
   - Let you **play translations aloud**.  
4. Click **Stop Recording** to end speech recognition.  

---

## 📦 Requirements
- Python 3.8+  
- Flask  
- Flask-Cors  
- google-generativeai  

(Already listed in `requirements.txt`)  

---

## 🔒 Notes
- Currently supports translations **only into Hindi and Spanish**.  
- For production, set `debug=False` in `server.py`.  
- Keep your **API key safe** — do not hardcode it.  

---
