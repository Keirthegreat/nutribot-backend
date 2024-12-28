from flask import Flask, request, jsonify, session
from flask_cors import CORS
import requests
import random
from flask_session import Session

app = Flask(__name__)
CORS(app, resources={r"/nutribot": {"origins": "*"}})

# Configure server-side session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'your_secret_key'
Session(app)

@app.after_request
def handle_cors(response):
    origin = request.headers.get('Origin')
    allowed_origins = [
        "http://127.0.0.1:3000",
        "https://keirthegreat.github.io",
        "https://www.nutrifitliving.website"
    ]
    if origin and (".vercel.app" in origin or origin in allowed_origins):
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return response


API_KEY = "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"
API_URL = "https://api.groq.com/openai/v1/chat/completions"
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

def fetch_user_profile(user_id):
    url = f"https://nutrifit-backend.onrender.com/fetchUserFitnessProfile.php?user_id={user_id}"
    response = requests.get(url)
    if response.status_code == 200:
        profile_data = response.json()
        user_info = {
            "full_name": profile_data.get("full_name"),
            "height": profile_data.get("height"),
            "weight": profile_data.get("weight"),
            "target_weight": profile_data.get("target_weight"),
            "ideal_bmi": profile_data.get("ideal_bmi")
        }
        return user_info
    else:
        return {"error": "Failed to fetch user profile data"}

@app.route('/nutribot', methods=['POST'])
def nutribot():
    user_message = request.json.get("message", "").strip()
    
    # Retrieve user_id from session
    user_id = session.get('user_id')
    
    if not user_id:
        return jsonify({"response": "User ID not found in session."})

    user_profile = fetch_user_profile(user_id)
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "messages": [
            {"role": "user", "content": user_message},
            {"role": "system", "content": f"User profile: {user_profile}. Provide personalized fitness and nutrition recommendations based on this data."}
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
        if any(word in bot_reply.lower() for word in ["fitness", "workout", "diet", "calories", "exercise"]):
            return jsonify({"response": bot_reply})
        else:
            return jsonify({"response": random.choice(DEFAULT_RESPONSES)})
    else:
        return jsonify({"response": random.choice(DEFAULT_RESPONSES)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
