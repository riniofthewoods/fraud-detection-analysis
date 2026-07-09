# Credit Card Transaction Fraud Detection — Exploratory Analysis & Baseline Model

## Overview

This project simulates a common fraud-analytics workflow: given a set of
credit card transactions, identify the patterns that distinguish fraudulent
activity from legitimate activity, and build a baseline model to flag likely
fraud.

**A note on the data:** this project uses a **synthetically generated
dataset** (20,000 simulated transactions, ~3% fraud rate), not real financial
data. The generation script deliberately encodes realistic fraud signal
patterns commonly discussed in fraud-analytics literature (e.g., unusual
transaction hours, distance anomalies, card-not-present risk) so the dataset
behaves like a real one for analysis purposes. This approach was used
because real transaction data is sensitive and not publicly available at
this scale — the goal here is to demonstrate the analytical workflow and
tools, not to claim access to real financial records.

## Tools Used

- **Python** (pandas, numpy) — data generation and manipulation
- **SQL** (SQLite) — exploratory queries and aggregation
- **scikit-learn** — baseline logistic regression fraud-detection model
- **matplotlib / seaborn** — data visualization

## Project Structure

```
fraud_project/
├── generate_data.py          # Generates the synthetic transaction dataset
├── sql_analysis.py           # Loads data into SQLite, runs exploratory SQL queries
├── fraud_analysis.py         # EDA visualizations + baseline ML model
├── data/
│   ├── transactions.csv      # Generated dataset
│   └── transactions.db       # SQLite database
├── sql/
│   └── query_results.md      # Full SQL query results
└── notebooks/
    ├── exploratory_analysis.png
    ├── roc_curve.png
    └── model_results.md
```

## Key Findings (SQL Exploratory Analysis)

- **Overall fraud rate:** 3.00% of transactions
- **Highest-risk merchant category:** Online retail (8.29% fraud rate) vs.
  gas stations, the lowest (0.77%)
- **Time-of-day risk:** Fraud is heavily concentrated in overnight hours —
  73.7% of transactions between midnight and 1 AM were fraudulent, dropping
  to near-zero during normal daytime hours
- **Channel risk:** Card-not-present transactions had an 9.08% fraud rate,
  more than 11x higher than card-present transactions (0.82%)
- **Distance anomalies:** Fraudulent transactions averaged 49.2 km from the
  cardholder's home address and 38.4 km from their previous transaction —
  both roughly 6-8x higher than legitimate transactions
- **Highest-risk segment identified:** transactions between midnight-5 AM
  AND card-not-present had a 58.9% fraud rate, versus 3.0% overall — a clear
  candidate for a targeted detection rule

See `sql/query_results.md` for the full query set and results.

## Baseline Model Results

A logistic regression model (class-balanced) was trained on the five core
features (hour of day, distance from home, distance from last transaction,
card-present flag, transaction amount, merchant category):

- **ROC AUC: 0.996**
- **Fraud recall: 97%** (correctly identified 145 of 150 fraud cases in the
  test set)
- **Fraud precision: 57%** (108 false positives — legitimate transactions
  incorrectly flagged)

The precision/recall tradeoff here is intentional and typical of real fraud
models: catching nearly all fraud (high recall) comes at the cost of also
flagging some legitimate transactions (lower precision). In a production
setting, this tradeoff would be tuned based on the business cost of a missed
fraud case versus the cost of a false alarm (e.g., a declined legitimate
purchase or a manual review queue).

See `notebooks/model_results.md` for the full classification report and
confusion matrix, and `notebooks/roc_curve.png` for the ROC curve.

## What This Project Demonstrates

- Writing and interpreting SQL aggregation queries to surface risk patterns
- Using Python/pandas for data manipulation and feature exploration
- Building clear, decision-relevant data visualizations
- Training and evaluating a baseline classification model with scikit-learn
- Translating analytical findings into a plain-language business
  recommendation (the "high-risk segment" rule above is exactly the kind of
  finding a fraud analyst would escalate for a real-time detection rule)

## Limitations & Next Steps

- Real-world fraud data would require additional features (device
  fingerprinting, velocity checks, historical account behavior) not modeled
  here
- A production model would need to be validated against concept drift, as
  fraud patterns evolve over time
- Next iteration: test a gradient-boosted model (XGBoost/LightGBM) and
  compare performance against this logistic regression baseline
