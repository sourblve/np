from datetime import datetime
from routes.api import api_bp
from routes.auth import auth_bp
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
from openai import OpenAI
import os
import requests
from utils.speech_to_text import speech_to_text
from utils.text_to_speech import text_to_speech

# Load OpenAI API key
load_dotenv()
api_key = os.environ.get("OPEN_AI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=OPEN_AI_API_KEY)

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(api_bp)


@app.route('/')
def index():
    return "Hello, this is the Flask app for handling WebSocket connections with Twilio."


@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('response', {'data': 'Connected to Flask WebSocket'})


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


@socketio.on('media')
def handle_media(data):
    # Handle the incoming audio data from Twilio
    audio_data = data['media_payload']

    # Convert audio to text using OpenAI Whisper
    text = speech_to_text(audio_data)

    # Send the text to Flowise
    flowise_response = requests.post(
        "https://flowiseai-qhlq.onrender.com/api/v1/prediction/34cbacab-36cd-4978-afc3-283629ad231f",
        json={"question": text}
    )
    response_data = flowise_response.json()
    response_text = response_data['answer']

    # Convert the response text to speech
    audio_url = text_to_speech(response_text)

    # Emit the audio URL back to the client
    emit('response_audio', {'audio_url': audio_url})


if __name__ == '__main__':
    socketio.run(app, debug=True)
