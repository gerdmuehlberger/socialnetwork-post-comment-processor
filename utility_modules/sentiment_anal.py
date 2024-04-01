import logging
import os
from functools import lru_cache
from abc import ABC, abstractmethod
from transformers import pipeline, AutoTokenizer

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger('transformers').setLevel(logging.ERROR)


class SentimentProvider(ABC):
    @abstractmethod
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def get_label(self, string_to_classify: str) -> str:
        return ""

    @abstractmethod
    def get_sentiment_score(self, string_to_score: str) -> float:
        return 0.


class DistillBertSentimentProvider(SentimentProvider):
    @lru_cache(maxsize=10)
    def __init__(self) -> None:
        super().__init__()
        model_name = "distilbert-base-uncased-finetuned-sst-2-english"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model=model_name
        )

    @lru_cache(maxsize=1000)
    def _cached_sentiment_analysis(self, text: str):
        truncated_tokens = self.get_truncated_tokens(text=text)
        return self.sentiment_pipeline(truncated_tokens)[0]

    def get_truncated_tokens(self, text):
        tokens = self.tokenizer.encode(
            text, add_special_tokens=True, truncation=True, max_length=512)
        return self.tokenizer.decode(
            tokens, skip_special_tokens=True)

    def get_label(self, string_to_classify: str) -> str:
        result = self._cached_sentiment_analysis(string_to_classify)
        return result['label']

    def get_sentiment_score(self, string_to_score: str) -> float:
        result = self._cached_sentiment_analysis(string_to_score)
        return result['score']


class SentimentProviderFactory:
    @staticmethod
    def get_provider(provider_type: str) -> SentimentProvider:
        if provider_type.lower() == "distillbert":
            return DistillBertSentimentProvider()
        return DistillBertSentimentProvider()
