from flask import Flask, request, jsonify
import sqlite3
import database as db_funcs
import datetime

app = Flask(__name__)


# Function to connect to the SQLite database
def connect_db():
    conn = sqlite3.connect('market.db')
    return conn

# Route to create a new user
@app.route('/adduser', methods=['POST'])
def add_user():
    conn = connect_db()
    cursor = conn.cursor()

    data = request.form

    money = data.get('accountMoney')
    firstName = data.get('firstName')
    lastName = data.get('lastName')

    # Insert data into the database
    cursor.execute("INSERT INTO users (AccountMoney, FirstName, LastName) VALUES (?, ?, ?)", (money, firstName, lastName))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'User created successfully'}), 201

# Route to get all users
@app.route('/users', methods=['GET'])
def get_users():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    
    conn.close()
    
    user_list = []
    for user in users:
        user_dict = {
            'userId': user[0],
            'money': user[1],
            'firstName': user[2],
            'lastName': user[3]
        }
        user_list.append(user_dict)
    
    return jsonify(user_list)

# Route to get a users balance
@app.route('/usermoney', methods=['GET'])
def get_user_money():
    conn = connect_db()
    cursor = conn.cursor()
    
    data = request.form
    userId = data.get('userId')

    print(userId)

    cursor.execute(f'SELECT AccountMoney FROM Users WHERE UserId = {userId}')
    money = cursor.fetchone()
    conn.close()
    
    return jsonify(money[0])

# Route to update a users balance
@app.route('/usermoneyupdate', methods=['POST'])
def update_user_money():
    conn = connect_db()
    cursor = conn.cursor()
    
    data = request.form
    userId = data.get('userId')
    updatedBalance = data.get('balance')

    cursor.execute("UPDATE Users SET AccountMoney = ? WHERE UserId = ?", (updatedBalance, userId))

    conn.commit()
    conn.close()
    
    return jsonify("Updated Account Balance")


@app.route('/addorders', methods=['POST'])
def add_orders():
    conn = connect_db()
    cursor = conn.cursor()

    data = request.form

    stationId = data.get('stationId')
    startTime = data.get('startTime')
    endTime = data.get('endTime')
    startBikes = data.get('startBikes')
    endBikes = data.get('endBikes')
    multiplier = data.get('multiplier')
    isBuy = data.get('isBuy')


    # Insert data into the database
    cursor.execute("INSERT INTO Orders (StationId, StartTime, EndTime, StartBikeCount, EndBikeCount, PayoutMultiplier, isBuy) VALUES (?, ?, ?, ?, ?, ?, ?)", (stationId, startTime, endTime, startBikes, endBikes, multiplier, isBuy))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Order created successfully'}), 201


@app.route('/orders', methods=['GET'])
def get_orders():
    conn = connect_db()
    cursor = conn.cursor()

    # Insert data into the database
    cursor.execute("SELECT * FROM Orders")
    orders = cursor.fetchall()
    
    conn.close()
    
    order_list = []
    for order in orders:
        order_dict = {
            'OrderId': order[0],
            'StationId': order[1],
            'StartTime':order[2],
            'EndTime': order[3],
            'StartBikeCount': order[4],
            'EndBikeCount': order[5],
            'PayoutMultiplier': order[6],
        }
        order_list.append(order_dict)
    
    return jsonify(order_list)


@app.route('/addcontract', methods=['POST'])
def add_contracts():
    conn = connect_db()
    cursor = conn.cursor()

    data = request.form
    userId = data.get('userId')
    userBet = data.get('userBet')
    orderId = data.get('orderId')

    # Insert data into the database
    cursor.execute("INSERT INTO Contracts (UserId, UserBet, OrderId) VALUES (?, ?, ?)", (userId, userBet, orderId))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Contract created successfully'}), 201

@app.route('/contracts', methods=['GET'])
def get_contracts():
    conn = connect_db()
    cursor = conn.cursor()

    # Insert data into the database
    cursor.execute("SELECT * FROM Contracts")
    contracts = cursor.fetchall()
    
    conn.close()
    
    contract_list = []
    for contract in contracts:
        contract_dict = {
            'ContractId': contract[0],
            'UserId': contract[1],
            'UserBet':contract[2],
            'OrderId': contract[3]
        }
        contract_list.append(contract_dict)
    
    return jsonify(contract_list)

@app.route('/livecontracts', methods=['GET'])
def get_live_contracts():
    conn = connect_db()
    cursor = conn.cursor()

    data = request.form
    earliestTime = data.get('earliestTime')
    latestTime = data.get('latestTime')

    # Insert data into the database
    cursor.execute(
        f'''
            SELECT Contracts.*, Orders.*
            FROM Contracts
            JOIN ORDERS ON Contracts.orderId = Orders.orderId
            WHERE Orders.EndTime > {earliestTime} AND Orders.EndTime < {latestTime}
            ORDER BY Orders.EndTime;
        '''
        )
    contracts = cursor.fetchall()
    
    conn.close()
    
    contract_list = []
    for contract in contracts:
        contract_dict = {
            'ContractId': contract[0],
            'UserId': contract[1],
            'UserBet':contract[2]
        }
        contract_list.append(contract_dict)
    
    return jsonify(contract_list)

@app.route('/stations', methods=['GET'])
def get_stations():
    return jsonify(db_funcs.get_stations())

@app.route('/addstation', methods = ['POST'])
def add_station():
    conn = sqlite3.connect('market.db')
    cursor = conn.cursor()
    
    data = request.form
    stationName = data.get('stationName')

    print(stationName)

    # Insert the station into the database
    cursor.execute("INSERT INTO Stations (stationName) VALUES (?)", (stationName,))
    
    conn.commit()
    conn.close()

    return jsonify("Added Station")


@app.route('/orderprices', methods=['GET'])
def get_orderprices():
    conn = connect_db()
    cursor = conn.cursor()
    now = datetime.datetime.now()
    before = datetime.timedelta(minutes = -15)

    cursor.execute(f'SELECT * FROM ORDERS')# WHERE ORDERS.StartTime > {before} AND ORDERS.StartTime < {now}')
    order_list = cursor.fetchall()
    
    orders = []
    for order in order_list:
        order_dict = {
            'order_id': order[0],
            'station_id': order[1],
            'start_time':order[2],
            'end_time':order[3],
            'start_bike_count':order[4],
            'end_bike_count':order[5],
            'payout_multiple':order[6],
            'is_buy':order[7]
        }
        orders.append(order_dict)
    
    return jsonify(orders)


if __name__ == '__main__':
    db_funcs.create_db()
    app.run(host='0.0.0.0', port=5000, debug=True)

