from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)
PV_DIR = "/ekta_PV_dir"  # Persistent volume directory
CONTAINER2_URL = "http://container2-service:5001" # External IP for Container 2

@app.route("/", methods=['GET'])
def home():
    return "Container 1 is running!", 200

@app.route('/store-file', methods=['POST'])
def store_file():
    data = request.get_json(force=True, silent=True)
    if not data or 'file' not in data or 'data' not in data:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    file_name = data['file']
    file_data = data['data']

    if not file_data or not file_data.strip():
        return jsonify({"file": file_name, "error": "File content cannot be empty."}), 400

    try:
        with open(os.path.join(PV_DIR, file_name), 'w') as f:
            f.write(file_data)
        return jsonify({"file": file_name, "message": "Success."}), 200
    except Exception:
        return jsonify({"file": file_name, "error": "Error while storing the file to the storage."}), 500

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json(force=True, silent=True)
    if not data or 'file' not in data or not data['file'] or 'product' not in data or not data['product']:
        return jsonify({"file": None, "sum": 0, "error": "Invalid JSON input."}), 400

    file_name = data['file']
    product = data['product']
    file_path = os.path.join(PV_DIR, file_name)

    if not os.path.exists(file_path):
        return jsonify({"file": file_name, "sum": 0, "error": "File not found."}), 404

    try:
        # Forward the request to Container 2
        response = requests.post(f"{CONTAINER2_URL}/calculate", json=data, timeout=5)
        
        # Return the response from Container 2
        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"file": file_name, "sum": 0, "error": f"Failed to connect to Container 2: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)