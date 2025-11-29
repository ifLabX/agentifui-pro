# API Contracts

**Feature**: 003-api-uv-run

This is a refactoring task. No new API contracts are introduced.

## Existing Endpoints (Unchanged)

All endpoints maintain backward compatibility:

- `GET /` - Root endpoint
- `GET /health` - Basic health check
- `GET /health/db` - Database health check

## Contract Modifications

None. This task focuses on internal improvements:

- Pydantic v2 migration
- Test fixes
- Error handling improvements
- Dead code removal

All external API contracts remain stable.
