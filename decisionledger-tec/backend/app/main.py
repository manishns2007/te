from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database.session import engine, Base
import app.models.all_models # Import models to ensure tables are created
from app.api.endpoints import router as api_router

# Ensure tables are created
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version='1.0.0',
    description='Backend API for DecisionLedger TEC'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/health')
def health_check():
    return {'status': 'ok', 'project': settings.PROJECT_NAME}

app.include_router(api_router, prefix="/api")
