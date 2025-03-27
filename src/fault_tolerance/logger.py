# src/fault_tolerance/logger.py
import time
import os

class FailureLogger:
    def __init__(self, log_file="../logs/system_logs.txt"):
        self.log_file = log_file
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

    def log_failure(self, task_name, reason):
        """Log a failure event to the file."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        log_entry = f"{timestamp} - Process '{task_name}' failed: {reason}\n"
        with open(self.log_file, 'a') as f:
            f.write(log_entry)
        print(f"Logged: {log_entry.strip()}")

if __name__ == "__main__":
    logger = FailureLogger()
    logger.log_failure("TransactionServer", "Memory overflow")