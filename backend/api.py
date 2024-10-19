from flask import Flask, request, jsonify
from services import process_request  
from Database.populate import init_messages_database, populate_vehicles_database
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route('/process', methods=['POST'])
@cross_origin(allow_headers=['Content-Type', ], origins='*')
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
    csv_file_path = '../backend/Database/ruptura_vehicles.csv' 
    db_file_path = '../backend/Database/ruptura_vehicles.db'


    populate_vehicles_database(csv_file_path, db_file_path)
    init_messages_database()


    app.run(debug=True)
