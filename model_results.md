# Baseline Fraud Detection Model — Results

Model: Logistic Regression (class-balanced), scikit-learn

**ROC AUC: 0.9963**

## Classification Report

```
              precision    recall  f1-score   support

  Legitimate       1.00      0.98      0.99      4850
       Fraud       0.57      0.97      0.72       150

    accuracy                           0.98      5000
   macro avg       0.79      0.97      0.85      5000
weighted avg       0.99      0.98      0.98      5000

```

## Confusion Matrix

```
[[4742  108]
 [   5  145]]
```
