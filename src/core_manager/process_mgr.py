# src/core_manager/process_mgr.py
import multiprocessing
import time
import random

def simulate_task(task_name, shutdown_flag, failure_flag):
    """Simulate a critical task (standalone to avoid pickling issues)."""
    print(f"Starting {task_name}...")
    while not shutdown_flag.value:
        try:
            time.sleep(random.uniform(0.5, 2.0))
            print(f"{task_name} is running...")
            if random.random() < 0.1:
                with failure_flag.get_lock():
                    failure_flag.value = True
                print(f"Simulated failure in {task_name}! Signaled for recovery.")
        except KeyboardInterrupt:
            print(f"{task_name} interrupted, shutting down...")
            return
    print(f"{task_name} shutting down gracefully...")

class ProcessManager:
    def __init__(self):
        self.processes = {}
        self.critical_tasks = ["HeartMonitor", "FlightControl", "TransactionServer"]
        self.shutdown_flag = multiprocessing.Value('b', False)
        self.failure_flag = multiprocessing.Value('b', False)

    def start_process(self, task_name):
        if task_name not in self.critical_tasks:
            print(f"Error: {task_name} is not a recognized critical task.")
            return
        process = multiprocessing.Process(
            target=simulate_task,  # Use standalone function
            args=(task_name, self.shutdown_flag, self.failure_flag)
        )
        self.processes[task_name] = process
        process.start()
        print(f"Process for {task_name} started with PID {process.pid}")

    def stop_process(self, task_name):
        if task_name in self.processes and self.processes[task_name].is_alive():
            self.processes[task_name].terminate()
            self.processes[task_name].join()
            del self.processes[task_name]
            print(f"Process for {task_name} stopped.")
        else:
            print(f"No active process to stop for {task_name}.")

    def get_running_processes(self):
        return {name: proc.is_alive() for name, proc in self.processes.items()}

    def check_failure(self):
        with self.failure_flag.get_lock():
            return self.failure_flag.value

    def reset_failure(self):
        with self.failure_flag.get_lock():
            self.failure_flag.value = False

    def shutdown(self):
        with self.shutdown_flag.get_lock():
            self.shutdown_flag.value = True
        for task_name in list(self.processes.keys()):
            self.stop_process(task_name)

if __name__ == "__main__":
    pm = ProcessManager()
    pm.start_process("HeartMonitor")
    time.sleep(5)
    pm.shutdown()