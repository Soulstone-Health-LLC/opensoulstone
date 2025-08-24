# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Comprehensive setup validation script (`make validate`)
- Configurable practice information via environment variables
- Enhanced database initialization with better error handling and logging
- Development Docker Compose configuration for easier local development
- Automated database initialization script (`make init-db`)
- Generic configuration templates removing hardcoded personal information
- Comprehensive documentation in README.md
- Contributing guidelines (CONTRIBUTING.md)
- AGPL-3.0 license
- Setup validation and troubleshooting tools

### Changed

- Removed hardcoded personal information from all configuration files
- Updated database initialization to use environment-based configuration
- Enhanced error handling and user feedback throughout setup process
- Improved Makefile with development and validation commands
- Updated HTML meta tags to be generic and professional

### Fixed

- Domain-specific configuration now uses environment variables
- SSL certificate paths now configurable for different domains
- Email configuration examples updated to be more generic

### Security

- Removed hardcoded passwords and personal information
- Added secure configuration examples and validation

## [1.0.0] - Initial Release

### Added

- Electronic Health Record (EHR) system for spiritual healers
- Client management with comprehensive profiles
- Visit notes with rich text editor support
- Appointment scheduling and calendar integration
- Billing system with invoice generation and payment tracking
- User management with role-based access control
- Reporting capabilities for practice management
- Docker-based deployment with PostgreSQL database
- Nginx reverse proxy with SSL support
- Email notifications and password reset functionality
- Test data seeding for development and testing

### Features

- **Client Management**: Store and manage client contact information and history
- **Visit Notes**: Document sessions with rich formatting options
- **Billing**: Generate invoices, track payments, and manage finances
- **Scheduling**: Manage appointments and events
- **Security**: Secure authentication and data protection
- **Multi-user**: Support for multiple practitioners and staff
- **Responsive UI**: Works on desktop and mobile devices

---

## Release Notes

### How to Upgrade

When upgrading between versions:

1. **Backup your data**:

   ```bash
   # Backup database
   docker compose exec postgres pg_dump -U $POSTGRES_USER $POSTGRES_DB > backup.sql

   # Backup uploaded files
   docker compose cp web:/app/static/profile_pics ./profile_pics_backup
   ```

2. **Update the code**:

   ```bash
   git pull origin main
   ```

3. **Update environment configuration** (if needed):

   ```bash
   # Compare your .env with the new .env.example
   diff .env .env.example
   ```

4. **Restart services**:

   ```bash
   make restart
   ```

5. **Run database migrations** (if any):

   ```bash
   make shell
   # Run any migration commands if provided in release notes
   ```

### Migration Notes

- **To v1.0.0**: Initial release, no migration needed
- **To Unreleased**:
  - Update `.env` file with new practice configuration variables
  - Run `make validate` to check your setup
  - Consider using `make dev-up` for local development

---

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the GNU Affero General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
