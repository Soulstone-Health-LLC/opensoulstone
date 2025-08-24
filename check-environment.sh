#!/bin/bash

# Environment Status Script
# Shows which environment is currently running

echo "======================================"
echo "  Soulstone Environment Status"
echo "======================================"
echo

# Check if any containers are running
if ! docker compose ps | grep -q "Up"; then
    if ! docker compose -f docker-compose.dev.yaml ps | grep -q "Up"; then
        echo "❌ No Soulstone containers are currently running"
        echo
        echo "To start:"
        echo "  make dev-up      # Development environment"
        echo "  make up          # Production environment"
        echo "  make test-env    # Development with sample data"
        exit 0
    fi
fi

echo "🔍 Checking running services..."
echo

# Check development environment
DEV_RUNNING=$(docker compose -f docker-compose.dev.yaml ps --services --filter "status=running" 2>/dev/null || echo "")
PROD_RUNNING=$(docker compose ps --services --filter "status=running" 2>/dev/null || echo "")

if [[ -n "$DEV_RUNNING" ]]; then
    echo "✅ DEVELOPMENT environment is running"
    echo "   - Configuration: docker-compose.dev.yaml"
    echo "   - SSL/HTTPS: Disabled"
    echo "   - Nginx: Not used"
    echo "   - Access: http://localhost:8000"
    echo

    echo "Services running:"
    for service in $DEV_RUNNING; do
        echo "   - $service"
    done
    echo

    echo "Management commands:"
    echo "   make dev-stop           # Stop development environment"
    echo "   docker compose -f docker-compose.dev.yaml logs -f  # View logs"

elif [[ -n "$PROD_RUNNING" ]]; then
    echo "✅ PRODUCTION environment is running"
    echo "   - Configuration: docker-compose.yaml"
    echo "   - SSL/HTTPS: Enabled (if configured)"
    echo "   - Nginx: Reverse proxy enabled"
    echo "   - Access: http://localhost or https://your-domain.com"
    echo

    echo "Services running:"
    for service in $PROD_RUNNING; do
        echo "   - $service"
    done
    echo

    echo "Management commands:"
    echo "   make stop               # Stop production environment"
    echo "   make logs               # View logs"

    # Check if nginx is running and warn about SSL
    if echo "$PROD_RUNNING" | grep -q "nginx"; then
        echo
        echo "⚠️  Note: Nginx is running but may show SSL errors if certificates"
        echo "   are not properly configured. For local development, consider:"
        echo "   make stop && make dev-up"
    fi
else
    echo "❓ Unknown environment state"
    echo "   Some containers may be running but not responding"
fi

echo
echo "======================================"
echo "Environment Information:"
echo "======================================"

# Show which .env is being used
if [[ -f .env ]]; then
    echo "✅ .env file found"
    if grep -q "dev" .env; then
        echo "   - Appears to be configured for development"
    else
        echo "   - Configuration type: Check your settings"
    fi
else
    echo "❌ No .env file found"
    echo "   Copy .env.example to .env and configure it"
fi

# Show port usage
echo
echo "Port status:"
if command -v netstat >/dev/null 2>&1; then
    if netstat -tuln 2>/dev/null | grep -q ":8000 "; then
        echo "   - Port 8000: In use (Flask app)"
    else
        echo "   - Port 8000: Available"
    fi

    if netstat -tuln 2>/dev/null | grep -q ":80 "; then
        echo "   - Port 80: In use (HTTP)"
    else
        echo "   - Port 80: Available"
    fi

    if netstat -tuln 2>/dev/null | grep -q ":443 "; then
        echo "   - Port 443: In use (HTTPS)"
    else
        echo "   - Port 443: Available"
    fi
else
    echo "   - Cannot check ports (netstat not available)"
fi

echo
