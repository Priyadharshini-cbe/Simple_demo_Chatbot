
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
import os
import uuid

# Load .env
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")  # Loads from .env

app = Flask(__name__)

# Set up Google API
genai.configure(api_key=API_KEY)

# Store chat sessions for multiple users
chat_sessions = {}

def get_or_create_chat(session_id):
    if session_id not in chat_sessions:
        model = genai.GenerativeModel('gemini-2.5-flash')
        chat_sessions[session_id] = model.start_chat(history=[])
    return chat_sessions[session_id]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        session_id = data.get('session_id', 'default')

        if not user_message.strip():
            return jsonify({'error': 'Empty message'}), 400

        chat = get_or_create_chat(session_id)
        response = chat.send_message(user_message)

        return jsonify({'response': response.text, 'success': True})

    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/new-chat', methods=['POST'])
def new_chat():
    session_id = str(uuid.uuid4())
    return jsonify({'session_id': session_id})

if __name__ == '__main__':
    print("🚀 Starting chatbot server...")
    print("📱 Open your browser at: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
