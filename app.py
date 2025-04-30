# Gotta run this file first from your terminal
# I don't have flask/cors installed so i usually have to create a 
# python virtual environment and then install it in there

# CREATE python environment: python3 -m venv venv
# ENTER python environment: source venv/bin/activate
# LEAVE python environment: deactivate

# INSTALL flask : pip install flask
# INSTALL CORS : pip install flask-cors

# RUN : python app.py
import re
import socket
import urllib.request
from urllib.parse import urlparse
from joblib import load
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

model = load('random_forest_model.pkl')
print("✅ Model loaded successfully!")

def abnormal_url(url):
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname or ''
        if re.fullmatch(r'\d+\.\d+\.\d+\.\d+', hostname):
            return 1
        suspicious_keywords = ['login', 'secure', 'bank', 'verify', 'update', 'password', 'signin']
        if any(keyword in url.lower() for keyword in suspicious_keywords):
            return 1
        if len(hostname.split('.')) > 3:
            return 1
        if len(url) > 100:
            return 1
        if hostname not in url:
            return 1
        return 0
    except Exception:
        return 1

def having_ip_address(url):
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname or ''
        socket.inet_aton(hostname)
        return 1
    except:
        return 0

def sum_count_special_characters(url):
    special_chars = ['@', '?', '-', '=', '.', '#', '%', '+', '$', '!', '*', ',', '//']
    return sum(url.count(char) for char in special_chars)

def httpSecured(url):
    return 1 if url.startswith('https') else 0

def digit_count(url):
    return sum(c.isdigit() for c in url)

def letter_count(url):
    return sum(c.isalpha() for c in url)

def Shortining_Service(url):
    shortening_services = ['bit.ly', 'tinyurl.com', 'goo.gl', 'ow.ly', 't.co', 'bit.do', 'adf.ly']
    return 1 if any(service in url for service in shortening_services) else 0

def google_index(url):
    try:
        search = urllib.request.urlopen("http://www.google.com/search?q=site:" + url)
        return 1
    except:
        return 0

def extract_features(url):
    return [
        len(url),
        abnormal_url(url),
        having_ip_address(url),
        sum_count_special_characters(url),
        httpSecured(url),
        digit_count(url),
        letter_count(url),
        Shortining_Service(url),
        google_index(url)
    ]

@app.route('/receive-url', methods=['POST'])
def receive_url():
    print("Request received!")
    data = request.get_json()
    url = data['url']

    features = extract_features(url)
    prediction_proba = model.predict_proba([features])[0] 
    prediction = model.predict([features])[0]

    confidence = round(100 * max(prediction_proba), 2)


    if prediction == 1:
        print(f"⚠️ Malicious URL detected: {url} ({confidence}%)")
        return jsonify({"verdict": "malicious", "confidence": confidence})
    else:
        print(f"✅ Safe URL detected: {url} ({confidence}%)")
        return jsonify({"verdict": "safe", "confidence": confidence})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
