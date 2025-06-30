# LinkOps Database Microservice

This service provides the persistent memory layer for Orbs, Runes, logs, approvals, and agent capabilities.

- **PostgreSQL 15**
- Tables: orbs, runes, logs, approvals, capabilities
- Use with Docker, GCP, or local setup

## Usage
- Add to `docker-compose.yml` as the `db` service
- Use `shared/db.py` for Python access

## Environment Variables
- `POSTGRES_USER=linkops`
- `POSTGRES_PASSWORD=secret`
- `POSTGRES_DB=linkops_core`

## Initialization
- Schema is created from `init.sql` on first run 