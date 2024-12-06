from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import random  # For randomizing responses

app = Flask(__name__)

# Set up CORS with multiple allowed origins
CORS(app, resources={
    r"/nutribot": {
        "origins": [
            "http://127.0.0.1:3000",
            "https://your-frontend-deployment.com",
            "https://keirthegreat.github.io",
            "https://nutri-fit-living-dj2jjsmrq-keirsephs-projects.vercel.app",
            "https://nutri-fit-living-git-main-keirsephs-projects.vercel.app"
        ]
    }
})


# Your Groq API Key
API_KEY = "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"  # Replace with your actual Groq API key
API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Define keywords related to allowed topics
ALLOWED_KEYWORDS = [
    "fitness", "nutrition", "workout", "calories", "diet", "exercise", 
    "health", "strength", "training", "yoga", "pilates", "cardio",
    "bodybuilding", "weightlifting", "running", "jogging", "cycling",
    "swimming", "aerobics", "HIIT", "flexibility", "mobility",
    "stretching", "warm-up", "cool-down", "endurance", "balance",
    "coordination", "core", "abs", "glutes", "quads", "hamstrings",
    "biceps", "triceps", "deltoids", "pecs", "lats", "fitness goals",
    "muscle", "fat loss", "weight loss", "weight gain", "lean mass",
    "toning", "hydration", "macros", "micronutrients", "protein",
    "carbs", "fats", "fiber", "meal prep", "meal plan",
    "recovery", "rest days", "gym", "home workout", "outdoor workout",
    "fitness tracker", "steps", "heart rate", "VO2 max", "BMI",
    "caloric deficit", "caloric surplus", "intermittent fasting",
    "supplements", "whey protein", "pre-workout", "post-workout",
    "creatine", "BCAAs", "electrolytes", "vegan diet",
    "keto diet", "paleo diet", "mediterranean diet", "strength training",
    "functional fitness", "sports performance", "plyometrics",
    "athleticism", "mental health", "stress relief",
    "mindfulness", "meditation", "self-care", "body positivity",
    "fitness motivation", "gym routine", "personal trainer",
    "fitness app", "virtual training", "online workout", "fitness community"
]

@app.route('/nutribot', methods=['POST'])
def nutribot():
    user_message = request.json.get("message", "").lower()  # Convert to lowercase for easier matching

    # Check if the message contains any allowed keywords
    if not any(keyword in user_message for keyword in ALLOWED_KEYWORDS):
        responses = [
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
        return jsonify({"response": random.choice(responses)})

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
