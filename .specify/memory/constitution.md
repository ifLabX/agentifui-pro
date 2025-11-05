<!--
Sync Impact Report:
- Version change: 0.0.0 → 1.0.0
- Modified principles:
  - Template principle 1 → I. Dual-Stack Monorepo Integrity
  - Template principle 2 → II. Continuous Quality Gates
  - Template principle 3 → III. Typed Contracts Everywhere
  - Template principle 4 → IV. Internationalized User Experience
  - Template principle 5 → V. Secure Configuration & Observability
- Added sections:
  - Operational Constraints & Tooling
  - Workflow & Review Requirements
- Removed sections:
  - None
- Templates requiring updates:
  - ✅ .specify/templates/plan-template.md (aligns Constitution Check with principles)
  - ✅ .specify/templates/spec-template.md (references i18n + typed contract obligations)
  - ✅ .specify/templates/tasks-template.md (reflects mandatory quality gates)
- Follow-up TODOs:
  - None
-->
# Agentifui Pro Constitution

## Core Principles

### I. Dual-Stack Monorepo Integrity
- MUST keep backend work inside `api/` and frontend work inside `web/`, each using their native toolchain (`uv` and `pnpm` respectively).
- MUST document and review any cross-layer contracts before merging to avoid implicit coupling.
- SHOULD isolate backend/frontend deployability so either side can release independently when contracts remain unchanged.
Rationale: Clear boundaries keep the monorepo maintainable and enable focused ownership of the FastAPI and Next.js stacks.

### II. Continuous Quality Gates
- MUST run and pass `uv run pytest` and `pnpm quality` (or stricter equivalents) before merging.
- MUST maintain ≥80% backend test coverage and add tests for every user-facing change on both stacks.
- MUST block merges on lint, type-check, or test regressions; waivers require documented maintainer approval.
Rationale: Enforced gates prevent regressions and ensure both stacks stay production-ready.

### III. Typed Contracts Everywhere
- MUST provide full type hints for Python functions and public docstrings for all exported interfaces.
- MUST avoid `any` in TypeScript; define explicit types or generics and prefer server components unless client state is required.
- MUST describe API contracts with Pydantic/Typed schema updates alongside implementation changes.
Rationale: Strong types and explicit contracts keep FastAPI and Next.js integrations predictable and debuggable.

### IV. Internationalized User Experience
- MUST route all user-facing copy through `next-intl` translation keys using kebab-case naming.
- MUST default internal documentation and comments to concise English and justify any deviations.
- SHOULD surface locale-ready backend messages through i18n-aware clients or structured payloads.
Rationale: Consistent localization ensures Agentifui Pro can serve global audiences without retrofit churn.

### V. Secure Configuration & Observability
- MUST keep secrets and credentials out of the repository; rely on environment variables and secret stores.
- MUST ensure structured logging, traceability, and metrics for new features across backend and frontend.
- MUST rely on PostgreSQL 18+ features (e.g., `uuidv7()`) only when the infrastructure contract is documented in specs.
Rationale: Secure-by-default practices and observability safeguard the platform while enabling confident debugging.

## Operational Constraints & Tooling
- Backend stack: FastAPI on Python ≥3.12 managed by `uv`; async-first services; Ruff for linting/formatting.
- Frontend stack: Next.js 15 + React 19 with App Router, Tailwind CSS v4, strict TypeScript, pnpm tooling.
- Required services: PostgreSQL 18+ for data persistence; environment configuration must document required variables.
- Preferred delivery: Server Components whenever possible; fall back to Client Components only for stateful UX.

## Workflow & Review Requirements
- Issue-first workflow: every PR links to `Fixes #<number>` and references relevant specs or plans.
- Branch naming uses `feature/`, `fix/`, or `docs/` prefixes; commits follow Conventional Commit syntax.
- Reviews verify constitution compliance, confirm quality gates passed, and reject untyped or non-i18n changes.
- Remove diagnostic logs and TODOs before merge; document rationale when quality gates are temporarily bypassed.

## Governance
- Amendments require a written proposal summarizing rationale, impact, and rollout; at least two maintainers must approve.
- Versioning follows semantic rules: MAJOR for principle changes/removals, MINOR for new principles/sections, PATCH for clarifications.
- Compliance reviews happen during PRs and at quarterly retrospectives; non-compliance must raise corrective tasks within one sprint.
- Post-amendment, update affected templates, runtime guidance, and tooling instructions before the change is considered ratified.

**Version**: 1.0.0 | **Ratified**: 2025-11-05 | **Last Amended**: 2025-11-05
