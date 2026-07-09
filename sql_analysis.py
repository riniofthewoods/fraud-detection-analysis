"""
sql_analysis.py
Loads the transaction data into a local SQLite database and runs a series of
SQL queries to explore fraud patterns -- the kind of exploratory analysis a
fraud analyst would run to understand where risk concentrates.
"""

import sqlite3
import pandas as pd

df = pd.read_csv("/home/claude/fraud_project/data/transactions.csv")

conn = sqlite3.connect("/home/claude/fraud_project/data/transactions.db")
df.to_sql("transactions", conn, if_exists="replace", index=False)

queries = {
    "Overall fraud rate": """
        SELECT
            COUNT(*) AS total_transactions,
            SUM(is_fraud) AS fraud_count,
            ROUND(100.0 * SUM(is_fraud) / COUNT(*), 2) AS fraud_rate_pct
        FROM transactions;
    """,
    "Fraud rate by merchant category": """
        SELECT
            merchant_category,
            COUNT(*) AS total_txns,
            SUM(is_fraud) AS fraud_txns,
            ROUND(100.0 * SUM(is_fraud) / COUNT(*), 2) AS fraud_rate_pct
        FROM transactions
        GROUP BY merchant_category
        ORDER BY fraud_rate_pct DESC;
    """,
    "Fraud rate by hour of day": """
        SELECT
            hour_of_day,
            COUNT(*) AS total_txns,
            SUM(is_fraud) AS fraud_txns,
            ROUND(100.0 * SUM(is_fraud) / COUNT(*), 2) AS fraud_rate_pct
        FROM transactions
        GROUP BY hour_of_day
        ORDER BY hour_of_day;
    """,
    "Card-present vs card-not-present fraud rate": """
        SELECT
            CASE WHEN card_present = 1 THEN 'Card Present' ELSE 'Card Not Present' END AS channel,
            COUNT(*) AS total_txns,
            SUM(is_fraud) AS fraud_txns,
            ROUND(100.0 * SUM(is_fraud) / COUNT(*), 2) AS fraud_rate_pct
        FROM transactions
        GROUP BY card_present;
    """,
    "Average distance metrics: fraud vs legitimate": """
        SELECT
            CASE WHEN is_fraud = 1 THEN 'Fraud' ELSE 'Legitimate' END AS txn_type,
            ROUND(AVG(distance_from_home_km), 2) AS avg_distance_from_home,
            ROUND(AVG(distance_from_last_txn_km), 2) AS avg_distance_from_last_txn,
            ROUND(AVG(amount), 2) AS avg_amount
        FROM transactions
        GROUP BY is_fraud;
    """,
    "Highest-risk segment: late night + card-not-present": """
        SELECT
            COUNT(*) AS total_txns,
            SUM(is_fraud) AS fraud_txns,
            ROUND(100.0 * SUM(is_fraud) / COUNT(*), 2) AS fraud_rate_pct
        FROM transactions
        WHERE hour_of_day BETWEEN 0 AND 5
          AND card_present = 0;
    """,
}

with open("/home/claude/fraud_project/sql/query_results.md", "w") as f:
    f.write("# SQL Exploratory Analysis Results\n\n")
    for title, query in queries.items():
        result = pd.read_sql_query(query, conn)
        f.write(f"## {title}\n\n")
        f.write(f"```sql\n{query.strip()}\n```\n\n")
        f.write(result.to_markdown(index=False))
        f.write("\n\n")
        print(f"\n=== {title} ===")
        print(result.to_string(index=False))

conn.close()
print("\nSaved full results to sql/query_results.md")
