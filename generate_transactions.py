import csv
import random
from datetime import datetime, timedelta

# Define merchants and their categories
MERCHANTS = {
    "Countdown Mt Eden": "Groceries",
    "Pak'nSave Hamilton": "Groceries",
    "New World Wellington": "Groceries",
    "Uber Eats NZ": "Food Delivery",
    "Dominos NZ": "Food Delivery",
    "Netflix.com": "Subscriptions",
    "Spotify AU": "Entertainment",
    "ANZ Home Loan": "Rent/Mortgage",
    "ASB Visa Debit": "General Spending",
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

ACCOUNTS = ["ANZ Everyday", "Visa Debit", "Savings", "Credit Card"]

def generate_random_transaction(date):
    merchant = random.choice(list(MERCHANTS.keys()))
    category = MERCHANTS[merchant]
    is_income = category == "Income"

    amount = round(random.uniform(500, 3000), 2) if is_income else round(random.uniform(5, 200), 2)
    if not is_income:
        amount *= -1

    return {
        "transaction_id": f"TX{random.randint(100000, 999999)}",
        "date": date.strftime("%Y-%m-%d"),
        "description": merchant,
        "amount": amount,
        "account": random.choice(ACCOUNTS),
        "category": category
    }

def generate_transactions(days=30, filename="transactions.csv"):
    today = datetime.today()
    transactions = []

    for i in range(days):
        date = today - timedelta(days=i)
        # 1 to 4 transactions per day
        for _ in range(random.randint(1, 4)):
            transactions.append(generate_random_transaction(date))

    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=transactions[0].keys())
        writer.writeheader()
        writer.writerows(transactions)

    print(f"✅ Generated {len(transactions)} transactions to {filename}")

if __name__ == "__main__":
    generate_transactions()
