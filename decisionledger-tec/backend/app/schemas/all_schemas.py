from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class TelemetryDataBase(BaseModel):
    device_fingerprint: str
    device_trust_score: float
    ip_address: str
    ip_reputation: str
    vpn_detected: bool
    failed_logins: int
    impossible_travel: bool
    browser_changed: bool
    powershell_execution: bool
    endpoint_alert: bool
    known_device: bool
    session_risk: float
    velocity_score: float

class TelemetryDataResponse(TelemetryDataBase):
    id: str
    transaction_id: str
    class Config:
        from_attributes = True

class PredictionBase(BaseModel):
    fraud_probability: float
    confidence_score: float
    expected_prevented_loss: float
    recommendation: str
    shap_top_features: str
    natural_language_explanation: str

class PredictionResponse(PredictionBase):
    id: str
    transaction_id: str
    class Config:
        from_attributes = True

class InvestigationDecisionBase(BaseModel):
    action_taken: str
    notes: str

class InvestigationDecisionCreate(InvestigationDecisionBase):
    investigator_id: str

class InvestigationDecisionResponse(InvestigationDecisionBase):
    id: str
    transaction_id: str
    investigator_id: str
    created_at: datetime
    class Config:
        from_attributes = True

class TransactionBase(BaseModel):
    account_id: str
    customer_name: str
    amount: float
    merchant_category: str
    status: str

class TransactionResponse(TransactionBase):
    id: str
    timestamp: datetime
    class Config:
        from_attributes = True

class TransactionDetailResponse(TransactionResponse):
    telemetry: Optional[TelemetryDataResponse] = None
    prediction: Optional[PredictionResponse] = None
    decision: Optional[InvestigationDecisionResponse] = None
