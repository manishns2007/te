from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.all_models import Transaction, InvestigationDecision
from app.schemas.all_schemas import InvestigationDecisionCreate

class DecisionService:
    @staticmethod
    def submit_decision(db: Session, transaction_id: str, decision_in: InvestigationDecisionCreate):
        tx = db.query(Transaction).filter(Transaction.id == transaction_id).first()
        if not tx:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        decision = InvestigationDecision(
            transaction_id=transaction_id,
            investigator_id=decision_in.investigator_id,
            action_taken=decision_in.action_taken,
            notes=decision_in.notes
        )
        db.add(decision)
        
        # Update transaction status
        tx.status = decision_in.action_taken
        
        db.commit()
        return {"status": "success", "message": "Decision saved successfully"}
