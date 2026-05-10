#!/bin/bash

# Startup script for Railway deployment
# Handles port environment variable properly

# Set default port if not provided
PORT=${PORT:-8000}

echo "Starting MCP Server on port $PORT..."

# Start the application with the correct port
exec uvicorn server:app --host 0.0.0.0 --port $PORT
