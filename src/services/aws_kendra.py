import boto3
import random
from typing import Optional, Any, List, Tuple

from src.configs.settings import settings
from src.utils.logger import csv_logger

class AWSKendra:
    """
    Singleton service class for interacting with AWS Kendra.
    """
    __instance = None
    _client = None
    
    @staticmethod 
    def get_instance() -> 'AWSKendra':
        """ Static access method. """
        if AWSKendra.__instance == None:
            AWSKendra()
        return AWSKendra.__instance
    
    def __init__(self):
        if AWSKendra.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            AWSKendra.__instance = self
            
    def get_kendra_client(self) -> Optional[Any]:
        """
        Creates and returns a boto3 Kendra client.

        Returns:
            Any: The boto3 Kendra client, or None if creation fails.
        """
        try:
            if self._client is None:
                self._client = boto3.client('kendra', 
                                           region_name=settings.get_aws_region(), 
                                           aws_access_key_id=settings.get_aws_access_key(), 
                                           aws_secret_access_key=settings.get_aws_secret_key())
            return self._client
        except Exception as ex:
            csv_logger.log("ERROR", "Exception in AWSKendra.get_kendra_client()", exception=ex)
            return None
    
    def get_kendra_query_results(self, query: str) -> Tuple[Optional[str], Optional[List[Any]]]:
        """
        Queries the Kendra index.

        Args:
            query (str): The search query.

        Returns:
            Tuple[Optional[str], Optional[List[Any]]]: A tuple containing the QueryId and a list of ResultItems.
        """
        try:
            client = self.get_kendra_client()
            if not client:
                return None, None
            response = client.query(QueryText=str(query), IndexId=settings.get_aws_kendra_index_id())
            query_id = response.get('QueryId')
            result_items = response.get('ResultItems')
            return query_id, result_items
        except Exception as ex:
            csv_logger.log("ERROR", "Exception in AWSKendra.get_kendra_query_results()", exception=ex)
            return None, None
        
    def get_answers_from_query_results(self, result_items: List[Any]) -> List[List[Any]]:
        """
        Extracts answers and their metadata from Kendra query results.

        Args:
            result_items (List[Any]): A list of Kendra result items.

        Returns:
            List[List[Any]]: A list of answers, where each answer is [text, url, confidence_score].
        """
        try:
            # DOC_URLS = []
            ANSWERS_WITH_URLS = []
            if result_items is None:
                return []
                
            for i in range(len(result_items)):
                answer = ""
                item = result_items[i]
                if item.get('Type') == 'ANSWER':
                    # get doc url 
                    item_doc_url = item.get('DocumentURI')
                    
                    # get doc kendra score
                    item_doc_score = item.get('ScoreAttributes')
                    if not item_doc_score:
                        continue  # Skip items without score attributes
                    
                    item_doc_confidence = item_doc_score.get('ScoreConfidence')
                    confidence = self.get_confidence_weightage_by_confidence(confidence=item_doc_confidence)

                    # get doc suggested text
                    item_doc_exercpt_prop = item.get('DocumentExcerpt')
                    item_doc_text = item_doc_exercpt_prop.get('Text')
                    item_doc_text = str(item_doc_text)
                    doc_text_splitted = item_doc_text.split('\n')
                    content = ""
                    for text in doc_text_splitted:
                        text = text.strip()
                        if text != "":
                            content += f" {text}"
                    answer = content.strip()
                    answer = answer.replace(u'\xa0', u' ') # replacing whitespaces with space
                    answer_with_url = [answer, str(item_doc_url), confidence]
                    ANSWERS_WITH_URLS.append(answer_with_url)
                
                if item.get('Type') == 'DOCUMENT':
                    # get doc url 
                    item_doc_url = item.get('DocumentURI')
                    
                    # get doc kendra score
                    item_doc_score = item.get('ScoreAttributes')
                    item_doc_confidence = item_doc_score.get('ScoreConfidence')
                    confidence = self.get_confidence_weightage_by_confidence(confidence=item_doc_confidence)

                    # get doc suggested text
                    item_doc_exercpt_prop = item.get('DocumentExcerpt')
                    item_doc_text = item_doc_exercpt_prop.get('Text')
                    item_doc_text = str(item_doc_text)
                    doc_text_splitted = item_doc_text.split('\n')
                    content = ""
                    for text in doc_text_splitted:
                        text = text.strip()
                        text = text.strip('.')
                        if text != "":
                            content += f" {text}"
                    answer = content.strip()
                    answer = answer.replace(u'\xa0', u' ') # replacing whitespaces with space
                    answer_with_url = [answer, str(item_doc_url), confidence]
                    ANSWERS_WITH_URLS.append(answer_with_url)
            return ANSWERS_WITH_URLS
        except Exception as ex:
            csv_logger.log("ERROR", "Exception in AWSKendra.get_answers_from_query_results()", exception=ex)
            return []
        
    def get_confidence_weightage_by_confidence(self, confidence: str) -> int:
        """
        Maps Kendra confidence levels to a numerical weight.

        Args:
            confidence (str): The confidence level string (e.g., 'VERY HIGH', 'HIGH').

        Returns:
            int: A random integer within the weighted range for the confidence level.
        """
        r = 0
        if confidence == 'VERY HIGH':
            r = random.randint(8, 10)
        elif confidence == 'HIGH':
            r = random.randint(6, 8)
        elif confidence == 'MEDIUM':
            r = random.randint(3, 5)
        elif confidence == 'LOW':
            r = random.randint(0, 2)
        
        if r >= 100:
            r = 100
        return r
