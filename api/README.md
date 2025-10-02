# FastAPI Backend Architecture Foundation

A modern, async FastAPI backend with PostgreSQL, SQLAlchemy 2.0, and Alembic migrations. Built for production with comprehensive health monitoring, structured error handling, and development-first experience.

## Features

- **Async Architecture**: FastAPI with SQLAlchemy 2.0 async engine and asyncpg driver
- **Type Safety**: Full Pydantic v2 integration with comprehensive validation
- **Health Monitoring**: Application and database health endpoints with metrics
- **Error Handling**: Structured error responses with request tracing
- **Database Ready**: PostgreSQL with connection pooling and migration framework
- **Production Ready**: Secret validation, logging, CORS, and container support
- **Developer Experience**: Hot reload, comprehensive tests, pre-commit hooks

## Prerequisites

- **Python**: 3.12 or higher
- **Package Manager**: [uv](https://docs.astral.sh/uv/) (modern Python package manager)
- **Database**: PostgreSQL 12+ (optional for development)
- **Tools**: Git, make (optional)

## Quick Setup

### 1. Clone and Install Dependencies

```bash
# Clone the repository
git clone <repository-url>
cd agentifui-pro

# Install dependencies using uv
uv sync

# Copy environment template
cp .env.example .env
```

### 2. Configure Environment

Edit `.env` with your settings:

```bash
# Application Configuration
APP_NAME="AgentifUI Pro API"
APP_VERSION="0.1.0"
DEBUG=true
ENVIRONMENT=development

# Database Configuration
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/agentifui_dev
DATABASE_POOL_SIZE=10
DATABASE_POOL_TIMEOUT=30

# Security
SECRET_KEY=your-secret-key-here-min-32-chars

# Logging
LOG_LEVEL=INFO
LOG_FORMAT="%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# CORS (for frontend integration)
CORS_ORIGINS=["http://localhost:3000"]

# Health Check Configuration
HEALTH_CHECK_TIMEOUT=5
DATABASE_HEALTH_CHECK_TIMEOUT=10
```

### 3. Run the Application

```bash
# Development server with hot reload (from api/ directory)
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# Or from project root
uv run --project api uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:
- **Application**: http://localhost:8000
- **Health Check**: http://localhost:8000/health
- **Database Health**: http://localhost:8000/health/db
- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc (ReDoc)

## Running Tests

```bash
# Run all tests (from api/ directory)
uv run pytest

# From project root
uv run --project api pytest

# Run with coverage
uv run pytest --cov=. --cov-report=html

# Run specific test categories
uv run pytest tests/test_health_endpoint.py
uv run pytest tests/test_performance.py
uv run pytest -k "health"

# Run tests in parallel (faster)
uv run pytest -n auto
```

## Development Workflow

### Code Quality

```bash
# Format code (from api/ directory)
uv run ruff format

# Lint code
uv run ruff check

# Fix linting issues
uv run ruff check --fix

# Type checking (if mypy is configured)
uv run mypy .
```

### Database Operations

```bash
# Create a new migration (from api/ directory)
uv run alembic revision --autogenerate -m "Description"

# Apply migrations
uv run alembic upgrade head

# Rollback migration
uv run alembic downgrade -1

# Show migration history
uv run alembic history
```

### Pre-commit Hooks

The project includes pre-commit hooks that automatically run linting and formatting:

```bash
# Install pre-commit hooks (already configured)
pre-commit install

# Run manually
pre-commit run --all-files
```

## API Endpoints

### Health Monitoring

#### `GET /health`
Basic application health check.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2025-09-23T10:30:00Z",
  "version": "0.1.0",
  "uptime_seconds": 3600
}
```

**Response (503 Service Unavailable):**
```json
{
  "status": "unhealthy",
  "timestamp": "2025-09-23T10:30:00Z",
  "version": "0.1.0",
  "errors": ["Service temporarily unavailable"]
}
```

#### `GET /health/db`
Database connectivity and health check.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2025-09-23T10:30:00Z",
  "database_connected": true,
  "response_time_ms": 15,
  "connection_pool": {
    "active_connections": 2,
    "pool_size": 10
  },
  "migration_status": "up_to_date"
}
```

**Response (503 Service Unavailable):**
```json
{
  "status": "unhealthy",
  "timestamp": "2025-09-23T10:30:00Z",
  "database_connected": false,
  "errors": ["Database connection failed"]
}
```

### Error Responses

All endpoints return structured error responses:

```json
{
  "error": "VALIDATION_ERROR",
  "message": "Request validation failed",
  "timestamp": "2025-09-23T10:30:00Z",
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "detail": "Additional error context (debug mode only)"
}
```

## Architecture Overview

### Project Structure

```
api/
  src/              # Application source code
    config/         # Configuration management
      settings.py   # Pydantic Settings with validation
      logging.py    # Structured logging setup

    database/       # Database layer
      connection.py # Async engine and connection factory
      session.py    # Session management and dependency injection
      health.py     # Database health monitoring utilities

    health/         # Health monitoring
      endpoints.py  # Health check endpoints
      models.py     # Health response models

    middleware/     # HTTP middleware
      error_handler.py # Global error handling

    models/         # Data models
      base.py       # Base model with UUID support
      errors.py     # Error response models

    main.py         # FastAPI application entry point

  migrations/       # Alembic migration files
    env.py          # Async migration environment
    script.py.mako  # Migration template

  tests/            # Test suite
    test_*.py       # Test modules
    conftest.py     # Test fixtures and configuration

  .env.example      # Environment template
  pyproject.toml    # Dependencies and project config
