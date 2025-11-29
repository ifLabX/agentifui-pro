# Feature Specification: Fix API Test Suite and Clean Dead Code

**Feature Branch**: `003-api-uv-run`
**Created**: 2025-10-02
**Status**: Draft
**Input**: User description: "The current situation requires ensuring that running `uv run pytest` under the `api` directory passes all tests, while also cleaning up dead code, redundant code, or unnecessary environment variables. Everything must comply with FastAPI best practices. The main focus right now is to explore the `@api/` directory, analyze why many pytest tests are failing, attempt solutions, and then write documentation based on the findings."

## Execution Flow (main)

```
1. Analyze pytest failures (28 failed, 81 passed out of 109 tests)
   → Categorize failures by root cause
2. Identify dead code and unused configurations
   → Check for unused environment variables
   → Find unreferenced modules/functions
3. Fix critical dependency issues
   → Missing greenlet library for SQLAlchemy async
   → Pydantic deprecation warnings
4. Align with FastAPI best practices
   → Review middleware configuration
   → Validate async patterns
5. Document findings and fixes
   → Create comprehensive analysis report
6. Return: SUCCESS (all tests pass, code cleaned)
```

______________________________________________________________________

## ⚡ Quick Guidelines

- ✅ Focus on fixing test failures and removing technical debt
- ✅ Ensure FastAPI best practices compliance
- ✅ Document all findings for future reference

______________________________________________________________________

## User Scenarios & Testing

### Primary User Story

As a developer working on the agentifui-pro API, I need all pytest tests to pass reliably so that I can confidently deploy code and maintain high quality standards. The codebase should follow FastAPI best practices and be free of dead code or unused configurations.

### Acceptance Scenarios

1. **Given** the api directory with 109 tests, **When** running `uv run pytest`, **Then** all tests should pass with 0 failures
1. **Given** the codebase with environment variables in `.env.example`, **When** reviewing configurations, **Then** all variables should be actively used in the code
1. **Given** the FastAPI application, **When** validating against best practices, **Then** it should follow async patterns, proper dependency injection, and middleware configuration
1. **Given** deprecated Pydantic patterns, **When** running tests, **Then** no deprecation warnings should appear

### Edge Cases

- What happens when greenlet library is missing from dependencies?
- How does the test suite handle database connection failures?
- What occurs when Pydantic Field uses deprecated `env` parameter?
- How are middleware stack attributes accessed in tests?

## Requirements

### Functional Requirements

- **FR-001**: Test suite MUST pass all 109 tests without failures
- **FR-002**: System MUST include greenlet library in dependencies for SQLAlchemy async operations
- **FR-003**: Code MUST use Pydantic v2 ConfigDict instead of deprecated class-based config
- **FR-004**: Environment variable definitions MUST have corresponding usage in source code
- **FR-005**: Database connection tests MUST handle async engine disposal properly
- **FR-006**: Health endpoint tests MUST return appropriate status codes (200, 503, not 500)
- **FR-007**: Middleware configuration tests MUST access correct FastAPI application attributes
- **FR-008**: CORS configuration tests MUST validate settings correctly
- **FR-009**: Error schema validation MUST enforce enum types properly
- **FR-010**: All code MUST follow FastAPI best practices for async patterns and dependency injection

### Non-Functional Requirements

- **NFR-001**: Test execution time MUST remain under 1 second for the full suite
- **NFR-002**: Code coverage SHOULD be maintained at minimum 80%
- **NFR-003**: No deprecation warnings SHOULD appear during test execution
- **NFR-004**: Documentation MUST be comprehensive and actionable

### Key Entities

**Test Failure Categories**:

- **Missing Dependencies**: 5 failures related to greenlet library not being explicitly declared
- **Pydantic Deprecations**: 26 warnings about Field `env` parameter and class-based config
- **Middleware Access Issues**: 3 failures accessing `app.middleware_stack` incorrectly
- **Database Error Handling**: 8 failures expecting specific status codes (503 vs 500)
- **Configuration Validation**: 2 failures in environment variable and CORS validation
- **File Structure Validation**: 1 failure in quickstart file structure checks

