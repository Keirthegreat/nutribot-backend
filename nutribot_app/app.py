from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, resources={r"/nutribot": {"origins": ["http://127.0.0.1:3000", "https://your-frontend-deployment.com"]}})
CORS(app, origins=["https://keirthegreat.github.io"]) # Allow only your GitHub Pages domain

# Your Groq API Key
API_KEY = "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"  # Replace with your actual Groq API key
API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Define keywords related to allowed topics
ALLOWED_KEYWORDS = ["fitness", "nutrition", "workout", "calories", "diet", "exercise"]

@app.route('/nutribot', methods=['POST'])
def nutribot():
    user_message = request.json.get("message", "").lower()  # Convert to lowercase for easier matching

    # Check if the message contains any allowed keywords
    if not any(keyword in user_message for keyword in ALLOWED_KEYWORDS):
        return jsonify({"response": "I’m your personal fitness assistant, here to help with questions about fitness, nutrition, workouts, and calories only. Let’s keep it focused on those topics!"})

    # If message contains allowed keywords, proceed to send to Groq API
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "messages": [
            {"role": "system", "content": "You are a fitness and nutrition expert assistant."},
            {"role": "user", "content": user_message}
        ],
        "model": "llama3-8b-8192",
        "temperature": 0.5,
        "max_tokens": 1024,
        "top_p": 1
    }

    response = requests.post(API_URL, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        bot_reply = data["choices"][0]["message"]["content"]
        return jsonify({"response": bot_reply})
    else:
        return jsonify({"error": response.text}), response.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Bind to 0.0.0.0 and set port to 5000

