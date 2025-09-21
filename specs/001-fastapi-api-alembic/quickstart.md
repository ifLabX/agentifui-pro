# Quickstart: Backend Foundation

## Prerequisites
- Python 3.12+
- PostgreSQL database
- uv package manager

## Setup Steps

1. **Install dependencies**:
   ```bash
   uv sync --project api
   ```

2. **Configure environment**:
   ```bash
   cp api/.env.example api/.env
   # Edit api/.env with your database credentials
   ```

3. **Initialize database**:
   ```bash
   cd api
   uv run alembic upgrade head
   ```

4. **Start development server**:
   ```bash
   uv run --project api dev
   ```

## Verification Tests

### Test 1: Basic Health Check
```bash
curl http://localhost:8000/health
```
**Expected Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-01-21T10:00:00Z"
}
```

### Test 2: Readiness Check
```bash
curl http://localhost:8000/health/ready
```
**Expected Response**:
```json
{
  "status": "ready",
  "database": "connected",
  "timestamp": "2025-01-21T10:00:00Z"
}
```

### Test 3: Application Info
```bash
curl http://localhost:8000/info
```
**Expected Response**:
```json
{
  "name": "AgentifUI-Pro Backend",
  "version": "1.0.0",
  "environment": "development",
  "python_version": "3.12.x",
  "fastapi_version": "0.x.x"
}
```

### Test 4: Code Quality
```bash
# Lint check
uv run --project api ruff check api/

# Format check
uv run --project api ruff format --check api/

# Type check (if configured)
uv run --project api mypy api/
```

### Test 5: Database Migration
```bash
# Generate a test migration
cd api
uv run alembic revision --autogenerate -m "test_migration"

# Apply migration
uv run alembic upgrade head

# Verify migration
uv run alembic current
```

## Success Criteria
✅ All API endpoints return expected responses
✅ Database connection is successful
✅ Code quality tools pass without errors
✅ Development server starts without errors
✅ Alembic migrations work correctly

## Troubleshooting

**Database connection fails**:
- Verify PostgreSQL is running
- Check credentials in .env file
- Ensure database exists

**Import errors**:
- Run `uv sync --project api` to install dependencies
- Verify Python version is 3.12+

**CORS errors from frontend**:
- Verify CORS_ORIGINS includes http://localhost:3000
- Check that frontend is running on port 3000