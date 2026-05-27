from flask import Flask, flash, redirect, url_for, request, jsonify,render_template
import time
from concurrent.futures import ThreadPoolExecutor
import os,json,uuid,platform
path = os.getcwd()
app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=4)
@app.route('/')
def index():
    host = request.host
    # Returns the host name without the port (e.g., 'localhost' or 'example.com')
    host_only = request.host.split(':')[0]
    # Returns the full base URL (e.g., 'http://localhost:5000/')
    host_url = request.host_url

    return render_template('index.html',current_ip = request.host,current_hostname=platform.node())


@app.route('/stress',methods=['POST'])
def stress():
    data = request.get_json()
    return jsonify(data)


def cpu_heavy_task(duration):
    """Burns CPU cycles for a specified number of seconds."""
    end_time = time.time() + duration
    count = 0
    while time.time() < end_time:
        # Perform mathematical operations to max out CPU
        count += 1
        _ = 1234567890 * 9876543210
    return count


@app.route('/stress-cpu', methods=['POST'])
def stress_cpu():
    # Get duration from request (default to 10 seconds if not provided)
    data = request.json or {}
    duration = float(data.get('duration'))

    # Run the CPU stress test in a separate thread so Flask can still process other requests
    future = executor.submit(cpu_heavy_task, duration)

    return jsonify({
        "status": "CPU stress test started",
        "duration_seconds": duration
    }), 202
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=8080,threaded=True)
