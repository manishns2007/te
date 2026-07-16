from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.database.session import Base

def generate_uuid():
    return str(uuid.uuid4())

class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    account_id = Column(String, index=True)
    customer_name = Column(String)
    amount = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    merchant_category = Column(String)
    status = Column(String, default='PENDING')
    
    telemetry = relationship('TelemetryData', back_populates='transaction', uselist=False)
    prediction = relationship('Prediction', back_populates='transaction', uselist=False)
    decision = relationship('InvestigationDecision', back_populates='transaction', uselist=False)

class TelemetryData(Base):
    __tablename__ = 'telemetry_data'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    transaction_id = Column(String, ForeignKey('transactions.id'))
    
    device_fingerprint = Column(String)
    device_trust_score = Column(Float)
    ip_address = Column(String)
    ip_reputation = Column(String)
    vpn_detected = Column(Boolean)
    failed_logins = Column(Integer)
    impossible_travel = Column(Boolean)
    browser_changed = Column(Boolean)
    powershell_execution = Column(Boolean)
    endpoint_alert = Column(Boolean)
    known_device = Column(Boolean)
    session_risk = Column(Float)
    velocity_score = Column(Float)
    
    transaction = relationship('Transaction', back_populates='telemetry')

class Prediction(Base):
    __tablename__ = 'predictions'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    transaction_id = Column(String, ForeignKey('transactions.id'))
    
    fraud_probability = Column(Float)
    confidence_score = Column(Float)
    expected_prevented_loss = Column(Float)
    recommendation = Column(String)
    shap_top_features = Column(Text) # JSON string
    natural_language_explanation = Column(Text)
    
    transaction = relationship('Transaction', back_populates='prediction')

class InvestigationDecision(Base):
    __tablename__ = 'investigation_decisions'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    transaction_id = Column(String, ForeignKey('transactions.id'))
    investigator_id = Column(String)
    action_taken = Column(String)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    transaction = relationship('Transaction', back_populates='decision')
