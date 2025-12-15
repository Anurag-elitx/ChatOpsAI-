# Astiva AI - Competitive Intelligence Platform (Internship Project)

An enterprise-grade conversational AI system that connects team chat and a stunning React dashboard to internal tools — powered by **Retrieval-Augmented Generation (RAG)**, **Agentic Workflows (LangChain)**, and backed by a full **MLOps / CI-CD** pipeline.

---

## Why I Built This

To demonstrate my capabilities for the Astiva AI Full Stack Engineering Intern role. I wanted to build a production-ready system that:

- **Understands intent and acts autonomously** using LangChain multi-step agents.
- **Retrieves relevant context** from a vector knowledge base via a robust RAG pipeline (ChromaDB + OpenAI Embeddings).
- **Orchestrates Background Jobs** using Celery and Redis to ingest documents without blocking REST APIs.
- **Provides a Premium UX** via a modern, dynamic React.js (Vite) dashboard built with custom Vanilla CSS (glassmorphism, dark mode).
- **Takes action** by calling enterprise APIs when the intent warrants it.

---

## Features

| Category | Details |
|---|---|
| **Agentic AI** | LangChain orchestrator, OpenAI function calling, Multi-step reasoning |
| **RAG Pipeline** | ChromaDB vector store, Chunking strategies, Semantic retrieval |
| **Frontend** | React.js (Vite), Glassmorphism, Backend API integration |
| **Backend / APIs** | FastAPI, Celery background workers, Redis message broker |
| **Monitoring** | Prometheus counters & histograms, structured loguru logging |

---

## Architecture

```
User (React Dashboard)
        │
        ▼
   FastAPI Gateway   ──►  Celery / Redis (Background Ingestion)
        │
        ▼
   LangChain Agent (Multi-step Reasoning)
   ├─ Tool 1: RAG Search (ChromaDB)
   ├─ Tool 2: External API Calls (Competitive Intel)
   └─ Response Generation (GPT-4o)
```

---

## Project Structure

```
├── app/
│   ├── main.py                  # FastAPI server & endpoints
│   ├── celery_worker.py         # Celery tasks (Background RAG ingestion)
│   ├── config.py                # Centralised env config
│   ├── agents/                  # LangChain Agentic AI
│   │   ├── tools.py             # Agent tools (RAG search, external APIs)
│   │   └── workflow.py          # Agent orchestrator 
│   ├── rag/                     # RAG Pipeline
│   │   ├── indexing.py          # Document loaders & chunking
│   │   └── retrieval.py         # ChromaDB retrieval strategies
│   └── integrations/
│       └── external_apis.py     # External platform integrations
├── frontend/                    # Premium React Dashboard (Vite)
│   ├── src/
│   │   ├── App.jsx              # Main Dashboard component
│   │   └── App.css              # Custom styling
│   └── package.json
├── docker/
├── k8s/
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js & npm (for frontend)
- Redis (for Celery background jobs)

### Local Setup (Backend)

```bash
# Clone the repository
git clone https://github.com/Anurag-elitx/ChatOpsAI-.git
cd ChatOpsAI-

# Create a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start Redis (Example using Docker)
docker run -p 6379:6379 -d redis

# Start the Celery worker
celery -A app.celery_worker.celery_app worker --loglevel=info

# Run the FastAPI server
uvicorn app.main:server --reload
```

### Local Setup (Frontend)

```bash
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Start the Vite development server
npm run dev
```

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Health check (used by K8s probes) |
| `POST` | `/chat` | Trigger the LangChain Agent for a conversational response |
| `POST` | `/api/v1/documents` | Ingest a document into the RAG vector store via background jobs |

---

## Deployment

The project includes Kubernetes manifests in `k8s/` and a GitHub Actions CI pipeline in `.github/workflows/ci.yml` that runs linting, tests, and a Docker build on every push to `main`.
