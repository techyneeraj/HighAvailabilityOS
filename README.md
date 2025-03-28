# Project Report: High Availability Operating Systems for Critical Systems

### 1. Project Overview
The *"High Availability Operating Systems for Critical Systems"* project is a simulation designed to mimic an operating system that ensures continuous operation for mission-critical applications, such as medical heart monitors or aerospace control systems. 
Developed in Python, it integrates process management, fault tolerance, and real-time monitoring to maintain system reliability under failure conditions. 
The system can be initiated via a Flask-based web interface (`src/main.py`) and runs its core logic through `src/start_system.py`, which manages processes and recovery mechanisms. 
This project showcases high-availability principles, making it suitable for educational demonstrations or as a foundation for real-world critical system designs.

### 2. Module-Wise Breakdown
- **Core Manager (`src/core_manager/`):**
  - **Process Manager:** Launches and manages critical processes (e.g., "HeartMonitor") with unique PIDs.
  - **Health Monitor:** Tracks system resources (CPU, memory) against thresholds.
  - **Redundancy Manager:** Maintains backup processes for failover.
- **Fault Tolerance (`src/fault_tolerance/`):**
  - **Failure Detector:** Identifies process timeouts or crashes (e.g., after 5 seconds).
  - **Recovery Manager:** Restarts failed processes or activates backups.
  - **Failure Logger:** Records failure events to a log file.
- **Dashboard (`src/dashboard/`):**
  - **GUI:** Visualizes system status (assumed Tkinter-based from typical setups).
  - **Status Monitor:** Collects metrics like uptime and CPU usage.
  - **Visualization:** Plots system data (assumed Matplotlib-based).
- **Main Components:**
  - **Flask Server (`src/main.py`):** Hosts a web interface to trigger the system.
  - **System Runner (`src/start_system.py`):** Executes the core simulation logic.

### 3. Functionalities
- **Process Management:** Starts critical processes and their backups as threads.
- **Fault Detection and Recovery:** Detects failures (e.g., timeouts) and switches to backups or restarts processes, logging events.
- **Real-Time Monitoring:** Tracks system uptime and resource usage, potentially displayed via a GUI dashboard.
- **Web Interface:** Provides a user-friendly way to start the system via `web/index.html` and the `/run` endpoint in `main.py`.
- **Logging:** Saves failure events with timestamps (e.g., to `logs/system_logs.txt` if implemented).

### 4. Technology Used
- **Programming Languages:**
  - Python: Core logic, server, and simulation.
  - HTML/CSS/JavaScript: Web interface (`web/` folder).
- **Libraries and Tools:**
  - Flask (3.0.3): Web server to initiate the system.
  - Psutil (5.9.8): Monitors CPU and memory usage (assumed from requirements).
  - Threading: Manages concurrent processes.
  - Tkinter: GUI dashboard (assumed for visualization).
  - Matplotlib (3.8.3): Plots system metrics (assumed for dashboard).
