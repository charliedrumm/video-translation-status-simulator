from flask import Flask, jsonify, request
import threading
import time
import random
import requests

app = Flask(__name__)

# Store the tasks in a dictionary
tasks = {}

# Configuration
TASK_COMPLETION_TIME = 10  
ERROR_RATE = 0.1          
def simulate_task(task_id, webhook_url):
    """Simulate a task's lifecycle."""
    time.sleep(random.uniform(1, TASK_COMPLETION_TIME))
    if random.random() < ERROR_RATE:
        tasks[task_id]["status"] = "error"
    else:
        tasks[task_id]["status"] = "completed"

    #Notify the client when the task is complete
    if webhook_url:
        try:
            requests.post(webhook_url, json={"task_id": task_id, "status": tasks[task_id]["status"]})
        except requests.exceptions.RequestException as e:
            print(f"Failed to send webhook for task {task_id}: {e}")

@app.route("/tasks", methods=["POST"])
def create_task():
    """Create a new task."""
    data = request.json
    webhook_url = data.get("webhook_url") if data else None

    task_id = str(len(tasks) + 1)
    tasks[task_id] = {
        "status": "pending",
        "webhook_url": webhook_url
    }

    #Simulate the task using a thread for async processing
    threading.Thread(target=simulate_task, args=(task_id, webhook_url)).start()
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
