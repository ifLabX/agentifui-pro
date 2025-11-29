# Data Model: Mypy Type Checking Configuration

## Overview

This document defines the data structures and configuration schema for mypy static type checking integration into the Python backend.

## Configuration Entities

### Entity 1: Mypy Configuration

**Location**: `api/pyproject.toml`

**Structure**:

```toml
[tool.mypy]
# Python version
python_version = "3.12"

# Strictness
strict = true

# Plugins
plugins = ["pydantic.mypy"]

# Source paths
mypy_path = "src"
packages = ["src"]

# Exclusions
exclude = [
    "^migrations/",
    "^\\.venv/",
]

# Error reporting
warn_unused_configs = true
show_error_codes = true
show_column_numbers = true
show_error_code_links = true
pretty = true
color_output = true
error_summary = true

# Caching
incremental = true
cache_dir = ".mypy_cache"

# Module overrides
[[tool.mypy.overrides]]
module = "migrations.*"
ignore_errors = true

[[tool.mypy.overrides]]
module = "asyncpg.*"
ignore_missing_imports = true
```

**Field Definitions**:

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| python_version | string | Yes | - | Target Python version (3.12) |
| strict | boolean | Yes | false | Enable all strict type checks |
| plugins | array[string] | Yes | [] | List of mypy plugins (pydantic.mypy) |
| mypy_path | string | Yes | - | Base path for module resolution |
| packages | array[string] | Yes | - | Packages to type check |
| exclude | array[regex] | Yes | [] | Patterns to exclude from checking |
| warn_unused_configs | boolean | No | false | Warn about unused config sections |
| show_error_codes | boolean | No | false | Display error codes in messages |
| show_column_numbers | boolean | No | false | Show column numbers in errors |
| show_error_code_links | boolean | No | false | Show documentation links |
| pretty | boolean | No | false | Use enhanced error formatting |
| color_output | boolean | No | true | Use colors in terminal output |
| error_summary | boolean | No | true | Show error count summary |
| incremental | boolean | No | true | Enable incremental type checking |
| cache_dir | string | No | .mypy_cache | Directory for cache files |

**Module Override Structure**:

```toml
[[tool.mypy.overrides]]
module = "pattern"          # Module name pattern (supports wildcards)
ignore_errors = boolean     # Ignore all errors for this module
ignore_missing_imports = boolean  # Ignore missing import errors
disallow_untyped_defs = boolean   # Override strict mode for specific module
```

**Validation Rules**:

- `python_version` must match project Python requirement (3.12+)
- `plugins` must reference installed packages
- `exclude` patterns must be valid regex
- `cache_dir` must be gitignored
- Module overrides must not conflict with global settings

______________________________________________________________________

### Entity 2: Type Cache

**Location**: `api/.mypy_cache/`

**Purpose**: Store incremental type checking state to accelerate subsequent runs

**Structure**:

```
.mypy_cache/
├── 3.12/                    # Python version-specific cache
│   ├── src/
│   │   ├── models/
│   │   │   ├── base.data.json          # Type analysis results
│   │   │   ├── base.meta.json          # Module metadata
│   │   │   └── __init__.data.json
│   │   ├── schemas/
│   │   ├── api/
│   │   └── core/
│   └── CACHEDIR.TAG         # Cache directory marker
```

**File Types**:

- `*.data.json`: Serialized type analysis results
- `*.meta.json`: Module metadata (mtime, size, hash)
- `CACHEDIR.TAG`: Cache directory identification

**Lifecycle**:

- **Creation**: Automatically on first mypy run
- **Update**: Incremental updates on file changes
- **Invalidation**: Automatic when source files change
- **Cleanup**: Manual via `mypy --clear-cache`

**Size Characteristics**:

- Small project (~15 files): ~1-2 MB
- Medium project (~50 files): ~3-5 MB
- Large project (~200 files): ~10-20 MB

**Performance Impact**:

- First run (cold cache): 100% time
- Subsequent run (warm cache): 10-20% time
- Single file change: ~3-5 seconds

______________________________________________________________________

### Entity 3: Pre-commit Hook Configuration

**Location**: `.husky/pre-commit`

**Purpose**: Run type checking before allowing git commits

**Implementation**:

