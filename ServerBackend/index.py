import json
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS package
import tiktoken
import openai

app = Flask(__name__)
CORS(app)  # Enable CORS for your Flask app and specify allowed origins

openai.api_type = "azure"
openai.api_base = "https://da-stg-openai-eu-fr-m6allrbs2iz3e.openai.azure.com/"
openai.api_version = "2023-03-15-preview"
openai.api_key = 'enter-key'

deployment_name = "cs-chat"

max_response_tokens = 250
token_limit= 4000

@app.route('/api/openai-chatbot', methods=['POST'])
def chat():
    user_input = request.json.get('user_input')
    conversation = request.json.get('conversation', [{"role": "system", "content": user_input}])

    conversation.append({"role": "user", "content": user_input})


    response = openai.ChatCompletion.create(
        engine="gpt-4-32k",
        messages = conversation,
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0
    )

    conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
    return jsonify(conversation)

if __name__ == '__main__':
    app.run(debug=True)