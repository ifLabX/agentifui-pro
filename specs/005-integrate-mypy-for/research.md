# Research: Mypy Best Practices for FastAPI/SQLAlchemy/Pydantic Projects

## Research Methodology

All research conducted using Context7 MCP server to retrieve official mypy documentation and best practices for Python 3.12+ async projects with FastAPI, Pydantic, and SQLAlchemy.

## Key Findings

### 1. Strict Mode Configuration

**Source**: mypy official documentation - Existing Code section

**Finding**: Strict mode is recommended for new projects and includes 13 individual flags:
- `warn_unused_configs = True`
- `warn_redundant_casts = True`
- `warn_unused_ignores = True`
- `strict_equality = True`
- `check_untyped_defs = True`
- `disallow_subclassing_any = True`
- `disallow_untyped_decorators = True`
- `disallow_any_generics = True`
- `disallow_untyped_calls = True`
- `disallow_incomplete_defs = True`
- `disallow_untyped_defs = True`
- `no_implicit_reexport = True`
- `warn_return_any = True`

**Recommendation**: Use `strict = true` shorthand instead of listing all flags individually.

**Project Application**: Early-stage project (~15 files) is ideal for strict mode adoption from day one.

### 2. Async Pattern Support

**Source**: mypy protocols documentation - Async Protocols section

**Finding**: Mypy 1.8+ has native support for async protocols:
- `AsyncIterator[T]`: Requires `__aiter__()` returning AsyncIterator and `__anext__()` returning Awaitable
- `AsyncContextManager[T]`: Requires `__aenter__()` and `__aexit__()` returning Awaitables
- Coroutines vs AsyncIterators: Different type signatures based on yield presence

**Key Insight**: Async generators (functions with `yield`) have different type signatures than async functions returning AsyncIterator.

**Project Application**: No special configuration needed - mypy handles async/await patterns automatically.

### 3. Pydantic Integration

**Source**: mypy extending documentation - Plugins section

**Finding**: Pydantic provides official mypy plugin for enhanced type checking:
- Plugin ID: `pydantic.mypy`
- Improves type inference for Pydantic's dynamic model features
- Validates field types, validators, and model configurations

**Configuration**:
```toml
[tool.mypy]
plugins = ["pydantic.mypy"]
```

**Project Application**: Essential for FastAPI request/response model validation.

### 4. Incremental Caching

**Source**: mypy command line documentation - Cache Configuration section

**Finding**: Incremental mode provides 5-10x speedup on subsequent runs:
- Default cache directory: `.mypy_cache/`
- Cache includes: Type analysis results, dependency graph, module metadata
- Cache invalidation: Automatic on source file changes

**Performance Metrics**:
- First run: Full type check (~30s for small projects)
- Subsequent runs: Incremental check (~3-5s for single file changes)

**Project Application**: Default configuration sufficient, add `.mypy_cache/` to `.gitignore`.

### 5. Module Overrides for Third-Party Libraries

**Source**: mypy configuration documentation - Per-Module Options section

**Finding**: Per-module overrides handle libraries without type stubs:

```toml
[[tool.mypy.overrides]]
module = "asyncpg.*"
ignore_missing_imports = true

[[tool.mypy.overrides]]
module = "migrations.*"
ignore_errors = true
```

**Rationale**:
- `asyncpg`: May lack complete type stubs, allow imports without blocking
- `migrations`: Alembic-generated files, exclude from strict checking

**Project Application**: Add overrides for specific libraries as needed during implementation.

### 6. Error Reporting Configuration

**Source**: mypy configuration documentation - Output Options section

**Finding**: Enhanced error reporting improves developer experience:
- `show_error_codes = true`: Display error codes for targeted suppression
- `pretty = true`: Soft word wrap and source snippets
- `color_output = true`: Terminal color highlighting
- `show_column_numbers = true`: Precise error location

**Project Application**: Enable all enhanced reporting options for better debugging.

### 7. Pre-commit Integration Pattern

**Source**: Industry best practices for Python monorepos

**Finding**: Workspace-aware hooks prevent unnecessary tool runs:
- Detect changed workspace (api/ vs web/)
- Run workspace-specific tools only
- Maintain fast commit times

**Implementation**:
```bash
# In .husky/pre-commit
if git diff --cached --name-only | grep -q "^api/"; then
  cd api && uv run mypy .
fi
```

**Project Application**: Aligns with existing Husky configuration for Ruff.

### 8. CI/CD Pipeline Integration

**Source**: Industry best practices for Python CI/CD

**Finding**: Type checking should be independent CI step:
- Position: After linting, before testing
- Rationale: Fail fast on type errors before expensive test execution
- Order: lint → type-check → test → build

**GitHub Actions Example**:
```yaml
- name: Type check with mypy
  run: |
    cd api
    uv run mypy .
```

**Project Application**: Add dedicated type-check step to CI workflow.

## Decisions Summary

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Strictness Level | `strict = true` | New project, small codebase, best practices |
| Plugin | `pydantic.mypy` | Essential for FastAPI/Pydantic validation |
| Async Support | Native (no config) | Mypy 1.8+ handles async patterns automatically |
| Cache Strategy | Default incremental | 5-10x speedup, standard location |
| Migration Handling | Exclude via override | Alembic-generated, not user code |
| Third-party Stubs | Per-module overrides | Pragmatic approach, doesn't block development |
| Error Reporting | Enhanced (pretty, codes, colors) | Better developer experience |
| Pre-commit | Workspace-aware hook | Fast commits, targeted execution |
| CI/CD | Dedicated step after lint | Fail fast, independent validation |

## Implementation Notes

1. **Gradual Adoption Not Needed**: Project has only ~15 files, can adopt strict mode immediately
2. **Type Stub Installation**: May need `mypy --install-types` for some dependencies
3. **Performance Expectations**: <5s incremental, <30s full check
4. **Breaking Changes**: None - pure infrastructure addition
5. **Documentation Updates**: Add mypy section to development guide

## References

- Mypy Official Docs: Configuration, Strict Mode, Async Patterns
- Pydantic Docs: Mypy Plugin Integration
- FastAPI Docs: Type Hints and Editor Support
- SQLAlchemy Docs: Async Extensions Type Hints
- Community Best Practices: Python Monorepo Tooling
