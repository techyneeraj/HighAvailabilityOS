# src/core_manager/redundancy.py
import multiprocessing
import time
from .process_mgr import simulate_task  # Import the standalone function

class RedundancyManager:
    def __init__(self, process_manager):
        self.process_mgr = process_manager
        self.backups = {}

    def create_backup(self, task_name):
        if task_name not in self.process_mgr.processes:
            print(f"Error: Cannot create backup for {task_name} - no primary process exists.")
            return
        backup_process = multiprocessing.Process(
            target=simulate_task,  # Use standalone function
            args=(task_name + "_Backup", self.process_mgr.shutdown_flag, self.process_mgr.failure_flag)
        )
        self.backups[task_name] = backup_process
        backup_process.start()
        print(f"Backup process for {task_name} started with PID {backup_process.pid}")

    def check_backup_status(self, task_name):
        if task_name in self.backups and self.backups[task_name].is_alive():
            return True
        return False

    def activate_backup(self, task_name):
        if self.check_backup_status(task_name):
            print(f"Activating backup for {task_name}...")
            self.process_mgr.stop_process(task_name)
            return True
        print(f"No active backup available for {task_name}.")
        return False

    def stop_backup(self, task_name):
        if task_name in self.backups and self.backups[task_name].is_alive():
            self.backups[task_name].terminate()
            self.backups[task_name].join()
            del self.backups[task_name]
            print(f"Backup for {task_name} stopped.")
        else:
            print(f"No active backup to stop for {task_name}.")

    def shutdown(self):
        for task_name in list(self.backups.keys()):
            self.stop_backup(task_name)

if __name__ == "__main__":
    from process_mgr import ProcessManager
    pm = ProcessManager()
    pm.start_process("TransactionServer")
    rm = RedundancyManager(pm)
    rm.create_backup("TransactionServer")
    time.sleep(3)
    pm.shutdown()
    rm.shutdown()