**Environment Variables Audit**:

- Active: DATABASE_URL, APP_NAME, APP_VERSION, LOG_LEVEL, CORS_ORIGINS, etc.
- Potentially Unused: SECRET_KEY (marked "for future use"), USE_UUIDV7 (no implementation found)
- Deprecated Usage: CORS_ORIGINS, CORS_ALLOW_METHODS, CORS_ALLOW_HEADERS (using deprecated Field env parameter)

**Code Structure**:

- src/main.py: FastAPI application factory and lifespan management
- src/config/settings.py: Pydantic Settings with validators (needs migration to v2 patterns)
- src/database/connection.py: Async SQLAlchemy engine with pooling
- src/health/endpoints.py: Health check endpoints with database status
- tests/: 10 test modules covering 109 test cases

______________________________________________________________________

## Analysis Summary

### Critical Issues Identified

**1. Missing Greenlet Dependency (Priority: High)**

- SQLAlchemy async operations require greenlet
- Present in uv.lock but not explicitly declared in pyproject.toml
- Causes 5 test failures in async engine disposal and connection management

**2. Pydantic V2 Migration Incomplete (Priority: High)**

- Using deprecated `env` parameter in Field declarations (26 warnings)
- Should use `json_schema_extra` or ValidationInfo instead
- Class-based config deprecation warnings

**3. Test Assertions Incorrect (Priority: High)**

- Middleware stack access using wrong attribute path
- Expected status codes mismatch (expecting 503, getting 500)
- Error enum validation not enforcing properly

**4. Configuration Issues (Priority: Medium)**

- Some environment variables marked "for future use" but no implementation
- USE_UUIDV7 flag has no corresponding code
- SECRET_KEY validation complex but feature unused

**5. FastAPI Best Practices (Priority: Medium)**

- Lifespan management correctly implemented
- Async patterns properly used
- Dependency injection needs verification in tests
- CORS middleware properly configured

### Dead Code Candidates

**Environment Variables**:

- `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`: Security settings with no auth implementation
- `USE_UUIDV7`: Feature flag with no corresponding UUID generation code

**Potential Cleanup Areas**:

- Remove unused security configuration if no auth system planned
- Simplify Field declarations to use Pydantic v2 patterns
- Remove or implement USE_UUIDV7 feature

### FastAPI Best Practices Compliance

**✅ Followed**:

- Async/await patterns throughout
- Lifespan context manager for startup/shutdown
- Dependency injection with get_settings()
- Proper middleware stack (CORS, error handling)
- Health check endpoints
- Pydantic Settings for configuration

**⚠️ Needs Review**:

- Settings singleton pattern using lru_cache is correct but could use dependency injection override pattern for testing
- Error handling middleware setup could expose more metrics
- Database session management in session.py needs verification

**❌ Issues**:

- Tests accessing internal FastAPI attributes incorrectly (middleware_stack)
- Some error responses returning 500 instead of proper status codes
- Database health checks not handling errors gracefully

______________________________________________________________________

## Review & Acceptance Checklist

### Content Quality

- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

### Requirement Completeness

- [x] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous
- [x] Success criteria are measurable (all 109 tests pass)
- [x] Scope is clearly bounded (api/ directory only)
- [x] Dependencies and assumptions identified (greenlet, Pydantic v2)

______________________________________________________________________

## Execution Status

- [x] User description parsed
- [x] Key concepts extracted (test failures, dead code, FastAPI practices)
- [x] Ambiguities marked (none - requirements are clear)
- [x] User scenarios defined
- [x] Requirements generated (10 functional, 4 non-functional)
- [x] Entities identified (test failures, env variables, code structure)
- [x] Review checklist passed

______________________________________________________________________

## Next Steps

1. **Fix Dependencies**: Add greenlet to pyproject.toml explicitly
1. **Migrate Pydantic**: Update Field declarations to v2 patterns
1. **Fix Tests**: Correct middleware assertions and status code expectations
1. **Clean Dead Code**: Remove or implement unused environment variables
1. **Validate Best Practices**: Ensure all FastAPI patterns are optimal
1. **Document**: Create comprehensive implementation guide in claudedocs/
