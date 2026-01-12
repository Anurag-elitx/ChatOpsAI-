"""Tests for the intent classification module."""

from app.models.intent_classifier import classify_intent

VALID_LABELS = {"joy", "happy", "surprise", "love", "anger", "sadness", "fear"}


class TestClassifyIntent:
    """Group intent-classifier tests."""

    def test_returns_string(self):
        """classify_intent should always return a string."""
        result = classify_intent("I feel great today!")
        assert isinstance(result, str)

    def test_positive_sentiment(self):
        """Positive input should map to a known emotion label."""
        result = classify_intent("I feel great today!")
        assert result in VALID_LABELS

    def test_negative_sentiment(self):
        """Negative input should still return a valid label."""
        result = classify_intent("This is terrible and I'm upset")
        assert result in VALID_LABELS

    def test_empty_string(self):
        """Empty string should not crash; returns any label or 'unknown'."""
        result = classify_intent("")
        assert isinstance(result, str)

    def test_none_input_returns_unknown(self):
        """Passing None should be handled gracefully."""
        result = classify_intent(None)
        assert result == "unknown"
