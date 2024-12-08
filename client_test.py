import threading
from client.CheckStatus import CheckStatus

def test_client_library():
    server_url = "http://localhost:5000"
    client = CheckStatus(server_url)

    # Create 4 tasks
    task_ids = [client.create_task() for _ in range(4)]
    print(f"Created tasks: {task_ids}")

    def wait_and_print(task_id):
        result = client.wait_for_completion(task_id)
        print(f"Task {task_id} completed with status: {result}")

    # Start threads to wait for each task
    threads = [threading.Thread(target=wait_and_print, args=(task_id,)) for task_id in task_ids]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    test_client_library()
