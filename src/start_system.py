# src/start_system.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core_manager import ProcessManager, HealthMonitor, RedundancyManager
from fault_tolerance import FailureDetector, RecoveryManager, FailureLogger
from dashboard import Dashboard, StatusMonitor, Visualization
import time
import signal
import threading
import random

pm = None
rm = None
dashboard = None
updater_thread = None
monitor_thread = None

def signal_handler(sig, frame):
    global pm, rm, dashboard
    print("\nCaught Ctrl+C, shutting down...")
    if pm:
        pm.shutdown()
    if rm:
        rm.shutdown()
    if dashboard:
        dashboard.running = False
    sys.exit(0)

def process_response_updater(pm, fd, stress=False):
    while not pm.shutdown_flag.value:
        task_names = list(pm.processes.keys())
        for task_name in task_names:
            if stress and random.random() < 0.3:
                print(f"Simulating delay for {task_name}...")
                time.sleep(random.uniform(2, 5))
            else:
                fd.update_response(task_name)
            time.sleep(1)

def monitor_system(pm, fd, rec, logger, rm):
    while True:
        failed_processes = fd.check_timeouts()
        for task in failed_processes:
            logger.log_failure(task, "Timeout or crash detected")
            rec.recover(task)
        with pm.failure_flag.get_lock():
            if pm.failure_flag.value:
                print("FAILURE DETECTED: Handling simulated failure...")
                logger.log_failure("HeartMonitor", "Simulated failure")
                if rm.activate_backup("HeartMonitor"):
                    print("Recovery successful: Backup activated.")
                pm.failure_flag.value = 0
        time.sleep(2)

def run_system():
    global pm, rm, dashboard, updater_thread, monitor_thread
    pm = ProcessManager()
    hm = HealthMonitor(cpu_threshold=90, mem_threshold=90)
    rm = RedundancyManager(pm)
    fd = FailureDetector(pm, timeout=5)
    rec = RecoveryManager(pm, rm)
    logger = FailureLogger()
    sm = StatusMonitor(pm, hm, fd)
    viz = Visualization()
    dashboard = Dashboard(sm, viz)

    signal.signal(signal.SIGINT, signal_handler)

    pm.start_process("HeartMonitor")
    rm.create_backup("HeartMonitor")

    updater_thread = threading.Thread(target=process_response_updater, args=(pm, fd, True), daemon=True)
    updater_thread.start()

    monitor_thread = threading.Thread(target=monitor_system, args=(pm, fd, rec, logger, rm), daemon=True)
    monitor_thread.start()

    print("Starting system monitoring...")
    dashboard.run()

if __name__ == "__main__":
    run_system()