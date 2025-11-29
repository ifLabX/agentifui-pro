<!--
Sync Impact Report:
Version change: 2.0.0 → 2.1.0
Modified principles:
- I. Dual-Stack Excellence (added App Router + Server Component default and OpenAPI type-gen enforcement)
- II. Quality-First Development (clarified lint/type gates across both stacks)
- III. Test-Driven Implementation (reaffirmed coverage and contract/integration testing)
- IV. Internationalization by Design (explicit next-intl server import and kebab-case enforcement)
- V. Convention Consistency (tightened frontend naming and comment scope)
Added sections:
- Security & Multi-Tenancy (under Development Standards)
Removed sections:
- None
Templates requiring updates:
✅ .specify/templates/plan-template.md (remove stale command reference)
✅ .specify/templates/tasks-template.md (align task generation with test-first requirements)
Follow-up TODOs: None
-->

# Agentifui Pro Constitution

## Core Principles

### I. Dual-Stack Excellence

Every change MUST maintain parity between the Next.js 15 frontend (App Router, Server Components by default) and the FastAPI 3.12+ backend. APIs expose typed OpenAPI schemas backed by Pydantic models, and the frontend consumes generated TypeScript clients/interfaces from the same schema. Server Components remain the default; Client Components are used only when interactivity demands and are documented.

**Rationale**: Guarantees type safety across the stack, reduces integration risk, and keeps contracts synchronized.

### II. Quality-First Development

Code MUST pass automated quality gates before merge:

- Python: Ruff linting/formatting (120 char lines), mypy strict typing, uv-managed environments
- TypeScript: ESLint + oxlint + Next.js type checking with strict mode, no `any` types
- Pre-commit/CI: Same gates run locally and in CI; dependencies added only with justification and documentation

**Rationale**: Prevents technical debt, keeps the codebase maintainable, and enforces consistent standards across teams.

### III. Test-Driven Implementation

All work follows a test-first workflow:

- Write failing tests first, then implement (red-green-refactor)
- Coverage: Backend ≥80%, frontend components covered by Jest + React Testing Library
- Contracts: New/changed endpoints require contract and integration tests plus OpenAPI/typegen verification
- Accessibility: UI changes include WCAG 2.1 AA checks and regressions are prevented

**Rationale**: Ensures reliability, enables safe refactoring, and catches regressions early.

### IV. Internationalization by Design

All user-facing text MUST use next-intl with strict conventions:

- Keys are kebab-case and namespaced: `t('namespace.section.key')`
- Server Components import from `next-intl/server`; Client Components use client-safe hooks
- New features create namespaces via `pnpm i18n:namespace <name>`; locales via `pnpm i18n:locale <locale>`
- No hardcoded strings in UI components; English baseline translations maintained and localized

**Rationale**: Ensures global readiness, avoids retrofitting costs, and keeps translations type-safe.

### V. Convention Consistency

Naming and communication remain predictable:

- Frontend files/directories use kebab-case; backend modules use snake_case; translation keys use kebab-case
- Commit messages follow conventional commits in English
- Comments are minimal, English, and explain WHY; remove debug logs and TODOs before merge
- Imports auto-sort via Prettier/ESLint/Ruff; project scripts follow documented commands

**Rationale**: Reduces cognitive load, speeds onboarding, and keeps the monorepo consistent.

## Development Standards

### Technology Stack

- Backend: FastAPI on Python 3.12+ managed by uv; async-first with Pydantic models
- Frontend: Next.js 15 App Router with React 19, TypeScript strict mode, Tailwind CSS v4, pnpm 10.17+
- Database: PostgreSQL 18+ (native `uuidv7()` support required); schema changes go through Alembic migrations only
- Tooling: pytest (backend), Jest + React Testing Library (frontend), Husky/pre-commit for local validation

### Spec-Kit Workflow

All features follow the Spec-Driven flow:

