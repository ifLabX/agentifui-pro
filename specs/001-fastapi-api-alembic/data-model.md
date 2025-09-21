# Data Model: Backend Foundation Architecture

## Core Foundation Entities

### Application Configuration
**Purpose**: System-wide configuration management
**Fields**:
- `database_url`: PostgreSQL connection string
- `cors_origins`: Allowed CORS origins for frontend integration
- `debug_mode`: Development/production mode flag
- `log_level`: Logging verbosity level

**Validation Rules**:
- database_url must be valid PostgreSQL URL format
- cors_origins must contain localhost:3000 for development
- log_level must be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL

**State Transitions**: Static configuration - no state changes

### Database Connection
**Purpose**: Database session and connection management
**Fields**:
- `engine`: SQLAlchemy async engine instance
- `session_factory`: Session factory for dependency injection
- `connection_pool`: Connection pooling configuration

**Validation Rules**:
- Connection must be established before serving requests
- Session factory must use async sessions
- Pool size must be reasonable for expected load

**State Transitions**:
- DISCONNECTED → CONNECTING → CONNECTED
- CONNECTED → DISCONNECTING → DISCONNECTED

### Migration Management
**Purpose**: Database schema version tracking
**Fields**:
- `alembic_version`: Current migration version
- `migration_history`: Applied migration timestamps
- `schema_state`: Current database schema state

**Validation Rules**:
- Migration versions must follow Alembic naming convention
- Schema state must match migration version
- Migration history must be chronologically ordered

**State Transitions**:
- PENDING → APPLYING → APPLIED
- APPLIED → ROLLING_BACK → ROLLED_BACK

## Entity Relationships

```
Application Configuration
    ├── Database Connection (1:1)
    │   └── Migration Management (1:many)
    └── Security Configuration (1:1)
```

## Foundation Schema Patterns

### Base Model Pattern
All future models will inherit from a common base providing:
- `id`: UUIDv7 primary key
- `created_at`: Timestamp of creation
- `updated_at`: Timestamp of last modification
- `is_active`: Soft delete flag

### Audit Trail Pattern
Critical operations will implement:
- `action_type`: CREATE, UPDATE, DELETE, etc.
- `actor_id`: Who performed the action
- `timestamp`: When the action occurred
- `metadata`: Additional context as JSON

These patterns establish the foundation for future entity development while maintaining consistency and auditability.