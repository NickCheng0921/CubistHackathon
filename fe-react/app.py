from flask import Flask, render_template, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map_data')
def map_data():
    # Generate random coordinates for demonstration
    lat = random.uniform(-90, 90)
    lng = random.uniform(-180, 180)
    data = {'lat': lat, 'lng': lng}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
