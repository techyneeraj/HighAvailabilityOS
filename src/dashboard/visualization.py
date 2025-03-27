# src/dashboard/visualization.py
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

class Visualization:
    def __init__(self, max_points=30):
        self.max_points = max_points
        self.times = []
        self.cpu_usages = []
        self.failures = []
        self.fig, self.ax = plt.subplots(figsize=(5, 3))
        self.ax.set_title("System Metrics Over Time")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("CPU Usage (%)")
        self.line, = self.ax.plot([], [], label="CPU Usage")
        self.failure_points, = self.ax.plot([], [], 'ro', label="Failures")
        self.ax.legend()
        self.ax.set_ylim(0, 100)

    def create_chart(self, root):
        return FigureCanvasTkAgg(self.fig, master=root)

    def update_data(self, cpu_usage, failure_detected):
        self.times.append(len(self.times) * 2)  # 2s intervals
        self.cpu_usages.append(cpu_usage)
        self.failures.append(1 if failure_detected else 0)

        if len(self.times) > self.max_points:
            self.times.pop(0)
            self.cpu_usages.pop(0)
            self.failures.pop(0)

        self.line.set_data(self.times, self.cpu_usages)
        failure_times = [t for t, f in zip(self.times, self.failures) if f]
        failure_values = [self.cpu_usages[i] for i, f in enumerate(self.failures) if f]
        self.failure_points.set_data(failure_times, failure_values)

        # Avoid singular transformation by ensuring valid x-limits
        if self.times:
            self.ax.set_xlim(min(self.times), max(self.times) + 1 if len(self.times) > 1 else 2)
        else:
            self.ax.set_xlim(0, 2)  # Default range when empty

    def draw(self):
        self.fig.canvas.draw()

if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    viz = Visualization()
    canvas = viz.create_chart(root)
    canvas.get_tk_widget().pack()
    for i in range(10):
        viz.update_data(i * 10, i % 3 == 0)
        root.update()
        time.sleep(0.5)
    root.mainloop()