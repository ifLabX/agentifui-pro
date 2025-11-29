# Data Model: FastAPI Backend Architecture Foundation

**Date**: 2025-09-23
**Phase**: Phase 1 Design
**Prerequisites**: research.md complete

## Core Entities

### 1. Database Connection

**Purpose**: Manages PostgreSQL connection pool and session lifecycle
**Scope**: Application-wide database connectivity

**Key Attributes**:

- Connection pool configuration (min/max connections, timeout settings)
- Database URL and authentication credentials
- Connection health status and retry logic
- Session factory for request-scoped database access

**Relationships**:

- Provides sessions to all application components
- Monitored by Health Status entity
- Configured by Application Configuration entity

**Validation Rules**:

- Database URL must be valid PostgreSQL connection string
- Connection pool settings must be within reasonable limits
- Authentication credentials required for non-development environments

### 2. Migration State

**Purpose**: Tracks database schema versions and migration history via Alembic
**Scope**: Database schema evolution and deployment

**Key Attributes**:

- Current schema version identifier
- Migration history and applied changes
- Migration script metadata and checksums
- Rollback capability and dependency tracking

**Relationships**:

- Managed by Alembic migration framework
- Reflects current state of Database Connection schema
- Validates against Application Configuration environment

**Validation Rules**:

- Schema version must match deployed migration files
- Migration dependencies must be satisfied in order
- Rollback operations must maintain data integrity

### 3. Application Configuration

**Purpose**: Manages environment variables and application settings
**Scope**: Runtime configuration and environment-specific behavior

**Key Attributes**:

- Database connection parameters (host, port, database name)
- Authentication and security settings
- Logging levels and output configuration
- Performance tuning parameters (connection pool, timeouts)
- Feature flags for PostgreSQL version-specific features

**Relationships**:

- Configures Database Connection parameters
- Influences Migration State environment settings
- Provides settings for Health Status monitoring

**Validation Rules**:

- Required environment variables must be present
- Database credentials must be valid for target environment
- Numeric settings must be within acceptable ranges
- Security settings must meet minimum requirements

### 4. Health Status

**Purpose**: Monitors application and database connectivity for operational visibility
**Scope**: System monitoring and diagnostic information

**Key Attributes**:

- Application startup status and readiness
- Database connection health and latency
- Migration state consistency
- Resource utilization metrics (connection pool usage)
- Error rates and failure conditions

**Relationships**:

- Monitors Database Connection availability
- Validates Migration State consistency
- Reports on Application Configuration effectiveness

**State Transitions**:

- `starting` → `healthy` (successful startup)
- `healthy` → `degraded` (partial functionality)
- `degraded` → `unhealthy` (connection failures)
- `unhealthy` → `healthy` (recovery)

**Validation Rules**:

- Health checks must complete within timeout limits
- Database connectivity must be verified before reporting healthy
- Migration state must be consistent for health status

## Entity Relationships

```
Application Configuration
    ↓ configures
Database Connection ←→ provides sessions to → [Future Business Entities]
    ↓ manages schema
Migration State
    ↑ all monitored by
Health Status
```

## Data Architecture Patterns

### Session Management Pattern

- **Request-scoped sessions**: Each HTTP request gets isolated database session
- **Dependency injection**: FastAPI dependencies provide clean session lifecycle
- **Async context management**: Proper resource cleanup with async context managers
- **Connection pooling**: Shared pool for efficient resource utilization

### Configuration Pattern

- **Environment-based**: Different settings per deployment environment
- **Type-safe validation**: Pydantic models for configuration validation
- **Hierarchical defaults**: Base settings with environment overrides
- **Secret management**: Secure handling of database credentials

### Migration Pattern

- **Version-controlled schema**: All changes tracked in migration files
- **Forward-only migrations**: Avoid complex rollback scenarios in foundation
- **Async-compatible**: Migration framework supports async database operations
- **Environment consistency**: Same migration tools for dev, staging, production

### Health Check Pattern

- **Layered monitoring**: Application health separate from database health
- **Fast response**: Health checks complete within 5 seconds
- **Detailed diagnostics**: Specific failure information for debugging
- **External monitoring**: Compatible with container orchestration health checks

## Future Extensions

### RLS Readiness

- **User context**: Session management designed to pass user/tenant information
- **Policy-ready tables**: Table design accommodates row-level security policies
- **Context injection**: Authentication middleware can provide security context
- **Flexible permissions**: Foundation supports both application and database-level security

### PostgreSQL 18 UUIDv7 Support

- **Generic UUID types**: Models use UUID type, not UUID4-specific implementations
- **Migration strategy**: Database function approach allows runtime UUID version switching
- **Performance optimization**: Time-ordered UUIDs improve index performance
- **Backward compatibility**: UUID4 fallback for older PostgreSQL versions

## Implementation Guidelines

### SQLAlchemy Model Base

- Use declarative base with UUID primary keys
- Include created_at/updated_at timestamps for auditing
- Async-compatible model definitions
- Type hints for all model attributes

### Database Session Lifecycle

- Session per request via FastAPI dependency
- Automatic rollback on unhandled exceptions
- Explicit commit for successful operations
- Connection pool health monitoring

### Configuration Management

- Pydantic Settings for type-safe environment handling
- Development defaults with production overrides
- Validation on application startup
- Clear error messages for misconfiguration

### Health Check Implementation

- Separate endpoints for application and database health
- Structured response format for monitoring tools
- Appropriate HTTP status codes for different health states
- Minimal overhead for high-frequency health checks
