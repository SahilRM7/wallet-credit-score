# 📊 Wallet Score Analysis — Aave V2 Credit Scoring

This document provides an analysis of wallet credit scores generated from transaction behavior on the Aave V2 protocol.

---

## 🔢 Credit Score Distribution (0 to 1000)

### 🎯 Binned Score Ranges:

| Score Range | Number of Wallets | % of Total |
|-------------|-------------------|------------|
| 0–100       | 142               | 14.2%      |
| 100–200     | 111               | 11.1%      |
| 200–300     | 97                | 9.7%       |
| 300–400     | 83                | 8.3%       |
| 400–500     | 95                | 9.5%       |
| 500–600     | 101               | 10.1%      |
| 600–700     | 97                | 9.7%       |
| 700–800     | 94                | 9.4%       |
| 800–900     | 104               | 10.4%      |
| 900–1000    | 76                | 7.6%       |

> 📌 Distribution is moderately right-skewed — more wallets fall in lower-to-mid ranges, while high scores are rarer.

---

## 🔍 Traits of Low-Scoring Wallets (0–200)

- Very few transactions (`total_txns` ≤ 2)
- Primarily single-type activity (e.g., only 1 `deposit`)
- Low net flows or zero repayments
- Often inactive for long (high `days_since_last_txn`)
- Use only 1–2 unique assets
- `repay_to_borrow_ratio` ≈ 0 or not applicable

---

## 🧠 Traits of High-Scoring Wallets (800–1000)

- Large and diverse volume in `deposit`, `borrow`, and `repay`
- High `repay_to_borrow_ratio` (≥ 0.8)
- Strong `net_flow` (more funds returned than borrowed)
- No `liquidationcall` records
- Consistent recent activity (≤ 300 days since last txn)
- Use multiple assets (3–6+), across different actions

---

## 🧮 Feature Correlations (Top Insights)

| Feature                    | Correlation with Credit Score |
|---------------------------|-------------------------------|
| `repay_to_borrow_ratio`   | +0.72                         |
| `net_flow`                | +0.68                         |
| `total_repay_usd`         | +0.60                         |
| `days_since_last_txn`     | -0.55                         |
| `total_liquidations`      | -0.44                         |

> 🔎 `repay_to_borrow_ratio` is the most reliable positive indicator of creditworthiness.

---

## 🧠 Observations

- **Wallets that repay loans consistently and avoid liquidation score significantly higher.**
- **Wallets with high deposit-to-borrow imbalance, no activity in years, or only speculative actions are penalized.**
- **Feature normalization and outlier handling (e.g., USDC vs MATIC scale) is key.**

---

## 📈 Score Distribution Plot

![score-distribution](notebook/assets/score_distribution.png)

---

## 📌 Limitations & Suggestions

- Currently only trained on **relative rank** (unsupervised); real-world ground truth would improve accuracy
- Time decay features (recent activity) can be expanded
- Can integrate risk metrics from other protocols
- Introduce anomaly detection (e.g., flashloan behavior or yield exploits)

---

## ✅ Summary

The scoring system is a useful proxy for understanding wallet behavior in Aave V2. It highlights how **responsibility in borrowing/lending, diversity of usage, and recency** all contribute to a stronger credit profile — even in permissionless DeFi.

---

