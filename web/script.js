// web/script.js
function toggleOutput() {
    const output = document.getElementById("terminal-output");
    output.classList.toggle("hidden");
}

function runSystem() {
    const status = document.getElementById("run-status");
    status.textContent = "Status: Starting system...";

    fetch('http://127.0.0.1:5000/run')
        .then(response => {
            if (!response.ok) {
                throw new Error(`Server responded with status ${response.status}`);
            }
            return response.text();
        })
        .then(data => {
            status.textContent = "Status: " + data;
        })
        .catch(error => {
            status.textContent = "Status: Error - " + error.message + " (Ensure python main.py is running in src/)";
        });
}