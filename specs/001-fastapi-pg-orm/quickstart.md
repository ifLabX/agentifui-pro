# Quickstart Guide: FastAPI Backend Architecture Foundation

**Version**: 0.1.0
**Date**: 2025-09-23
**Prerequisites**: PostgreSQL database, Python 3.12+, uv package manager

## Quick Setup (5 minutes)

### 1. Environment Setup
```bash
# Navigate to project root
cd /path/to/agentifui-pro

# Verify Python version
python --version  # Should be 3.12+

# Install dependencies (automatically handled by uv)
cd api
uv sync
```

### 2. Database Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your PostgreSQL settings
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/agentifui_dev
DATABASE_POOL_SIZE=10
DATABASE_POOL_TIMEOUT=30
LOG_LEVEL=INFO
```

### 3. Database Initialization
```bash
# Initialize Alembic migration framework
uv run alembic init alembic

# Run initial migration (creates schema)
uv run alembic upgrade head
```

### 4. Start Application
```bash
# Start development server
uv run dev

# Verify startup in logs:
# INFO: Application startup complete
# INFO: Uvicorn running on http://0.0.0.0:8000
```

## Verification Tests (2 minutes)

### Health Check Validation
```bash
# Test application health
curl http://localhost:8000/health
# Expected: {"status": "healthy", "timestamp": "...", "version": "0.1.0"}

# Test database health
curl http://localhost:8000/health/db
# Expected: {"status": "healthy", "database_connected": true, ...}
```

### Database Connection Test
```bash
# Test database connectivity
uv run python -c "
from database.connection import get_async_engine
import asyncio

async def test_db():
    engine = get_async_engine()
    async with engine.connect() as conn:
        result = await conn.execute('SELECT 1 as test')
        print(f'Database test: {result.scalar()}')
    await engine.dispose()

asyncio.run(test_db())
"
# Expected: Database test: 1
```

## Development Workflow

### Daily Development
```bash
# Start development server with auto-reload
uv run dev

# Run tests
uv run pytest

# Check code quality
uv run ruff check api/
uv run ruff format api/
```

### Database Changes
```bash
# Create new migration
uv run alembic revision --autogenerate -m "descriptive message"

# Review generated migration in alembic/versions/

# Apply migration
uv run alembic upgrade head

# Check migration status
uv run alembic current
```

### Adding Dependencies
```bash
# Add runtime dependency
uv add "new-package>=1.0.0"

# Add development dependency
uv add --dev "dev-package>=1.0.0"

# Update lockfile
uv lock
```

## Testing Scenarios

### Scenario 1: Fresh Developer Setup
**Given**: New developer with clean environment
**When**: Following quickstart steps 1-4
**Then**: Application starts successfully and health checks pass
**Validation**:
- [ ] Python 3.12+ available
- [ ] uv package manager installed
- [ ] PostgreSQL accessible with provided credentials
- [ ] Health endpoints return 200 status
- [ ] Database migrations complete successfully

### Scenario 2: Database Connection Failure
**Given**: Application configured with invalid database credentials
**When**: Starting the application
**Then**: Application starts but health checks report database issues
**Validation**:
- [ ] Application health endpoint returns 503
- [ ] Database health endpoint returns 503 with connection error
- [ ] Error logs clearly indicate database connection failure
- [ ] Application remains responsive for non-database operations

### Scenario 3: Migration Scenario
**Given**: Existing database with migrations applied
**When**: New migration is created and applied
**Then**: Database schema updates without data loss
**Validation**:
- [ ] `alembic current` shows latest migration
- [ ] Database schema reflects changes
- [ ] Existing data remains intact
- [ ] Application continues to function normally

## Troubleshooting

### Common Issues

#### Database Connection Failed
```bash
# Check PostgreSQL service
systemctl status postgresql  # Linux
brew services list | grep postgresql  # macOS

# Test direct connection
psql -h localhost -U username -d database_name

# Verify environment variables
echo $DATABASE_URL
```

#### Migration Errors
```bash
# Check current migration status
uv run alembic current

# View migration history
uv run alembic history

# Reset to specific revision (CAUTION: data loss risk)
uv run alembic downgrade <revision_id>
```

#### Import Errors
```bash
# Verify Python path
uv run python -c "import sys; print('\n'.join(sys.path))"

# Check module imports
uv run python -c "from database import connection"
```

### Performance Validation

#### Connection Pool Testing
```bash
# Test connection pool under load
uv run python scripts/test_connection_pool.py
# Expected: All connections successful, no timeouts

# Monitor active connections
psql -d database_name -c "SELECT count(*) FROM pg_stat_activity WHERE usename='username';"
```

#### Response Time Testing
```bash
# Test health endpoint response time
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/health
# Expected: total_time < 0.200 (200ms)

# Test database health response time
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/health/db
# Expected: total_time < 0.500 (500ms)
```

## Success Criteria

### Foundation Ready ✅
- [x] FastAPI application starts without errors
- [x] PostgreSQL connection established and tested
- [x] SQLAlchemy async ORM configured and functional
- [x] Alembic migrations initialize and run successfully
- [x] Health check endpoints respond correctly
- [x] Environment configuration loads and validates
- [x] Logging configured for development and debugging
- [x] Code quality tools (Ruff) pass without warnings

### Development Ready ✅
- [x] Auto-reload development server functional
- [x] Database schema versioning with Alembic
- [x] Test infrastructure configured and passing
- [x] Error handling for database connection failures
- [x] Performance monitoring via health endpoints

### Future Ready ✅
- [x] Architecture supports Row Level Security (RLS) addition
- [x] Database design accommodates PostgreSQL 18 UUIDv7 migration
- [x] Async patterns established for scalable development
- [x] Configuration management supports multiple environments

## Next Steps

After completing quickstart validation:

1. **Business Logic Development**: Add feature-specific models and endpoints
2. **Authentication Integration**: Implement user management and security
3. **Testing Enhancement**: Add comprehensive test coverage
4. **Production Configuration**: Environment-specific optimizations
5. **Monitoring & Observability**: Enhanced logging and metrics
6. **PostgreSQL 18 Migration**: Upgrade to UUIDv7 when stable
7. **RLS Implementation**: Add row-level security policies

## Support

### Documentation
- [SQLAlchemy 2.0 Async Documentation](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Alembic Migration Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [FastAPI Database Integration](https://fastapi.tiangolo.com/tutorial/sql-databases/)

### Internal References
- `api/config/settings.py` - Configuration management
- `api/database/connection.py` - Database connection setup
- `api/alembic/env.py` - Migration environment configuration
- `api/tests/conftest.py` - Test configuration and fixtures