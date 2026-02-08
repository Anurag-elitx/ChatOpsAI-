# ChatOps AI Platform

An enterprise-grade conversational AI system that connects team chat (Slack, Teams, Web) to internal tools like **JIRA**, **Salesforce**, and **Zendesk** — powered by **Retrieval-Augmented Generation (RAG)** and backed by a full **MLOps / CI-CD** pipeline.

![System Architecture](https://github.com/user-attachments/assets/f8f7722a-e1e6-48e5-aef9-8fcbe1dcf5ad)

---

## Why I Built This

Most internal support workflows still depend on humans triaging messages, copy-pasting ticket details, and manually looking up docs. I wanted to build a system that:

- **Understands intent** using a fine-tuned transformer (distilBERT)
- **Retrieves relevant context** from a vector knowledge base (FAISS + Sentence-BERT)
- **Generates natural replies** via an LLM (GPT-2 locally, swappable to GPT-4 / Claude)
- **Takes action** by calling enterprise APIs when the intent warrants it
- **Retrains itself** when data drift is detected, with full observability

---

## Features

| Category | Details |
|---|---|
| **NLP Pipeline** | Intent classification → Entity extraction (spaCy) → RAG retrieval → LLM response |
| **Integrations** | JIRA (bug tickets), Salesforce (account queries), Zendesk (support tickets) |
| **Infrastructure** | Docker multi-stage build, Kubernetes (Deployment + Service + HPA), GitHub Actions CI |
| **Monitoring** | Prometheus counters & histograms, Sentry error tracking, structured loguru logging |
| **MLOps** | MLflow experiment tracking, DVC pipeline, automated retraining on drift (Evidently.ai) |

---

## Architecture

```
User (Slack / Teams / Web)
        │
        ▼
   FastAPI Gateway   ──►  Enterprise APIs
        │                 (JIRA, Salesforce, Zendesk)
        ▼
   NLP Pipeline
   ├─ Intent Classifier (distilBERT)
   ├─ Entity Extractor  (spaCy)
   ├─ Vector Search      (FAISS + Sentence-BERT)
   └─ Response Generator (GPT-2 / LLM)
        │
        ▼
   Monitoring & Retraining
   ├─ Prometheus + Grafana
   ├─ Sentry
   └─ MLflow + DVC pipeline
```

---

## Project Structure

```
├── app/
│   ├── main.py                  # FastAPI server & endpoints
│   ├── pipeline.py              # End-to-end NLP pipeline
│   ├── monitoring.py            # Prometheus + Sentry helpers
│   ├── retrain_trigger.py       # MLflow-based retraining trigger
│   ├── config.py                # Centralised env config
│   ├── integrations/
│   │   └── external_apis.py     # JIRA / Salesforce / Zendesk
│   ├── models/
│   │   ├── intent_classifier.py
│   │   ├── response_generator.py
│   │   ├── entity_extractor.py
│   │   └── vector_search.py
│   └── utils/
│       └── logger.py            # Loguru-based logger
├── tests/
│   ├── conftest.py
│   ├── test_main.py
│   └── test_intent_classifier.py
├── docker/
│   └── Dockerfile
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
├── retraining/
│   └── pipeline.yaml
├── .github/workflows/
│   └── ci.yml
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── CONTRIBUTING.md
└── README.md
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- Docker & Docker Compose (optional, for containerised setup)

### Local Setup

```bash
# Clone the repository
git clone https://github.com/your-username/chatops-ai-platform.git
cd chatops-ai-platform

# Create a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys / endpoints

# Run the server
uvicorn app.main:server --reload
```

### Docker Setup

```bash
docker compose up --build
```

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Health check (used by K8s probes) |
| `GET` | `/status` | Detailed app status |
| `POST` | `/chat` | Send a message and get an AI response |

### Example Request

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I found a bug in the login page"}'
```

---

## Running Tests

```bash
pytest tests/ -v
```

---

## Deployment

The project includes Kubernetes manifests in `k8s/` and a GitHub Actions CI pipeline in `.github/workflows/ci.yml` that runs linting, tests, and a Docker build on every push to `main`.

![Deployment Diagram](https://github.com/user-attachments/assets/26732501-abcc-47e9-acfd-81e2cb43f4db)

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
