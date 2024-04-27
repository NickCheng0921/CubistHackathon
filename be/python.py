from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Function to connect to the SQLite database
def connect_db():
    conn = sqlite3.connect('example.db')
    return conn

# Route to create a new user
@app.route('/user', methods=['POST'])
def create_user():
    conn = connect_db()
    cursor = conn.cursor()
    
    # Extract data from the request
    data = request.json
    userId = data.get('userId')
    contractId = data.get('email')
    
    # Insert data into the database
    cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", (username, email))
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
            'id': user[0],
            'username': user[1],
            'email': user[2]
        }
        user_list.append(user_dict)
    
    return jsonify(user_list)


# Route to get all users
@app.route('/get_pricing', methods=['GET'])
def get_users():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Stations")
    station_list = cursor.fetchall()

    data = request.json
    
    station_list = []
    for station in station_list:
        station_dict = {
            'id': station[0],
            'station name': station[1],
        }
        station_list.append(station_dict)
    
    return jsonify(station_list)

# Route to get all users
@app.route('/test', methods=['GET'])
def get_test():

    
    return jsonify("Hello World")

if __name__ == '__main__':
    app.run(debug=True)
