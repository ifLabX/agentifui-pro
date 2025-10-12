# Feature Specification: Update Dify SDK Test Suite for httpx Migration

**Feature Branch**: `006-update-api-tests`
**Created**: 2025-10-11
**Status**: Draft
**Input**: User description: "update @api/tests/dify/ all test files for httpx, check git status and git diff first."

## Clarifications

### Session 2025-10-11

- Q: Async vs Sync Client Architecture - Should tests use synchronous httpx.Client or asynchronous httpx.AsyncClient? → A: Use httpx.AsyncClient throughout + pytest-asyncio for async test support (all test methods become async def test_*)
- Q: Async Context Manager Mock Strategy - How should test fixtures handle httpx.AsyncClient's async context manager (__aenter__ / __aexit__) behavior? → A: Fixture returns pre-configured mock with async context manager support (reusable, consistent)
- Q: pytest-asyncio Configuration Mode - Which pytest-asyncio mode should be used for async test discovery? → A: auto mode in pytest.ini (all async def test_* automatically marked, no decorator needed)
- Q: Async Response Mock Implementation - Should httpx.Response mock methods like .json(), .text be async or sync? → A: Response data methods remain synchronous (only client methods are async, matches real httpx behavior)
- Q: Mock Patching Target for AsyncClient - Where should httpx.AsyncClient be patched in tests? → A: Patch at SDK module level where AsyncClient is imported and used (follows "patch where used" principle)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Developer runs existing tests after SDK update (Priority: P1)

When the dify-python-sdk dependency is updated from version 0.1.14 (which uses `requests`) to version 0.1.15 (which uses `httpx`), developers need all existing test files to pass without errors using async testing patterns.

**Why this priority**: This is critical because failing tests block development and deployment. The SDK upgrade introduces breaking changes to the HTTP client implementation, requiring immediate test updates to maintain continuous integration with async/await patterns.

**Independent Test**: Can be fully tested by running `pytest api/tests/dify/` and verifying all async tests pass with the new SDK version. Delivers immediate value by restoring test suite functionality.

**Acceptance Scenarios**:

1. **Given** the test suite uses `requests` library mocking, **When** `pytest api/tests/dify/` is executed, **Then** all async tests pass with the httpx.AsyncClient-based SDK
2. **Given** conftest.py contains async request fixtures, **When** test files import these fixtures, **Then** httpx.AsyncClient and async response objects are correctly mocked
3. **Given** async test methods verify HTTP calls, **When** assertions check call arguments, **Then** httpx.AsyncClient methods are validated with proper async patterns

---

### User Story 2 - Developer adds new Dify SDK integration tests (Priority: P2)

After the test migration, developers need to write new async tests for Dify SDK features using the updated httpx.AsyncClient-based patterns, ensuring consistency across the test suite.

**Why this priority**: Important for maintaining test quality standards and preventing regression, but less urgent than fixing existing broken tests. New tests can reference updated async patterns from migrated tests.

**Independent Test**: Can be tested by creating a new async test file following the migrated patterns, verifying it correctly mocks httpx.AsyncClient and validates SDK behavior.

**Acceptance Scenarios**:

1. **Given** updated async test fixtures in conftest.py, **When** a developer creates a new test file, **Then** httpx.AsyncClient mocking patterns are readily available and documented
2. **Given** existing migrated async test files, **When** a developer needs httpx async mock examples, **Then** consistent async/await patterns are observable across all test files

---

### Edge Cases

