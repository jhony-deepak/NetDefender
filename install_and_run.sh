#!/bin/bash

echo "🔧 Setting up NetDefender..."

# Check for Docker
if ! command -v docker &> /dev/null
then
    echo "❌ Docker not found. Please install Docker before running this script."
    exit 1
fi

# Build and run the container
echo "🐳 Building Docker image..."
docker-compose up --build -d

# Wait a moment and open browser
sleep 3
echo "🌐 Opening NetDefender Dashboard..."
open http://localhost:5000

echo "✅ NetDefender is now running in Docker!"