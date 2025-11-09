"""
Semantic vector search using FAISS and Sentence-Transformers.

Encodes the user query into a dense vector, searches a FAISS index
for the nearest neighbours, and returns the matching document texts
concatenated as RAG context.
"""

import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

from app.config import (
    EMBEDDING_MODEL_NAME,
    FAISS_INDEX_PATH,
    ID_TO_TEXT_PATH,
    VECTOR_SEARCH_TOP_K,
)
from app.utils.logger import logger

# ── Load embedding model & index ─────────────────────────────
sentence_encoder = SentenceTransformer(EMBEDDING_MODEL_NAME)

try:
    faiss_index = faiss.read_index(FAISS_INDEX_PATH)
    with open(ID_TO_TEXT_PATH, "r", encoding="utf-8") as fh:
        _id_to_document = json.load(fh)
    logger.info(
        f"FAISS index loaded — {faiss_index.ntotal} vectors, "
        f"{len(_id_to_document)} document mappings"
    )
except FileNotFoundError:
    faiss_index = None
    _id_to_document = {}
    logger.warning(
        "FAISS index or document mapping not found; "
        "vector search will return empty results"
    )


def semantic_search(query: str, top_k: int | None = None) -> str:
    """
    Retrieve the top-k most relevant documents for the query.

    Returns the matched documents joined by newlines, suitable for
    injection as context into an LLM prompt.
    """
    if faiss_index is None:
        return ""

    k = top_k or VECTOR_SEARCH_TOP_K

    try:
        query_embedding = sentence_encoder.encode([query])
        distances, indices = faiss_index.search(
            np.array(query_embedding, dtype="float32"), k
        )

        matched_docs = [
            _id_to_document[str(idx)]
            for idx in indices[0]
            if str(idx) in _id_to_document
        ]
        logger.debug(f"Vector search returned {len(matched_docs)} docs for query")
        return "\n".join(matched_docs)
    except Exception as exc:
        logger.error(f"Semantic search failed: {exc}")
        return ""
