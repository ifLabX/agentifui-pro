# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Structure

Monorepo with:
- **Backend (`api/`)**: FastAPI + Python 3.12+ managed by `uv`
- **Frontend (`web/`)**: Next.js 15 + TypeScript managed by `pnpm`

Backend runs on port 8000, frontend on port 3000.

## Essential Commands

### Backend (api/)
```bash
cd api
uv run pytest                           # Run tests
uv run ruff check . --fix                 # Lint & fix
uv run alembic upgrade head             # Apply migrations
```

### Frontend (web/)
```bash
cd web
pnpm test                               # Run tests
pnpm fix                                # Lint & format
pnpm type-check                         # Type checking
pnpm quality                            # Run all checks
```

## Code Standards

### Language & Comments
- **All content in English**: Comments, commits, PRs, documentation
- **Minimal comments**: Only when necessary, explain WHY not WHAT

### Naming Conventions
- **Frontend files**: Use kebab-case for all file and directory names
- **Translation keys**: Use kebab-case format
  - ✅ `t('common.navigation.home')`, `t('auth.sign-in.email')`
  - ❌ `t('common.Navigation.home')`, `t('auth.SignIn.email')`

### Commit Convention
Follow conventional commits format (title only, body optional):
```
feat: add user authentication
fix: resolve build errors
```

## Internationalization (i18n)

- Use `t('namespace.section.key')` format for all translations
- Import from `next-intl/server` for server components
- All user-facing text must use i18n

**Add translations**:
```bash
cd web
pnpm i18n:locale <locale>      # Add new language
pnpm i18n:namespace <name>     # Add feature namespace
```

## Quality Standards

### Python (Backend)
- Type hints required for all function signatures
- Docstrings required for public functions and classes
- Use specific exceptions, never bare `except:`
- Prefer async/await for I/O operations
- Line length: 120 characters

### TypeScript (Frontend)
- Strict TypeScript mode enabled
- No `any` types - use proper type definitions
- Component props must be typed with interfaces
- Maximum cyclomatic complexity: 15
- Import organization is automatic via Prettier plugin

## Key Technical Constraints

- **PostgreSQL 18+ required**: Backend uses native `uuidv7()` function
- **Next.js App Router only**: No Pages Router
- **Prefer Server Components**: Over Client Components when possible
- **Test coverage**: Minimum 80% for backend
- **Security**: No secrets in code, use environment variables only

- **FastAPI tenancy (api/)**: Only accept `x-tenant-id`/`x-actor-id` headers (UUID); `tenant_id` query param is rejected. Public routes are `/`, `/health` (+ `/db` `/redis`), `/docs`, `/redoc`, `/openapi.json`; all other routers should enforce `require_tenant_member` / `require_tenant_role` at router level.

## Pull Requests

**Before creating PRs**:
- Read `.github/pull_request_template.md` first
- Link to issue: `Fixes #<number>`
- All PRs must be in English
- All quality checks must pass
- Remove console.log and TODO comments
