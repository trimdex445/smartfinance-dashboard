from pymongo import MongoClient
from datetime import datetime
import random

MONGO_URI = "mongodb+srv://eh01:iqLz13LBk7auQdQb@cluster0.szati1m.mongodb.net/SmartFinance?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["SmartFinance"]
collection = db["transactions"]

MERCHANTS = {
    "Countdown Grey Lynn": "Groceries",
    "Uber Eats": "Food Delivery",
    "Netflix": "Subscriptions",
    "Spotify": "Entertainment",
    "Fuel BP": "Transport",
    "Salary NZ Ltd": "Income",
    "Xero Software": "Office/Work Tools",
    "Bunnings DIY": "Home Improvement",
}

ACCOUNTS = ["ANZ Everyday", "Credit Card", "Visa Debit"]

def insert_random_transactions(n=3):
    today = datetime.today().strftime("%Y-%m-%d")
    inserted = []

    for _ in range(n):
        merchant = random.choice(list(MERCHANTS.keys()))
        category = MERCHANTS[merchant]
        is_income = category == "Income"

        amount = round(random.uniform(800, 3000), 2) if is_income else round(random.uniform(5, 200), 2)
        if not is_income:
            amount *= -1

        txn = {
            "transaction_id": f"TX{random.randint(100000, 999999)}",
            "date": today,
            "description": merchant,
            "amount": amount,
            "account": random.choice(ACCOUNTS),
            "category": category
        }
        inserted.append(txn)

    collection.insert_many(inserted)
    print(f"✅ Inserted {len(inserted)} random transactions for {today}.")

if __name__ == "__main__":
    insert_random_transactions(random.randint(2, 5))
