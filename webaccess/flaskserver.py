from flask import Flask, render_template, request, jsonify
import logging

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)  # Enable detailed logging

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_text', methods=['POST'])
def process_text():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        # Save the recognized text to a file
        with open("recognized_text.txt", "w") as f:
            f.write(text)
        
        response = {"response_text": f"Processed and saved: {text}"}
        return jsonify(response)
    except Exception as e:
        app.logger.error(f"Error processing text: {e}")
        return jsonify({"error": "Error processing text"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)