# src/core_manager/health_mon.py
import psutil
import time

class HealthMonitor:
    def __init__(self, cpu_threshold=90, mem_threshold=90):
        self.cpu_threshold = cpu_threshold
        self.mem_threshold = mem_threshold

    def check_system_health(self):
        cpu_usage = psutil.cpu_percent(interval=1)
        mem_usage = psutil.virtual_memory().percent
        return {
            "cpu_usage": cpu_usage,
            "memory_usage": mem_usage,
            "cpu_alert": cpu_usage > self.cpu_threshold,
            "mem_alert": mem_usage > self.mem_threshold
        }

if __name__ == "__main__":
    hm = HealthMonitor()
    print(hm.check_system_health())