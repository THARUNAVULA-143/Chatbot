from flask import Flask, request, jsonify, send_file , render_template
from flask_cors import CORS
import ollama
import json
import os

app = Flask(__name__)
CORS(app)

# Define the available models
MODELS = {
    'qwen2.5:0.5b': 'qwen2.5:0.5b',
    'llama3.2:1b': 'llama3.2:1b',
    'phi3:3.8b': 'phi3:3.8b'
}

# Set the default model
DEFAULT_MODEL = 'qwen2.5:0.5b'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message')
        model = data.get('model', DEFAULT_MODEL)

        # Create conversation with Ollama using the selected model
        response = ollama.chat(
            model=MODELS[model],
            messages=[{'role': 'user', 'content': message}],
        )

        return jsonify({
            'response': response['message']['content'],
            'status': 'success'
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)