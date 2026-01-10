from typing import List, Optional
from src.services.aws_kendra import AWSKendra
from src.services.openai import OpenAI
from src.utils.logger import csv_logger
from src.models.chatbot_response import ChatbotResponse

def get_response_from_bot(query: str) -> Optional[ChatbotResponse]:
    """
    Orchestrates the chatbot response generation process.

    Args:
        query (str): The user's query string.

    Returns:
        Optional[ChatbotResponse]: A structured response object, or None if no answer found.
    """
    query_id, result_items = AWSKendra.get_instance().get_kendra_query_results(query=query)
    answers_with_urls = AWSKendra.get_instance().get_answers_from_query_results(result_items=result_items)
    
    statements: List[str] = []
    weights: List[int] = []
    urls: List[str] = []
    
    csv_logger.log("INFO", f"Kendra returned {len(answers_with_urls)} answers for query: {query}")

    for item in answers_with_urls:
        ans = item[0]
        weight = item[2]
        statements.append(ans)
        weights.append(weight)
        if item[1] not in urls:
            urls.append(item[1])
            
    res = OpenAI.get_instance().get_consensus(statements, weights, query)
    
    result: Optional[ChatbotResponse] = None
    for key, value in res.items():
        result = ChatbotResponse(
            queryId=str(query_id),
            answer=key,
            score=value,
            urls=urls[:3]
        )

    if not result:
        csv_logger.log("WARNING", f"No consensus answer found for query: {query}")

    return result