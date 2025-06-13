# from flask import Flask, render_template, request, jsonify
# from groq import Groq
# import re
#
# app = Flask(__name__)
#
# # Initialize Groq Client
# api_key = "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"
#
#
# def initialize_groq_client(api_key):
#     try:
#         return Groq(api_key=api_key)
#     except Exception as e:
#         print(f"Error initializing Groq client: {e}")
#         return None
#
#
# groq_client = initialize_groq_client(api_key)
#
# # System prompt for Groq LLM
# system_prompt = """
# You are an AI-powered URL threat detection assistant. Your task is to analyze a URL and assess its potential risk level.
#
# Instructions:
# - Based on the structure and content of the URL, classify it as: "Safe", "Suspicious", "Risky", or "Dangerous".
# - Consider known phishing patterns, keyword tricks (e.g., 'login', 'verify', 'secure'), unusual domains, or obfuscation.
# - Be brief, but highlight any specific red flags found in the URL.
# """
#
#
# # Analyze URL with Groq
# def analyze_url_with_groq(url):
#     try:
#         user_prompt = f"""
# Analyze the following URL and classify its threat level.
#
# URL: {url}
#
# Respond with:
# 1. Risk Classification (Safe / Suspicious / Risky / Dangerous)
# 2. Explanation for the classification
# """
#         response = groq_client.chat.completions.create(
#             messages=[
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": user_prompt}
#             ],
#             model="llama3-70b-8192",
#             temperature=0.5
#         )
#         return response.choices[0].message.content
#     except Exception as e:
#         return f"Error analyzing URL: {str(e)}"
#
#
# # Home Route
# @app.route('/')
# def home():
#     return render_template('index.html', title="AI Risk Management Assistant")
#
#
# # URL Risk Checking Route
# @app.route("/check_url", methods=["POST"])
# def check_url():
#     try:
#         url = request.form.get("url")
#         if not url:
#             return jsonify({"error": "No URL provided"}), 400
#         if not groq_client:
#             return jsonify({"error": "Groq client not initialized"}), 500
#
#         result = analyze_url_with_groq(url)
#
#         if request.is_json:
#             return jsonify({"result": result})
#         else:
#             return render_template("result.html", result=result, title="URL Threat Detection")
#     except Exception as e:
#         return jsonify({"error": "Failed to process request", "details": str(e)}), 500
#
#
# # Text Risk Analysis (unchanged for now)
# @app.route('/analyze_text', methods=['POST'])
# def analyze_text():
#     text = request.form['text'].strip()
#     if not text:
#         return render_template('result.html', result="Error: No text provided.", title="Text Risk Analysis")
#     with open('scraped_content.txt', 'w', encoding='utf-8') as f:
#         f.write(text)
#     result = run_script('text_risk_identification.py')
#     return render_template('result.html', result=result, title="Text Risk Analysis")
#
#
# # Helper: Run external scripts
# import subprocess
#
#
# def run_script(script_name, *args):
#     try:
#         result = subprocess.run(['python', script_name, *args], capture_output=True, text=True)
#         return result.stdout
#     except Exception as e:
#         return str(e)
#
#
# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from groq import Groq
import re
import subprocess

app = Flask(__name__)
CORS(app)  # ✅ Allow CORS for Chrome Extension communication

# Initialize Groq Client
api_key = "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"

def initialize_groq_client(api_key):
    try:
        return Groq(api_key=api_key)
    except Exception as e:
        print(f"Error initializing Groq client: {e}")
        return None

groq_client = initialize_groq_client(api_key)

# System prompt for Groq LLM
system_prompt = """
You are an AI-powered URL threat detection assistant. Your task is to analyze a URL and assess its potential risk level.

Instructions:
- Based on the structure and content of the URL, classify it as: "Safe", "Suspicious", "Risky", or "Dangerous".
- Consider known phishing patterns, keyword tricks (e.g., 'login', 'verify', 'secure'), unusual domains, or obfuscation.
- Be brief, but highlight any specific red flags found in the URL.
"""

# Analyze URL with Groq
def analyze_url_with_groq(url):
    try:
        user_prompt = f"""
Analyze the following URL and classify its threat level.

URL: {url}

Respond with:
1. Risk Classification (Safe / Suspicious / Risky / Dangerous)
2. Explanation for the classification
"""
        response = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="llama3-70b-8192",
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error analyzing URL: {str(e)}"

# Home Route
@app.route('/')
def home():
    return render_template('index.html', title="AI Risk Management Assistant")

# URL Risk Checking Route
@app.route("/check_url", methods=["POST"])
def check_url():
    try:
        url = request.form.get("url")
        if not url:
            return jsonify({"error": "No URL provided"}), 400
        if not groq_client:
            return jsonify({"error": "Groq client not initialized"}), 500

        result = analyze_url_with_groq(url)

        if request.is_json:
            return jsonify({"result": result})
        else:
            return render_template("result.html", result=result, title="URL Threat Detection")
    except Exception as e:
        return jsonify({"error": "Failed to process request", "details": str(e)}), 500

# 🔄 Updated Text Risk Analysis to handle JSON from extension
@app.route('/analyze_text', methods=['POST'])
def analyze_text():
    try:
        if request.is_json:
            data = request.get_json()
            text = data.get('text', '').strip()
        else:
            text = request.form.get('text', '').strip()

        if not text:
            return jsonify({"result": "Error: No text provided."}), 400

        with open('scraped_content.txt', 'w', encoding='utf-8') as f:
            f.write(text)

        result = run_script('text_risk_identification.py')

        if request.is_json:
            return jsonify({"result": result})
        else:
            return render_template('result.html', result=result, title="Text Risk Analysis")
    except Exception as e:
        return jsonify({"error": "Text analysis failed", "details": str(e)}), 500

# Helper: Run external scripts
def run_script(script_name, *args):
    try:
        result = subprocess.run(['python', script_name, *args], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
