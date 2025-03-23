from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Persistent volume directory
PV_DIR = "/ekta_PV_dir"

@app.route('/calculate-total', methods=['POST'])
def calculate_total():
    try:
        data = request.get_json(force=True)
        if not data or 'file' not in data or 'product' not in data:
            return jsonify({"file": None, "sum": 0, "error": "Invalid JSON input."}), 400

        app.logger.info("B01013736_ekta")
        file_name = data['file']
        product = data['product']
    except Exception:
        return jsonify({"file": None, "sum": 0, "error": "Invalid JSON format."}), 400

    try:
        file_path = os.path.join(PV_DIR, file_name)

        if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
            return jsonify({"file": file_name, "sum": 0, "error": "Input file not in CSV format."}), 400

        with open(file_path, 'r') as f:
            lines = f.readlines()

        if len(lines) < 1:
            return jsonify({"file": file_name, "sum": 0, "error": "Input file not in CSV format."}), 400

        header = lines[0].strip().split(',')
        if len(header) != 2 or header[0].strip().lower() != "product" or header[1].strip().lower() != "amount":
            return jsonify({"file": file_name, "sum": 0, "error": "Input file not in CSV format."}), 400

        for line in lines[1:]:
            parts = line.strip().split(',')
            if len(parts) != 2 or not parts[1].strip().isdigit():
                return jsonify({"file": file_name, "sum": 0, "error": "Input file not in CSV format."}), 400

        total = 0
        for line in lines[1:]:
            parts = line.strip().split(',')
            if parts[0].strip() == product:
                total += int(parts[1].strip())

        return jsonify({"file": file_name, "sum": total}), 200

    except FileNotFoundError:
        return jsonify({"file": file_name, "sum": 0, "error": "File not found."}), 404
    except Exception:
        return jsonify({"file": file_name, "sum": 0, "error": "Input file not in CSV format."}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)