import subprocess
import re
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

def js(url, file="link.chunk.js"):
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        with open(file, "w", encoding="utf-8") as f:
            f.write(res.text)
        return file
    except requests.RequestException as e:
        return None

def crack(file):
    try:
        res = subprocess.run(["webcrack", file], capture_output=True, text=True, check=True)
        return res.stdout
    except subprocess.CalledProcessError:
        return None

def extract(out):
    e = re.search(r"var x = ([0-9]+);", out)
    s = re.search(r"var S = \"([a-fA-F0-9]{64})\";", out)
    return (e.group(1) if e else None), (s.group(1) if s else None)

@app.route("/extract", methods=["GET"])
def extract_api():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400
    
    file = js(url)
    if not file:
        return jsonify({"error": "Failed to download JS file"}), 500
    
    out = crack(file)
    if not out:
        return jsonify({"error": "Failed to process file with webcrack"}), 500
    
    e, s = extract(out)
    if not e or not s:
        return jsonify({"error": "Failed to extract values"}), 500
    
    return jsonify({"epoch": e, "sha256": s})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
