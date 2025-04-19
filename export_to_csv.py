from pymongo import MongoClient
import csv

MONGO_URI = "mongodb+srv://eh01:iqLz13LBk7auQdQb@cluster0.szati1m.mongodb.net/SmartFinance?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["SmartFinance"]
collection = db["transactions"]

def export_csv(output_file="cleaned_transactions.csv"):
    transactions = list(collection.find())
    
    if not transactions:
        print("⚠️ No data found.")
        return

    keys = ["transaction_id", "date", "description", "amount", "account", "category"]

    with open(output_file, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        for txn in transactions:
            # Filter only expected keys and clean values
            row = {k: txn.get(k, "") for k in keys}
            writer.writerow(row)

    print(f"✅ Exported {len(transactions)} transactions to '{output_file}'.")

if __name__ == "__main__":
    export_csv()
