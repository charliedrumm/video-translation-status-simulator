import threading
from client.CheckStatus import CheckStatus



def test_client_library():
    # Server configuration
    server_url = "http://localhost:5000"
    websocket_url = "http://localhost:5000/socket.io/"

    # Initialize the client library
    client = CheckStatus(server_url, websocket_url)

    # Connect to the WebSocket server
    client.connect()

    try:
        # Create tasks
        task_ids = [client.create_task() for _ in range(3)]
        print(f"Created tasks: {task_ids}")

        # Wait for each task to complete
        for task_id in task_ids:
            status = client.wait_for_task(task_id)
            print(f"Task {task_id} completed with status: {status}")

    finally:
        # Disconnect from the WebSocket server
        client.disconnect()


if __name__ == "__main__":
    test_client_library()