- **Other Tools:**
  - GitHub: Version control and hosting at [https://github.com/techyneeraj/HighAvailabilityOS](https://github.com/techyneeraj/HighAvailabilityOS).
  - Git: Command-line tool for repository management.

### 5. Flow Diagram
```
[User] --> [Web Interface (index.html)] --> [Click "Run the System"]
          |
          v
[Flask Server (main.py)] --> [Triggers start_system.py]
          |
          v
[Core System (start_system.py)]
  |
  +--> [Process Manager] --> [Start "HeartMonitor" & Backup]
  |      |
  |      v
  +--> [Failure Detector] --> [Check Timeouts]
  |      |
  |      v
  +--> [Recovery Manager] --> [Activate Backup on Failure]
  |      |
  |      v
  +--> [Logger] --> [Log Failures]
  |
  v
[Dashboard] --> [Display Metrics]
```

### 6. Revision Tracking on GitHub
- **Repository Name:** HighAvailabilityOS
- **GitHub Link:** [https://github.com/techyneeraj/HighAvailabilityOS](https://github.com/techyneeraj/HighAvailabilityOS)
  - **Upload Process:**
    1. Initialized Git in `osproject/` with `git init`.
    2. Staged all files (including subfolders) with `git add .`.
    3. Committed with `git commit -m "Initial upload"`.
    4. Pushed to GitHub with `git push -u origin master:main`.
  - **Update Process:**
    1. Modified `src/main.py` (e.g., added a comment).
    2. Staged with `git add src/main.py`.
    3. Committed with `git commit -m "Updated main.py"`.
    4. Pushed with `git push origin master`.
  - Tracks 45 files in the initial commit (March 27, 2025), with updates tracked in subsequent commits.

### 7. Conclusion and Future Scope
- **Conclusion:** This project effectively simulates a high-availability OS, demonstrating process management, fault tolerance, and web-based control. It’s a practical proof-of-concept for critical system reliability.
- **Future Scope:**
  - Implement a GUI stop button or `/stop` endpoint in Flask.
  - Simulate multi-node distributed systems.
  - Add real-time user controls to the dashboard (e.g., process restart).

### 8. References
- Python Documentation: [python.org](https://www.python.org)
- Flask Documentation: [flask.palletsprojects.com](https://flask.palletsprojects.com)
- GitHub Help: [docs.github.com](https://docs.github.com)
- Psutil Documentation: [psutil.readthedocs.io](https://psutil.readthedocs.io)


## Appendix

### A. AI-Generated Project Elaboration/Breakdown Report
This project simulates a high-availability OS for critical systems where downtime is unacceptable. Key components include:
- **Core Manager:** Launches processes like "HeartMonitor" with backups, using Python’s `threading` and `psutil` for resource monitoring.
- **Fault Tolerance:** Detects failures (e.g., 5-second timeouts) and recovers via backups, logging to a file.
- **Web Interface:** A Flask server (`main.py`) triggers `start_system.py` through a webpage (`index.html`).
- **Execution:** Developed iteratively, with Git tracking at [https://github.com/techyneeraj/HighAvailabilityOS](https://github.com/techyneeraj/HighAvailabilityOS).

### B. Problem Statement
Create a simulation of a high-availability operating system for critical applications that ensures uninterrupted operation. It must manage processes, detect and recover from failures, provide monitoring, and be deployable via GitHub with a user-friendly interface.

### C. Solution/Code
Below are key files (full code assumed in the GitHub repo):

#### `src/main.py`
```python
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, Response

app = Flask(__name__)
system_started = False

@app.route('/')
def home():
    return Response("Welcome! Open web/index.html to start.", status=200)

@app.route('/run', methods=['GET'])
def start_system():
    global system_started
    if not system_started:
        os.system("start python src/start_system.py")
        system_started = True
        return Response("System starting!", status=200)
    return Response("System already running!", status=200)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=False)
```

#### `src/start_system.py`
```python
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

def signal_handler(sig, frame):
    global pm, rm, dashboard
    print("\nCaught Ctrl+C, shutting down...")
    if pm: pm.shutdown()
    if rm: rm.shutdown()
    if dashboard: dashboard.running = False
    sys.exit(0)

def run_system():
    global pm, rm, dashboard
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

    updater_thread = threading.Thread(target=lambda: None, daemon=True)
    updater_thread.start()
    monitor_thread = threading.Thread(target=lambda: None, daemon=True)
    monitor_thread.start()

    print("Starting system monitoring...")
    dashboard.run()

if __name__ == "__main__":
    run_system()
```

#### `web/index.html`
```html
<!DOCTYPE html>
<html>
<head>
    <title>High Availability OS</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <h1>High Availability OS</h1>
    <button onclick="runSystem()">Run the System</button>
    <p id="run-status">Status: Waiting...</p>
    <script src="script.js"></script>
</body>
</html>
```

#### `web/script.js`
```javascript
function runSystem() {
    const status = document.getElementById("run-status");
    status.textContent = "Status: Starting system...";
    fetch('http://127.0.0.1:5000/run')
        .then(response => response.text())
        .then(data => status.textContent = "Status: " + data)
        .catch(error => status.textContent = "Status: Error - " + error);
}
```

#### `requirements.txt`
```
flask==3.0.3
psutil==5.9.8
matplotlib==3.8.3
```

**Note:** Subfolder files (e.g., `core_manager/process_mgr.py`) are assumed in the repo—add them if missing.

---

### Instructions for Completion
1. **Add Full Code:** Expand Appendix C with all subfolder files from `src/core_manager/`, `src/fault_tolerance/`, etc., if not fully represented above.
2. **Run and Test:**
   - Core system: `python src/start_system.py`
   - Full system: `python src/main.py`, then open `web/index.html`.
3. **Screenshots:**
   - Capture terminal output from `start_system.py` (e.g., "Starting system monitoring...").
   - Screenshot `web/index.html` in action.
   - Add to repo in `images/` folder and update README with links.
4. **Push Updates:**
   ```
   git add .
   git commit -m "Finalized report and code"
   git push origin master
   ```
