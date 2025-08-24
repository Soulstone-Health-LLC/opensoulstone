#!/bin/bash

# Configuration validation script
# Helps users verify their setup before running the application

echo "======================================"
echo "  Soulstone Setup Validation"
echo "======================================"
echo

ERRORS=0
WARNINGS=0

# Function to report errors
report_error() {
    echo "❌ ERROR: $1"
    ERRORS=$((ERRORS + 1))
}

# Function to report warnings
report_warning() {
    echo "⚠️  WARNING: $1"
    WARNINGS=$((WARNINGS + 1))
}

# Function to report success
report_success() {
    echo "✅ $1"
}

# Check for required files
echo "Checking required files..."

if [ -f .env ]; then
    report_success ".env file exists"
else
    report_error ".env file not found. Copy .env.example to .env and configure it."
fi

if [ -f docker-compose.yaml ]; then
    report_success "docker-compose.yaml exists"
else
    report_error "docker-compose.yaml not found"
fi

if [ -f web/requirements.txt ]; then
    report_success "requirements.txt exists"
else
    report_error "web/requirements.txt not found"
fi

echo

# Check Docker
echo "Checking Docker..."

if command -v docker >/dev/null 2>&1; then
    report_success "Docker is installed"

    if docker info >/dev/null 2>&1; then
        report_success "Docker is running"
    else
        report_error "Docker is installed but not running. Please start Docker."
    fi
else
    report_error "Docker is not installed. Please install Docker first."
fi

if command -v "docker compose" >/dev/null 2>&1 || command -v docker-compose >/dev/null 2>&1; then
    report_success "Docker Compose is available"
else
    report_error "Docker Compose is not available. Please install Docker Compose."
fi

echo

# Check environment variables
echo "Checking environment configuration..."

if [ -f .env ]; then
    # Source the .env file
    set -a
    source .env
    set +a

    # Check required variables
    if [ -n "$SECRET_KEY" ] && [ "$SECRET_KEY" != "your-unique-secret-key-replace-this-with-64-character-random-string" ]; then
        report_success "SECRET_KEY is configured"
    else
        report_error "SECRET_KEY is not properly configured. Please set a unique secret key."
    fi

    if [ -n "$POSTGRES_USER" ]; then
        report_success "POSTGRES_USER is set"
    else
        report_error "POSTGRES_USER is not set"
    fi

    if [ -n "$POSTGRES_PASSWORD" ] && [ "$POSTGRES_PASSWORD" != "your-secure-database-password-here" ]; then
        report_success "POSTGRES_PASSWORD is configured"
    else
        report_error "POSTGRES_PASSWORD is not properly configured"
    fi

    if [ -n "$SUPPORT_EMAIL" ] && [ "$SUPPORT_EMAIL" != "admin@your-domain.com" ]; then
        report_success "SUPPORT_EMAIL is configured"
    else
        report_error "SUPPORT_EMAIL is not properly configured"
    fi

    if [ -n "$SUPPORT_PASSWORD" ] && [ "$SUPPORT_PASSWORD" != "your-secure-admin-password" ]; then
        report_success "SUPPORT_PASSWORD is configured"
    else
        report_error "SUPPORT_PASSWORD is not properly configured"
    fi

    # Check email configuration
    if [ -n "$MAIL_SERVER" ] && [ "$MAIL_SERVER" != "smtp.your-email-provider.com" ]; then
        report_success "Email server is configured"

        if [ -n "$MAIL_USERNAME" ] && [ "$MAIL_USERNAME" != "your-email@example.com" ]; then
            report_success "Email username is configured"
        else
            report_warning "Email username should be configured for full functionality"
        fi
    else
        report_warning "Email server not configured. Password resets and notifications will not work."
    fi

    # Check practice configuration
    if [ -n "$PRACTICE_NAME" ] && [ "$PRACTICE_NAME" != "Your Practice Name" ]; then
        report_success "Practice name is configured"
    else
        report_warning "Practice name not customized (will use default)"
    fi
fi

echo

# Check port availability
echo "Checking port availability..."

if command -v netstat >/dev/null 2>&1; then
    if netstat -tuln | grep -q ":8000 "; then
        report_warning "Port 8000 is already in use. You may need to stop other services."
    else
        report_success "Port 8000 is available"
    fi

    if netstat -tuln | grep -q ":5432 "; then
        report_warning "Port 5432 is already in use. You may need to stop other PostgreSQL services."
    else
        report_success "Port 5432 is available"
    fi
else
    report_warning "Cannot check port availability (netstat not available)"
fi

echo

# Summary
echo "======================================"
echo "         Validation Summary"
echo "======================================"

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo "🎉 All checks passed! Your setup looks good."
    echo
    echo "You can now run:"
    echo "  make dev-up      # For development"
    echo "  make test-env    # For testing with sample data"
    echo "  make init-db     # To initialize database only"
elif [ $ERRORS -eq 0 ]; then
    echo "✅ No critical errors found, but there are $WARNINGS warning(s)."
    echo "You can proceed, but consider addressing the warnings for full functionality."
else
    echo "❌ Found $ERRORS error(s) and $WARNINGS warning(s)."
    echo "Please fix the errors before proceeding."
    exit 1
fi

echo
