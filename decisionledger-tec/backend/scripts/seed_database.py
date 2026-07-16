import os
import sys
import json
import uuid
import random
from datetime import datetime, timedelta, UTC
import joblib
import pandas as pd
import numpy as np
import xgboost as xgb
import shap

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.database.session import engine, Base, SessionLocal
from app.models.all_models import Transaction, TelemetryData, Prediction

# Define fixed random seed for deterministic generation
random.seed(42)
np.random.seed(42)

def generate_natural_language_explanation(top_features: dict) -> str:
    """Generates a human-readable explanation based on top SHAP features."""
    feature_descriptions = {
        "impossible_travel": "an impossible travel pattern was detected",
        "vpn_detected": "the connection originated from a VPN",
        "ip_reputation": "the IP address has a poor reputation",
        "velocity_score": "the transaction velocity is unusually high",
        "failed_logins": "there were multiple failed login attempts recently",
        "powershell_execution": "suspicious PowerShell execution was detected on the endpoint",
        "browser_changed": "the user logged in from a newly changed browser",
        "known_device": "the device used is unknown or new",
        "session_risk": "the session risk score is elevated",
        "device_trust_score": "the device trust score is critically low",
        "endpoint_alert": "a security alert was triggered on the endpoint",
        "amount": "the transaction amount is unusually large for this account",
    }
    
    reasons = []
    for feature, impact in top_features.items():
        if impact > 0.05 and feature in feature_descriptions:
            reasons.append(feature_descriptions[feature])
    
    if not reasons:
        return "This transaction appears normal with no significant risk factors."
        
    explanation = "This transaction is considered high risk because "
    if len(reasons) == 1:
        explanation += reasons[0] + "."
    elif len(reasons) == 2:
        explanation += f"{reasons[0]} and {reasons[1]}."
    else:
        explanation += ", ".join(reasons[:-1]) + f", and {reasons[-1]}."
        
    return explanation

def get_recommendation(probability: float) -> str:
    if probability >= 0.85:
        return "FREEZE"
    elif probability >= 0.60:
        return "STEP_UP"
    return "MONITOR"

