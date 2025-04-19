import streamlit as st
from pymongo import MongoClient
import pandas as pd
from datetime import datetime, timedelta
from fuzzywuzzy import process
import random
from dotenv import load_dotenv
import os

# Load .env and get Mongo URI
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# === MongoDB Setup ===
client = MongoClient(MONGO_URI)
db = client["SmartFinance"]
collection = db["transactions"]

KNOWN_MERCHANTS = {
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

# === Functions ===

def get_data():
    data = list(collection.find())
    df = pd.DataFrame(data)
    if "_id" in df.columns:
        df.drop(columns=["_id"], inplace=True)
    df["date"] = pd.to_datetime(df["date"])
    df["amount"] = df["amount"].astype(float)
    return df

def auto_tag_new_merchants(threshold=80):
    unknowns = list(collection.find({
        "$or": [{"category": {"$exists": False}}, {"category": "Uncategorised"}]
    }))
    for txn in unknowns:
        merchant = txn.get("description", "")
        match, score = process.extractOne(merchant, KNOWN_MERCHANTS.keys())
        if score >= threshold:
            category = KNOWN_MERCHANTS[match]
            collection.update_one({"_id": txn["_id"]}, {"$set": {"category": category}})

def generate_fake_transactions(n=3):
    today = datetime.today().strftime("%Y-%m-%d")
    for _ in range(n):
        merchant = random.choice(list(KNOWN_MERCHANTS.keys()))
        category = KNOWN_MERCHANTS[merchant]
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
        collection.insert_one(txn)

# === Streamlit UI ===

st.title("💸 SmartFinance Dashboard")
st.markdown("Live personal finance simulator powered by MongoDB + Streamlit")

if st.button("➕ Generate Random Transactions"):
    generate_fake_transactions(random.randint(2, 5))
    st.success("New data added! Refreshing...")
    st.experimental_rerun()

# Categorise unknowns
auto_tag_new_merchants()
df = get_data()

# === Daily Summary ===
today = datetime.today().date()
daily_df = df[df["date"].dt.date == today]

st.subheader("📅 Daily Summary")
if daily_df.empty:
    st.warning("No transactions yet today.")
else:
    col1, col2 = st.columns(2)
    col1.metric("💰 Income", f"${daily_df[daily_df['amount'] > 0]['amount'].sum():.2f}")
    col2.metric("💸 Expenses", f"${daily_df[daily_df['amount'] < 0]['amount'].sum():.2f}")

    st.write("**Category Breakdown (Today)**")
    st.bar_chart(daily_df.groupby("category")["amount"].sum())

    st.write("**Top Merchants (Today)**")
    top_today = (
        daily_df[daily_df["amount"] < 0]
        .groupby("description")["amount"]
        .sum()
        .sort_values()
        .head(5)
        .abs()
        .reset_index()
        .rename(columns={"amount": "Total Spent"})
    )
    top_today.index = range(1, len(top_today) + 1)
    st.dataframe(top_today)

# === All-Time Overview ===
st.subheader("📈 All-Time Overview")
col1, col2 = st.columns(2)
col1.metric("🟢 Total Income", f"${df[df['amount'] > 0]['amount'].sum():.2f}")
col2.metric("🔴 Total Expenses", f"${df[df['amount'] < 0]['amount'].sum():.2f}")

net_flow = df.groupby("date")["amount"].sum().cumsum()
st.write("**Net Cashflow Over Time**")
st.line_chart(net_flow)

st.write("**Total Spend by Category**")
cat_total = df[df["amount"] < 0].groupby("category")["amount"].sum().abs()
st.bar_chart(cat_total)

st.subheader("🏆 Top 5 Merchants by Spend (All Time)")
top_merchants = (
    df[df["amount"] < 0]
    .groupby("description")["amount"]
    .sum()
    .sort_values()
    .head(5)
    .abs()
    .reset_index()
    .rename(columns={"amount": "Total Spent"})
)
top_merchants.index = range(1, len(top_merchants) + 1)
st.dataframe(top_merchants)

# === Full Table ===
st.subheader("📋 All Transactions")
st.dataframe(df.sort_values(by="date", ascending=False).reset_index(drop=True))
