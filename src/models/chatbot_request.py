from pydantic import BaseModel, Field

class ChatbotRequest(BaseModel):
    """
    Represents the request body for the chatbot endpoint.
    """
    query: str = Field(..., description="The user's input query string", min_length=1)
