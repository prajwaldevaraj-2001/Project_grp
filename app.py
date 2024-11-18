from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo
from flask_socketio import SocketIO, emit

# Initialize Flask app
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/inventory_db"
mongo = PyMongo(app)
socketio = SocketIO(app)

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Get all inventory items
@app.route('/inventory', methods=['GET'])
def get_inventory():
    inventory = list(mongo.db.inventory.find({}, {"_id": 0}))
    return jsonify(inventory)

# Add a new item
@app.route('/inventory', methods=['POST'])
def add_item():
    data = request.json
    mongo.db.inventory.insert_one(data)
    return jsonify({"message": "Item added successfully"}), 201

# Update an item
@app.route('/inventory/<string:item_name>', methods=['PUT'])
def update_item(item_name):
    data = request.json
    mongo.db.inventory.update_one({"name": item_name}, {"$set": data})
    return jsonify({"message": "Item updated successfully"})

# Delete an item
@app.route('/inventory/<string:item_name>', methods=['DELETE'])
def delete_item(item_name):
    mongo.db.inventory.delete_one({"name": item_name})
    return jsonify({"message": "Item deleted successfully"})

# Real-time stock alerts
@socketio.on('check_stock')
def check_stock(data):
    stock_level = data.get('stock_level', 0)
    if stock_level < 5:  # Threshold for alerts
        emit('low_stock_alert', {'message': f"Low stock alert for {data['name']}!"}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
