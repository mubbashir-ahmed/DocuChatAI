from openai import OpenAI as OpenAIClient
from typing import List, Optional, Dict, Any
import ast

from src.configs.settings import settings
from src.utils.logger import csv_logger

class OpenAI:
    """
    Singleton service class for interacting with OpenAI's API.
    """
    __instance = None
    _client: Optional[OpenAIClient] = None
    
    @staticmethod 
    def get_instance() -> 'OpenAI':
        """ Static access method. """
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
            
    def get_chatgpt_response(self, query: str, temp: float) -> Optional[str]:
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
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an intelligent assistant."},
                    {"role": "user", "content": query}
                ],
                temperature=temp,
                max_tokens=1000
            )
            message = response.choices[0].message.content
            return message.strip() if message else None
        except Exception as ex:
            csv_logger.log("ERROR", "Exception in OpenAI.get_chatgpt_response()", exception=ex)
            return None
            
    def get_consensus(self, statements: List[str], weights: List[int], my_query: str) -> Dict[str, int]:
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

If the answer contains multiple items, write the statement id and convert the items into a list like this
Statements:
0 | They used A, B.
1 | B was their tools.
2 | They chose C plus A.

Question:
What do they use?

Answers:
The answers are items
0 | ["A", "B"]
1 | ["B"]
2 | ["A", "C"]

If they are statements without a list of items, unify them into a coherent statement like this
Statements:
0 | This medicine XYZ is used to treat lung cancer.
1 | XYZ is developed by the company ABC.
2 | The drug XYZ is approved by the FDA.

Question:
Explain the drug XYZ.

Answers:
The answer is a statement
The company ABC has developed the drug XYZ to treat lung cancer. XYZ has reveiced the FDA approval.


Statements:
{statements_str}

Question:
{my_query}

Answers:
"""
    
        result = self.get_chatgpt_response(ensemble_prompt, 0)
        container = {}
        if not result:
             return container
             
        is_list = True
        for line in result.split("\n"):
            line = line.strip()
            if len(line) > 0:
                if line == "The answers are items":
                    is_list = True
                    continue
                elif line == "The answer is a statement":
                    is_list = False
                    continue
                
                if is_list == True:
                    if "|" in line:
                        fields = line.split("|")

                        id = int(fields[0].strip())
                        try:
                            items = ast.literal_eval(fields[1].strip())
                            for item in items:
                                if item not in container:
                                    container[item] = 0
                                container[item] += weights[id]
                        except Exception as e:
                            csv_logger.log("WARNING", f"Failed to parse items line: {line}", exception=e)
                            pass
                else:
                    container[line] = sum(weights)
        return container
    