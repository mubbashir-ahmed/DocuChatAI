import json
from openai import OpenAI as OpenAIClient
from typing import List, Optional, Dict

from src.configs.settings import settings
from src.utils.logger import csv_logger


class OpenAI:
    """
    Singleton service class for interacting with OpenAI's API.
    """

    __instance = None
    _client: Optional[OpenAIClient] = None
    
    # Const
    CONSENSUS_TEMPERATURE = 0.0

    @staticmethod
    def get_instance() -> "OpenAI":
        """Static access method."""
        if OpenAI.__instance == None:
            OpenAI()
        return OpenAI.__instance

    def __init__(self):
        if OpenAI.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            OpenAI.__instance = self

    def get_openai_client(self) -> OpenAIClient:
        """
        Creates and returns the OpenAI client instance.

        Returns:
            OpenAIClient: Configured OpenAI client with API key.
        """
        if self._client is None:
            self._client = OpenAIClient(api_key=settings.get_openai_secret_key())
        return self._client

    def get_chatgpt_response(self, query: str, temp: float, **kwargs) -> Optional[str]:
        """
        Sends a query to OpenAI and returns the response.

        Args:
            query (str): The prompt for the model.
            temp (float): The temperature for the model (0.0 to 1.0).

        Returns:
            Optional[str]: The generated text response, or None if an error occurs.
        """
        try:
            client = self.get_openai_client()
            response = client.chat.completions.create(
                model=settings.get_open_ai_model(),
                messages=[
                    {
                        "role": "system",
                        "content": "You are an intelligent assistant. Output valid JSON.",
                    },
                    {"role": "user", "content": query},
                ],
                temperature=temp,
                max_tokens=settings.get_max_tokens(),
            )
            message = response.choices[0].message.content
            return message.strip() if message else None
        except Exception as ex:
            csv_logger.log(
                "ERROR", "Exception in OpenAI.get_chatgpt_response()", exception=ex
            )
            return None

    def get_consensus(
        self, statements: List[str], weights: List[int], my_query: str
    ) -> Dict[str, int]:
        """
        Generates a consensus answer from multiple statements using ChatGPT.

        Args:
            statements (List[str]): A list of candidate answer statements.
            weights (List[int]): Weights associated with each statement.
            my_query (str): The original user query.

        Returns:
            Dict[str, int]: A dictionary mapping consolidated answers to their aggregate scores.
        """
        statements_str = "\n".join([f"{i} | {y}" for i, y in enumerate(statements)])

        ensemble_prompt = f"""
        You have three answers to the same question.

        Output a JSON object with one of two structures:

        1. If the answers are a lists of items:
        {{
            "type": "items",
            "data": [
                {{ "id": 0, "items": ["Item A", "Item B"] }},
                {{ "id": 1, "items": ["Item B"] }}
            ]
        }}

        2. If the answers are descriptive statements:
        {{
            "type": "statement",
            "text": "The unified summary statement..."
        }}

        Statements:
        {statements_str}

        Question:
        {my_query}

        Answers:
        """

        result = self.get_chatgpt_response(
            ensemble_prompt, self.CONSENSUS_TEMPERATURE, response_format={"type": "json_object"}
        )
        container = {}
        if not result:
            return container

        try:
            data = json.loads(result)

            if data.get("type") == "items":
                for entry in data.get("data", []):
                    statement_id = entry.get("id")
                    items = entry.get("items", [])

                    for item in items:
                        if item not in container:
                            container[item] = 0
                        # map item back to the original statement's weight
                        if 0 <= statement_id < len(weights):
                            container[item] += weights[statement_id]
            elif data.get("type") == "statement":
                text = data.get("text")
                if text:
                    container[text] = sum(weights)
        except json.JSONDecodeError as e:
            csv_logger.log(
                "ERROR", f"Failed to parse JSON response: {result}", exception=e
            )
        except Exception as e:
            csv_logger.log("ERROR", "Error processing consensus data", exception=e)

        return container
