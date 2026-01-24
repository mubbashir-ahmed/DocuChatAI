import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from typing import Optional


class Settings:
    """
    Configuration settings for the application.
    Loads environment variables from .env file.
    """

    def get_aws_access_key(self) -> Optional[str]:
        """Returns the AWS Access Key ID."""
        return os.getenv("AWS_ACCESS_KEY_ID", "")

    def get_aws_secret_key(self) -> Optional[str]:
        """Returns the AWS Secret Access Key."""
        return os.getenv("AWS_SECRET_ACCESS_KEY", "")

    def get_aws_kendra_index_id(self) -> str:
        """Returns the Kendra Index ID."""
        return os.getenv("AWS_KENDRA_INDEX_ID", "")

    def get_openai_secret_key(self) -> Optional[str]:
        """Returns the OpenAI API Key."""
        return os.getenv("OPENAI_API_KEY", "")

    def get_aws_region(self) -> str:
        """Returns the AWS Region. Defaults to 'us-east-2'."""
        return os.getenv("AWS_REGION", "us-east-2")

    def get_log_dir(self) -> str:
        """Returns the directory for log files. Defaults to 'logs'."""
        return os.getenv("LOG_DIR", "logs")

    def get_log_filename_suffix(self) -> str:
        """Returns the suffix for log files. Defaults to 'app_log.csv'."""
        return os.getenv("LOG_FILENAME_SUFFIX", "app_log.csv")

    def get_open_ai_model(self) -> str:
        """Returns the OpenAI model. Defaults to 'gpt-3.5-turbo'."""
        return os.getenv("OPEN_AI_MODEL", "gpt-3.5-turbo")

    def get_max_urls_to_process(self) -> int:
        """Returns the maximum number of URLs to process. Defaults to 3."""
        return int(os.getenv("MAX_URLS_TO_PROCESS", 3))

    def get_api_rate_limit(self) -> str:
        """Returns the API rate limit. Defaults to 10/minute."""
        return str(os.getenv("API_RATE_LIMIT", "10/minute"))

    def get_max_tokens(self) -> int:
        """Returns the max tokens. Defaults to 1000."""
        return int(os.getenv("MAX_TOKENS", 1000))


# Create a global instance to be used by other modules
settings = Settings()
