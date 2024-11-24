from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app)

# Connect to MongoDB
client = MongoClient("mongodb+srv://<username>:<password>@cluster.mongodb.net/test")
db = client['inventory_db']
products = db['products']

@app.route("/")
def home():
    """Render the dashboard."""
    return render_template("dashboard.html")

@app.route("/api/products", methods=["GET"])
def get_products():
    """Fetch all products."""
    product_list = list(products.find({}, {"_id": 0}))
    return jsonify(product_list)

@app.route("/api/update-stock", methods=["POST"])
def update_stock():
    """Update stock levels."""
    data = request.json
    products.update_one(
        {"ProductID": data['ProductID']},
        {"$set": {
            "StockLevel": data['StockLevel'],
            "LastUpdated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }}
    )
    # Emit a real-time update to all connected clients
    socketio.emit("update", {"ProductID": data['ProductID'], "StockLevel": data['StockLevel']})
    return jsonify({"message": "Stock updated successfully."})

@socketio.on("connect")
def on_connect():
    print("Client connected.")

if __name__ == "__main__":
    socketio.run(app, debug=True)
