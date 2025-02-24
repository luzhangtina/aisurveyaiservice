from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
import pyttsx3
import speech_recognition as sr
from io import BytesIO

app = Flask(_name_)
socketio = SocketIO(app)

# In-memory storage for clients' context
client_context = {}

# Initialize TTS engine
engine = pyttsx3.init()

# Dummy AI response for the demo (you can replace this with actual AI models)
def get_ai_response(text):
    return f"Hello {text}, how can I assist you today?"

# Start WebSocket session and initialize client memory
@socketio.on('start_session')
def start_session(client_info):
    # Initialize client context
    client_context[client_info['client_id']] = {'history': []}
    print(f"Client {client_info['client_id']} {client_info['name']} started a session.")
    
    # Send back an AI response
    ai_response = get_ai_response(client_info['name'])

    # Convert the AI response to speech
    engine.save_to_file(ai_response, 'response.mp3')
    engine.runAndWait()

    # Stream AI response back to the client
    with open('response.mp3', 'rb') as audio_file:
        audio_data = audio_file.read()
        emit('ai_speech', audio_data)  # Send speech as a binary stream

# Handle receiving voice from client and process it
@socketio.on('client_voice')
def handle_client_voice(audio_data):
    # Convert the client's voice to text
    recognizer = sr.Recognizer()
    audio = BytesIO(audio_data)
    with sr.AudioFile(audio) as source:
        audio_recorded = recognizer.record(source)
    
    try:
        # Recognize speech using Google's Web Speech API
        client_text = recognizer.recognize_google(audio_recorded)
        print(f"Client said: {client_text}")

        # Process AI response
        ai_response = get_ai_response(client_text)
        
        # Convert the AI response to speech
        engine.save_to_file(ai_response, 'response.mp3')
        engine.runAndWait()

        # Stream AI response back to the client
        with open('response.mp3', 'rb') as audio_file:
            audio_data = audio_file.read()
            emit('ai_speech', audio_data)  # Send speech as a binary stream

    except Exception as e:
        print(f"Error: {e}")
        emit('error', {'message': 'Sorry, I could not understand your voice.'})

@app.route('/')
def index():
    return 'WebSocket and TTS Demo'

if _name_ == '_main_':
    socketio.run(app, debug=True)