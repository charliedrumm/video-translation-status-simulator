import requests
import socketio


class CheckStatus:
    def __init__(self, server_url, websocket_url):
        self.server_url = server_url
        self.websocket_url = websocket_url
        self.sio = socketio.Client()
        self.received_updates = {}

        # WebSocket event handlers
        @self.sio.on("connect")
        def on_connect():
            print("Connected to WebSocket server.")
            self.sid = self.sio.sid  # Store the session ID
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

    def create_task(self):
        """Create a new task."""
        response = requests.post(f"{self.server_url}/tasks")
        if response.status_code == 201:
            task_id = response.json()["task_id"]
            print(f"Task {task_id} created.")
            return task_id
        else:
            raise Exception(f"Failed to create task: {response.text}")

    def wait_for_task(self, task_id):
        """Send a `wait_for_task` event and block until a response is received."""
        print(f"Waiting for task {task_id} to complete...")
        self.sio.emit("wait_for_task", {"task_id": task_id})

        # Block until the task status is updated
        while task_id not in self.received_updates:
            pass

        return self.received_updates[task_id]
