from pymongo import MongoClient
import csv

# Replace this with your actual connection string
MONGO_URI = "mongodb+srv://eh01:iqLz13LBk7auQdQb@cluster0.szati1m.mongodb.net/SmartFinance?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)
db = client["SmartFinance"]
collection = db["transactions"]

def insert_transactions(csv_file):
    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file)
        transactions = list(reader)
        for txn in transactions:
            txn["amount"] = float(txn["amount"])
        collection.insert_many(transactions)
        print(f"✅ Inserted {len(transactions)} transactions into MongoDB Atlas.")

if __name__ == "__main__":
    insert_transactions("transactions.csv")
