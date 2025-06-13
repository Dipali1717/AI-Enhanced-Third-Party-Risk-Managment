from groq import Groq

# Replace with your actual Groq API key
api_key = "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"

# Initialize Groq client
def initialize_groq_client(api_key):
    try:
        return Groq(api_key=api_key)
    except Exception as e:
        print(f"Error initializing Groq client: {e}")
        return None

# System prompt for Groq
system_prompt = """
You are an AI-powered URL threat detection assistant. Your task is to analyze a URL and assess its potential risk level.

Instructions:
- Based on the structure and content of the URL, classify it as: "Safe", "Suspicious", "Risky", or "Dangerous".
- Consider known phishing patterns, keyword tricks (e.g., 'login', 'verify', 'secure'), unusual domains, or obfuscation.
- Be brief, but highlight any specific red flags found in the URL.
"""

# Analyze the risk of a single URL
def url_risk_identify(client, url):
    try:
        user_prompt = f"""
Analyze the following URL and classify its threat level.

URL: {url}

Respond with:
1. Risk Classification (Safe / Suspicious / Risky / Dangerous)
2. Explanation for the classification
"""

        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="llama3-70b-8192",
            temperature=0.5
        )

        print("\n[Threat Analysis]")
        print(response.choices[0].message.content)

    except Exception as e:
        print(f"Error analyzing URL: {e}")

# Entry point
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        url = sys.argv[1]
        print(f"[INFO] Checking URL: {url}")
        client = initialize_groq_client(api_key)
        if client:
            url_risk_identify(client, url)
    else:
        print("Usage: python url_risk_checker.py <url>")
