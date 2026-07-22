# BriefToLaunch 🚀

> **Elite Dynamic B2B Marketing Strategy & Financial Stress-Testing SaaS Platform**

---

## 📌 Executive Summary & Core Value Proposition

Most modern marketing briefs and agency proposals are saturated with subjective fluff, vanity metrics, vague commitments, and unrealistic ROI projections. **BriefToLaunch** is an autonomous, full-stack B2B SaaS platform engineered for ruthless business auditing and financial stress-testing of marketing strategies.

The platform ingests raw corporate marketing briefs and instantly converts them into a deterministic, cash-flow-resilient financial model. Instead of generating plain text, the core engine executes strict resource allocation calculations, detects hidden margin leaks, and prepares brand leadership for the harsh realities of B2B contract negotiations.

### 🎯 Key Business Problems Solved:

* **The Illusion of Budget Efficiency:** Calculates channel budget splits in **USD ($)** with exact mathematical precision, locking every percentage directly to executable activations.
* **Static & Unrealistic B2B Partner Pitches:** The *Dynamic Partner Extraction* engine parses brief inputs in real-time, isolates commercial entities (retail networks, distributors, venue networks, CSR entities), and crafts margin-driven commercial pitches for each.
* **Hidden Capital Losses (Margin Leaks):** The *Burn Rate Simulator* analyzes capital dissipation risks caused by agency markups, logistical friction, and unoptimized B2B discounts, delivering an automated Risk Score and financial warning before capital is deployed.
* **Negotiation Unpreparedness:** The integrated *War Room* provides a live, context-aware negotiation environment powered by a stubborn Category Buyer AI to stress-test proposed strategies before signing binding contracts.

---

## 🏗️ Repository Directory & Architecture Tree
```text
BriefToLaunch/
├── backend/                        # FastAPI Backend Application Engine
│   ├── app/                        # Application Core Source Code
│   │   ├── api/                    # API Route Handlers
│   │   │   └── router.py           # API endpoints (/campaign/generate, /campaign/negotiate)
│   │   ├── core/                   # Core App Configuration
│   │   │   └── config.py           # Environment variables & OpenAI client config
│   │   ├── prompts/                # AI Agent System Instructions
│   │   │   └── cmo_prompt.py       # System prompt for audit-driven tone
│   │   ├── schemas/                # Pydantic Data Models (Structured Outputs)
│   │   │   └── campaign.py         # JSON schema rules (CampaignResponse, B2BPitch)
│   │   ├── services/               # Core LLM Business Logic
│   │   │   └── llm.py              # OpenAI API integration & mock fallback engine
│   │   └── main.py                 # FastAPI instance & CORS middleware setup
│   ├── tests/                      # Automated Test Suite
│   │   ├── conftest.py             # Pytest fixtures and mock client setup
│   │   └── test_campaign.py        # Unit tests for schemas and API endpoints
│   ├── .env.example                # Template for required environment variables
│   ├── requirements.txt            # Backend Python dependencies
│   └── run.py                      # Local server launcher wrapper (Uvicorn)
│
├── frontend/                       # Next.js 14 Frontend User Interface
│   ├── src/                        # React Application Source Code
│   │   └── app/                    # Next.js App Router Structure
│   │       ├── page.tsx            # Single-Screen High-Density Terminal Dashboard
│   │       ├── layout.tsx          # Root HTML layout & metadata setup
│   │       └── globals.css         # Tailwind CSS imports & terminal dark-mode styles
│   ├── package.json                # Frontend Node.js dependencies & scripts
│   ├── tailwind.config.js          # Custom theme, neon palette & grid tokens
│   ├── tsconfig.json               # TypeScript compiler configuration
│   ├── next.config.mjs             # Next.js framework build rules
│   └── postcss.config.js           # PostCSS plugin settings for Tailwind
│
├── .gitignore                      # Git exclusion rules (builds, .env, cache)
└── README.md                       # Complete project documentation
```
---

## 🚀 Quick Start & Local Setup

Follow these steps to get the entire full-stack application running locally in under 2 minutes.

### Prerequisites
* **Python 3.11+**
* **Node.js 18+** & `npm`

---

### 1. Backend Setup (FastAPI)

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv

# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from example
cp .env.example .env

# Run the backend server
python run.py

# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

cd backend
pytest
