from pymongo import MongoClient
from collections import defaultdict

MONGO_URI = "mongodb+srv://eh01:iqLz13LBk7auQdQb@cluster0.szati1m.mongodb.net/SmartFinance?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["SmartFinance"]
collection = db["transactions"]

def analyse_transactions():
    transactions = list(collection.find())

    total_income = 0
    total_expense = 0
    category_totals = defaultdict(float)
    merchant_totals = defaultdict(float)

    for txn in transactions:
        amount = txn["amount"]
        category = txn.get("category", "Uncategorised")
        merchant = txn.get("description", "Unknown")

        if amount > 0:
            total_income += amount
        else:
            total_expense += amount

        category_totals[category] += amount
        merchant_totals[merchant] += amount

    print(f"\n💰 Total Income: ${round(total_income, 2)}")
    print(f"💸 Total Expenses: ${round(total_expense, 2)}\n")

    print("📊 Spend by Category:")
    for cat, amt in category_totals.items():
        print(f" - {cat}: ${round(amt, 2)}")

    print("\n🏷️ Top 5 Merchants by Expense:")
    sorted_merchants = sorted(merchant_totals.items(), key=lambda x: x[1])
    for merchant, amt in sorted_merchants[:5]:
        print(f" - {merchant}: ${round(amt, 2)}")

if __name__ == "__main__":
    analyse_transactions()
