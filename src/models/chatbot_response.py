from pydantic import BaseModel
from typing import List

class ChatbotResponse(BaseModel):
    """
    Represents the response from the chatbot.
    """
    queryId: str
    answer: str
    score: int
    urls: List[str]
