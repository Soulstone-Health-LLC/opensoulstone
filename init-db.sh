#!/bin/bash

# Database initialization and setup script
# This script provides a user-friendly way to initialize the database

echo "======================================"
echo "  Soulstone Database Initialization"
echo "======================================"
echo

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ ERROR: .env file not found!"
    echo "Please copy .env.example to .env and configure your settings:"
    echo "  cp .env.example .env"
    echo "  # Then edit .env with your configuration"
    echo
    exit 1
fi

echo "✓ Found .env configuration file"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ ERROR: Docker is not running!"
    echo "Please start Docker and try again."
    echo
    exit 1
fi

echo "✓ Docker is running"

# Check if containers are running
if docker compose ps | grep -q "Up"; then
    echo "✓ Docker containers are running"
else
    echo "⚠️  Docker containers are not running"
    echo "Starting containers..."
    docker compose up -d
    echo "Waiting for containers to be ready..."
    sleep 10
fi

echo "🔄 Initializing database..."
echo

# Run the database creation script
docker compose exec web python3 create_db.py

if [ $? -eq 0 ]; then
    echo
    echo "======================================"
    echo "✅ Database initialization completed!"
    echo "======================================"
    echo
    echo "Next steps:"
    echo "1. Access the application at: http://localhost:8000"
    echo "2. Use your configured admin credentials to log in"
    echo "3. Optionally seed with test data: make db_seed_all"
    echo
else
    echo
    echo "❌ Database initialization failed!"
    echo "Check the logs for more details: make logs"
    echo
    exit 1
fi
