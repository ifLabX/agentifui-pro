# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Architecture

**Agentifui Pro** is a modern monorepo with dual-stack architecture:
- **Backend (`api/`)**: FastAPI Python application managed by `uv`
- **Frontend (`web/`)**: Next.js 15 TypeScript application managed by `pnpm`

The backend runs on port 8000 with CORS configured for Next.js development server on localhost:3000.

## Code Standards & Guidelines

### Code Comments Policy
- **Language**: All comments MUST be written in English
- **Minimalism**: Comments should be written only when absolutely necessary
- **Focus**: Explain WHY, not WHAT the code does

### Naming Conventions
- **Components** (web/): Use kebab-case for all file and directory names
- **Translation Keys**: Use kebab-case to match component naming consistency
  - Correct: `t('common.navigation.home')`, `t('auth.sign-in.email')`
  - Incorrect: `t('common.Navigation.home')`, `t('auth.SignIn.email')`
- **Consistency**: All naming should follow the same case convention throughout the project

### Commit Convention
- **Format**: Follow conventional commit format with title only
- **Title**: Required - clear, concise description of changes
- **Body**: Optional - use only for complex changes that need explanation
- **Language**: All commit messages MUST be in English

Example:
```
feat: add bundle analyzer configuration
fix: resolve TypeScript compilation errors
```

## Internationalization (i18n) Rules

**Architecture**: Next-intl with automated namespace management and type safety

### Development Rules
- **Single t() function**: Always use `t('namespace.section.key')` format
- **Kebab-case keys**: Match component naming (`sign-in`, not `SignIn`)
- **Server vs Client**: Import from `next-intl/server` for server components
- **Type safety**: All translation keys are compile-time validated
- **No hardcoded strings**: All user-facing text must use i18n

### Quick Commands
```bash
cd web
pnpm i18n:locale <locale>     # Add new language (auto-detects common names)
pnpm i18n:namespace <name>    # Add feature namespace (updates types)
```

## Code Quality Standards

### Python (Backend)
- **Linting**: Ruff with extensive ruleset (120 char line length)
- **Type hints**: Required for all function signatures
- **Docstrings**: Required for all public functions and classes
- **Error handling**: Use specific exceptions, never bare `except:`
- **Async patterns**: Prefer async/await for I/O operations

#### Ruff Configuration (api/.ruff.toml)
- Comprehensive ruleset including security, bugbear, and style rules
- Line length: 120 characters
- Excludes migrations, .venv, __pycache__
- Per-file ignores for __init__.py, configs/, tests/

### TypeScript (Frontend)
- **Strict mode**: TypeScript strict mode enabled
- **No `any` types**: Use proper type definitions
- **Component props**: All props must be typed with interfaces
- **Event handlers**: Properly typed event parameters
- **Complexity limit**: Maximum cyclomatic complexity of 15

#### ESLint Configuration (web/eslint.config.mjs)
- Next.js recommended config + TypeScript
- Oxlint plugin integration for enhanced performance
- Caching enabled for faster subsequent runs
- Code complexity enforcement (max: 15)

### Import Organization
Frontend uses automatic import sorting via Prettier plugin:
- React/Next.js imports first
- Third-party packages
- Internal imports by type (@/types, @/lib, @/components, etc.)
- Relative imports last

## Architecture Constraints

### Backend Patterns
- **PostgreSQL 18+**: Required for native `uuidv7()` function support
- **Dependency injection**: Use FastAPI's dependency injection for database sessions
- **Async everywhere**: All database operations must be async
- **Error handling**: Structured error responses with request tracing
- **Health monitoring**: All services must expose health endpoints
- **Environment config**: All settings via Pydantic Settings with validation
- **Database migrations**: Use Alembic for all schema changes

### Frontend Patterns
- **App Router only**: Use Next.js 15 App Router, no Pages Router
- **Server Components**: Prefer Server Components over Client Components
- **Type safety**: Full TypeScript coverage with strict mode
- **Performance**: Use React.memo, useCallback, useMemo appropriately
- **Accessibility**: All components must meet WCAG 2.1 AA standards

## Testing Requirements

### Backend Testing
- **Coverage**: Minimum 80% test coverage
- **Async tests**: Use pytest-asyncio for async code
- **Test isolation**: Each test must be independent with automatic cache reset
- **Database tests**: Use PostgreSQL 18+ (real database, not SQLite mocks)
- **Fixtures**: Auto-reset settings and session factory between tests

### Frontend Testing
- **Jest + RTL**: Jest with React Testing Library
- **Component testing**: Test behavior, not implementation
- **Accessibility**: Include accessibility tests
- **User interaction**: Test user flows, not just rendering

## Security Standards

### General Security
- **No secrets in code**: Use environment variables only
- **Input validation**: Validate all inputs with Pydantic/Zod
- **SQL injection**: Use ORM query builders, never raw SQL with user input
- **XSS protection**: Sanitize all user-generated content

### API Security
- **CORS**: Properly configured CORS origins
- **Rate limiting**: Implement rate limiting for public endpoints
- **Authentication**: JWT tokens with proper expiration
- **Authorization**: Role-based access control

## Pre-commit Quality Gates

The repository uses Husky with monorepo-aware pre-commit hooks that:
- Detect which workspace (api/ or web/) has changes
- Run appropriate linters only for modified code
- Apply automatic fixes where possible
- Enforce code quality before commits
- Block commits if quality checks fail

## Pull Request Guidelines

### Before Creating PRs
- **Always read PR template first**: Before using `gh pr create` or GitHub MCP to create PRs, you MUST read `.github/pull_request_template.md` to understand the required format and checklist
- **Follow template structure**: Use the template's format including summary, type checkboxes, and issue linking
- **All PRs in English**: Ensure all PR titles, descriptions, and comments are written in English

### Quality Requirements
- **All checks must pass**: Linting, type checking, tests
- **No console.log**: Remove all debugging statements
- **No TODO comments**: Complete implementation or create issues
- **Documentation updates**: Update docs if changing public APIs
- **Breaking changes**: Must be explicitly marked and justified

## Key Files Reference

### Backend (api/)
- `src/main.py`: FastAPI application entry point with CORS middleware
- `src/database/`: Database connection, session management, and health checks
- `src/models/base.py`: Base model with PostgreSQL 18 uuidv7() support
- `migrations/`: Alembic migration files (never edit after applying)
- `alembic.ini`: Alembic configuration (script_location = migrations)
- `.ruff.toml`: Python linting configuration
- `pyproject.toml`: Dependencies and project configuration
- `README.md`: Development setup, Alembic workflow, and commands

### Frontend (web/)
- `app/`: Next.js App Router pages and layouts
- `i18n/config.ts`: Single source of truth for i18n configuration
- `types/i18n.d.ts`: Auto-generated i18n type definitions
- `eslint.config.mjs`: TypeScript linting configuration
- `tailwind.config.ts`: Tailwind CSS configuration with theme extensions
- `jest.config.ts`: Jest testing configuration

### Root
- `package.json`: Monorepo scripts and husky configuration
- `CONTRIBUTING.md`: Contribution guidelines
