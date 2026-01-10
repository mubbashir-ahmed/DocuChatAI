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

# Create a global instance to be used by other modules
settings = Settings()
