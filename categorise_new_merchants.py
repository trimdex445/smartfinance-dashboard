from pymongo import MongoClient
from fuzzywuzzy import process

MONGO_URI = "mongodb+srv://eh01:iqLz13LBk7auQdQb@cluster0.szati1m.mongodb.net/SmartFinance?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["SmartFinance"]
collection = db["transactions"]

# Known merchants + their categories
KNOWN_MERCHANTS = {
    "Countdown Mt Eden": "Groceries",
    "Pak'nSave Hamilton": "Groceries",
    "New World Wellington": "Groceries",
    "Uber Eats NZ": "Food Delivery",
    "Dominos NZ": "Food Delivery",
    "Netflix.com": "Subscriptions",
    "Spotify AU": "Entertainment",
    "ANZ Home Loan": "Rent/Mortgage",
    "Apple iCloud": "Subscriptions",
    "BP Fuel Auckland": "Transport",
    "Z Energy Newtown": "Transport",
    "Warehouse Stationery": "Office/School Supplies",
    "Noel Leeming": "Electronics",
    "Chemist Warehouse": "Healthcare",
    "Gym NZ Ltd": "Fitness",
    "Salary Payment": "Income",
    "Freelance Transfer": "Income",
    "IRD Refund": "Income",
    "Bunnings Warehouse": "Home Improvement",
}

def tag_unknown_merchants(threshold=80):
    transactions = list(collection.find({
        "$or": [{"category": {"$exists": False}}, {"category": "Uncategorised"}]
    }))

    print(f"\n🔍 Found {len(transactions)} uncategorised transactions...\n")

    for txn in transactions:
        merchant = txn.get("description", "")
        match, score = process.extractOne(merchant, KNOWN_MERCHANTS.keys())
        
        if score >= threshold:
            new_category = KNOWN_MERCHANTS[match]
            collection.update_one(
                {"_id": txn["_id"]},
                {"$set": {"category": new_category}}
            )
            print(f"✅ Matched '{merchant}' to '{match}' ({score}) → {new_category}")
        else:
            print(f"❌ No good match for: '{merchant}' (score {score})")

if __name__ == "__main__":
    tag_unknown_merchants()
