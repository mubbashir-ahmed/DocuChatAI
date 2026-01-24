import os
import pandas as pd
import threading
from datetime import datetime
from typing import Optional
from src.configs.settings import settings

class CsvLogger:
    """
    A logger that writes logs to day-wise CSV files using pandas.
    """
    
    def __init__(self):
        """
        Initialize the logger.
        """
        self.log_dir = settings.get_log_dir()
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        # Initialize a lock for thread-safe logging
        self.lock = threading.Lock()

    def _get_log_filename(self, timestamp: datetime) -> str:
        """
        Generates the log filename based on the provided timestamp.
        
        Args:
            timestamp (datetime): The timestamp for the log entry.

        Returns:
            str: Absolute path to the log file (e.g., logs/2024-01-10_app_log.csv).
        """
        current_date = timestamp.strftime("%Y-%m-%d")
        suffix = settings.get_log_filename_suffix()
        filename = f"{current_date}_{suffix}"
        return os.path.join(self.log_dir, filename)

    def log(self, level: str, message: str, exception: Optional[Exception] = None) -> None:
        """
        Logs an entry to the CSV file.
        
        Args:
            level (str): Log level (INFO, ERROR, WARNING, etc.).
            message (str): Log message.
            exception (Optional[Exception]): Exception object if available.
        """
        now = datetime.now()
        timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
        
        log_entry = {
            "timestamp": timestamp_str,
            "level": level,
            "message": message,
            "exception": str(exception) if exception else ""
        }
        
        # Create a DataFrame for the single log entry
        df = pd.DataFrame([log_entry])
        
        file_path = self._get_log_filename(now)
        
        # Critical section for thread-safe file writing
        with self.lock:
            # Check if file exists to determine if header is needed
            header = not os.path.exists(file_path)
        
            try:
                # Append to CSV
                df.to_csv(file_path, mode='a', header=header, index=False)
            except Exception as e:
                print(f"Failed to write log to CSV: {e}")

# Global instance
csv_logger = CsvLogger()
