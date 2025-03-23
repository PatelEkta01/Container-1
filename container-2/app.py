from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Persistent volume directory
PV_DIR = "/ekta_PV_dir"

@app.route('/calculate-total', methods=['POST'])
def calculate_total():
    try:
       
        

        data = request.get_json(force=True)  
        print("DEBUG: Received JSON:", data)

        if not data or 'file' not in data or 'product' not in data:
            return jsonify({"file": None, "error": "Invalid JSON input."}), 400

        file_name = data['file']
        product = data['product']
    except Exception as e:
        print("DEBUG: Error while parsing JSON:", str(e))
        return jsonify({"file": None, "error": "Invalid JSON format."}), 400


    try:
        # Read file from persistent volume
        file_path = os.path.join(PV_DIR, file_name)
        
        
        if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
            return jsonify({"file": file_name, "error": "File is empty or not in CSV format."}), 400

        with open(file_path, 'r') as f:
            lines = f.readlines()
        
       
        print("File contents:", lines)
        

        if len(lines) < 1:
            return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400
        
        # Validate CSV header
        header = lines[0].strip().split(',')
        print("Header:", header)  
        
        if len(header) != 2 or header[0].strip().lower() != "product" or header[1].strip().lower() != "amount":
            return jsonify({"file": file_name, "error": "Invalid CSV header format."}), 400
        
         # Validate missing commas
        for line in lines[1:]:
            parts = line.strip().split(',')
            if len(parts) != 2:  # If there are not exactly two columns, return an error
                return jsonify({"file": file_name, "error": "Missing commas or incorrect CSV format."}), 400

            if not parts[1].strip().isdigit(): 
                return jsonify({"file": file_name, "error": "Invalid CSV data format."}), 400

        # Calculate total for the product
        total = 0
        for line in lines[1:]:  
            parts = line.strip().split(',')
            print("Parts:", parts)  
            
            if len(parts) != 2:  
                return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400
            if not parts[1].strip().isdigit(): 
                return jsonify({"file": file_name, "error": "Invalid CSV data format."}), 400
            if parts[0].strip() == product:
                total += int(parts[1].strip())
        
        return jsonify({"file": file_name, "sum": total}), 200
    except FileNotFoundError:
        return jsonify({"file": file_name, "error": "File not found."}), 404
    except Exception as e:
        return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
