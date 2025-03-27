# src/main.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, Response

app = Flask(__name__)

# Track if the system has been started to prevent multiple launches
system_started = False

@app.route('/')
def home():
    """Root endpoint to guide users."""
    return Response("Welcome! Open web/index.html and click 'Run the System' to start.", status=200)

@app.route('/run', methods=['GET'])
def start_system():
    """Endpoint to trigger the system by launching start_system.py."""
    global system_started
    if not system_started:
        # Windows-specific: Opens a new terminal window and runs start_system.py
        os.system("start python start_system.py")
        system_started = True
        return Response("System starting! Check your GUI shortly.", status=200)
    else:
        return Response("System already running! Check your GUI.", status=200)

if __name__ == "__main__":
    # Run Flask server on localhost:5000
    app.run(host='127.0.0.1', port=5000, debug=False)