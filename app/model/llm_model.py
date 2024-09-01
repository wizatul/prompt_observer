from builtins import str

from openai import BaseModel
from typing import Optional, List


class LLMConversation(BaseModel):
    prompt: Optional[List[str]] = None
    answer: Optional[List[str]] = None
    modelType: Optional[str] = None