```


### Key Components

**Configuration Management**
- Environment-based configuration with Pydantic v2 Settings
- Production secret key validation
- Type-safe configuration with validation

**Database Layer**
- SQLAlchemy 2.0 with async engine and asyncpg driver
- Connection pooling with health monitoring
- Session-per-request pattern with dependency injection
- Alembic migrations with async support

**Health Monitoring**
- Application health endpoint with uptime tracking
- Database health with connection pool metrics
- Structured error responses following OpenAPI contracts

**Error Handling**
- Global error handling middleware
- Standardized error response format
- Request ID tracking for debugging
- Production-safe error messages

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `APP_NAME` | Application name | "AgentifUI Pro API" | No |
| `APP_VERSION` | Application version | "0.1.0" | No |
| `DEBUG` | Debug mode | false | No |
| `ENVIRONMENT` | Environment (development/staging/production) | development | No |
| `DATABASE_URL` | PostgreSQL connection URL | - | Yes |
| `DATABASE_POOL_SIZE` | Connection pool size | 10 | No |
| `DATABASE_POOL_TIMEOUT` | Pool timeout in seconds | 30 | No |
| `SECRET_KEY` | Application secret key | - | Yes |
| `LOG_LEVEL` | Logging level | INFO | No |
| `LOG_FORMAT` | Log format string | Standard format | No |
| `CORS_ORIGINS` | Allowed CORS origins | ["http://localhost:3000"] | No |
| `HEALTH_CHECK_TIMEOUT` | Health check timeout | 5 | No |
| `DATABASE_HEALTH_CHECK_TIMEOUT` | DB health timeout | 10 | No |

### Production Configuration

For production deployment:

1. **Set secure secret key**: Minimum 32 characters, cryptographically random
2. **Configure database**: Use connection pooling and SSL
3. **Enable structured logging**: JSON format with log aggregation
4. **Set CORS origins**: Restrict to your frontend domains
5. **Use environment variables**: Never hardcode secrets

```bash
# Production example
ENVIRONMENT=production
SECRET_KEY=your-very-secure-secret-key-minimum-32-characters
DATABASE_URL=postgresql+asyncpg://user:pass@db.example.com:5432/db?sslmode=require
CORS_ORIGINS=["https://app.example.com"]
LOG_LEVEL=INFO
```

## Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

# Copy application code
COPY . .

EXPOSE 8000

# Run with uvicorn
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Monitoring and Observability

### Health Check Integration

The health endpoints are designed for:
- **Load balancers**: Use `/health` for basic availability
- **Container orchestration**: Kubernetes readiness/liveness probes
- **Monitoring systems**: Prometheus, DataDog, New Relic integration
- **APM tools**: Request tracing with request IDs

### Logging

Structured logging with:
- JSON format in production for log aggregation
- Request ID tracking for distributed tracing
- Configurable log levels per environment
- Health check noise filtering in production

### Performance Monitoring

Built-in performance tracking:
- Response time measurement for database health checks
- Connection pool monitoring
- Performance tests ensuring <200ms health check responses
- Memory usage monitoring during load testing

## Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes following the coding standards
4. Run tests: `uv run --project api pytest`
5. Run linting: `uv run --project api ruff check api/`
6. Commit your changes: `git commit -m "feat: add your feature"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a Pull Request

### Coding Standards

- **Code formatting**: Use Ruff for formatting and linting
- **Type hints**: Required for all function signatures
- **Documentation**: Docstrings for all public functions and classes
- **Testing**: Comprehensive test coverage for new features
- **Commit messages**: Follow conventional commit format

### Project Guidelines

- **No business logic**: This is a foundation layer only
- **Environment configuration**: All settings via environment variables
- **Database agnostic**: Prepare for PostgreSQL UUIDv7 but maintain compatibility
- **Production ready**: Security, monitoring, and error handling first
- **Developer experience**: Hot reload, comprehensive tests, clear documentation

## License

This project is licensed under the terms specified in the root LICENSE file.

## Troubleshooting

### Common Issues

**Database Connection Failed**
```bash
# Check database is running
pg_isready -h localhost -p 5432

# Verify connection string
echo $DATABASE_URL

# Test connection
uv run --project api python -c "from database.connection import get_async_engine; print('Database connection OK')"
```

**Import Errors**
```bash
# Reinstall dependencies
uv sync --project api

# Check Python version
python --version  # Should be 3.12+
```

**Tests Failing**
```bash
# Run specific failing test with verbose output
uv run --project api pytest tests/test_health_endpoint.py -v

# Check test database configuration
uv run --project api pytest tests/ --tb=short
```

**Performance Issues**
```bash
# Run performance tests
uv run --project api pytest tests/test_performance.py

# Check connection pool settings
grep -r "DATABASE_POOL" api/.env
```

For additional support, check the project documentation or create an issue in the repository.
