from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.models.all_models import Transaction, Prediction
from app.schemas.api_schemas import DashboardResponse, KPIMetrics
from app.schemas.all_schemas import TransactionResponse

class DashboardService:
    @staticmethod
    def get_dashboard_data(db: Session) -> DashboardResponse:
        # High Risk Transactions
        high_risk_count = db.query(Transaction).join(Prediction).filter(
            Transaction.status == 'FLAGGED',
            Prediction.fraud_probability >= 0.85
        ).count()
        
        # Pending Investigations
        pending_count = db.query(Transaction).filter(
            Transaction.status.in_(['PENDING', 'FLAGGED'])
        ).count()
        
        # Average Confidence
        avg_confidence = db.query(func.avg(Prediction.confidence_score)).scalar() or 0.0
        
        # Estimated Prevented Loss (sum of expected prevented loss for high risk pending)
        epl = db.query(func.sum(Prediction.expected_prevented_loss)).join(Transaction).filter(
            Transaction.status.in_(['PENDING', 'FLAGGED']),
            Prediction.fraud_probability >= 0.85
        ).scalar() or 0.0
        
        kpis = KPIMetrics(
            high_risk_transactions=high_risk_count,
            pending_investigations=pending_count,
            average_confidence=round(avg_confidence, 2),
            estimated_prevented_loss=round(epl, 2)
        )
        
        # Queue (top 50 pending/flagged, sorted by probability descending)
        queue_records = db.query(Transaction).join(Prediction).filter(
            Transaction.status.in_(['PENDING', 'FLAGGED'])
        ).order_by(Prediction.fraud_probability.desc()).limit(50).all()
        
        queue = [TransactionResponse.model_validate(tx) for tx in queue_records]
        
        return DashboardResponse(kpis=kpis, queue=queue)
