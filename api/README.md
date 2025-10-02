# FastAPI Backend - Agentifui Pro

Modern async FastAPI backend with PostgreSQL 18, SQLAlchemy 2.0, and Alembic migrations.

## Prerequisites

- **Python**: 3.12+
- **uv**: [Install uv](https://docs.astral.sh/uv/)
- **PostgreSQL**: 18+ (required for native `uuidv7()` support)

```bash
# Install PostgreSQL 18
brew install postgresql@18
brew services start postgresql@18
```

## Quick Start

```bash
# 1. Install dependencies
uv sync

# 2. Configure environment
cp .env.example .env
# Edit .env with your settings

# 3. Setup database
createdb agentifui_pro
uv run alembic upgrade head

# 4. Run server
uv run uvicorn src.main:app --reload
```

Server runs at http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health
- DB Health: http://localhost:8000/health/db

## Development

### Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov

# Run specific tests
uv run pytest tests/test_health_endpoint.py
uv run pytest -k "health"
```

### Code Quality

```bash
# Format and lint
uv run ruff format
uv run ruff check --fix
```

### Database Migrations

```bash
# Create migration from model changes
uv run alembic revision --autogenerate -m "description"

# Apply migrations
uv run alembic upgrade head

# Rollback one version
uv run alembic downgrade -1

# View history
uv run alembic history
```

**Migration Best Practices**:
- Always review auto-generated migrations before applying
- Test on copy of production data
- Never edit applied migrations

## Configuration

Key environment variables in `.env`:

```bash
# Database (PostgreSQL 18+ required)
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/agentifui_pro

# Application
DEBUG=true
ENVIRONMENT=development

# CORS
CORS_ORIGINS=["http://localhost:3000"]
```

## Project Structure

```
api/
  src/
    config/         # Settings and configuration
    database/       # Connection, sessions, health
    health/         # Health endpoints
    models/         # SQLAlchemy models (Base uses uuidv7)
    middleware/     # Error handling
    main.py         # FastAPI app entry
  migrations/       # Alembic migrations
  tests/            # Test suite
```

## Features

- **Async Architecture**: FastAPI + SQLAlchemy 2.0 + asyncpg
- **Type Safety**: Pydantic v2 with full validation
- **UUIDv7 PKs**: PostgreSQL 18 native time-ordered UUIDs
- **Health Monitoring**: App and database health endpoints
- **Error Handling**: Structured responses with request tracing
- **Test Coverage**: 106 tests passing (97% coverage)

## UUIDv7 Primary Keys

All models inherit from `Base` which uses PostgreSQL 18's `uuidv7()`:

```python
from models.base import Base

class User(Base):
    __tablename__ = "users"
    # id column auto-generated with uuidv7()
```

Benefits:
- **Time-ordered**: Better index performance
- **Sortable**: Natural chronological ordering
- **Native**: Database-side generation
- **Unique**: Globally unique identifiers

## Troubleshooting

**Database connection failed**
```bash
# Check PostgreSQL version
psql --version  # Must be 18+

# Test uuidv7() function
psql agentifui_pro -c "SELECT uuidv7();"

# Verify connection
uv run alembic upgrade head
curl http://localhost:8000/health/db
```

**Tests failing**
```bash
# Clear caches
uv sync

# Run with verbose output
uv run pytest -vv --tb=short
```

## Production Deployment

```dockerfile
FROM python:3.12-slim
WORKDIR /app
RUN pip install uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen
COPY . .
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0"]
```

**Production checklist**:
- Configure DATABASE_URL with SSL
- Set `ENVIRONMENT=production`
- Restrict `CORS_ORIGINS`
- Use `LOG_LEVEL=INFO`

## Contributing

1. Create feature branch
2. Make changes following code standards
3. Run tests: `uv run pytest`
4. Run linting: `uv run ruff check`
5. Commit: `git commit -m "feat: description"`
6. Create PR

See [CLAUDE.md](../CLAUDE.md) for detailed coding standards and conventions.


