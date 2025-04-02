from flask import Flask, jsonify, request
from data_clean import parse_lkd_profile  # Import function

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the LinkedIn Profile Cleaning API"

@app.route('/clean_profile', methods=['POST', 'GET'])
def clean_profile():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing JSON data"}), 400
        
        result = parse_lkd_profile(data)
        return jsonify(result)

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

if __name__ == '__main__':
    app.run()