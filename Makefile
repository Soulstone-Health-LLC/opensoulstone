# Makefile
.PHONY: build run up stop clean logs shell db_seed_all test-env restart dev-up dev-stop login-soulstone init-db validate status health-check

# Docker-related variables
DOCKER_COMPOSE = docker compose
DOCKER_COMPOSE_DEV = docker compose -f docker-compose.dev.yaml

# Setup validation and health checks
validate:
	./validate-setup.sh

health-check:
	./health-check.sh

# Environment status
status:
	./check-environment.sh

# Database initialization
init-db:
	./init-db.sh

# Build the Docker image
build:
	$(DOCKER_COMPOSE) build

# Development commands (no SSL, simplified setup)
dev-up:
	$(DOCKER_COMPOSE_DEV) up --build

dev-stop:
	$(DOCKER_COMPOSE_DEV) down

# Production commands (with nginx and SSL)
# Run the Docker container
run:
	$(DOCKER_COMPOSE) up

# Build and run the Docker container
up:
	$(DOCKER_COMPOSE) up --build -d

# Stop and remove the Docker container
stop:
	$(DOCKER_COMPOSE) down

# Clean up Docker images and volumes
clean:
	$(DOCKER_COMPOSE) down -v

# View the logs
logs:
	$(DOCKER_COMPOSE) logs --tail=100 -f

# Container shell
shell:
	$(DOCKER_COMPOSE) exec web sh

# Legacy alias for shell command
login-soulstone: shell

# Seed the database with test data
db_seed_practice:
	$(DOCKER_COMPOSE) exec web flask commands db_seed_practice

db_seed_users:
	$(DOCKER_COMPOSE) exec web flask commands db_seed_users

db_seed_people:
	$(DOCKER_COMPOSE) exec web flask commands db_seed_people

db_seed_charges:
	$(DOCKER_COMPOSE) exec web flask commands db_seed_charges

db_seed_ledger_charges:
	$(DOCKER_COMPOSE) exec web flask commands db_seed_ledger_charges

db_seed_ledger_payments:
	$(DOCKER_COMPOSE) exec web flask commands db_seed_ledger_payments

db_seed_event_types:
	$(DOCKER_COMPOSE) exec web flask commands db_seed_event_types

db_seed_events:
	$(DOCKER_COMPOSE) exec web flask commands db_seed_events

db_seed_visit_notes:
	$(DOCKER_COMPOSE) exec web flask commands db_seed_visit_notes

db_seed_release_notes:
	$(DOCKER_COMPOSE) exec web flask commands db_seed_release_notes

db_seed_terms_of_service:
	$(DOCKER_COMPOSE) exec web flask commands db_seed_terms_of_service

db_seed_all: db_seed_practice db_seed_users db_seed_people db_seed_charges db_seed_ledger_charges db_seed_ledger_payments db_seed_event_types db_seed_events db_seed_visit_notes db_seed_release_notes db_seed_terms_of_service

# Test environment
test-env: clean up db_seed_all logs

# Quick restrat
restart: stop up logs
