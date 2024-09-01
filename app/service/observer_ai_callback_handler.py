from datetime import datetime

from contextvars import ContextVar

from builtins import super, str

from langchain_community.callbacks.openai_info import standardize_model_name
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import Generation
from typing import Dict, Any, List

from app.model.llm_model import LLMConversation
from app.utils.llm_conversation_cache import LLMConversationCache

llm_conversation_value: ContextVar[LLMConversation] = ContextVar("llm_conversation", default=None)


llm_conversation_cache = LLMConversationCache()


def validate_generations(generations: List[List[Generation]]) -> List[List[str]]:
    standardized_generations = []

    for generation_list in generations:
        standardized_generation_list = []
        for generation in generation_list:
            # Validate and standardize the generation text
            standardized_text = generation.text.strip()  # Example of standardization
            standardized_generation_list.append(standardized_text)
        standardized_generations.append(standardized_generation_list)

    return standardized_generations


class CustomOpenAICallbackHandler(BaseCallbackHandler):
    def __init__(self):
        llm_conversation = None
        super().__init__()

    def on_llm_start(
            self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        super().on_llm_start(serialized, prompts, **kwargs)
        if llm_conversation_value is not None:
            llm_conversation_value.prompt = prompts

    def on_llm_end(self, response, **kwargs):
        super().on_llm_end(response, **kwargs)
        model_name = standardize_model_name(response.llm_output.get("model_name", ""))
        generation_text = validate_generations(response.generations)
        if llm_conversation_value is not None:
            llm_conversation_value.modelType = model_name
            llm_conversation_value.answer = generation_text
            llm_conversation_cache.insert(llm_conversation_value)

