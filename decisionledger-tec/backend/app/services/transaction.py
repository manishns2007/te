from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.all_models import Transaction
from app.schemas.all_schemas import TransactionDetailResponse

class TransactionService:
    @staticmethod
    def get_transaction_details(db: Session, transaction_id: str) -> TransactionDetailResponse:
        tx = db.query(Transaction).filter(Transaction.id == transaction_id).first()
        if not tx:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        return TransactionDetailResponse.model_validate(tx)
