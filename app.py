from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv() #read .env file

app = Flask(__name__)
CORS(app) #allows frontend to call backend API

#Frontend
@app.route("/")
def index():
    return render_template("index.html")

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://ngocvo14198_db_user:Phuongthy1411!@5-dollar.7iv3lca.mongodb.net/?appName=5-dollar")
client = MongoClient(MONGO_URI)
db = client["budget_bites"]
items_collection = db["food_items"]

def seed_data():
    if items_collection.count_documents({}) == 0:
        sample_items = [
            {"name": "Subway", "price": 8.99, "category": "sandwich", "image_url": "https://www.allrecipes.com/thmb/r6AiELAYCRkEtawhdfSMSrxZYkM=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/ar-subway-taste-test-4x3-7089b564638a438d822f29712fb4b9aa.jpg"},
            {"name": "McDonald's", "price": 5.49, "category": "burger", "image_url": "https://www.foodandwine.com/thmb/8N5jLutuTK4TDzpDkhMfdaHLZxI=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/McDonalds-Hacks-Menu-FT-1-BLOG0122-4ac9d62f6c9143be8da3d0a8553348b0.jpg"},
            {"name": "Starbucks", "price": 6.25, "category": "drink", "image_url": "https://about.starbucks.com/uploads/2025/07/Starbucks-Strato-Frappuccino.png"},
            {"name": "Chipotle", "price": 9.50, "category": "mexican", "image_url": "https://people.com/thmb/NCcT2j0aSvaQoqEqyx--VjwSrnk=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc():focal(722x388:724x390)/Chipotle-Carne-Asada-090225-fe7611404903410c86b07f56d8336904.jpg"},
            {"name": "Panda Express", "price": 8.25, "category": "asian", "image_url": "https://tb-static.uber.com/prod/image-proc/processed_images/6e31d1c53b6237ef53f7c3ec6d570589/c67d558c633281f9c71fc6a90ef470ae.jpeg"},
            {"name": "Taco Bell", "price": 7.99, "category": "mexican", "image_url": "https://tacobell.com.my/wp-content/uploads/2020/09/CRUNCHY-TACO-SUPREME-COMBO-400x400-2.jpg"},
            {"name": "Pizza Hut", "price": 3.99, "category": "pizza", "image_url": "http://a.mktgcdn.com/p/d9AXTJEWMZ156q11dLLVRHsmufNu0K-ng4JYb_4WwRI/4500x3381.jpg"},
        ]
        items_collection.insert_many(sample_items)
        print("Seeded database with sample food items.")

#reads from MongoDB, filters by budget and/or category, returns JSON.
@app.route("/api/items", methods=["GET"])
def get_items():
    budget = request.args.get("budget", type=float)
    category = request.args.get("category", "")

    query = {}
    if budget is not None:
        query["price"] = {"$lte": budget}
    if category:
        query["category"] = category

    items = list(items_collection.find(query, {"_id": 0}).sort("price", 1))
    return jsonify({"items": items, "count": len(items)})

#creates a new food item in MongoDB.
@app.route("/api/items", methods=["POST"])
def add_item():
    data = request.get_json()
    required = ["name", "price", "category"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    new_item = {
        "name": data["name"],
        "price": float(data["price"]),
        "category": data["category"],
        "image_url": data.get("image_url", ""),
    }
    items_collection.insert_one(new_item)
    new_item.pop("_id", None)
    return jsonify({"message": "Item added!", "item": new_item}), 201

# returns all unique category names.
@app.route("/api/categories", methods=["GET"])
def get_categories():
    cats = items_collection.distinct("category")
    return jsonify({"categories": sorted(cats)})

#check if the server is alive
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    seed_data()
    app.run(host="0.0.0.0", port=5000, debug=False)