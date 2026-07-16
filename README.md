# 🛡️ DecisionLedger TEC

> **AI-Powered Banking Fraud Decision Intelligence Platform**

DecisionLedger TEC is an enterprise-grade fraud investigation platform that combines **transactional behavior**, **cybersecurity telemetry**, and **Explainable AI (XAI)** to help fraud analysts make faster, transparent, and more informed decisions on high-value banking transactions.

Built as a hackathon prototype, the platform demonstrates how AI can augment fraud investigators by correlating banking events with endpoint and identity telemetry while providing human-readable explanations for every recommendation.

---

## 🚀 Overview

Traditional fraud detection systems often provide only a risk score, leaving investigators to manually correlate logs, customer information, and endpoint events.

DecisionLedger TEC bridges this gap by providing a unified investigation workspace that:

- Detects suspicious banking transactions
- Correlates cybersecurity telemetry
- Explains AI predictions using SHAP Explainability
- Visualizes fraud relationships
- Assists investigators with AI-generated summaries
- Generates compliance-ready investigation reports

---

# ✨ Features

## 📊 Executive Dashboard

- High-Risk Transaction Queue
- Estimated Prevented Loss
- Average AI Confidence
- Pending Investigations
- Risk Distribution Charts
- Recommendation Analytics
- Transaction Status Overview

---

## 🧠 Explainable AI

Powered by:

- XGBoost
- SHAP Explainability

Instead of simply saying:

> "Fraud Probability: 92%"

DecisionLedger TEC explains **why** the model reached that conclusion.

Example:

- Impossible Travel
- VPN Usage
- Unknown Device
- Endpoint Alert
- Browser Change

Each prediction includes human-readable explanations to improve analyst trust.

---

## 🔒 Cybersecurity Telemetry Correlation

Every transaction is enriched with cybersecurity intelligence including:

- Device Fingerprint
- Device Trust Score
- IP Reputation
- VPN Detection
- Impossible Travel
- Failed Login Attempts
- Browser Change Detection
- Endpoint Alerts
- PowerShell Execution
- Session Risk
- Velocity Score

---

## 🔍 Decision Console

The investigation workspace provides:

### Transaction Context

- Customer Information
- Transaction Details
- Merchant Information
- Timeline

### AI Intelligence

- Fraud Probability
- Confidence Score
- Expected Prevented Loss
- SHAP Feature Importance
- AI Recommendation

### Investigation Actions

- Freeze Transaction
- Step-Up Authentication
- Monitor
- Dismiss
- Investigator Notes

---

## 🌐 Fraud Relationship Graph

Interactive relationship visualization inspired by enterprise investigation platforms such as:

- Palantir Gotham
- IBM i2 Analyst Notebook
- CrowdStrike Falcon

Relationships include:

- Customer
- Account
- Device
- IP Address
- Merchant
- Previous Fraud Cases

Features:

- Zoom
- Pan
- Node Selection
- Relationship Highlighting
- Entity Inspector

---

## 🤖 AI Investigation Copilot

Generate structured investigation summaries using AI.

Produces:

- Executive Summary
- Risk Assessment
- Key Evidence
- Behavioral Analysis
- Recommended Actions

---

## 📄 Suspicious Activity Report (SAR)

Generate printable compliance-ready reports containing:

- Transaction Details
- Customer Information
- Cybersecurity Evidence
- AI Findings
- Investigator Decision
- SHAP Explanations

---

# 🏗️ System Architecture

```
                    React + TypeScript
                           │
                           ▼
                     FastAPI Backend
                           │
      ┌────────────────────┼────────────────────┐
      ▼                    ▼                    ▼
 SQLite Database     XGBoost Model      SHAP Explainability
      │                    │                    │
      └──────────────► AI Decision Engine ◄─────┘
                           │
                           ▼
                  Investigation Workspace
```

---

# 🛠️ Technology Stack

## Frontend

- React
- TypeScript
- Vite
- TailwindCSS
- Framer Motion
- Recharts
- React Flow
- Axios
- Lucide React

---

## Backend

- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Uvicorn

---

## Machine Learning

- XGBoost
- SHAP
- Scikit-learn
- NumPy
- Pandas
- Joblib

---

# 📁 Project Structure

```
decisionledger-tec/

├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── database/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── ml/
│   │   └── main.py
│   │
│   ├── scripts/
│   │   └── seed_database.py
│   │
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   ├── layouts/
    │   ├── services/
    │   ├── hooks/
    │   ├── types/
    │   └── App.tsx
    │
    └── package.json
```

---

# 🔌 API Endpoints

## Dashboard

```
GET /api/dashboard
```

Returns:

- KPI Metrics
- Investigation Queue

---

## Transaction Details

```
GET /api/transactions/{transaction_id}
```

Returns:

- Transaction Details
- Customer Context
- Telemetry
- AI Prediction
- SHAP Explanation

---

## Submit Decision

```
POST /api/transactions/{transaction_id}/decision
```

Stores:

- Investigator Decision
- Notes
- Status

---

## Re-Predict

```
POST /api/transactions/{transaction_id}/repredict
```

Runs:

- XGBoost Prediction
- SHAP Explainability

---

## Relationship Graph

```
GET /api/transactions/{transaction_id}/relationship-graph
```

Returns:

- Graph Nodes
- Graph Edges

---

# 🧠 Machine Learning Pipeline

1. Generate synthetic banking data
2. Train XGBoost classifier
3. Compute SHAP values
4. Generate explanations
5. Cache predictions
6. Serve predictions through FastAPI

---

# 🎯 Investigation Workflow

```
Transaction

        │

        ▼

Cybersecurity Telemetry

        │

        ▼

AI Fraud Prediction

        │

        ▼

SHAP Explainability

        │

        ▼

Relationship Analysis

        │

        ▼

Investigator Review

        │

        ▼

Freeze / Step-Up / Monitor

        │

        ▼

SAR Generation
```

---

# 🚀 Running the Project

## Backend

```bash
cd backend

pip install -r requirements.txt

python scripts/seed_database.py

uvicorn app.main:app --reload
```

Backend:

```
http://localhost:8000
```

Swagger Docs:

```
http://localhost:8000/docs
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend:

```
http://localhost:5173
```

---

# 🌍 Deployment

### Frontend

- Vercel

### Backend

- Render / Railway

---

# 🎯 Future Roadmap

- Real-time transaction streaming
- Kafka event ingestion
- Neo4j fraud graph
- LLM-powered investigation assistant
- Multi-bank support
- Role-Based Access Control
- Audit Logging
- SIEM Integration
- Threat Intelligence APIs
- Continuous Model Retraining

---

# 🏆 Hackathon Highlights

- Explainable AI with SHAP
- XGBoost Fraud Detection
- Cybersecurity Telemetry Correlation
- Interactive Fraud Relationship Graph
- AI Investigation Copilot
- SAR Report Generation
- Enterprise Investigation Console
- Modern Banking Fraud Analytics Dashboard

---

# 📸 Screenshots

> Add screenshots of:
>
> - Landing Page
> - Executive Dashboard
> - Decision Console
> - Relationship Graph
> - AI Copilot
> - SAR Report

---

# 👨‍💻 Authors

Developed for a Hackathon Prototype

**DecisionLedger TEC**

AI-Powered Banking Fraud Decision Intelligence Platform

---

## 📄 License

This project is intended for educational, research, and hackathon demonstration purposes.
