# Data Model Design: Configuration Management Enhancement

**Project**: Agentifui Pro Backend Refactoring
**Date**: 2025-09-24
**Phase**: 1 - Design & Contracts

## Overview

This document defines the data models and configuration entities required for the FastAPI backend architecture optimization. The design focuses on flexible database configuration composition, enhanced environment variable parsing, and improved validation patterns while maintaining backward compatibility.

## Primary Entities

### 1. DatabaseConfig

**Purpose**: Composable database connection configuration with validation and URL generation.

**Fields**:
- `host: str` - Database server hostname or IP address
- `port: int` - Database server port (default: 5432)
- `username: str` - Database authentication username
- `password: SecretStr` - Database authentication password (secured)
- `database: str` - Target database name
- `driver: str` - Database driver specification (default: "postgresql+asyncpg")

**Computed Properties**:
- `url: str` - Composed connection string for SQLAlchemy
- `connection_info: dict` - Sanitized connection information for logging

**Validation Rules**:
- Host must be valid hostname or IP address
- Port must be in range 1-65535
- Username and database must be non-empty
- Password must meet environment-specific security requirements
- Driver must be supported by SQLAlchemy

**Relationships**:
- Used by `ConnectionManager` for engine creation
- Referenced in health check responses
- Validated by `EnvironmentSettings`

```python
class DatabaseConfig(BaseModel):
    host: str = Field(..., env="DB_HOST")
    port: int = Field(default=5432, env="DB_PORT", ge=1, le=65535)
    username: str = Field(..., env="DB_USERNAME", min_length=1)
    password: SecretStr = Field(..., env="DB_PASSWORD")
    database: str = Field(..., env="DB_DATABASE", min_length=1)
    driver: str = Field(default="postgresql+asyncpg", env="DB_DRIVER")

    @computed_field
    @property
    def url(self) -> str:
        return f"{self.driver}://{self.username}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.database}"

    @computed_field
    @property
    def connection_info(self) -> dict[str, Any]:
        return {
            "host": self.host,
            "port": self.port,
            "database": self.database,
            "driver": self.driver
        }
```

### 2. EnvironmentSettings

**Purpose**: Enhanced application settings with environment-aware validation and flexible parsing.

**Fields**:
- `environment: str` - Application environment (development, staging, production)
- `database: DatabaseConfig` - Database configuration composition
- `cors_origins: list[str]` - CORS allowed origins with flexible parsing
- `cors_allow_credentials: bool` - CORS credential support
- `cors_allow_methods: list[str]` - CORS allowed HTTP methods
- `cors_allow_headers: list[str]` - CORS allowed headers
- `secret_key: SecretStr` - Application secret key with security validation
- `log_level: str` - Logging level with validation
- `feature_flags: dict[str, bool]` - Application feature toggles

**Validation Rules**:
- Environment must be in allowed values (development, staging, production)
- Production environment enforces stricter validation rules
- CORS origins must be valid URLs or wildcards
- Secret key length and security based on environment
- Log level must be valid logging level
- Feature flags must be boolean values

**Parsing Features**:
- Comma-separated value support for list fields
- JSON array backward compatibility
- Environment variable composition
- Automatic type coercion with validation

```python
class EnvironmentSettings(BaseSettings):
    environment: str = Field(default="development", env="ENVIRONMENT")
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)

    cors_origins: list[str] = Field(default=["http://localhost:3000"], env="CORS_ORIGINS")
    cors_allow_credentials: bool = Field(default=True, env="CORS_ALLOW_CREDENTIALS")
    cors_allow_methods: list[str] = Field(default=["*"], env="CORS_ALLOW_METHODS")
    cors_allow_headers: list[str] = Field(default=["*"], env="CORS_ALLOW_HEADERS")

    secret_key: SecretStr = Field(env="SECRET_KEY")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    feature_flags: dict[str, bool] = Field(default_factory=dict, env="FEATURE_FLAGS")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        # Implementation for comma-separated parsing with JSON fallback

    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, v, info):
        # Environment-specific secret key validation
```

### 3. ConnectionManager

**Purpose**: Database connection lifecycle management with health monitoring and graceful shutdown.

**Properties**:
- `engine: Optional[AsyncEngine]` - SQLAlchemy async engine instance
- `session_factory: Optional[async_sessionmaker]` - Session factory for dependency injection
- `is_initialized: bool` - Initialization status
- `connection_count: int` - Current active connections
- `pool_status: dict` - Connection pool status information

**Methods**:
- `initialize(config: DatabaseConfig)` - Initialize connection with configuration
- `get_session()` - Create new database session (dependency injectable)
- `health_check()` - Comprehensive database health verification
- `dispose()` - Graceful connection cleanup
- `get_metrics()` - Connection and performance metrics

