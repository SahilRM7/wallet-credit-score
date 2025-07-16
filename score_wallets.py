import pandas as pd
import numpy as np
from datetime import datetime
import json
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler
import joblib

# Load and normalize JSON
def load_data(json_path):
    with open(json_path, 'r') as f:
        raw_data = json.load(f)

    # Flatten top level and actionData.* keys
    df = pd.json_normalize(raw_data, sep='_')

    return df

# Preprocess and convert values
def preprocess(df):
    # Convert timestamp
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')

    # Check and convert nested keys
    if 'actionData_amount' in df.columns and 'actionData_assetPriceUSD' in df.columns:
        df['amount'] = pd.to_numeric(df['actionData_amount'], errors='coerce')
        df['assetPriceUSD'] = pd.to_numeric(df['actionData_assetPriceUSD'], errors='coerce')
        df['assetSymbol'] = df['actionData_assetSymbol']
    else:
        raise KeyError("Expected keys like 'actionData_amount' not found. Check JSON structure.")

    # Calculate amount_usd
    df['amount_usd'] = df['amount'] * df['assetPriceUSD'] / 1e18

    # Adjust for stablecoins
    usdc_mask = df['assetSymbol'].str.upper().str.contains('USDC|USDT', na=False)
    df.loc[usdc_mask, 'amount_usd'] = df.loc[usdc_mask, 'amount'] * df.loc[usdc_mask, 'assetPriceUSD'] / 1e6

    return df

# Generate wallet-level features
def generate_features(df):
    group = df.groupby('userWallet')
    features = pd.DataFrame(index=df['userWallet'].unique())

    features['total_txns'] = group.size()
    features['total_deposit_usd'] = df[df['action'] == 'deposit'].groupby('userWallet')['amount_usd'].sum()
    features['total_borrow_usd'] = df[df['action'] == 'borrow'].groupby('userWallet')['amount_usd'].sum()
    features['total_repay_usd'] = df[df['action'] == 'repay'].groupby('userWallet')['amount_usd'].sum()
    features['total_redeem_usd'] = df[df['action'] == 'redeemunderlying'].groupby('userWallet')['amount_usd'].sum()
    features['total_liquidations'] = df[df['action'] == 'liquidationcall'].groupby('userWallet').size()

    features['unique_assets'] = group['assetSymbol'].nunique()
    features['num_actions'] = group['action'].nunique()

    features = features.fillna(0)

    # Behavioral metrics
    features['repay_to_borrow_ratio'] = features['total_repay_usd'] / (features['total_borrow_usd'] + 1)
    features['net_flow'] = features['total_deposit_usd'] - features['total_borrow_usd'] - features['total_redeem_usd']
    features['is_liquidated'] = features['total_liquidations'].apply(lambda x: 1 if x > 0 else 0)

    # Recency: days since last txn
    last_txn = group['datetime'].max()
    features['days_since_last_txn'] = (datetime.utcnow() - last_txn).dt.days
    features['days_since_last_txn'] = features['days_since_last_txn'].fillna(features['days_since_last_txn'].max())

    features = features.fillna(0).reset_index()

    # Rename index column properly
    if 'userWallet' in features.columns:
        features = features.rename(columns={'userWallet': 'wallet'})
    elif 'index' in features.columns:
        features = features.rename(columns={'index': 'wallet'})
    return features

# Score wallets with RandomForest + MinMaxScaler
def score_wallets(features_df, model_path='model.pkl'):
    X = features_df.drop(columns=['wallet'])

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, np.arange(len(X)))

    # Save model to file
    joblib.dump(model, model_path)

    raw_scores = model.predict(X)
    scaler = MinMaxScaler(feature_range=(0, 1000))
    scaled_scores = scaler.fit_transform(raw_scores.reshape(-1, 1)).flatten()

    features_df['credit_score'] = scaled_scores.astype(int)
    return features_df[['wallet', 'credit_score']]

# Run everything
def main():
    json_path = 'data/user-wallet-transactions.json'  # <-- update path if needed

    print("📥 Loading data...")
    df = load_data(json_path)

    print("⚙️ Preprocessing...")
    df = preprocess(df)

    print("📊 Generating features...")
    features = generate_features(df)

    print("🧠 Scoring wallets...")
    scored = score_wallets(features)

    print("💾 Saving to wallet_scores.csv...")
    scored.to_csv('wallet_scores.csv', index=False)
    print("✅ Done!")

if __name__ == '__main__':
    main()
