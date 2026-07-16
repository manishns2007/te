# DecisionLedger TEC: AI-Powered Fraud Intelligence

DecisionLedger TEC is a next-generation "Command Center" designed for banking Security Operations Centers (SOC). Traditional banking fraud tools analyze financial transactions in isolation. DecisionLedger breaks down these silos by correlating financial data with real-time cybersecurity telemetry (e.g., VPN detection, impossible travel, endpoint malware alerts). 

Powered by Explainable AI (SHAP) and GenAI (Gemini), the platform calculates fraud probabilities and provides investigators with instant, human-readable compliance reports, allowing them to freeze fraudulent activity before funds are lost.

## 🌟 Key Features

- **Unified Telemetry:** Correlates money movement with cyber-risk indicators.
- **Explainable AI (XAI):** Uses SHAP values to explain exactly *why* a transaction was flagged (no "black box" decisions).
- **GenAI Copilot:** Automates the drafting of FinCEN-compliant Suspicious Activity Reports (SAR) using Google's Gemini API.
- **Neon Command Center UI:** A stunning, highly-interactive frontend built with React Bits (WebGL Particles, Electric Borders, Proximity text).

## 🛠️ Tech Stack

**Frontend:**
- React (Vite)
- TypeScript
- Tailwind CSS (v4)
- Framer Motion
- React Bits (UI Components)
- Vercel (Deployment)

**Backend:**
- Python 3
- FastAPI & Uvicorn
- SQLite (Persistent Storage)
- XGBoost (Machine Learning)
- Railway / Render (Deployment)

## 🚀 How to Run Locally

### 1. Start the Backend (FastAPI)
Open a terminal in the `backend` directory:
```bash
cd backend
python -m venv venv
# Activate virtual environment
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```
The backend API will be available at `http://localhost:8000`.

### 2. Start the Frontend (React/Vite)
Open a new terminal in the `frontend` directory:
```bash
cd frontend
npm install
npm run dev
```
The frontend will be available at `http://localhost:5173`. 

*(Note: Ensure your `.env` file in the frontend has `VITE_API_BASE_URL=http://localhost:8000/api` for local testing).*

## 🏆 Hackathon Submission

This project was built for the **Finspark Hackathon 2026** sponsored by the Bank of Maharashtra.
