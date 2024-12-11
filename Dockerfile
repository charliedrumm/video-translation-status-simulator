FROM python:3.9-slim

WORKDIR /app
RUN apt-get update && apt-get install -y curl && apt-get clean
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY client_test.py .
COPY client client

COPY wait-for-it.sh .
ENV PYTHONUNBUFFERED=1
RUN chmod +x wait-for-it.sh

CMD ["./wait-for-it.sh", "python", "client_test.py"]
