"""
Centralized configuration module.

Loads all environment variables and provides default values
for local development. Used across the application to avoid
scattering os.getenv() calls everywhere.
"""

import os
from dotenv import load_dotenv

load_dotenv()


# ── Application Settings ─────────────────────────────────────
APP_NAME = "ChatOps AI Platform"
APP_VERSION = "1.0.0"
APP_ENV = os.getenv("ENV", "development")
DEBUG = APP_ENV == "development"

# ── Server ────────────────────────────────────────────────────
HOST = os.getenv("APP_HOST", "0.0.0.0")
PORT = int(os.getenv("APP_PORT", "8000"))

# ── Database / Vector Store ───────────────────────────────────
POSTGRES_USER = os.getenv("POSTGRES_USER", "user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
POSTGRES_DB = os.getenv("POSTGRES_DB", "vectordb")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))

FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "vector_store/index.faiss")
ID_TO_TEXT_PATH = os.getenv("ID_TO_TEXT_PATH", "vector_store/id_to_text.json")

# ── External Services ────────────────────────────────────────
SENTRY_DSN = os.getenv("SENTRY_DSN", "")
SLACK_API_TOKEN = os.getenv("SLACK_API_TOKEN", "")
CLOUD_API_KEY = os.getenv("CLOUD_API_KEY", "")

# ── Integrations ─────────────────────────────────────────────
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL", "https://your-jira-instance.atlassian.net")
SALESFORCE_BASE_URL = os.getenv("SALESFORCE_BASE_URL", "https://login.salesforce.com")
ZENDESK_BASE_URL = os.getenv("ZENDESK_BASE_URL", "https://your-subdomain.zendesk.com")
API_TIMEOUT_SECONDS = int(os.getenv("API_TIMEOUT_SECONDS", "30"))

# ── Model Configuration ──────────────────────────────────────
INTENT_MODEL_NAME = os.getenv(
    "INTENT_MODEL_NAME",
    "bhadresh-savani/distilbert-base-uncased-emotion",
)
GENERATION_MODEL_NAME = os.getenv("GENERATION_MODEL_NAME", "gpt2")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
SPACY_MODEL = os.getenv("SPACY_MODEL", "en_core_web_sm")

VECTOR_SEARCH_TOP_K = int(os.getenv("VECTOR_SEARCH_TOP_K", "3"))
GENERATION_MAX_TOKENS = int(os.getenv("GENERATION_MAX_TOKENS", "100"))
