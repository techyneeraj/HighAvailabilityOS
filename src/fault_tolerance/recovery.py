# src/fault_tolerance/recovery.py
from core_manager.process_mgr import ProcessManager  # Absolute import
from core_manager.redundancy import RedundancyManager  # Absolute import

class RecoveryManager:
    def __init__(self, process_manager, redundancy_manager):
        self.process_mgr = process_manager
        self.redundancy_mgr = redundancy_manager

    def recover(self, failed_task):
        """Attempt to recover a failed process."""
        if self.redundancy_mgr.check_backup_status(failed_task):
            print(f"Switching to backup for {failed_task}...")
            self.redundancy_mgr.activate_backup(failed_task)
            return True
        else:
            print(f"No backup available for {failed_task}, restarting process...")
            self.process_mgr.stop_process(failed_task)
            self.process_mgr.start_process(failed_task)
            return True
        return False

if __name__ == "__main__":
    from core_manager.process_mgr import ProcessManager  # Absolute import
    from core_manager.redundancy import RedundancyManager  # Absolute import
    pm = ProcessManager()
    rm = RedundancyManager(pm)
    pm.start_process("FlightControl")
    rm.create_backup("FlightControl")
    rec = RecoveryManager(pm, rm)
    rec.recover("FlightControl")
    pm.shutdown()
    rm.shutdown()