def seed_database():
    """Main script to seed the database and train the ML model."""
    print("Starting Phase 2: Database Seeding & Offline ML Pipeline...")
    
    # 1. Reset Database
    print("Resetting database...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    # 2. Generate Dataset
    print("Generating dataset...")
    transactions = []
    telemetries = []
    labels = []  # 1 for fraud, 0 for normal
    
    # NORMAL TRANSACTIONS (35)
    for i in range(35):
        tx_id = str(uuid.uuid4())
        transactions.append({
            "id": tx_id,
            "account_id": f"ACC-{random.randint(10000, 99999)}",
            "customer_name": f"Customer {i}",
            "amount": round(random.uniform(10, 500), 2),
            "timestamp": datetime.now(UTC) - timedelta(hours=random.randint(1, 72)),
            "merchant_category": random.choice(["Retail", "Groceries", "Dining", "Utilities"]),
            "status": "PENDING"
        })
        telemetries.append({
            "transaction_id": tx_id,
            "device_fingerprint": f"DEV-{random.randint(1000, 9999)}",
            "device_trust_score": round(random.uniform(0.8, 1.0), 2),
            "ip_address": f"192.168.1.{random.randint(1, 255)}",
            "ip_reputation": "Safe",
            "vpn_detected": False,
            "failed_logins": 0,
            "impossible_travel": False,
            "browser_changed": False,
            "powershell_execution": False,
            "endpoint_alert": False,
            "known_device": True,
            "session_risk": round(random.uniform(0.0, 0.2), 2),
            "velocity_score": round(random.uniform(0.1, 0.5), 2),
        })
        labels.append(0)

    # SUSPICIOUS TRANSACTIONS (10)
    for i in range(10):
        tx_id = str(uuid.uuid4())
        transactions.append({
            "id": tx_id,
            "account_id": f"ACC-{random.randint(10000, 99999)}",
            "customer_name": f"Suspicious Cust {i}",
            "amount": round(random.uniform(500, 2000), 2),
            "timestamp": datetime.now(UTC) - timedelta(hours=random.randint(1, 12)),
            "merchant_category": random.choice(["Electronics", "Travel", "Crypto"]),
            "status": "PENDING"
        })
        telemetries.append({
            "transaction_id": tx_id,
            "device_fingerprint": f"DEV-{random.randint(1000, 9999)}",
            "device_trust_score": round(random.uniform(0.4, 0.7), 2),
            "ip_address": f"10.0.0.{random.randint(1, 255)}",
            "ip_reputation": "Suspicious",
            "vpn_detected": random.choice([True, False]),
            "failed_logins": random.randint(0, 2),
            "impossible_travel": False,
            "browser_changed": random.choice([True, False]),
            "powershell_execution": False,
            "endpoint_alert": False,
            "known_device": random.choice([True, False]),
            "session_risk": round(random.uniform(0.3, 0.6), 2),
            "velocity_score": round(random.uniform(0.5, 0.8), 2),
        })
        labels.append(random.choice([0, 1])) # Mix of false positives and true positives
        
    # SCENARIO-DRIVEN FRAUD TRANSACTIONS (5)
    fraud_scenarios = [
        {
            "desc": "Scenario A: New Device + Impossible Travel",
            "tx": {"amount": 8500.00, "merchant_category": "Wire Transfer"},
            "tel": {"known_device": False, "impossible_travel": True, "device_trust_score": 0.1, "ip_reputation": "Suspicious"}
        },
        {
            "desc": "Scenario B: VPN + Malicious IP + High Velocity",
            "tx": {"amount": 3200.00, "merchant_category": "Crypto"},
            "tel": {"vpn_detected": True, "ip_reputation": "Malicious", "velocity_score": 0.95, "session_risk": 0.85}
        },
        {
            "desc": "Scenario C: Failed Logins + Large Transfer",
            "tx": {"amount": 12000.00, "merchant_category": "Wire Transfer"},
            "tel": {"failed_logins": 5, "device_trust_score": 0.3, "session_risk": 0.9}
        },
        {
            "desc": "Scenario D: PowerShell + Endpoint Alert",
            "tx": {"amount": 4500.00, "merchant_category": "Electronics"},
            "tel": {"powershell_execution": True, "endpoint_alert": True, "browser_changed": True, "device_trust_score": 0.2}
        },
        {
            "desc": "Scenario E: Browser Change + Unknown Device + High Risk",
            "tx": {"amount": 6700.00, "merchant_category": "Luxury Goods"},
            "tel": {"browser_changed": True, "known_device": False, "session_risk": 0.92, "device_trust_score": 0.15}
        }
    ]
    
    for i, scenario in enumerate(fraud_scenarios):
        tx_id = str(uuid.uuid4())
        transactions.append({
            "id": tx_id,
            "account_id": f"ACC-FRAUD-{i}",
            "customer_name": f"Victim {i}",
            "amount": scenario["tx"]["amount"],
            "timestamp": datetime.now(UTC) - timedelta(minutes=random.randint(5, 60)),
            "merchant_category": scenario["tx"]["merchant_category"],
            "status": "PENDING"
        })
        
        base_tel = {
            "transaction_id": tx_id,
            "device_fingerprint": f"DEV-FRAUD-{i}",
            "device_trust_score": 0.2,
            "ip_address": f"192.168.100.{i}",
            "ip_reputation": "Suspicious",
            "vpn_detected": False,
            "failed_logins": 0,
            "impossible_travel": False,
            "browser_changed": False,
            "powershell_execution": False,
            "endpoint_alert": False,
            "known_device": True,
            "session_risk": 0.8,
            "velocity_score": 0.7,
        }
        base_tel.update(scenario["tel"])
        telemetries.append(base_tel)
        labels.append(1)

    # 3. Train XGBoost Model
    print("Preparing features for ML training...")
    df_tx = pd.DataFrame(transactions)
    df_tel = pd.DataFrame(telemetries)
    df = pd.merge(df_tx, df_tel, left_on="id", right_on="transaction_id")
    
    # Feature Engineering for ML
    features = [
        "amount", "device_trust_score", "vpn_detected", "failed_logins",
        "impossible_travel", "browser_changed", "powershell_execution", 
        "endpoint_alert", "known_device", "session_risk", "velocity_score"
    ]
    
    # Convert booleans to int, calculate IP Reputation numerically
    df["vpn_detected"] = df["vpn_detected"].astype(int)
    df["impossible_travel"] = df["impossible_travel"].astype(int)
    df["browser_changed"] = df["browser_changed"].astype(int)
    df["powershell_execution"] = df["powershell_execution"].astype(int)
    df["endpoint_alert"] = df["endpoint_alert"].astype(int)
    df["known_device"] = df["known_device"].astype(int)
    df["ip_rep_score"] = df["ip_reputation"].map({"Safe": 0, "Suspicious": 1, "Malicious": 2})
    features.append("ip_rep_score")
    
    X = df[features]
    y = np.array(labels)
    
    print("Training XGBoost Model...")
    model = xgb.XGBClassifier(n_estimators=50, max_depth=4, learning_rate=0.1, random_state=42)
    model.fit(X, y)
    
    # Save Model
    ml_dir = os.path.join(os.path.dirname(__file__), "..", "app", "ml")
    os.makedirs(ml_dir, exist_ok=True)
    model_path = os.path.join(ml_dir, "model.joblib")
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")
    
    # 4. Generate Predictions & SHAP Explanations
    print("Generating Predictions and SHAP Explanations...")
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)
    probabilities = model.predict_proba(X)[:, 1]
    
    predictions = []
    for i, row in df.iterrows():
        prob = float(probabilities[i])
        
        # Calculate confidence score (distance from decision boundary 0.5)
        # Closer to 0 or 1 means high confidence.
        margin = abs(prob - 0.5) * 2
        confidence = float(np.clip(margin + 0.1, 0, 1)) # Add slight baseline
        
        # Expected Prevented Loss
        epl = float(row["amount"] * prob)
        
        # SHAP Explanations
        row_shap = shap_values[i]
        feature_impacts = {features[j]: float(row_shap[j]) for j in range(len(features))}
        # Sort by absolute impact
        sorted_impacts = sorted(feature_impacts.items(), key=lambda item: abs(item[1]), reverse=True)
        top_features_dict = {k: v for k, v in sorted_impacts[:4] if v > 0} # Only positive contributors to fraud
        
        nl_explanation = generate_natural_language_explanation(top_features_dict)
        
        # For non-fraud, keep explanation simple
        if prob < 0.5:
             nl_explanation = "This transaction appears normal with no significant risk factors."
             top_features_dict = {}

        predictions.append({
            "id": str(uuid.uuid4()),
            "transaction_id": row.get("id_x", row.get("id")),
            "fraud_probability": prob,
            "confidence_score": confidence,
            "expected_prevented_loss": epl,
            "recommendation": get_recommendation(prob),
            "shap_top_features": json.dumps(top_features_dict),
            "natural_language_explanation": nl_explanation
        })
        
        # Update transaction status if it's flagged by model for the dashboard to pick up
        if prob >= 0.6:
             transactions[i]["status"] = "FLAGGED"
             
    # 5. Insert into Database
    print("Saving to database...")
    db = SessionLocal()
    try:
        # Insert Transactions
        db.bulk_insert_mappings(Transaction, transactions)
        # Insert Telemetry
        db.bulk_insert_mappings(TelemetryData, telemetries)
        # Insert Predictions
        db.bulk_insert_mappings(Prediction, predictions)
        db.commit()
        print("Database seeded successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
