from pymongo import MongoClient

# Your connection string
MONGO_URI = "mongodb+srv://ngocvo14198_db_user:Phuongthy1411!@cluster0.gfm5gls.mongodb.net/?appName=Cluster0"

print("🔄 Testing MongoDB connection...")

try:
    # Connect to MongoDB
    client = MongoClient(MONGO_URI)

    # Test the connection with ping
    client.admin.command('ping')
    print("✅ SUCCESS! Connected to MongoDB Atlas!")

    # Access the database and collection
    db = client['lunch_database']
    collection = db['menu_items']

    print(f"✅ Database: {db.name}")
    print(f"✅ Collection: {collection.name}")

    # Insert a test item
    test_item = {
        'name': 'Test Pizza',
        'price': 4.99
    }
    result = collection.insert_one(test_item)
    print(f"✅ Test item inserted with ID: {result.inserted_id}")

    # Read it back
    found = collection.find_one({'_id': result.inserted_id})
    print(f"✅ Retrieved: {found['name']} - ${found['price']}")

    # Clean up - delete test item
    collection.delete_one({'_id': result.inserted_id})
    print("✅ Test item cleaned up")

    print("\n🎉 All tests passed! MongoDB is ready to use!")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\n💡 Troubleshooting:")
    print("1. Check Network Access in MongoDB allows your IP")
    print("2. Verify the connection string is correct")
    print("3. Make sure database user password is correct")