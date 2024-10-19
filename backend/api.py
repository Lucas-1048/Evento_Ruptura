from flask import Flask, request, jsonify
from services import process_request  
from Database.populate import initialize_databases
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route('/process', methods=['POST'])
def process():
    try:
        data = request.get_json()

        if 'message' not in data:
            return jsonify({'error': 'Mensagem não fornecida'}), 400
        
        response = process_request(data['message'])
        return jsonify({'response': response}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    initialize_databases()
    app.run(debug=True)
