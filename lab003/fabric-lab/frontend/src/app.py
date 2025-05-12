# app.py
from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
from lib.fabric_client import FabricHelper

app = Flask(__name__)

# Initialize the Fabric client
connection_profile = os.path.join(os.path.dirname(__file__), 'connection-profiles/org1-connection.json')
fabric_client = FabricHelper(
    net_profile=connection_profile,
    channel_name='mychannel',
    org_name='Org1',
    user_name='admin',
    cc_name='asset'  # Replace with your chaincode name
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/get-data', methods=['POST'])
def get_data():
    key = request.form.get('key')
    if not key:
        return jsonify({"error": "Key is required"}), 400

    try:
        result = fabric_client.get_data(key)
        # Convert byte response to JSON if needed
        if isinstance(result, bytes):
            result = result.decode('utf-8')
        try:
            result = json.loads(result)
        except:
            pass
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/set-data', methods=['POST'])
def set_data():
    key = request.form.get('key')
    value = request.form.get('value')

    if not key or not value:
        return jsonify({"error": "Both key and value are required"}), 400

    try:
        result = fabric_client.set_data(key, value)
        return jsonify({"success": True, "result": "Data stored successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)