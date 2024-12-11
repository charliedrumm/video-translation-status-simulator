import os
from client.CheckStatus import CheckStatus
from concurrent.futures import ThreadPoolExecutor


def test_client_library():
    server_url = os.getenv("SERVER_URL", "http://localhost:5000")
    websocket_url = os.getenv("WEBSOCKET_URL", "http://localhost:5000/socket.io/")
    client = CheckStatus(server_url, websocket_url)
    client.connect()

    try:
        task_times = [7, 4, 6, 2, 8] 
        
        for i, delay in enumerate(task_times, start=1):
            print(f"\nCreating Task {i} with a delay of {delay} seconds...")
            task_id, result = client.create_and_wait(delay)
            print(f"Task {i} (ID: {task_id}) completed with status: {result['status']}")
            
    finally:
        client.disconnect()

if __name__ == "__main__":
    test_client_library()