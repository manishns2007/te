from pydantic import BaseModel
from typing import List, Optional
from app.schemas.all_schemas import TransactionResponse, TransactionDetailResponse

class KPIMetrics(BaseModel):
    high_risk_transactions: int
    pending_investigations: int
    average_confidence: float
    estimated_prevented_loss: float

class DashboardResponse(BaseModel):
    kpis: KPIMetrics
    queue: List[TransactionResponse]

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