- What happens when test fixtures need to mock both successful httpx async responses and error responses (status codes 400, 401, 403, 404, 500)?
- How does the test suite handle async streaming responses that use httpx's aiter_bytes and aiter_lines patterns?
- What happens when tests need to verify httpx-specific async behaviors like HTTP/2 support, connection pooling, or async context managers?
- How do tests handle httpx async exceptions (httpx.HTTPStatusError, httpx.RequestError) in async test methods?
- How are async context managers (__aenter__, __aexit__) properly mocked for httpx.AsyncClient?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Test suite MUST replace all `requests` library imports with `httpx` library imports in conftest.py
- **FR-002**: Test fixtures MUST mock `httpx.Response` objects with synchronous data access methods (.json(), .text, .headers) matching real httpx behavior
- **FR-003**: Test fixtures MUST mock `httpx.AsyncClient` request methods (get, post, put, delete, patch) instead of `requests.request` function, with pre-configured async context manager support (__aenter__, __aexit__)
- **FR-004**: All test methods MUST be converted to async def test_* pattern and use await for async client operations (auto-discovered via pytest-asyncio auto mode)
- **FR-005**: All test assertions MUST verify calls to httpx.AsyncClient methods with correct parameters using async-aware mocking (patched at SDK module level where used)
- **FR-006**: Streaming response fixtures MUST use httpx's async streaming patterns (aiter_bytes, aiter_lines)
- **FR-007**: Error response fixtures MUST include httpx-specific status code handling and async exception types
- **FR-008**: File upload test fixtures MUST use httpx's async multipart file handling patterns
- **FR-009**: Test suite MUST maintain 100% backward compatibility with existing test logic and assertions (only async conversion layer changes)
- **FR-010**: All seven test files MUST pass successfully after async migration (test_chat_client.py, test_completion_client.py, test_dify_client.py, test_knowledge_base_client.py, test_workflow_client.py, test_workspace_client.py, conftest.py)
- **FR-011**: Async context manager behavior (__aenter__, __aexit__) MUST be properly mocked for httpx.AsyncClient instances

### Key Entities *(include if feature involves data)*

- **httpx.Response Mock**: Represents HTTP response objects with status_code, json(), text, headers, aiter_lines() for async streaming
- **httpx.AsyncClient Mock**: Represents async HTTP client with async methods like get(), post(), put(), delete(), patch() and async context manager support
- **Test Fixtures**: Reusable async mock objects (mock_successful_response, mock_error_response, mock_streaming_response, mock_async_client)
- **Test Files**: Seven Python test files covering different Dify SDK client types, all using async test patterns
- **Assertions**: Verification points checking httpx.AsyncClient method calls and async response handling

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All existing tests in api/tests/dify/ pass with 100% success rate after httpx async migration
- **SC-002**: Test execution completes without any import errors, missing mock attribute errors, or async-related errors
- **SC-003**: Code coverage for api/tests/dify/ maintains or exceeds the current coverage percentage (minimum 80%)
- **SC-004**: Test suite execution time remains within 10% of previous execution time despite async conversion
- **SC-005**: All test assertions correctly validate httpx.AsyncClient interactions (verifiable by reviewing call_args assertions)
- **SC-006**: Zero test failures related to requests library or synchronous patterns after migration (measurable by pytest output)
- **SC-007**: All async test methods properly use pytest-asyncio markers and execute without event loop errors

## Assumptions *(include when making informed guesses)*

- The dify-python-sdk 0.1.15 uses httpx.AsyncClient for all HTTP operations
- Existing test logic and business assertions remain valid; only HTTP mocking layer needs async conversion
- The httpx.Response mock interface for async operations is similar enough to requests.Response that most fixture structures can be preserved with async wrappers
- Test files use pytest fixtures for dependency injection, making centralized async fixture updates in conftest.py sufficient
- No integration tests require actual network calls; all tests use async mocks
- pytest-asyncio is compatible with the existing pytest test discovery and execution patterns

## Out of Scope *(include to clarify boundaries)*

- Migrating the dify-python-sdk library itself (already completed upstream)
- Adding new test coverage for previously untested SDK features
- Changing test structure, organization, or testing frameworks (only adding async/await patterns)
- Performance optimization of test execution beyond maintaining current speeds
- Converting any production code to async patterns (test-only changes)
- Updating documentation or README files for test usage

## Dependencies *(include when external factors exist)*

- **dify-python-sdk==0.1.15**: Already updated in pyproject.toml with httpx dependency
- **httpx library**: Must be available in the test environment (included as transitive dependency via dify-python-sdk)
- **pytest**: Existing test framework and fixtures
- **pytest-asyncio**: Required for async test support and event loop management (configured in auto mode via pytest.ini)
- **unittest.mock**: Python's standard mocking library used for creating async mock objects

## Notes *(optional - for clarifications)*

This specification focuses on a technical migration task rather than a user-facing feature. The "users" in this context are developers maintaining the test suite. The migration is necessary because the upstream dify-python-sdk changed its HTTP client library from requests to httpx in version 0.1.15, breaking all existing test mocks that assumed requests-based implementations. Additionally, all tests must be converted to async patterns to properly test the AsyncClient-based SDK.
