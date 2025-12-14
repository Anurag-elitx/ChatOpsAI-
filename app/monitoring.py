"""
Observability helpers — Sentry error tracking + Prometheus metrics.

Initialises Sentry on import and exposes a `track_request` function
that other modules call after processing a user message.
"""

import os
import logging

import sentry_sdk
from prometheus_client import Counter, Histogram

from app.config import SENTRY_DSN

# ── Sentry setup ──────────────────────────────────────────────
if SENTRY_DSN:
    sentry_sdk.init(dsn=SENTRY_DSN, traces_sample_rate=0.2)

# ── Prometheus metrics ────────────────────────────────────────
REQUEST_COUNT = Counter(
    "chatops_requests_total",
    "Total chat requests processed",
    ["intent"],
)

LATENCY_HISTOGRAM = Histogram(
    "chatops_request_duration_seconds",
    "Time spent processing a single chat request",
)

_logger = logging.getLogger(__name__)


def track_request(message: str, intent: str) -> None:
    """
    Record a processed request for observability.

    Increments the Prometheus counter (labelled by intent) and
    writes an INFO-level log line.
    """
    REQUEST_COUNT.labels(intent=intent).inc()
    _logger.info("Processed request — intent=%s, length=%d", intent, len(message))

    try:
        # Placeholder for pushing to a custom metrics backend
        pass
    except Exception as exc:
        sentry_sdk.capture_exception(exc)
        _logger.error("Failed to push custom metrics: %s", exc)
