import os
import pytest
import threading
import pandas as pd

from unittest.mock import patch
from datetime import datetime

from src.utils.logger import csv_logger


def test_concurrency_logging_safety(tmp_path) -> None:
    """
    Spawn multiple threads to write logs simultaneously.
    Verifies that no data is lost and the file is not corrupted.
    """
    # 1. Setup: Direct logs to a temporary directory to not mess up real logs
    ## patch the instance attribute 'log_dir' directly for this test
    temp_log_dir = str(tmp_path)
    csv_logger.log_dir = temp_log_dir

    ## configuration
    num_threads = 10
    logs_per_thread = 50
    total_expected_logs = num_threads * logs_per_thread

    # 2. Define worker function
    def worker(thread_id) -> None:
        for i in range(logs_per_thread):
            csv_logger.log("INFO", f"Thread-{thread_id} log message {i}")

    # 3. Execution: create and start threads
    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    # 4. Wait for all threads to finish
    for t in threads:
        t.join()

    # 5. Verification
    ## construct the expected filename
    now = datetime.now()
    log_filename = csv_logger._get_log_filename(now)

    assert os.path.exists(log_filename), "Log file does not exist"

    ## Read csv file and verify the count
    try:
        df = pd.read_csv(log_filename)

        assert len(df) == total_expected_logs, (
            f"Expected {total_expected_logs} logs, but found {len(df)}"
        )
        print(f"Success! {len(df)} logs written safely.")

    except Exception as e:
        pytest.fail(f"Failed to read CSV file (file might be corrupted): {e}")
