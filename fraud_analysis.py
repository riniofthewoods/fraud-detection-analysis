"""
fraud_analysis.py
Exploratory data analysis, visualization, and a baseline fraud-detection
model built with scikit-learn. This is the core analytical piece of the
portfolio project -- it demonstrates Python, pandas, visualization, and
basic machine learning applied to a fraud-detection problem.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report, confusion_matrix, roc_auc_score, roc_curve
)

sns.set_theme(style="whitegrid")
OUT = "/home/claude/fraud_project/notebooks"

df = pd.read_csv("/home/claude/fraud_project/data/transactions.csv")

# ---------------------------------------------------------------
# 1. Exploratory visualizations
# ---------------------------------------------------------------

fig, axes = plt.subplots(2, 2, figsize=(13, 9))

# Fraud rate by hour
hourly = df.groupby("hour_of_day")["is_fraud"].mean() * 100
axes[0, 0].bar(hourly.index, hourly.values, color="#c0392b")
axes[0, 0].set_title("Fraud Rate by Hour of Day")
axes[0, 0].set_xlabel("Hour of Day")
axes[0, 0].set_ylabel("Fraud Rate (%)")

# Amount distribution: fraud vs legit
sns.kdeplot(data=df[df.is_fraud == 0], x="amount", label="Legitimate", ax=axes[0, 1], fill=True)
sns.kdeplot(data=df[df.is_fraud == 1], x="amount", label="Fraud", ax=axes[0, 1], fill=True)
axes[0, 1].set_title("Transaction Amount Distribution")
axes[0, 1].set_xlim(0, 500)
axes[0, 1].legend()

# Distance from home: fraud vs legit
sns.boxplot(data=df, x="is_fraud", y="distance_from_home_km", ax=axes[1, 0])
axes[1, 0].set_xticklabels(["Legitimate", "Fraud"])
axes[1, 0].set_title("Distance from Home")
axes[1, 0].set_ylim(0, 200)

# Fraud rate by merchant category
cat_rate = (df.groupby("merchant_category")["is_fraud"].mean() * 100).sort_values(ascending=False)
axes[1, 1].barh(cat_rate.index, cat_rate.values, color="#2980b9")
axes[1, 1].set_title("Fraud Rate by Merchant Category")
axes[1, 1].set_xlabel("Fraud Rate (%)")

plt.tight_layout()
plt.savefig(f"{OUT}/exploratory_analysis.png", dpi=150)
plt.close()
print("Saved exploratory_analysis.png")

# ---------------------------------------------------------------
# 2. Baseline fraud-detection model (Logistic Regression)
# ---------------------------------------------------------------

feature_cols = [
    "hour_of_day", "distance_from_home_km", "distance_from_last_txn_km",
    "card_present", "amount", "merchant_category"
]
X = df[feature_cols]
y = df["is_fraud"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

numeric_features = ["hour_of_day", "distance_from_home_km", "distance_from_last_txn_km", "amount"]
categorical_features = ["merchant_category"]
passthrough_features = ["card_present"]

preprocessor = ColumnTransformer(transformers=[
    ("num", StandardScaler(), numeric_features),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
])

model = Pipeline(steps=[
    ("preprocess", preprocessor),
    ("classifier", LogisticRegression(class_weight="balanced", max_iter=1000)),
])

model.fit(X_train, y_train)
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

report = classification_report(y_test, y_pred, target_names=["Legitimate", "Fraud"])
auc = roc_auc_score(y_test, y_proba)
cm = confusion_matrix(y_test, y_pred)

print("\n=== Classification Report ===")
print(report)
print(f"ROC AUC: {auc:.4f}")
print("\nConfusion Matrix:")
print(cm)

# Save model results to a markdown file for the README/portfolio writeup
with open(f"{OUT}/model_results.md", "w") as f:
    f.write("# Baseline Fraud Detection Model — Results\n\n")
    f.write("Model: Logistic Regression (class-balanced), scikit-learn\n\n")
    f.write(f"**ROC AUC: {auc:.4f}**\n\n")
    f.write("## Classification Report\n\n```\n")
    f.write(report)
    f.write("\n```\n\n")
    f.write("## Confusion Matrix\n\n")
    f.write(f"```\n{cm}\n```\n")

# ROC curve plot
fpr, tpr, _ = roc_curve(y_test, y_proba)
plt.figure(figsize=(6, 6))
plt.plot(fpr, tpr, label=f"Logistic Regression (AUC = {auc:.3f})", color="#27ae60")
plt.plot([0, 1], [0, 1], linestyle="--", color="gray", label="Random Guess")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve — Fraud Detection Model")
plt.legend()
plt.tight_layout()
plt.savefig(f"{OUT}/roc_curve.png", dpi=150)
plt.close()
print("\nSaved roc_curve.png and model_results.md")
