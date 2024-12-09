from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

# In-memory storage for tasks and clients
tasks = {}  # Stores task info with task_id as key

# Configuration
TASK_COMPLETION_TIME = 10  # Time in seconds to complete a task
ERROR_RATE = 0.1           # 10% chance for a task to end in "error"


@socketio.on("connect")
def handle_connect():
    """Handle client connection."""
    sid = request.sid
    print(f"Client connected: {sid}")
    emit("server_response", {"message": "Connection successful"})


@socketio.on("disconnect")
def handle_disconnect():
    """Handle client disconnection."""
    sid = request.sid
    print(f"Client disconnected: {sid}")


@socketio.on("wait_for_task")
def handle_wait_for_task(data):
    """Associate a task with the client's session."""
    task_id = data.get("task_id")
    sid = request.sid
    if task_id in tasks:
        tasks[task_id]["sid"] = sid
        print(f"Client {sid} is waiting for task {task_id}")
    else:
        emit("task_error", {"message": f"Task {task_id} not found"}, to=sid)


def simulate_task(task_id):
    """Simulate task processing."""
    print(f"Simulating task {task_id}...")
    socketio.sleep(TASK_COMPLETION_TIME)  # Non-blocking delay

    # Randomly determine task outcome
    status = "completed" if random.random() >= ERROR_RATE else "error"
    tasks[task_id]["status"] = status
    sid = tasks[task_id].get("sid")

    # Notify the client when task is finished
    if sid:
        print(f"Task {task_id} completed with status '{status}'. Notifying client {sid}.")
        socketio.emit("task_update", {"task_id": task_id, "status": status}, to=sid)
    else:
        print(f"Task {task_id} has no associated client.")



@app.route("/tasks", methods=["POST"])
def create_task():
    """Create a new task."""
    task_id = str(len(tasks) + 1)
    tasks[task_id] = {
        "status": "pending",
        "sid": None  # Will be assigned when the client listens for the task
    }
    # Start processing the task asynchronously
    socketio.start_background_task(simulate_task, task_id)
    print(f"Task {task_id} created and started.")
    return jsonify({"task_id": task_id}), 201


@app.route("/tasks/<task_id>/status", methods=["GET"])
def get_task_status(task_id):
    """Get the status of a specific task."""
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
    """Delete a specific task."""
    if task_id not in tasks:
        return jsonify({"error": "Task not found"}), 404
    del tasks[task_id]
    print(f"Task {task_id} deleted.")
    return jsonify({"message": f"Task {task_id} deleted."}), 200


if __name__ == "__main__":
    socketio.run(app, debug=True, port=5000)
