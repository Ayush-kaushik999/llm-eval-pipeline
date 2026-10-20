# 🚀 Automated LLM Output Benchmark & Evaluation Pipeline

A production-grade, modular LLMOps backend service and interactive dashboard designed to systematically benchmark and evaluate Large Language Model outputs across accuracy, semantic faithfulness, and performance metrics.

---

## 🛠️ Tech Stack & Architecture

* **Backend Framework:** FastAPI, Uvicorn, Pydantic (v2)
* **Database & Persistence:** MongoDB Atlas, Motor (Async IO)
* **Evaluation Framework:** Hybrid deterministic metrics (keyword matching) and LLM-as-a-Judge evaluation (Groq / Gemini APIs)
* **Frontend UI:** Streamlit, Plotly
* **Containerization:** Docker & Docker Compose

---

## 📂 Project Directory Structure

```text
llm-eval-pipeline/
├── app/
│   ├── api/                # FastAPI routers and route definitions
│   ├── controllers/        # Business logic and controller layer
│   ├── core/               # Configuration and database connection handlers
│   ├── models/             # Pydantic data validation schemas
│   ├── services/           # Evaluation engines and metrics calculation
│   └── main.py             # FastAPI entry point
├── dashboard/              # Streamlit interactive UI & Dockerfile
├── data/                   # Default benchmark datasets (JSON)
├── tests/                  # Unit and integration test suite
├── Dockerfile              # Backend container configuration
├── docker-compose.yml      # Multi-container orchestration
├── requirements.txt        # Project dependencies
└── README.md
