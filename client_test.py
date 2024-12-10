from client.CheckStatus import CheckStatus
from concurrent.futures import ThreadPoolExecutor


def test_client_library():
    server_url = "http://localhost:5000"
    websocket_url = "http://localhost:5000/socket.io/"
    client = CheckStatus(server_url, websocket_url)
    client.connect()

    try:
        #Threads run this function
        def create_and_wait_task(delay):
            task_id, result = client.create_and_wait(delay)
            print(f"Task {task_id} completed with status: {result['status']}")

        #I am using ThreadPoolExecuter to simulate multiple tasks being made at once
        with ThreadPoolExecutor(max_workers=5) as executor:
            task_times = [10,4,6,7,8] #make the tasks different times to show shorter tasks are not blocked
            for i in range(5):
                executor.submit(create_and_wait_task, task_times[i])
            
    finally:
        client.disconnect()

if __name__ == "__main__":
    test_client_library()