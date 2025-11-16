"""
LLM-based response generator.

Uses a HuggingFace text-generation pipeline (default: GPT-2)
to produce natural-language replies given the user's message,
detected intent, and optional RAG context.
"""

from transformers import pipeline as hf_pipeline
from app.config import GENERATION_MODEL_NAME, GENERATION_MAX_TOKENS
from app.utils.logger import logger

# Initialise the text generation pipeline once
text_gen_pipeline = hf_pipeline(
    "text-generation",
    model=GENERATION_MODEL_NAME,
)

logger.info(f"Response generator loaded — model={GENERATION_MODEL_NAME}")

_FALLBACK_REPLY = "I'm sorry, I wasn't able to generate a response. Please try again."


def generate_response(
    message: str,
    intent: str,
    context: str = "",
) -> str:
    """
    Generate a chatbot reply.

    Constructs a prompt from the intent, user message, and any
    retrieved context, then feeds it through the LLM pipeline.
    """
    prompt = (
        f"[Intent: {intent}]\n"
        f"User: {message}\n"
        f"Context: {context}\n"
        f"Assistant:"
    )

    try:
        outputs = text_gen_pipeline(
            prompt,
            max_length=GENERATION_MAX_TOKENS,
            num_return_sequences=1,
        )
        generated_text = outputs[0]["generated_text"]
        # Extract only the assistant's part of the reply
        reply = generated_text.split("Assistant:")[-1].strip()
        logger.debug(f"Generated reply ({len(reply)} chars) for intent={intent}")
        return reply
    except Exception as exc:
        logger.error(f"Response generation failed: {exc}")
        return _FALLBACK_REPLY
