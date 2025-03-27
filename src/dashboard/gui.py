# src/dashboard/gui.py
import tkinter as tk
from tkinter import messagebox
import threading
import time
import queue

class Dashboard:
    def __init__(self, status_monitor, visualization):
        self.status_monitor = status_monitor
        self.visualization = visualization
        self.root = tk.Tk()
        self.root.title("High Availability OS Dashboard")
        self.root.geometry("600x400")

        self.status_label = tk.Label(self.root, text="System Status: Initializing...", font=("Arial", 12))
        self.status_label.pack(pady=10)

        self.alert_label = tk.Label(self.root, text="Alerts: None", font=("Arial", 10), fg="red")
        self.alert_label.pack(pady=5)

        self.canvas = None
        self.setup_visualization()

        self.alert_queue = queue.Queue()  # Queue for thread-safe alerts
        self.running = True
        self.monitor_thread = threading.Thread(target=self.update_dashboard, daemon=True)
        self.monitor_thread.start()

        # Check queue periodically in main thread
        self.root.after(100, self.check_alert_queue)

    def setup_visualization(self):
        self.canvas = self.visualization.create_chart(self.root)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def update_dashboard(self):
        while self.running:
            status = self.status_monitor.get_status()
            # Update label in main thread via after
            self.root.after(0, self.status_label.config, {"text": f"System Status: Uptime={status['uptime']}%, "
                                                                 f"CPU={status['cpu_usage']}%, "
                                                                 f"Processes={status['processes']}"})
            if status['failure_detected']:
                self.root.after(0, self.alert_label.config, {"text": f"Alerts: {status['failure_message']}"})
                self.alert_queue.put(status['failure_message'])  # Queue alert for main thread
            else:
                self.root.after(0, self.alert_label.config, {"text": "Alerts: None"})

            self.visualization.update_data(status['cpu_usage'], status['failure_detected'])
            self.root.after(0, self.canvas.draw)
            time.sleep(2)

    def check_alert_queue(self):
        """Process alerts in the main thread."""
        try:
            while not self.alert_queue.empty():
                message = self.alert_queue.get_nowait()
                messagebox.showwarning("Failure Alert", message)
        except queue.Empty:
            pass
        if self.running:
            self.root.after(100, self.check_alert_queue)  # Check again after 100ms

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
        self.running = False
        self.root.destroy()

if __name__ == "__main__":
    from dashboard.status import StatusMonitor
    from dashboard.visualization import Visualization
    sm = StatusMonitor(None, None, None)  # Dummy args for testing
    viz = Visualization()
    dashboard = Dashboard(sm, viz)
    dashboard.run()