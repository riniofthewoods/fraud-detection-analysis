"""
generate_data.py
Generates a synthetic credit card transaction dataset for the fraud detection
portfolio project. Data is entirely simulated (not real customer data) but is
built with realistic fraud signal patterns commonly seen in industry
literature and public datasets:
  - Fraud is more likely at unusual hours (late night)
  - Fraud is more likely at larger distances from home / from the last transaction
  - Fraud is more likely on card-not-present transactions
  - Fraud is more likely at higher transaction amounts (with some overlap)
"""

import numpy as np
import pandas as pd

np.random.seed(42)

N = 20000
FRAUD_RATE = 0.03  # ~3% fraud, realistic-ish for a portfolio-scale dataset

merchant_categories = [
    "grocery", "electronics", "gas_station", "restaurant",
    "online_retail", "travel", "entertainment", "pharmacy"
]

def generate_row(is_fraud):
    hour = np.random.normal(loc=2 if is_fraud else 14, scale=4 if is_fraud else 5)
    hour = int(np.clip(hour, 0, 23))

    distance_from_home = np.random.exponential(scale=50 if is_fraud else 8)
    distance_from_last_txn = np.random.exponential(scale=40 if is_fraud else 5)

    card_present = np.random.choice([1, 0], p=[0.2, 0.8] if is_fraud else [0.75, 0.25])

    base_amount = np.random.gamma(shape=2.0, scale=60 if is_fraud else 35)
    amount = round(min(base_amount, 5000), 2)

    category = np.random.choice(
        merchant_categories,
        p=[0.05, 0.20, 0.05, 0.05, 0.45, 0.10, 0.08, 0.02] if is_fraud
        else [0.25, 0.10, 0.20, 0.15, 0.15, 0.05, 0.08, 0.02]
    )

    return {
        "hour_of_day": hour,
        "distance_from_home_km": round(distance_from_home, 2),
        "distance_from_last_txn_km": round(distance_from_last_txn, 2),
        "card_present": card_present,
        "amount": amount,
        "merchant_category": category,
        "is_fraud": int(is_fraud),
    }

n_fraud = int(N * FRAUD_RATE)
n_legit = N - n_fraud

rows = [generate_row(True) for _ in range(n_fraud)] + \
       [generate_row(False) for _ in range(n_legit)]

df = pd.DataFrame(rows).sample(frac=1, random_state=42).reset_index(drop=True)
df.insert(0, "transaction_id", [f"TXN{100000+i}" for i in range(len(df))])

df.to_csv("/home/claude/fraud_project/data/transactions.csv", index=False)
print(f"Generated {len(df)} transactions, {df['is_fraud'].sum()} fraudulent ({df['is_fraud'].mean()*100:.2f}%)")
print(df.head())
