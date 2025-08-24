# Soulstone

Soulstone is an electronic health record (EHR) system specifically designed for spiritual healers, alternative medicine practitioners, and holistic health providers. It provides a comprehensive platform for managing client records, appointments, billing, and visit notes in a secure, user-friendly interface.

## Features

- **Client Management**: Comprehensive client profiles with contact information and history
- **Visit Notes**: Detailed session documentation with rich text editor support
- **Appointment Scheduling**: Event management and calendar integration
- **Billing System**: Invoice generation, payment tracking, and financial reporting
- **User Management**: Role-based access control for practitioners and support staff
- **Reporting**: Generate various reports for practice management
- **Security**: Secure authentication and data protection

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Docker** (version 20.0 or higher) - [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose** (version 2.0 or higher) - Usually included with Docker Desktop
- **Make** (for easier command execution):
  - [Windows](https://gnuwin32.sourceforge.net/packages/make.htm)
  - [macOS](https://www.freecodecamp.org/news/how-to-download-and-install-xcode/) (via Xcode Command Line Tools)
  - [Linux](https://wiki.gnucash.org/wiki/Install_Build_Tools) (usually pre-installed)

## Quick Start

1. **Clone the repository**

   ```bash
   git clone https://github.com/rodneygauna/soulstone.git
   cd soulstone
   ```

2. **Set up environment variables**

   ```bash
   cp .env.example .env
   ```

   Edit the `.env` file and update the values according to your setup (see [Environment Configuration](#environment-configuration) below).

3. **Validate your setup (recommended)**

   ```bash
   make validate
   ```

   This will check your configuration and dependencies before starting.

4. **Start the application**

   **For development/testing:**

   ```bash
   make dev-up          # Simple development setup (recommended)
   # OR
   make test-env        # Development setup with sample data
   ```

   **For production-like testing:**

   ```bash
   make up              # Full production stack with nginx
   ```

   The development commands will:
   - Build the Docker containers
   - Create the database
   - Start all services (without SSL complexity)
   - Show logs

5. **Access the application**
   - **Development**: `http://localhost:8000` (direct Flask app)
   - **Production**: `http://localhost` (via nginx, may need SSL setup)
   - Use the default support credentials from your `.env` file to log in

## Environment Configuration

Copy `.env.example` to `.env` and configure the following variables:

### Required Configuration

```bash
# Application Security
SECRET_KEY="your-unique-secret-key-here"

# Database Configuration
POSTGRES_USER="soulstone_user"
POSTGRES_PASSWORD="secure_database_password"
POSTGRES_DB="soulstone_db"

# Email Configuration (for notifications and password resets)
MAIL_SERVER="smtp.your-email-provider.com"
MAIL_PORT=587
MAIL_USE_TLS="True"
MAIL_USE_SSL="False"
MAIL_USERNAME="your-email@example.com"
MAIL_PASSWORD="your-email-password"

# Support Account (admin user created on first run)
SUPPORT_EMAIL="admin@your-domain.com"
SUPPORT_PASSWORD="secure_admin_password"

# Practice Configuration (created on first run)
PRACTICE_NAME="Your Practice Name"
PRACTICE_ADDRESS="123 Main Street"
PRACTICE_CITY="Your City"
PRACTICE_STATE="Your State"
PRACTICE_ZIPCODE="12345"
PRACTICE_PHONE="555-123-4567"
PRACTICE_PHONE_TYPE="Office"
```

### Email Configuration Examples

**Gmail:**

```bash
MAIL_SERVER="smtp.gmail.com"
MAIL_PORT=587
MAIL_USE_TLS="True"
MAIL_USE_SSL="False"
MAIL_USERNAME="your-gmail@gmail.com"
MAIL_PASSWORD="your-app-password"
```

**Outlook/Hotmail:**

```bash
MAIL_SERVER="smtp.live.com"
MAIL_PORT=587
MAIL_USE_TLS="True"
MAIL_USE_SSL="False"
```

## Available Commands

### Make Commands

| Command | Description | Environment |
|---------|-------------|-------------|
| `make validate` | **Run first** - Validate your setup and configuration | Any |
| `make status` | Check which environment is currently running | Any |
| `make dev-up` | **Recommended for development** - Start without SSL complexity | Development |
| `make dev-stop` | Stop development environment | Development |
| `make test-env` | Development environment with sample data (⚠️ **resets data**) | Development |
| `make up` | Start production stack with nginx and SSL | Production |
| `make stop` | Stop all running containers | Any |
| `make start` | Start previously stopped containers | Any |
| `make restart` | Stop and restart all services | Any |
| `make logs` | View application logs | Any |
| `make shell` | Access the web container shell for debugging | Any |
| `make clean` | Stop containers and remove volumes (⚠️ **destroys data**) | Any |
| `make init-db` | Initialize database only (useful for custom setups) | Any |

### Database Seeding Commands

| Command | Description |
|---------|-------------|
| `make db_seed_all` | Seed all sample data |
| `make db_seed_practice` | Add sample practice information |
| `make db_seed_users` | Add sample users |
| `make db_seed_people` | Add sample clients |
| `make db_seed_charges` | Add sample billing charges |
| `make db_seed_events` | Add sample appointments |

### Flask CLI Commands (Advanced)

Access these via `make shell` then run:

```bash
flask commands db_create    # Create database tables
flask commands db_seed      # Insert test data
flask commands db_drop      # Drop all database tables
```

## Database Initialization

Soulstone includes improved database initialization with configurable practice settings:

### Automatic Initialization

The database is automatically initialized when you run:

```bash
make test-env    # Creates database + sample data
make up          # Creates database only
make dev-up      # Development mode
```

### Manual Database Setup

For custom setups or troubleshooting:

```bash
# Initialize database with your configured practice information
make init-db

# This will:
# - Validate your .env configuration
# - Create database tables
# - Create your practice with configured details
# - Create the admin user from SUPPORT_EMAIL/SUPPORT_PASSWORD
```

### Practice Configuration

Your practice information is configured via environment variables in `.env`:

```bash
PRACTICE_NAME="Your Practice Name"      # Will appear in the application
PRACTICE_ADDRESS="123 Main Street"     # Practice address
PRACTICE_CITY="Your City"              # City
PRACTICE_STATE="Your State"            # State/Province
PRACTICE_ZIPCODE="12345"               # Postal code
PRACTICE_PHONE="555-123-4567"          # Contact phone
PRACTICE_PHONE_TYPE="Office"           # Phone type (Office/Mobile/Fax)
```

## Development Setup

### Quick Development Start (Recommended)

For local development without SSL complexity:

```bash
# Start development environment (no nginx, no SSL)
make dev-up

# Access the application
# - Application: http://localhost:8000
# - Database: localhost:5432
```

### Alternative Development Options

If you want to test the full production stack locally:

```bash
# Start with production configuration (includes nginx)
make up

# Note: This will try to use SSL certificates, which may cause issues locally
# Better to use make dev-up for local development
```

### Development Workflow

1. **Use the development environment**:

   ```bash
   make dev-up
   ```

2. **Make your changes** to the code

3. **Restart if needed**:

   ```bash
   make dev-stop
   make dev-up
   ```

4. **View logs for debugging**:

   ```bash
   docker compose -f docker-compose.dev.yaml logs -f
   ```

### Development vs Production

| Aspect | Development (`make dev-up`) | Production (`make up`) |
|--------|----------------------------|------------------------|
| **SSL/HTTPS** | ❌ No SSL (HTTP only) | ✅ SSL with certificates |
| **Nginx** | ❌ Direct Flask access | ✅ Nginx reverse proxy |
| **Ports** | 8000 (direct) | 80/443 (via nginx) |
| **Certificates** | ❌ Not needed | ✅ Required (Let's Encrypt) |
| **Restart Policy** | ❌ Manual restart | ✅ Auto-restart |
| **Best For** | Local development | Production deployment |

### Project Structure

```text
soulstone/
├── web/                    # Main Flask application
│   ├── app.py             # Application entry point
│   ├── config.py          # Configuration settings
│   ├── requirements.txt   # Python dependencies
│   ├── billing/           # Billing and invoicing module
│   ├── events/            # Appointment scheduling module
│   ├── persons/           # Client management module
│   ├── users/             # User authentication module
│   ├── visit_notes/       # Session documentation module
│   └── templates/         # HTML templates
├── nginx/                 # Nginx reverse proxy configuration
├── tests/                 # Test files
├── docker-compose.yaml    # Production services (with nginx & SSL)
├── docker-compose.dev.yaml # Development services (simplified)
└── Makefile              # Convenient command shortcuts
```

## Production Deployment

### ⚠️ Important: Development vs Production

- **For development**: Use `make dev-up` (simple, no SSL)
- **For production**: Use `make up` (full stack with nginx and SSL)

### Production Setup Steps

1. **Configure your domain** in `nginx/conf.d/app.conf`:

   ```bash
   # Replace "your-domain.com" with your actual domain
   server_name your-domain.com www.your-domain.com;
   ```

2. **Update SSL certificate paths** in the same file:

   ```bash
   ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
   ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
   ```

3. **Configure SSL certificates** using `init-letsencrypt.sh`:

   ```bash
   # Edit init-letsencrypt.sh and update:
   domains="your-domain.com"
   email="admin@your-domain.com"

   # Then run:
   chmod +x init-letsencrypt.sh
   ./init-letsencrypt.sh
   ```

4. **Use production-grade secrets** in your `.env` file:
   - Strong SECRET_KEY (64+ characters)
   - Secure database passwords
   - Real email configuration

5. **Enable restart policies** by uncommenting in `docker-compose.yaml`:

   ```yaml
   restart: unless-stopped
   ```

6. **Start production environment**:

   ```bash
   make up
   ```

### Production Checklist

- [ ] Domain DNS points to your server
- [ ] `.env` configured with production values
- [ ] `nginx/conf.d/app.conf` updated with your domain
- [ ] SSL certificates generated and working
- [ ] Firewall configured (ports 80, 443, 22)
- [ ] Database backups configured
- [ ] Monitoring setup (optional)

See the [Production Deployment Guide](docs/DEPLOYMENT.md) for detailed instructions.

## Setup Validation

Before running the application, use the built-in validation script to check your configuration:

```bash
make validate
```

This script will check:

- ✅ Required files (`.env`, `docker-compose.yaml`, etc.)
- ✅ Docker installation and status
- ✅ Environment variable configuration
- ✅ Port availability (8000, 5432)
- ⚠️  Common configuration issues

### Example validation output

```text
✅ .env file exists
✅ Docker is running
✅ SECRET_KEY is configured
✅ Database credentials are set
⚠️  Email server not configured (optional for basic functionality)
🎉 All checks passed! Your setup looks good.
```

## Testing

Run the test suite:

```bash
# Run all tests
make shell
pytest

# Run specific test file
pytest tests/test_login.py

# Run with coverage
pytest --cov=web tests/
```

## Troubleshooting

### Development vs Production Issues

**Can't access the application:**

- **Development**: Use `http://localhost:8000` (not https://)
- **Production**: Use `https://your-domain.com` (requires SSL setup)

**SSL certificate errors:**

- **Development**: Use `make dev-up` instead of `make up` to avoid SSL
- **Production**: Ensure certificates are properly generated with `init-letsencrypt.sh`

**Port conflicts:**

- **Development**: Application runs on port 8000
- **Production**: Nginx runs on ports 80/443, application on 8000 internally

### Common Issues

**Port already in use:**

```bash
# Check what's using the port
sudo lsof -i :8000
sudo lsof -i :5432

# Stop conflicting services or change ports in docker-compose.yaml
```

**Database connection errors:**

```bash
# Check if PostgreSQL container is running
docker compose ps

# View database logs
docker compose logs postgres

# Initialize database manually
make init-db

# Reset database (⚠️ destroys data)
make clean
make test-env
```

**Configuration issues:**

```bash
# Validate your setup first
make validate

# Check environment variables
cat .env

# Common issues:
# - Missing required environment variables
# - Using default/example values instead of real ones
# - Incorrect email server settings
```

**Database initialization fails:**

```bash
# Check database initialization logs
make logs

# Common causes:
# - Missing SUPPORT_EMAIL or SUPPORT_PASSWORD
# - Invalid email format
# - Database connection issues

# Manual database initialization with detailed output
make init-db
```

**Email configuration issues:**

- Verify SMTP settings with your email provider
- For Gmail, use App Passwords instead of your regular password
- Check firewall settings for outbound SMTP connections

**Permission issues:**

```bash
# Fix file permissions
sudo chown -R $USER:$USER .
```

### Getting Help

- **First step**: Run `make validate` to check your configuration
- Check the application logs: `make logs`
- Access container shell for debugging: `make shell`
- Review Docker container status: `docker compose ps`
- Initialize database manually: `make init-db`

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on:

- Setting up the development environment
- Code style and standards
- Submitting pull requests
- Reporting issues

## License

This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0). See the [LICENSE](LICENSE) file for details.

## Support

- **Documentation**: Check this README and the docs/ directory
- **Issues**: Report bugs or request features via [GitHub Issues](https://github.com/rodneygauna/soulstone/issues)
- **Discussions**: Join conversations in [GitHub Discussions](https://github.com/rodneygauna/soulstone/discussions)

## Acknowledgments

- Built with Flask, PostgreSQL, and Docker
- UI components from various open-source libraries
- Special thanks to the spiritual healing and alternative medicine community
