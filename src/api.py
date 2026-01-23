from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from src.main import get_response_from_bot
from src.models.chatbot_request import ChatbotRequest
from src.models.chatbot_response import ChatbotResponse
from src.utils.logger import csv_logger
from src.configs.settings import settings

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="DocuChatAI API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler to catch unhandled errors.
    """
    csv_logger.log("ERROR", f"Unhandled exception for request {request.url}", exception=exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Handler for HTTPExceptions to ensure they are logged.
    """
    # Log 500s as errors, others as warnings
    if exc.status_code >= 500:
        csv_logger.log("ERROR", f"HTTP {exc.status_code} at {request.url}: {exc.detail}")
    else:
        csv_logger.log("WARNING", f"HTTP {exc.status_code} at {request.url}: {exc.detail}")
        
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.post("/chatbot", response_model=ChatbotResponse)
@limiter.limit(settings.get_api_rate_limit())
def chatbot_endpoint(request: Request, chatbot_data: ChatbotRequest):
    """
    Process a chatbot query and return the response.

    Args:
        request (Request): The raw HTTP request (required for rate limiting).
        chatbot_data (ChatbotRequest): The request body containing the user's query.

    Returns:
        ChatbotResponse: A structured response containing the answer, query ID, score, and source URLs.

    Raises:
        HTTPException: 
            - 400 if the query is empty.
            - 500 if an internal server error occurs during processing.
            - 404 if no answer is found.
            - 429 if rate limit is exceeded.
    """
    if not chatbot_data.query:
        raise HTTPException(status_code=400, detail="Empty query.")
    
    csv_logger.log("INFO", f"Processing query: {chatbot_data.query}")
    response = get_response_from_bot(chatbot_data.query)
    
    if not response:
        raise HTTPException(status_code=404, detail="No answer found for your query.")
        
    csv_logger.log("INFO", f"Successfully processed query: {chatbot_data.query}")
    return response
