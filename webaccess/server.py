from flask import Flask, send_file, jsonify, render_template, request
import os
import time
from threading import Thread
from gtts import gTTS

app = Flask(__name__)

OUTPUT_FILE = "generated_output.txt"
AUDIO_FILE = "output_audio.mp3"
PROMPT_FILE = "prompt.txt"  # File to save recognized text

last_output_content = ""  # Variable to keep track of the last content

def generate_audio():
    global last_output_content
    while True:
        if os.path.exists(OUTPUT_FILE):
            with open(OUTPUT_FILE, 'r') as f:
                current_content = f.read().strip()
                # Check if the content has changed
                if current_content and current_content != last_output_content:
                    last_output_content = current_content
                    tts = gTTS(text=current_content, lang='en')
                    tts.save(AUDIO_FILE)
                    print(f"Generated TTS audio for text: {current_content}")
        time.sleep(1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/audio')
def get_audio():
    if os.path.exists(AUDIO_FILE):
        return send_file(AUDIO_FILE)
    return "Audio file not found.", 404

@app.route('/output')
def get_output():
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r') as f:
            text = f.read().strip()
            return jsonify(text=text)
    return jsonify(text="Output file not found."), 404

@app.route('/save_prompt', methods=['POST'])
def save_prompt():
    """Save the recognized text to prompt.txt."""
    data = request.json
    prompt = data.get('prompt', '')
    if prompt:
        with open(PROMPT_FILE, 'w') as f:
            f.write(prompt)
        return jsonify(success=True), 200
    return jsonify(success=False, error="No prompt provided."), 400

if __name__ == "__main__":
    audio_thread = Thread(target=generate_audio, daemon=True)
    audio_thread.start()
    app.run(host='0.0.0.0', port=5000, debug=True)