from pymongo import MongoClient

def initialize_db():
    client = MongoClient("mongodb+srv://pdevaraj:pdevaraj*01@cluster.mongodb.net/test")
    db = client['inventory_db']
    collection = db['products']
    
    # Initialize sample data
    collection.insert_many([
        {"ProductID": 1, "Name": "Widget A", "StockLevel": 50, "ReorderLevel": 20, "LastUpdated": "2024-11-24"},
        {"ProductID": 2, "Name": "Widget B", "StockLevel": 10, "ReorderLevel": 15, "LastUpdated": "2024-11-24"}
    ])
    print("Database initialized with sample data.")
    return db

if __name__ == "__main__":
    initialize_db()
