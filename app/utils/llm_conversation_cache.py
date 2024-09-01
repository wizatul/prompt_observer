from builtins import super, hasattr, set

import logging
from threading import Lock
from typing import Set

from app.model.llm_model import LLMConversation

log = logging.getLogger(__name__)


class LLMConversationCache:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(LLMConversationCache, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._cache: Set[LLMConversation] = set()
            self._initialized = True

    def insert(self, interaction: LLMConversation):
        required_fields = {
            'modelType': interaction.modelType,
            'answer': interaction.answer,
            'prompt': interaction.prompt,
        }
        print("answer:", interaction.answer)
        print("prompt:", interaction.prompt)
        print("modelType:", interaction.modelType)
        with self._lock:
                self._cache.difference_update({interaction})
                self._cache.add(interaction)

    def get_all(self) -> Set[LLMConversation]:
        with self._lock:
            return self._cache

    def remove(self, interactions: Set[LLMConversation]):
        with self._lock:
            self._cache.difference_update(interactions)
