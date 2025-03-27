# src/fault_tolerance/failure_det.py
import time
from core_manager.process_mgr import ProcessManager

class FailureDetector:
    def __init__(self, process_manager, timeout=5):
        self.process_mgr = process_manager
        self.timeout = timeout
        self.last_response = {}

    def update_response(self, task_name):
        self.last_response[task_name] = time.time()

    def check_timeouts(self):
        current_time = time.time()
        failed_processes = []
        # Use a copy of items to avoid iteration issues
        for task_name, process in list(self.process_mgr.processes.items()):
            if process.is_alive():
                last_time = self.last_response.get(task_name, current_time)
                if current_time - last_time > self.timeout:
                    failed_processes.append(task_name)
                    print(f"Timeout detected: {task_name} hasn’t responded in {self.timeout} seconds.")
            else:
                if task_name in self.last_response:
                    failed_processes.append(task_name)
                    print(f"Crash detected: {task_name} is no longer alive.")
        return failed_processes

    def monitor(self, interval=1):
        while not self.process_mgr.shutdown_flag.value:
            failed = self.check_timeouts()
            if failed:
                return failed
            time.sleep(interval)
        return []

if __name__ == "__main__":
    from core_manager.process_mgr import ProcessManager
    pm = ProcessManager()
    pm.start_process("HeartMonitor")
    fd = FailureDetector(pm)
    time.sleep(6)
    failed = fd.check_timeouts()
    print(f"Failed processes: {failed}")
    pm.shutdown()