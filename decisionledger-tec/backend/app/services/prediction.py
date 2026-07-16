import os
import joblib
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.all_models import Transaction, TelemetryData, Prediction
import shap
import json
from app.services.explanation import ExplanationService
from app.schemas.all_schemas import PredictionResponse

class PredictionService:
    _model = None
    _explainer = None

    @classmethod
    def load_model(cls):
        if cls._model is None:
            model_path = os.path.join(os.path.dirname(__file__), "..", "ml", "model.joblib")
            if not os.path.exists(model_path):
                raise HTTPException(status_code=500, detail="ML model not found.")
            cls._model = joblib.load(model_path)
            cls._explainer = shap.TreeExplainer(cls._model)
    
    @staticmethod
    def repredict(db: Session, transaction_id: str) -> PredictionResponse:
        PredictionService.load_model()
        
        tx = db.query(Transaction).filter(Transaction.id == transaction_id).first()
        if not tx or not tx.telemetry:
            raise HTTPException(status_code=404, detail="Transaction or telemetry not found")
            
        tel = tx.telemetry
        
        features = [
            "amount", "device_trust_score", "vpn_detected", "failed_logins",
            "impossible_travel", "browser_changed", "powershell_execution", 
            "endpoint_alert", "known_device", "session_risk", "velocity_score", "ip_rep_score"
        ]
        
        ip_rep_map = {"Safe": 0, "Suspicious": 1, "Malicious": 2}
        
        row = {
            "amount": tx.amount,
            "device_trust_score": tel.device_trust_score,
            "vpn_detected": int(tel.vpn_detected),
            "failed_logins": tel.failed_logins,
            "impossible_travel": int(tel.impossible_travel),
            "browser_changed": int(tel.browser_changed),
            "powershell_execution": int(tel.powershell_execution),
            "endpoint_alert": int(tel.endpoint_alert),
            "known_device": int(tel.known_device),
            "session_risk": tel.session_risk,
            "velocity_score": tel.velocity_score,
            "ip_rep_score": ip_rep_map.get(tel.ip_reputation, 0)
        }
        
        X = pd.DataFrame([row], columns=features)
        
        prob = float(PredictionService._model.predict_proba(X)[0][1])
        margin = abs(prob - 0.5) * 2
        confidence = float(np.clip(margin + 0.1, 0, 1))
        epl = float(tx.amount * prob)
        
        if prob >= 0.85:
            rec = "FREEZE"
        elif prob >= 0.60:
            rec = "STEP_UP"
        else:
            rec = "MONITOR"
            
        shap_values = PredictionService._explainer.shap_values(X)[0]
        feature_impacts = {features[j]: float(shap_values[j]) for j in range(len(features))}
        sorted_impacts = sorted(feature_impacts.items(), key=lambda item: abs(item[1]), reverse=True)
        top_features_dict = {k: v for k, v in sorted_impacts[:4] if v > 0}
        
        nl_explanation = ExplanationService.generate_explanation(top_features_dict, prob)
        
        pred = tx.prediction
        if not pred:
            pred = Prediction(transaction_id=tx.id)
            db.add(pred)
            
        pred.fraud_probability = prob
        pred.confidence_score = confidence
        pred.expected_prevented_loss = epl
        pred.recommendation = rec
        pred.shap_top_features = json.dumps(top_features_dict)
        pred.natural_language_explanation = nl_explanation
        
        # Optionally update transaction status if needed
        if prob >= 0.6 and tx.status == "PENDING":
             tx.status = "FLAGGED"
        
        db.commit()
        db.refresh(pred)
        
        return PredictionResponse.model_validate(pred)
