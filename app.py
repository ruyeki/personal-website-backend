from flask import Flask, request, jsonify, session
from flask_cors import CORS
from openai import OpenAI
import os
from dotenv import load_dotenv
import google.generativeai as genai
import os

port = int(os.environ.get("PORT", 10000))

load_dotenv()

app = Flask(__name__)

CORS(app)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
app.secret_key = os.getenv("APP_SECRET_KEY")

@app.route('/chat', methods = ['POST'])
def chat():
    user_query = request.get_json()
    data = user_query['inputMessage']

    if "chat_history" not in session:
        session["chat_history"] = []

    session["chat_history"].append(f"user question: {data}")

    with open('about.txt', 'r') as f:
        about_me = f.read()

    prompt = f"""
    You're a friendly and natural-sounding person having a casual conversation.
    Answer clearly, like you're explaining it to a friend.
    Don't say things like "based on the context" or "according to the text".
    Don't use bold or markdown formatting.
    Don't always start with 'Oh'.
    Use the context, the user question, and the chat history to answer accordingly. 

    Context:
    {about_me}

    Question:
    {data}

    Chat History: 
    {session["chat_history"]}

    """
    model = genai.GenerativeModel("gemini-2.5-pro")
    response = model.generate_content(prompt)
    session["chat_history"].append(f"bot response: {response.text}")
    # Save session
    session.modified = True

    text_response = {"data": response.text}

    return jsonify(text_response)
    



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
