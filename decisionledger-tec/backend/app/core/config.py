from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = 'DecisionLedger TEC'
    DATABASE_URL: str = 'sqlite:///./decisionledger.db'
    CORS_ORIGINS: List[str] = ['*']
    
    class Config:
        env_file = '.env'

settings = Settings()
