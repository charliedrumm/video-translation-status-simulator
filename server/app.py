from flask import Flask, jsonify, request
import threading
import time
import random

app = Flask(__name__)

# Store the tasks in a dictionary
tasks = {}

# Configuration
TASK_COMPLETION_TIME = 10  # Time in seconds to complete a task
ERROR_RATE = 0.1          # 10% chance for a task to end in "error"


def simulate_task(task_id):
    """Simulate a task's lifecycle. This is done with threading to allow server remain responsive"""
    time.sleep(TASK_COMPLETION_TIME)
    if random.random() < ERROR_RATE:
        tasks[task_id]["status"] = "error"
    else:
        tasks[task_id]["status"] = "completed"


@app.route("/tasks", methods=["POST"])
def create_task():
    """Create a new task."""
    task_id = str(len(tasks) + 1)
    tasks[task_id] = {
        "status": "pending"
    }
    #Threading ensures the server is responsive
    threading.Thread(target=simulate_task, args=(task_id,)).start()
    return jsonify({"task_id": task_id}), 201


@app.route("/tasks/<task_id>/status", methods=["GET"])
def get_task_status(task_id):
    """Get the status of a task."""
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({"status": task["status"]})


@app.route("/tasks", methods=["GET"])
def list_tasks():
    """List all task IDs."""
    return jsonify({"task_ids": list(tasks.keys())}), 200


@app.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Delete a task by ID."""
    if task_id not in tasks:
        return jsonify({"error": "Task not found"}), 404

    del tasks[task_id]
    return jsonify({"message": f"Task {task_id} deleted."}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
