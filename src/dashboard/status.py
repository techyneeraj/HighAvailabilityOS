# src/dashboard/status.py
import time
from core_manager.process_mgr import ProcessManager  # Absolute import
from core_manager.health_mon import HealthMonitor  # Absolute import
from fault_tolerance.failure_det import FailureDetector  # Absolute import

class StatusMonitor:
    def __init__(self, process_manager, health_monitor, failure_detector):
        self.process_mgr = process_manager
        self.health_mon = health_monitor
        self.failure_det = failure_detector
        self.start_time = time.time()

    def get_status(self):
        system_health = self.health_mon.check_system_health()
        process_health = self.process_mgr.get_running_processes()
        uptime = self.calculate_uptime()
        failed_processes = self.failure_det.check_timeouts()

        failure_detected = bool(failed_processes or self.process_mgr.check_failure())
        failure_message = (f"Process {failed_processes[0] if failed_processes else 'unknown'} "
                          f"failed; recovery attempted.") if failure_detected else ""

        return {
            "uptime": round(uptime, 2),
            "cpu_usage": system_health["cpu_usage"],
            "processes": process_health,
            "failure_detected": failure_detected,
            "failure_message": failure_message
        }

    def calculate_uptime(self):
        current_time = time.time()
        elapsed = current_time - self.start_time
        return 100.0 if elapsed > 0 else 0.0

if __name__ == "__main__":
    from core_manager.process_mgr import ProcessManager  # Absolute import
    from core_manager.health_mon import HealthMonitor  # Absolute import
    from fault_tolerance.failure_det import FailureDetector  # Absolute import
    pm = ProcessManager()
    hm = HealthMonitor()
    fd = FailureDetector(pm)
    sm = StatusMonitor(pm, hm, fd)
    print(sm.get_status())