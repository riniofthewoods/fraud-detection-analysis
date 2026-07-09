# SQL Exploratory Analysis Results

## Overall fraud rate

```sql
SELECT
            COUNT(*) AS total_transactions,
            SUM(is_fraud) AS fraud_count,
            ROUND(100.0 * SUM(is_fraud) / COUNT(*), 2) AS fraud_rate_pct
        FROM transactions;
```

|   total_transactions |   fraud_count |   fraud_rate_pct |
|---------------------:|--------------:|-----------------:|
|                20000 |           600 |                3 |

## Fraud rate by merchant category

```sql
SELECT
            merchant_category,
            COUNT(*) AS total_txns,
            SUM(is_fraud) AS fraud_txns,
            ROUND(100.0 * SUM(is_fraud) / COUNT(*), 2) AS fraud_rate_pct
        FROM transactions
        GROUP BY merchant_category
        ORDER BY fraud_rate_pct DESC;
```

| merchant_category   |   total_txns |   fraud_txns |   fraud_rate_pct |
|:--------------------|-------------:|-------------:|-----------------:|
| online_retail       |         3208 |          266 |             8.29 |
| electronics         |         2072 |          122 |             5.89 |
| travel              |         1077 |           59 |             5.48 |
| entertainment       |         1631 |           50 |             3.07 |
| pharmacy            |          430 |            9 |             2.09 |
| restaurant          |         2857 |           26 |             0.91 |
| grocery             |         4813 |           38 |             0.79 |
| gas_station         |         3912 |           30 |             0.77 |

## Fraud rate by hour of day

```sql
SELECT
            hour_of_day,
            COUNT(*) AS total_txns,
            SUM(is_fraud) AS fraud_txns,
            ROUND(100.0 * SUM(is_fraud) / COUNT(*), 2) AS fraud_rate_pct
        FROM transactions
        GROUP BY hour_of_day
        ORDER BY hour_of_day;
```

|   hour_of_day |   total_txns |   fraud_txns |   fraud_rate_pct |
|--------------:|-------------:|-------------:|-----------------:|
|             0 |          350 |          258 |            73.71 |
|             1 |          132 |           64 |            48.48 |
|             2 |          174 |           55 |            31.61 |
|             3 |          228 |           52 |            22.81 |
|             4 |          321 |           59 |            18.38 |
|             5 |          414 |           37 |             8.94 |
|             6 |          507 |           31 |             6.11 |
|             7 |          687 |           20 |             2.91 |
|             8 |          893 |           11 |             1.23 |
|             9 |         1027 |            5 |             0.49 |
|            10 |         1267 |            5 |             0.39 |
|            11 |         1357 |            3 |             0.22 |
|            12 |         1437 |            0 |             0    |
|            13 |         1500 |            0 |             0    |
|            14 |         1535 |            0 |             0    |
|            15 |         1449 |            0 |             0    |
|            16 |         1422 |            0 |             0    |
|            17 |         1140 |            0 |             0    |
|            18 |         1046 |            0 |             0    |
|            19 |          878 |            0 |             0    |
|            20 |          637 |            0 |             0    |
|            21 |          521 |            0 |             0    |
|            22 |          368 |            0 |             0    |
|            23 |          710 |            0 |             0    |

## Card-present vs card-not-present fraud rate

```sql
SELECT
            CASE WHEN card_present = 1 THEN 'Card Present' ELSE 'Card Not Present' END AS channel,
            COUNT(*) AS total_txns,
            SUM(is_fraud) AS fraud_txns,
            ROUND(100.0 * SUM(is_fraud) / COUNT(*), 2) AS fraud_rate_pct
        FROM transactions
        GROUP BY card_present;
```

| channel          |   total_txns |   fraud_txns |   fraud_rate_pct |
|:-----------------|-------------:|-------------:|-----------------:|
| Card Not Present |         5277 |          479 |             9.08 |
| Card Present     |        14723 |          121 |             0.82 |

## Average distance metrics: fraud vs legitimate

```sql
SELECT
            CASE WHEN is_fraud = 1 THEN 'Fraud' ELSE 'Legitimate' END AS txn_type,
            ROUND(AVG(distance_from_home_km), 2) AS avg_distance_from_home,
            ROUND(AVG(distance_from_last_txn_km), 2) AS avg_distance_from_last_txn,
            ROUND(AVG(amount), 2) AS avg_amount
        FROM transactions
        GROUP BY is_fraud;
```

| txn_type   |   avg_distance_from_home |   avg_distance_from_last_txn |   avg_amount |
|:-----------|-------------------------:|-----------------------------:|-------------:|
| Legitimate |                     7.96 |                         4.95 |        69.87 |
| Fraud      |                    49.22 |                        38.4  |       121.41 |

## Highest-risk segment: late night + card-not-present

```sql
SELECT
            COUNT(*) AS total_txns,
            SUM(is_fraud) AS fraud_txns,
            ROUND(100.0 * SUM(is_fraud) / COUNT(*), 2) AS fraud_rate_pct
        FROM transactions
        WHERE hour_of_day BETWEEN 0 AND 5
          AND card_present = 0;
```

|   total_txns |   fraud_txns |   fraud_rate_pct |
|-------------:|-------------:|-----------------:|
|          705 |          415 |            58.87 |

