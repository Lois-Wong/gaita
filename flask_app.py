from flask import Flask, request, jsonify, render_template, Response, stream_with_context
import os
import rag_chatbot  # Ensure this supports streaming

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")

    if not user_input:
        return jsonify({"error": "No message provided."}), 400

    def generate():
        for chunk in rag_chatbot.get_response_stream(user_input):  # Ensure this returns partial responses
            yield f"data: {chunk}\n\n"  # SSE format

    return Response(stream_with_context(generate()), content_type="text/event-stream")