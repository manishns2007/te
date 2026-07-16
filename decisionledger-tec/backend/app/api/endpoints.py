from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import logging

from app.database.session import get_db
from app.schemas.api_schemas import DashboardResponse, HealthResponse
from app.schemas.all_schemas import TransactionDetailResponse, InvestigationDecisionCreate, PredictionResponse
from app.services.dashboard import DashboardService
from app.services.transaction import TransactionService
from app.services.decision import DecisionService
from app.services.prediction import PredictionService
from app.services.graph import GraphService
from app.schemas.graph_schemas import GraphResponse
from app.core.logger import get_logger

logger = get_logger("api")
router = APIRouter()

@router.get("/health", response_model=HealthResponse, summary="Health Check")
def health_check():
    return HealthResponse(
        status="healthy",
        service="DecisionLedger TEC Backend",
        version="1.0.0"
    )

@router.get("/dashboard", response_model=DashboardResponse, summary="Get Dashboard Data")
def get_dashboard(db: Session = Depends(get_db)):
    logger.info("Fetching dashboard data")
    return DashboardService.get_dashboard_data(db)

@router.get("/transactions/{transaction_id}", response_model=TransactionDetailResponse, summary="Get Transaction Details")
def get_transaction(transaction_id: str, db: Session = Depends(get_db)):
    logger.info(f"Fetching transaction details for {transaction_id}")
    return TransactionService.get_transaction_details(db, transaction_id)

@router.post("/transactions/{transaction_id}/decision", summary="Submit Investigator Decision")
def submit_decision(transaction_id: str, decision: InvestigationDecisionCreate, db: Session = Depends(get_db)):
    logger.info(f"Submitting decision for {transaction_id}")
    return DecisionService.submit_decision(db, transaction_id, decision)

@router.post("/transactions/{transaction_id}/repredict", response_model=PredictionResponse, summary="Repredict Fraud Score")
def repredict_transaction(transaction_id: str, db: Session = Depends(get_db)):
    logger.info(f"Running repredict for {transaction_id}")
    return PredictionService.repredict(db, transaction_id)

@router.get("/transactions/{transaction_id}/relationship-graph", response_model=GraphResponse, summary="Get Fraud Investigation Graph")
def get_relationship_graph(transaction_id: str, db: Session = Depends(get_db)):
    logger.info(f"Fetching relationship graph for {transaction_id}")
    return GraphService.get_relationship_graph(db, transaction_id)
