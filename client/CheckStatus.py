import requests
import socketio


class CheckStatus:
    def __init__(self, server_url, websocket_url):
        self.server_url = server_url
        self.websocket_url = websocket_url
        self.sio = socketio.Client()
        self.received_updates = {}

        
        @self.sio.on("connect")
        def on_connect():
            print("Connected to WebSocket server.")
            self.sid = self.sio.sid 
            print(f"Session ID: {self.sid}")

        @self.sio.on("task_update")
        def on_task_update(data):
            task_id = data["task_id"]
            status = data["status"]
            print(f"Received update for task {task_id}: {status}")
            self.received_updates[task_id] = status

        @self.sio.on("disconnect")
        def on_disconnect():
            print("Disconnected from WebSocket server.")

    def connect(self):
        """Connect to the WebSocket server."""
        self.sio.connect(self.websocket_url)

    def disconnect(self):
        """Disconnect from the WebSocket server."""
        self.sio.disconnect()

    def create_task(self, delay=10):
        """Create a new task."""
        payload = {"delay": delay}
        response = requests.post(f"{self.server_url}/tasks", json=payload)
        if response.status_code == 201:
            task_id = response.json()["task_id"]
            print(f"Task {task_id} created.")
            return task_id
        else:
            raise Exception(f"Failed to create task: {response.text}")
        
    def get_status(self, task_id):
        """Get the current status of a task"""
        response = requests.get(f"{self.server_url}/tasks/{task_id}/status")
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get status for task {task_id}: {response.text}")

    def wait_for_task(self, task_id):
        """Send wait_for_task to server and wait for response"""
        self.sio.emit("wait_for_task", {"task_id": task_id})

        #wait until the task is over
        while task_id not in self.received_updates:
            pass

        return {"status" :self.received_updates[task_id]}
    
    def create_and_wait(self, delay):
        """Create a task and wait for its completion."""
        task_id = self.create_task(delay)
        result = self.wait_for_task(task_id)
        return task_id, result
