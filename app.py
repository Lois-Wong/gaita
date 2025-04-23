from flask import Flask, Response, stream_with_context
from stream_handler import stream_completion

app = Flask(__name__)

@app.route('/stream', methods=['POST'])
def stream():
    def generate():
        for token in stream_completion(prompt):
            yield token

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(port=8000)  # Using port 8000 to avoid conflict with AirPlay