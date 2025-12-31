import os
import re
import json
import base64
from io import BytesIO
from PIL import Image
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv

import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

# 1. SETUP GEMINI
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash') 

# 2. SETUP FIREBASE
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate("firebase_key.json")
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("✅ Connected to Firebase Firestore")
    except Exception as e:
        print(f"⚠️ Firebase Error: {e}")
        db = None

def scrub_pii(text):
    if not text: return ""
    text = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[REDACTED_EMAIL]', text)
    return text

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        raw_text = data.get('text', '')
        image_b64 = data.get('image', None)
        clean_text = scrub_pii(raw_text)

        # --- IMPROVED PROMPT ---
        prompt_text = f"""
        Act as a Cybersecurity Expert. Analyze this website content.
        
        DATA FROM PAGE:
        "{clean_text}"
        
        INSTRUCTIONS:
        1. **ANALYZE RISK:** Look for phishing signs (urgency, fake login, suspicious domains).
        2. **IDENTIFY DESTINATION:** - Look at "FORM DESTINATIONS".
           - If that says "No forms found", look at "LINKS" and pick the most suspicious link (the one the user is urged to click).
        
        SCORING: 0-10 (Safe) to 80-100 (Phishing).
        
        Return ONLY valid JSON:
        {{
            "verdict": "Safe/Suspicious/Malicious",
            "confidence_score": 0,
            "explanation": "Brief reason.",
            "hacker_dest": "The specific URL where data/clicks are going (or N/A)"
        }}
        """

        inputs = [prompt_text]
        if image_b64:
            try:
                if "base64," in image_b64: image_b64 = image_b64.split("base64,")[1]
                image = Image.open(BytesIO(base64.b64decode(image_b64)))
                inputs.append(image)
            except: pass

        response = model.generate_content(inputs)
        
        # Clean & Parse JSON
        response_text = response.text.replace('```json', '').replace('```', '').strip()
        result_json = json.loads(response_text)

        return jsonify(result_json)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            "verdict": "Error", 
            "confidence_score": 0, 
            "explanation": "Server Error",
            "hacker_dest": "Unknown"
        })

@app.route('/report', methods=['POST'])
def report_attack():
    try:
        data = request.json
        # We explicitly print what we receive to debug
        print(f"🚨 REPORTING: {data}")
        
        url = data.get('url', 'Unknown URL')
        destination = data.get('destination', 'Unknown Dest')

        if db:
            db.collection('phishing_reports').add({
                'url': url,
                'hacker_destination': destination,
                'reported_at': datetime.now().isoformat(),
                'status': 'Under Review'
            })
            return jsonify({"status": "saved"})
        else:
            return jsonify({"status": "offline"})

    except Exception as e:
        print(f"Report Error: {e}")
        return jsonify({"status": "error"})

if __name__ == '__main__':
    app.run(debug=True)