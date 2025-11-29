# AGENTS.md

Single source of truth (CLAUDE.md is a symlink): edit this file only.

## Stack
- Backend `api/`: FastAPI, Python 3.11+, PostgreSQL 18 (native `uuidv7()`), managed by `uv` (port 8000).
- Frontend `web/`: Next.js 15 + React 19 + TypeScript, Node.js ≥20, managed by `pnpm` (port 3000).

## Fast commands
Backend (run inside `api/`):
```bash
uv run pytest                  # Tests
uv run ruff check . --fix      # Lint & fix
uv run alembic upgrade head    # Migrations
``````````

Frontend (run inside `web/`):
```bash
pnpm test                      # Frontend tests
pnpm fix                       # ESLint only (no Prettier)
pnpm type-check                # TypeScript
pnpm quality                   # Type-check + lint + prettier check
```

## Rules for AI changes
- Language: Everything in English; comments only when they explain “why”.
- Commits: Conventional commits (e.g., `feat: ...`, `fix: ...`).
- Naming: Frontend files/folders kebab-case; translation keys kebab-case (`t('namespace.section.key')`).
- i18n: All user-facing text goes through `next-intl`; use `next-intl/server` in server components.
- Frontend: App Router only; prefer Server Components; no `any`; props typed; cyclomatic complexity ≤15.
- Backend: PostgreSQL 18+ with `uuidv7()`; async I/O preferred; type hints and docstrings required for public APIs.
- Tenancy (api): Only accept `x-tenant-id` / `x-actor-id` headers (UUID); reject `tenant_id` query param. Public routes: `/`, `/health`, `/health/db`, `/health/redis`, `/docs`, `/redoc`, `/openapi.json`. Protect others with `require_tenant_member` / `require_tenant_role`.
- Security & quality: No secrets in code (env vars only). Backend coverage target ≥80%. Remove `console.log` and TODOs before PRs.
