# 🛡️ DecisionLedger TEC
> **AI-Powered Banking Fraud Decision Intelligence Platform**

DecisionLedger TEC is an enterprise-grade hackathon prototype designed for banking Security Operations Centers (SOC). It breaks traditional data silos by correlating financial transactions with real-time cybersecurity telemetry (e.g., VPN usage, endpoint malware). Powered by **Explainable AI** and **GenAI**, it calculates fraud probabilities and automates compliance reporting—allowing investigators to freeze fraudulent funds faster and with absolute confidence.

🔗 **Live Demo:** [dec-ledger.vercel.app](https://dec-ledger.vercel.app) *(Replace with your actual links)*

---

## ✨ Why It Stands Out

*   **Unified Telemetry:** We don't just look at money moving. We correlate transaction amounts with IP trust scores, impossible travel alerts, and endpoint malware data.
*   **Explainable AI (XAI):** No "black box" decisions. Using XGBoost and SHAP values, the platform tells the investigator exactly *why* a transaction was flagged (e.g., "Flagged due to: Unknown Device & Impossible Travel").
*   **GenAI Copilot:** Integrates Google Gemini to instantly translate complex telemetry into structured, FinCEN-ready Suspicious Activity Reports (SARs).
*   **"Neon" Command Center:** A highly interactive, dark-mode workspace built specifically to reduce cognitive load during high-stress SOC investigations.

---

## 🛠️ Tech Stack

**Frontend (The Command Center):**
*   React, TypeScript, Vite, Tailwind CSS (v4)
*   Framer Motion & React Bits (For premium UI/UX)
*   Deployed on **Vercel**

**Backend (The Intelligence Engine):**
*   Python 3, FastAPI, SQLite
*   Deployed on **Railway**

**Machine Learning (The Brain):**
*   **XGBoost:** Core predictive model.
*   **SHAP:** For Explainable AI feature importance.
*   **Google Gemini API:** For automated SAR generation.

---

## 🚀 Quick Start (Run Locally)

### 1. Start the Backend API
```bash
cd backend
python -m venv venv
# Activate venv (Windows: venv\Scripts\activate | Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
python scripts/seed_database.py
uvicorn app.main:app --reload
```
*API runs at `http://localhost:8000` | Swagger Docs at `http://localhost:8000/docs`*

### 2. Start the Frontend UI
```bash
cd frontend
npm install
npm run dev
```
*App runs at `http://localhost:5173`*

---

## 🏆 Finspark Hackathon 2026
Built as a demonstration of next-generation fraud analytics, proving that combining AI with deep cybersecurity context creates a fundamentally safer banking ecosystem.