**State Management**:
- Singleton pattern for application-wide connection management
- Thread-safe initialization and disposal
- Connection pool optimization based on environment
- Error recovery and reconnection logic

```python
class ConnectionManager:
    def __init__(self):
        self._engine: Optional[AsyncEngine] = None
        self._session_factory: Optional[async_sessionmaker] = None
        self._initialized: bool = False

    async def initialize(self, config: DatabaseConfig) -> None:
        # Initialize async engine and session factory

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        # Provide database session for FastAPI dependency injection

    async def health_check(self) -> DatabaseHealthInfo:
        # Comprehensive health check with metrics

    async def dispose(self) -> None:
        # Graceful cleanup of connections
```

### 4. DatabaseHealthInfo

**Purpose**: Structured health check response with comprehensive database metrics.

**Fields**:
- `connected: bool` - Basic connectivity status
- `response_time_ms: int` - Database response time in milliseconds
- `version: Optional[str]` - PostgreSQL version information
- `database_name: Optional[str]` - Current database name
- `connection_pool: Optional[ConnectionPoolInfo]` - Pool status if available
- `migration_status: MigrationStatus` - Alembic migration status
- `errors: list[str]` - Any error messages or warnings

**Usage**:
- Health check endpoint responses
- Operational monitoring and alerting
- Diagnostic information for troubleshooting
- Performance metrics collection

### 5. ConnectionPoolInfo

**Purpose**: Connection pool status and metrics for monitoring.

**Fields**:
- `pool_size: int` - Configured pool size
- `active_connections: int` - Currently active connections
- `checked_out_connections: int` - Connections in use
- `overflow_connections: int` - Overflow connections if applicable
- `invalid_connections: int` - Invalid connections requiring cleanup

## Configuration Composition Patterns

### Environment Variable Mapping

**Development Environment**:
```bash
# Individual database fields
DB_HOST=localhost
DB_PORT=5432
DB_USERNAME=agentifui_user
DB_PASSWORD=dev_password
DB_DATABASE=agentifui_dev

# Comma-separated CORS origins
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

**Production Environment**:
```bash
# Production database configuration
DB_HOST=prod-db.company.com
DB_PORT=5432
DB_USERNAME=agentifui_prod
DB_PASSWORD=${SECRET_DB_PASSWORD}
DB_DATABASE=agentifui_prod

# Production CORS configuration
CORS_ORIGINS=https://app.company.com,https://admin.company.com
```

### Backward Compatibility Support

**Legacy DATABASE_URL Support**:
- Automatic parsing of existing DATABASE_URL format
- Migration helper for converting to component fields
- Validation warnings for deprecated patterns
- Gradual migration path documentation

**JSON Array Compatibility**:
- Continued support for JSON array format in CORS settings
- Automatic detection and parsing
- Migration recommendations in logs
- Documentation for new comma-separated format

## Validation Hierarchy

### Field-Level Validation
- Type checking with Pydantic type system
- Range validation for numeric fields
- Pattern matching for string fields
- Security validation for sensitive fields

### Cross-Field Validation
- Database connection parameter consistency
- CORS origin format validation
- Environment-specific requirement enforcement
- Feature flag dependency checking

### Environment-Level Validation
- Production security requirement enforcement
- Development convenience feature enablement
- Staging environment configuration validation
- Cross-environment consistency checking

## Error Handling Patterns

### Configuration Errors
- Clear error messages with field-specific guidance
- Environment variable name suggestions for typos
- Migration guidance for deprecated formats
- Security requirement explanation for production

### Connection Errors
- Detailed connection failure diagnostics
- Network connectivity troubleshooting information
- Authentication error specifics
- Database availability status

### Validation Errors
- Field-specific validation failure messages
- Environment context in error descriptions
- Remediation steps for common issues
- Security consideration explanations

## Integration Points

### FastAPI Application
- Settings dependency injection through factory pattern
- Middleware configuration from environment settings
- Health check integration with configuration validation
- Error handling middleware with configuration context

### Testing Framework
- Test-specific configuration overrides
- Database connection mocking patterns
- Environment variable testing utilities
- Configuration validation test coverage

### Operational Monitoring
- Configuration change detection and logging
- Database connection metrics collection
- Health check status integration
- Performance monitoring data structure

## Migration Strategy

### Phase 1: Backward Compatible Enhancement
- Add new configuration classes alongside existing
- Implement flexible environment variable parsing
- Maintain existing DATABASE_URL support
- Add deprecation warnings for old patterns

### Phase 2: Default Transition
- Switch default behavior to new configuration patterns
- Provide migration utilities and documentation
- Enhanced validation and error messages
- Performance optimization for new patterns

### Phase 3: Legacy Cleanup
- Remove deprecated configuration patterns
- Optimize for new configuration structure
- Enhanced security and validation features
- Full integration testing and validation

---
**Data Model Design Complete** ✅ All entities defined with validation rules and integration patterns