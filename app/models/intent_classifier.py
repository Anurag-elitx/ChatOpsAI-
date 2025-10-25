"""
Intent classification using a distilBERT-based emotion model.

Wraps the HuggingFace transformers pipeline so the rest of the
application can call `classify_intent(text)` without worrying
about model details.
"""

from transformers import pipeline as hf_pipeline
from app.config import INTENT_MODEL_NAME
from app.utils.logger import logger

# Load the classification pipeline once at module level
intent_pipeline = hf_pipeline(
    "text-classification",
    model=INTENT_MODEL_NAME,
    return_all_scores=True,
)

logger.info(f"Intent classifier loaded — model={INTENT_MODEL_NAME}")


def classify_intent(text: str) -> str:
    """
    Predict the most likely intent / emotion label for the input text.

    Returns the label string (e.g. 'joy', 'anger', 'sadness') or
    'unknown' if classification fails.
    """
    try:
        scores = intent_pipeline(text)
        top_label = max(scores[0], key=lambda item: item["score"])["label"]
        logger.debug(f"Intent for '{text[:40]}…' → {top_label}")
        return top_label
    except Exception as exc:
        logger.error(f"Intent classification failed: {exc}")
        return "unknown"
