# Gotta run this file first from your terminal
# I don't have flask/cors installed so i usually have to create a 
# python virtual environment and then install it in there

# CREATE python environment: python3 -m venv venv
# ENTER python environment: source venv/bin/activate
# LEAVE python environment: deactivate

# INSTALL flask : pip install flask
# INSTALL CORS : pip install flask-cors

# RUN : python app.py

from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/receive-url', methods=['POST'])
def receive_url():
    print("Request received!")
    data = request.get_json()
    print(f"Received URL: {data['url']}")
    return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
