# Feature Specification: Update Dify SDK Test Suite for httpx Migration

**Feature Branch**: `006-update-api-tests`
**Created**: 2025-10-11
**Status**: Draft
**Input**: User description: "update @api/tests/dify/ all test files for httpx, check git status and git diff first."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Developer runs existing tests after SDK update (Priority: P1)

When the dify-python-sdk dependency is updated from version 0.1.14 (which uses `requests`) to version 0.1.15 (which uses `httpx`), developers need all existing test files to pass without errors.

**Why this priority**: This is critical because failing tests block development and deployment. The SDK upgrade introduces breaking changes to the HTTP client implementation, requiring immediate test updates to maintain continuous integration.

**Independent Test**: Can be fully tested by running `pytest api/tests/dify/` and verifying all tests pass with the new SDK version. Delivers immediate value by restoring test suite functionality.

**Acceptance Scenarios**:

1. **Given** the test suite uses `requests` library mocking, **When** `pytest api/tests/dify/` is executed, **Then** all tests pass with the httpx-based SDK
2. **Given** conftest.py contains request fixtures, **When** test files import these fixtures, **Then** httpx response objects are correctly mocked
3. **Given** test methods verify HTTP calls, **When** assertions check call arguments, **Then** httpx client methods are validated instead of requests methods

---

### User Story 2 - Developer adds new Dify SDK integration tests (Priority: P2)

After the test migration, developers need to write new tests for Dify SDK features using the updated httpx-based patterns, ensuring consistency across the test suite.

**Why this priority**: Important for maintaining test quality standards and preventing regression, but less urgent than fixing existing broken tests. New tests can reference updated patterns from migrated tests.

**Independent Test**: Can be tested by creating a new test file following the migrated patterns, verifying it correctly mocks httpx responses and validates SDK behavior.

**Acceptance Scenarios**:

1. **Given** updated test fixtures in conftest.py, **When** a developer creates a new test file, **Then** httpx mocking patterns are readily available and documented
2. **Given** existing migrated test files, **When** a developer needs httpx mock examples, **Then** consistent patterns are observable across all test files

---

### Edge Cases

- What happens when test fixtures need to mock both successful httpx responses and error responses (status codes 400, 401, 403, 404, 500)?
- How does the test suite handle streaming responses that use httpx's async iteration vs requests' iter_lines?
- What happens when tests need to verify httpx-specific behaviors like HTTP/2 support or connection pooling?
- How do tests handle httpx exceptions (httpx.HTTPStatusError, httpx.RequestError) instead of requests exceptions?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Test suite MUST replace all `requests` library imports with `httpx` library imports in conftest.py
- **FR-002**: Test fixtures MUST mock `httpx.Response` objects instead of `requests.Response` objects
- **FR-003**: Test fixtures MUST mock `httpx.Client` request methods instead of `requests.request` function
- **FR-004**: All test assertions MUST verify calls to httpx client methods with correct parameters
- **FR-005**: Streaming response fixtures MUST use httpx's streaming patterns (iter_bytes, iter_lines, aiter_bytes, aiter_lines)
- **FR-006**: Error response fixtures MUST include httpx-specific status code handling and exception types
- **FR-007**: File upload test fixtures MUST use httpx's multipart file handling patterns
- **FR-008**: Test suite MUST maintain 100% backward compatibility with existing test logic and assertions
- **FR-009**: All seven test files MUST pass successfully after migration (test_chat_client.py, test_completion_client.py, test_dify_client.py, test_knowledge_base_client.py, test_workflow_client.py, test_workspace_client.py, conftest.py)

### Key Entities *(include if feature involves data)*

- **httpx.Response Mock**: Represents HTTP response objects with status_code, json(), text, headers, iter_lines() for streaming
- **httpx.Client Mock**: Represents HTTP client with methods like get(), post(), put(), delete(), patch() instead of requests.request()
- **Test Fixtures**: Reusable mock objects (mock_successful_response, mock_error_response, mock_streaming_response, mock_requests_request)
- **Test Files**: Seven Python test files covering different Dify SDK client types
- **Assertions**: Verification points checking httpx client method calls and response handling

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All existing tests in api/tests/dify/ pass with 100% success rate after httpx migration
- **SC-002**: Test execution completes without any import errors or missing mock attribute errors
- **SC-003**: Code coverage for api/tests/dify/ maintains or exceeds the current coverage percentage (minimum 80%)
- **SC-004**: Test suite execution time remains within 10% of previous execution time
- **SC-005**: All test assertions correctly validate httpx client interactions (verifiable by reviewing call_args assertions)
- **SC-006**: Zero test failures related to requests library after migration (measurable by pytest output)

## Assumptions *(include when making informed guesses)*

- The dify-python-sdk 0.1.15 uses httpx synchronously (not async httpx.AsyncClient), based on standard SDK patterns
- Existing test logic and business assertions remain valid; only HTTP mocking layer needs updates
- The httpx.Response mock interface is similar enough to requests.Response that most fixture structures can be preserved
- Test files use pytest fixtures for dependency injection, making centralized fixture updates in conftest.py sufficient
- No integration tests require actual network calls; all tests use mocks

## Out of Scope *(include to clarify boundaries)*

- Migrating the dify-python-sdk library itself (already completed upstream)
- Adding new test coverage for previously untested SDK features
- Changing test structure, organization, or testing frameworks
- Performance optimization of test execution beyond maintaining current speeds
- Adding async/await test patterns (assuming SDK uses synchronous httpx)
- Updating documentation or README files for test usage

## Dependencies *(include when external factors exist)*

- **dify-python-sdk==0.1.15**: Already updated in pyproject.toml with httpx dependency
- **httpx library**: Must be available in the test environment (included as transitive dependency via dify-python-sdk)
- **pytest**: Existing test framework and fixtures
- **unittest.mock**: Python's standard mocking library used for creating mock objects

## Notes *(optional - for clarifications)*

This specification focuses on a technical migration task rather than a user-facing feature. The "users" in this context are developers maintaining the test suite. The migration is necessary because the upstream dify-python-sdk changed its HTTP client library from requests to httpx in version 0.1.15, breaking all existing test mocks that assumed requests-based implementations.
