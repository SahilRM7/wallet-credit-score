# 🏦 Aave Wallet Credit Scoring (DeFi)

This project builds a **credit scoring system (0–1000 scale)** for wallets based on their historical activity on the Aave V2 protocol. It uses **DeFi transaction-level data** to evaluate responsible or risky behaviors across actions like `deposit`, `borrow`, `repay`, `redeemunderlying`, and `liquidationcall`.

---

## 🔍 Objective

Assign a **credit score** to each wallet based on:
- Behavioral signals (deposits vs borrows, repayments)
- Activity diversity and frequency
- Asset usage and liquidation risk
- Recency of activity

---

## 📁 Project Structure

aave-wallet-credit-score/ 
│
├── notebooks/
│   ├─── EDA_and_Feature_Engineering.ipynb
│   └─── data/
│        └── user-wallet-transaction.json
├── score_wallets.py
├── model.pkl
├── requirements.txt
├── README.md
├── analysis.md

---

## ⚙️ Methodology

### 1. Data Source
- Format: JSON file (`user-wallet-transaction.json`)
- Each entry contains:
  - `userWallet`, `action`, `amount`, `assetSymbol`, `timestamp`, etc.
  - Nested `actionData` field flattened for modeling

### 2. Feature Engineering
Features created per wallet:
| Category         | Features                                                                 |
|------------------|--------------------------------------------------------------------------|
| Volume-based     | `total_deposit_usd`, `total_borrow_usd`, `total_repay_usd`, `net_flow`  |
| Behavior-based   | `repay_to_borrow_ratio`, `is_liquidated`, `unique_assets`, `num_actions`|
| Activity         | `total_txns`, `days_since_last_txn`                                     |

### 3. Model
- Model: `RandomForestRegressor` (sklearn)
- Target: Relative ranking (unsupervised), scaled to 0–1000 using `MinMaxScaler`
- Output: `credit_score` for each wallet

---

## 🚀 How to Run

### ⚡ 1. Install Dependencies

```bash
pip install -r requirements.txt
```
### ⚡ 2. RUN FILE

```bash
python score_wallets.py
