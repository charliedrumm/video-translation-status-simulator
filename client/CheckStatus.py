import requests
from flask import Flask, request, jsonify
import threading

class CheckStatus:
    def __init__(self, server_url, webhook_port=5001):
        self.server_url = server_url
        self.webhook_port = webhook_port
        self.webhook_thread = threading.Thread(target=self._start_webhook_server)
        self.webhook_thread.daemon = True
        self.received_webhooks = {}
        self.start_webhook_listener()

    def create_task(self):
        """Creates a task on the server with a webhook URL."""
        webhook_url = f"http://localhost:{self.webhook_port}/webhook"
        response = requests.post(f"{self.server_url}/tasks", json={"webhook_url": webhook_url})
        if response.status_code == 201:
            return response.json()["task_id"]
        else:
            raise Exception(f"Failed to create task: {response.text}")

    def get_task_status(self, task_id):
        """Polls the server for the status of a task."""
        response = requests.get(f"{self.server_url}/tasks/{task_id}/status")
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get task status: {response.text}")

    def wait_for_completion(self, task_id):
        """Blocks until the task is completed or an error occurs, using webhooks."""
        while task_id not in self.received_webhooks:
            pass
        return {'status': self.received_webhooks[task_id]}

    def _start_webhook_server(self):
        """Starts a Flask server to handle webhooks."""
        app = Flask(__name__)

        @app.route("/webhook", methods=["POST"])
        def webhook_handler():
            data = request.json
            task_id = data.get("task_id")
            status = data.get("status")
            if task_id:
                self.received_webhooks[task_id] = status
            return jsonify({"message": "Webhook received."}), 200

        app.run(port=self.webhook_port, debug=False)

    def start_webhook_listener(self):
        """Starts the webhook listener in a background thread."""
        self.webhook_thread.start()
