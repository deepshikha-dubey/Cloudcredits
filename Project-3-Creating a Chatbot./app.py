# Tech Stack: Flask + OpenAI API + HTML UI
# =============================

# ---------- app.py ----------
from flask import Flask, request, jsonify, render_template
import os
import requests

app = Flask(__name__)

# Set your API key as environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/chat', methods=['POST'])
# def chat():
#     user_message = request.json.get("message")

#     if not OPENAI_API_KEY:
#         return jsonify({"reply": "API key missing. Please add it."})

#     from openai import OpenAI
#     client = OpenAI(api_key=OPENAI_API_KEY)

#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": "You are a helpful chatbot."},
#             {"role": "user", "content": user_message}
#         ]
#     )

#     reply = response.choices[0].message.content

#     return jsonify({"reply": reply})

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")

    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/google/flan-t5-base",
            headers={"Content-Type": "application/json"},
            json={"inputs": user_message}
        )

        result = response.json()

        # Extract response safely
        if "error" in result:
          reply = "Model is waking up... try again in 5 seconds ⏳"
        elif isinstance(result, list):
          reply = result[0].get("generated_text", "No response")
        else:
          reply = "Unexpected response"
    except Exception as e:
        print("ERROR:", e)
        reply = "Something went wrong."
       

    return jsonify({"reply": reply})

# def get_bot_reply(user_message):
#     user_message = user_message.lower()

#     if "hello" in user_message:
#         return "Hi! How can I help you?"
#     elif "devops" in user_message:
#         return "DevOps is a practice that combines development and operations to automate and improve software delivery."
#     elif "docker" in user_message:
#         return "Docker is a containerization tool used to package applications."
#     else:
#         return "Sorry, I am still learning. Please ask something else."
   
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)