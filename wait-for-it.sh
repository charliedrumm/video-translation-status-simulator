#!/bin/sh

# Wait for the server to be ready
echo "Waiting for the server to start..."

while ! curl -s http://server:5000 > /dev/null; do
  sleep 1
done

echo "Server is ready. Starting the client..."
exec "$@"
