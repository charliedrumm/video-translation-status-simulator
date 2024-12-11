# video-translation-status-simulator

The library uses WebSockets to communicate with the server. I chose this implementation over repetitive HTTP polling because it provides the client with real-time updates on when their video has finished processing, eliminating the need to continuously poll the server with HTTP requests to get the status. Based on the brief, “When you use video translation on Heygen, behind the scenes it is a time-consuming process depending on how long the video is and many other factors,” I determined that continuous HTTP polling would not be ideal, as the client might have to make numerous requests while waiting for the video to finish processing. Since the server only needs to send a small status update, WebSockets were a better fit for the task.

## **How to Run**

### **1. Prerequisites**

- Docker and Docker Compose installed on your system.

### **2. Clone the Repository**

```bash
git clone https://github.com/charliedrumm/video-translation-status-simulator.git
cd video-translation-status-simulator
```

### **3. Start the Application**

Build and run the Docker containers:

```bash
docker-compose up --build
```

### **4. View the Output**

The client will:

- Create tasks with different durations.
- Receive and print status updates in real-time when tasks are completed.

### **5. Stop the Application**

To stop the application:

```bash
docker-compose down
```