```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Detect workspace changes
API_CHANGES=$(git diff --cached --name-only | grep "^api/" || true)
WEB_CHANGES=$(git diff --cached --name-only | grep "^web/" || true)

# API workspace checks
if [ -n "$API_CHANGES" ]; then
  echo "🔍 Checking API workspace..."

  # Run Ruff (existing)
  cd api && uv run ruff check . || exit 1

  # Run mypy (new)
  echo "🔎 Running type checker..."
  uv run mypy . || exit 1

  cd ..
fi

# Web workspace checks
if [ -n "$WEB_CHANGES" ]; then
  echo "🔍 Checking Web workspace..."
  cd web && pnpm lint || exit 1
  cd ..
fi
```

**Configuration Parameters**:

- **Trigger**: Git commit with staged changes
- **Workspace Detection**: File path pattern matching
- **Execution**: Sequential (Ruff → mypy)
- **Failure Handling**: Block commit on any error
- **Output**: Console error messages

______________________________________________________________________

### Entity 4: Type Error Report

**Purpose**: Structured representation of type checking results

**Schema**:

```typescript
interface TypeCheckResult {
  exitCode: 0 | 1;
  errors: TypeError[];
  summary: {
    filesChecked: number;
    errorsFound: number;
    warningsFound: number;
    timeElapsed: number;  // milliseconds
  };
}

interface TypeError {
  file: string;          // Relative path from api/
  line: number;          // Line number (1-indexed)
  column: number;        // Column number (1-indexed)
  errorCode: string;     // e.g., "assignment", "arg-type"
  severity: "error" | "note";
  message: string;       // Human-readable error message
  context?: string[];    // Surrounding code lines
}
```

**Example Error Output**:

```
src/api/endpoints/health.py:15:12: error: Incompatible return value type (got "str", expected "int")  [return-value]
src/models/base.py:8:5: error: Missing type annotation for variable "metadata"  [var-annotated]
Found 2 errors in 2 files (checked 15 source files)
```

**Error Codes** (most common):

- `arg-type`: Argument has incompatible type
- `return-value`: Incompatible return value type
- `assignment`: Incompatible types in assignment
- `var-annotated`: Need type annotation for variable
- `call-overload`: No overload variant matches argument types
- `attr-defined`: Module/class has no attribute
- `import-untyped`: Missing type stubs for import

______________________________________________________________________

## Relationships

```
MyPy Configuration (pyproject.toml)
    ↓ configures
Type Checking Service
    ↓ uses
Type Cache (.mypy_cache/)
    ↓ produces
Type Error Report
    ↓ triggers
Pre-commit Hook
    ↓ blocks/allows
Git Commit
```

______________________________________________________________________

## State Transitions

### Type Cache States

```
[Empty]
  → (first mypy run) →
[Valid Cache]
  → (source file change) →
[Partially Invalid Cache]
  → (incremental mypy run) →
[Valid Cache]

[Valid Cache]
  → (mypy --clear-cache) →
[Empty]

[Valid Cache]
  → (mypy version change) →
[Incompatible Cache]
  → (automatic rebuild) →
[Valid Cache]
```

### Pre-commit Hook States

```
[Commit Initiated]
  → (detect api/ changes) →
[Run Type Check]
  → (mypy exit 0) →
[Commit Allowed]

[Run Type Check]
  → (mypy exit 1) →
[Display Errors]
  → (user fixes errors) →
[Commit Blocked]
```

______________________________________________________________________

## Validation Requirements

### Configuration Validation

1. All required fields present in `[tool.mypy]`
1. Python version matches project requirement
1. Plugins reference installed packages
1. Exclude patterns are valid regex
1. Cache directory in `.gitignore`

### Runtime Validation

1. Mypy executable available via `uv run mypy`
1. All source files accessible from mypy_path
1. Pydantic plugin loads successfully
1. Cache directory writable

### Integration Validation

1. Pre-commit hook executes mypy correctly
1. Type errors block commits
1. Cache provides expected speedup
1. Error messages display properly

______________________________________________________________________

## Performance Characteristics

| Operation | Expected Time | Caching | Parallelization |
|-----------|---------------|---------|-----------------|
| First run (15 files) | 10-15s | Cold | No |
| Incremental (1 file changed) | 3-5s | Warm | No |
| Full re-check (warm cache) | 8-12s | Warm | No |
| Cache clear + rebuild | 10-15s | Cold | No |

**Optimization Strategies**:

1. Incremental mode (default enabled)
1. Exclude large generated files (migrations)
1. Use module overrides to skip problematic libraries
1. Cache directory on fast storage (SSD)
