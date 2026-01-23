from pydantic import BaseModel, Field

class ChatbotRequest(BaseModel):
    """
    Represents the request body for the chatbot endpoint.
    """
    # Const
    MIN_LENGTH = 1

    query: str = Field(..., description="The user's input query string", min_length=MIN_LENGTH)
