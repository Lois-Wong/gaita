from flask import Flask, request, jsonify, render_template
import os
import rag_chatbot  # Replace with the actual import for your chatbot logic

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    response = rag_chatbot.get_response(user_input)  # Replace with the actual function
    return jsonify({"response": response})

@app.route('/')
def home():
    # Render the home page
    return render_template('index.html')

if __name__ == '__main__':
    # Set host to '0.0.0.0' and port from the environment variable (provided by Render)
    port = int(os.environ.get('PORT', 5000))  # Render sets the PORT environment variable
    app.run(host='0.0.0.0', port=port, debug=True)
