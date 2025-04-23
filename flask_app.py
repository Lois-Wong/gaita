from flask import Flask, request, jsonify, render_template, Response, stream_with_context
import os
import rag_chatbot

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    
    def generate():
        for token in rag_chatbot.get_response(user_input):
            # Format each token as a proper SSE message
            if token:
                yield f"data: {token}\n\n"
        
        # Send a completion signal
        yield "data: [DONE]\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive'
        }
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