1. Feature specification at `specs/###-feature-name/spec.md`
1. Implementation plan at `specs/###-feature-name/plan.md` with Constitution Check gates before research and after design
1. Phase outputs (research, data-model, quickstart, contracts) generated via the plan workflow
1. Task breakdown at `specs/###-feature-name/tasks.md` created via the tasks command and executed with TDD

Exceptions are documented in the Complexity Tracking table inside plan.md.

### Architecture Patterns

- Backend: Dependency injection for DB sessions, async/await for all I/O, structured logging and error handling, Alembic for migrations, health endpoints maintained
- Frontend: Prefer Server Components; Client Components only for required interactivity with justification; follow App Router patterns and typed fetchers generated from OpenAPI
- Cross-stack: OpenAPI schema is the single source of truth; regenerate frontend types whenever API contracts change
- Performance/observability: Structured logging, avoid unnecessary dependencies, keep configuration typed and centralized

### Security & Multi-Tenancy

- Non-public routes MUST enforce tenant/actor guards using `x-tenant-id` and `x-actor-id` UUID headers; reject `tenant_id` query params
- Public routes are limited to `/`, `/health`, `/health/db`, `/health/redis`, `/docs`, `/redoc`, `/openapi.json`; infra endpoints (e.g., `/metrics`, `/livez`, `/static/...`, auth callbacks) remain public but do not bypass tenant enforcement elsewhere
- Apply `require_tenant_member` or `require_tenant_role` on all other routers
- Secrets and credentials live in environment variables only; never commit secrets or hardcode tokens
- Data stores must target PostgreSQL 18+ for `uuidv7()`; migrations accompany every schema change

## Quality Assurance

### Quality Gates

- Type checking: mypy strict for backend; TypeScript strict + Next.js type checks for frontend
- Linting/formatting: Ruff for Python; ESLint + oxlint + Prettier (with import sorting) for frontend
- Testing: `uv run pytest` for backend, `pnpm test` for frontend; backend coverage ≥80%
- Accessibility/i18n: UI changes include WCAG 2.1 AA checks and translation coverage (no untranslated strings)
- Performance: Bundle impact reviewed for frontend changes; backend endpoints target sub-200ms p95 when feasible
- Pre-commit/CI: Same gates executed locally and in CI before merging

### Pull Request Requirements

- All automated checks pass; no debugging artifacts (`console.log`, stray `TODO`) remain
- Documentation updated for public API, contract, or command changes
- Breaking changes flagged with migration steps and risks
- i18n and tenancy rules verified for affected code paths (translations present; headers enforced in new endpoints)
- PR templates completed with English content and linked issues

### Testing Standards

- Tests are isolated and repeatable; DB tests run against PostgreSQL 18+ (no SQLite fallbacks)
- Contract/integration tests include tenant headers and validate OpenAPI schema drift
- Component tests validate behavior and accessibility rather than implementation details
- Follow red-green-refactor: write failing tests before implementation

## Governance

This constitution supersedes other development practices and sets project-wide standards. Amendments require documentation updates, team approval, and a migration plan for existing code.

### Compliance

- All Pull Requests must confirm adherence to Core Principles, Development Standards, and Quality Assurance; any exceptions are captured in the plan.md Complexity Tracking table
- Feature plans must include Constitution Checks before research and after design to prevent drift

### Runtime Guidance

- Codex/CLI developers follow `AGENTS.md`; Claude users follow `CLAUDE.md`
- New agent-specific guides must mirror constitutional rules and be updated alongside amendments

### Amendment Process

Constitutional amendments follow semantic versioning:

- **MAJOR**: Backward-incompatible governance/principle removals or redefinitions
- **MINOR**: New principles/sections added or materially expanded guidance
- **PATCH**: Clarifications, wording fixes, non-semantic refinements

All amendments must update the Sync Impact Report and propagate changes to dependent templates in `.specify/templates/`.

**Version**: 2.1.0 | **Ratified**: 2025-09-21 | **Last Amended**: 2025-11-27
