from pymongo import MongoClient
from datetime import datetime, timedelta
from collections import defaultdict

MONGO_URI = "mongodb+srv://eh01:iqLz13LBk7auQdQb@cluster0.szati1m.mongodb.net/SmartFinance?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["SmartFinance"]
collection = db["transactions"]

def generate_daily_summary():
    today = datetime.today().strftime("%Y-%m-%d")
    transactions = list(collection.find({"date": today}))

    if not transactions:
        print(f"\n📅 {today}: No transactions found.")
        return

    income, expense = 0, 0
    by_category = defaultdict(float)

    for txn in transactions:
        amount = txn["amount"]
        category = txn.get("category", "Uncategorised")

        if amount > 0:
            income += amount
        else:
            expense += amount

        by_category[category] += amount

    print(f"\n📅 Daily Summary for {today}")
    print(f"💰 Income:     ${round(income, 2)}")
    print(f"💸 Expenses:   ${round(expense, 2)}")
    print("\n📊 By Category:")
    for cat, amt in by_category.items():
        print(f" - {cat}: ${round(amt, 2)}")

if __name__ == "__main__":
    generate_daily_summary()
