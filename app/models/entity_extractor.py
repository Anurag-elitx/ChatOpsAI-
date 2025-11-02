"""
Named Entity Recognition (NER) using spaCy.

Extracts entities from user messages and returns them as a
list of dicts with label, text, and character offsets.
"""

import spacy
from app.config import SPACY_MODEL
from app.utils.logger import logger

# Load the spaCy language model once
ner_model = spacy.load(SPACY_MODEL)
logger.info(f"NER model loaded — {SPACY_MODEL}")


def extract_entities(text: str) -> list[dict]:
    """
    Extract named entities from the input text.

    Returns a list of dicts, each containing:
      - label:  entity type (PERSON, ORG, DATE, etc.)
      - text:   the matched span
      - start:  character start offset
      - end:    character end offset
    """
    try:
        doc = ner_model(text)
        entities = [
            {
                "label": ent.label_,
                "text": ent.text,
                "start": ent.start_char,
                "end": ent.end_char,
            }
            for ent in doc.ents
        ]
        logger.debug(f"Extracted {len(entities)} entities from input")
        return entities
    except Exception as exc:
        logger.error(f"Entity extraction failed: {exc}")
        return []
