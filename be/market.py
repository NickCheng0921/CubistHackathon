from flask import Flask, request, jsonify
import sqlite3
import database as db_funcs
import requests

app = Flask(__name__)


# Route for the front end to get all possible pricings.
@app.route('/assets', methods=['GET'])
def get_assets():
    response = requests.get('http://127.0.0.1:5000/orderprices')
    
    # Check if the request was successful
    if response.status_code == 200:
        #print(response.json)
        return response.json()

# Route for the front end to purchase a pricing.
@app.route('/addcontract', methods=['POST'])
def add_contracts():
    data = request.form
    userId = data.get('userId')
    userBet = data.get('userBet')
    orderId = data.get('orderId')

    files = {
        'userId': (None, userId),
        'userBet': (None, userBet),
        'orderId': (None, orderId)
    }
    response = requests.post(url='http://127.0.0.1:5000/addcontract', files=files)

    return jsonify({'message': 'Order placed'}), 201


if __name__ == '__main__':
    db_funcs.create_db()
    app.run(host='0.0.0.0', port=4000, debug=True)

