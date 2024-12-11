# CheckStatus Client Library

The `CheckStatus` client library allows you to communicate with a server via WebSockets to create tasks, check their status, and receive real-time updates when tasks are completed.

## Installation

Clone or download the repository, then include the `CheckStatus` library in your Python project.

```bash
pip install requests python-socketio
```

## Features

- **Create Tasks**: Create tasks with a specified delay (processing time).
- **Real-Time Updates**: Get notified via WebSocket when tasks are completed.
- **Check Task Status**: Query the current status of a task via HTTP.
- **Timeout Handling**: Wait for task completion with an optional timeout.

---

## How to Use

### **1. Initialize the Client**

Provide the server and WebSocket URLs when creating an instance of the `CheckStatus` class.

```python
client = CheckStatus(server_url="http://localhost:5000", websocket_url="http://localhost:5000/socket.io/")
```

---

### **2. Connect to the WebSocket Server**

Establish a WebSocket connection before creating or managing tasks.

```python
client.connect()
```

---

### **3. Create a Task**

Use the `create_task` method to create a new task. You can specify the delay (processing time) for the task in seconds.

```python
task_id = client.create_task(delay=10)
print(f"Task {task_id} created.")
```

---

### **4. Get the Status of a Task**

Use the `get_status` method to query the current status of a task at any time.

```python
status = client.get_status(task_id)
print(f"Current status of task {task_id}: {status['status']}")
```

---

### **5. Wait for Task Completion**

Use the `wait_for_task` method to wait for the task to complete. The method will block until the task finishes or the timeout is reached.

```python
result = client.wait_for_task(task_id, timeout=30)
print(f"Task {task_id} completed with status: {result['status']}")
```

---

### **6. Create and Wait for a Task in One Step**

Use `create_and_wait` to create a task and wait for its completion in a single method call.

```python
task_id, result = client.create_and_wait(delay=10)
print(f"Task {task_id} completed with status: {result['status']}")
```

---

### **7. Disconnect**

After completing your operations, disconnect from the WebSocket server.

```python
client.disconnect()
```

---

## Example Usage

Here’s how you can use the library end-to-end:

```python
client = CheckStatus(server_url="http://localhost:5000", websocket_url="http://localhost:5000/socket.io/")

try:
    client.connect()
    task_id, result = client.create_and_wait(delay=10)
    print(f"Task {task_id} completed with status: {result['status']}")
finally:
    client.disconnect()
```

This library is simple to use and provides real-time updates for your tasks using WebSockets.
