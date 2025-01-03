from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import random  # For randomizing responses

app = Flask(__name__)

# Allow all origins temporarily (not recommended for production)
CORS(app, resources={r"/nutribot": {"origins": "*"}})

@app.after_request
def handle_cors(response):
    origin = request.headers.get('Origin')
    # Dynamically allow origins from *.vercel.app or other allowed domains
    if origin and (".vercel.app" in origin or origin in [
        "http://127.0.0.1:3000",
        "https://keirthegreat.github.io"
    ]):
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return response

# Your Groq API Key
API_KEY = "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"  # Replace with your actual Groq API key
API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Default responses for non-fitness-related questions
DEFAULT_RESPONSES = [
    "I’m your personal fitness assistant, here to help with questions about fitness, nutrition, workouts, and calories only. Let’s keep it focused on those topics!",
    "It seems your question isn’t related to fitness. Try asking me about workouts, meal plans, or calorie tracking!",
    "I'm here to guide you on your fitness journey! Let’s stick to topics like exercise, nutrition, and healthy living.",
    "My expertise is in fitness and nutrition. How about we discuss your fitness goals or meal planning?",
    "Let’s focus on health and fitness topics! How can I help you with your workouts or diet?",
    "It looks like your question isn’t about fitness. Remember, I’m here for nutrition, workouts, and health advice!",
    "I specialize in fitness and health-related queries. Let’s talk about your diet or exercise routine!",
    "Fitness is my specialty. Let’s keep the conversation on topics like workouts, nutrition, or staying fit.",
    "I’m here for your fitness needs! Feel free to ask me anything about exercise, meal prep, or calorie management.",
    "Let’s stay on track with fitness and nutrition topics. I’d love to help you with your health goals!"
]

@app.route('/nutribot', methods=['POST'])
def nutribot():
    user_message = request.json.get("message", "").strip()  # Get user message and strip extra spaces

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # Payload for Groq API
    payload = {
        "messages": [
            {"role": "user", "content": user_message}
        ],
        "model": "llama3-70b-8192",
        "temperature": 0.5,
        "max_tokens": 1024,
        "top_p": 1
    }

    response = requests.post(API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        bot_reply = data["choices"][0]["message"]["content"]
        # Check if bot reply mentions fitness-related topics; otherwise, default reply
        if any(word in bot_reply.lower() for word in ["fitness", "workout", "diet", "calories", "exercise"]):
            return jsonify({"response": bot_reply})
        else:
            return jsonify({"response": random.choice(DEFAULT_RESPONSES)})
    else:
        # Return default response on API error
        return jsonify({"response": random.choice(DEFAULT_RESPONSES)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Bind to 0.0.0.0 and set port to 5000
