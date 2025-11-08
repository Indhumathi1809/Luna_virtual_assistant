from flask import Flask, render_template, request, redirect, url_for, jsonify
from gtts import gTTS
import os
import uuid
import google.generativeai as gen_ai
import speech_recognition as sr

app = Flask(__name__)

# Input your Google API Key here
GOOGLE_API_KEY = "YOUR_API_KEY"

# Check if API key is provided
if not GOOGLE_API_KEY:
    raise ValueError("Please enter your Google API Key.")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-1.0-pro')

# Function to convert text to speech using gTTS
def text_to_speech(text, output_folder="static/audio"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    unique_filename = str(uuid.uuid4()) + ".mp3"
    output_path = os.path.join(output_folder, unique_filename)

    tts = gTTS(text=text, lang="en")
    tts.save(output_path)
    return output_path

# Function to make the API call and return the response
def make_genai_request(user_input):
    chat_session = model.start_chat(history=[])
    gemini_response = chat_session.send_message(user_input)
    return gemini_response.text

@app.route('/', methods=['GET', 'POST'])
def index():
    user_input = None
    assistant_response = None
    audio_path = None

    if request.method == 'POST':
        data = request.get_json()
        if data and 'user_input' in data:
            user_input = data['user_input']
        elif 'audio_input' in request.files:
            recognizer = sr.Recognizer()
            audio_file = request.files['audio_input']
            with sr.AudioFile(audio_file) as source:
                audio_data = recognizer.record(source)
                try:
                    user_input = recognizer.recognize_google(audio_data)
                except sr.UnknownValueError:
                    user_input = "Sorry, I could not understand your speech."
                except sr.RequestError as e:
                    user_input = f"Error: {e}"

        if user_input and user_input.lower() in ["exit", "quit"]:
            return redirect(url_for('goodbye'))

        if user_input:
            assistant_response = make_genai_request(user_input)
            audio_path = text_to_speech(assistant_response, output_folder="static/audio")
        
        return jsonify({
            'user_input': user_input,
            'assistant_response': assistant_response,
            'audio_path': audio_path
        })

    return render_template('index.html', user_input=user_input, assistant_response=assistant_response, audio_path=audio_path)



@app.route('/goodbye')
def goodbye():
    return "Goodbye!"

if __name__ == '__main__':
    app.run(debug=True)
