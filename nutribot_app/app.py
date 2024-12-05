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
    "fitness app", "virtual training", "online workout", "fitness community",
    "barbell", "dumbbell", "kettlebell", "resistance bands", "pull-ups", 
    "push-ups", "squats", "deadlifts", "lunges", "planks", "crunches", 
    "burpees", "mountain climbers", "rower", "treadmill", "elliptical", 
    "spin class", "crossfit", "Zumba", "dance workout", "bootcamp", 
    "bodyweight exercises", "calisthenics", "aqua aerobics", "rowing", 
    "nutrition plan", "meal replacement", "high protein", "low carb", 
    "plant-based diet", "calorie tracking", "food log", "organic foods", 
    "whole grains", "superfoods", "antioxidants", "omega-3", 
    "probiotics", "prebiotics", "vitamins", "minerals", "greens", 
    "smoothies", "juicing", "clean eating", "portion control", 
    "healthy snacks", "meal timing", "cheat meal", "hydration levels", 
    "sports drinks", "caffeine", "energy bars", "energy gels", 
    "fasting", "recovery shakes", "muscle repair", "DOMS (Delayed Onset Muscle Soreness)", 
    "stretch bands", "TRX", "tabata", "rowing machine", "functional training", 
    "injury prevention", "fitness assessment", "body composition", 
    "metabolism", "lean muscle", "high-intensity", "low-impact", 
    "cross-training", "intervals", "endurance sports", "athletic training", 
    "track and field", "marathon", "triathlon", "obstacle course", 
    "recovery foods", "post-exercise meals", "balanced diet", 
    "glycogen replenishment", "energy balance", "hydration packs", 
    "activewear", "fitness equipment", "training shoes", "foam rolling", 
    "sports therapy", "massage", "dynamic stretching", "static stretching"
]


@app.route('/nutribot', methods=['POST'])
def nutribot():
    user_message = request.json.get("message", "").lower()  # Convert to lowercase for easier matching

    # Check if the message contains any allowed keywords
      if not any(keyword in user_message for keyword in ALLOWED_KEYWORDS):
        responses = [
            "I’m your personal fitness assistant, here to help with questions about fitness, nutrition, workouts, and calories only. Let’s keep it focused on those topics!",
            "My expertise is in fitness and nutrition. Please ask me anything related to workouts, diets, or calories!",
            "I'm here to guide you on your fitness journey! Let’s stick to topics like exercise, nutrition, and healthy living.",
            "It seems your question isn’t related to fitness. Try asking me about workouts, meal plans, or calorie tracking.",
            "I specialize in fitness and nutrition advice. How can I help you achieve your health goals today?",
            "My focus is on fitness, workouts, and nutrition. Feel free to ask about meal plans, exercise routines, or health tips!",
            "Let’s keep our conversation fitness-focused. I’m happy to help with topics like exercise, diet, or calorie counting.",
            "I’m your fitness assistant! Ask me about workouts, healthy eating, or anything related to staying fit.",
            "Fitness is my specialty. Let’s talk about exercise, meal prep, or achieving your fitness goals!",
            "I’m here for all your fitness and health-related queries. Let’s stay on track with topics like workouts and nutrition!"
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

