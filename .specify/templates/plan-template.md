# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

**Language/Version**: Python 3.12 (FastAPI, uv) and TypeScript (Next.js 15, React 19)  
**Primary Dependencies**: FastAPI, Pydantic, PostgreSQL 18+, Next.js App Router, Tailwind CSS v4  
**Storage**: PostgreSQL 18+ with `uuidv7()` identifiers  
**Testing**: `uv run pytest`, `pnpm test`, `pnpm type-check`, `pnpm quality`  
**Target Platform**: Backend services on Linux; frontend served via Next.js with Server Components preferred  
**Project Type**: Dual-stack web application (`api/` backend, `web/` frontend)  
**Performance Goals**: Document feature-specific SLAs; default expectation ≤200 ms backend p95 for API requests  
**Constraints**: Respect monorepo boundaries, async-first backend implementations, no secrets committed  
**Scale/Scope**: Designed for enterprise workloads; confirm feature load expectations during research

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- `Dual-Stack Monorepo Integrity`: Describe which side (`api/` or `web/`) each deliverable touches and document any cross-layer contract.
- `Continuous Quality Gates`: Plan explicit test, lint, and coverage work required for the feature.
- `Typed Contracts Everywhere`: Capture API schemas, type additions, and documentation updates introduced by the feature.
- `Internationalized User Experience`: Note required translation keys and how UX text flows through `next-intl`.
- `Secure Configuration & Observability`: Account for logging, metrics, secrets management, and infrastructure assumptions.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
api/
├── app/               # FastAPI application modules
├── tests/             # pytest suites (unit, integration, contract)
└── alembic/           # Database migrations

web/
├── app/               # Next.js App Router routes
├── components/        # Shared React components (server-first)
├── lib/               # Client/server utilities
└── tests/             # Jest + RTL suites
```

**Structure Decision**: Document the exact subdirectories touched by the feature and reference any new folders added to either `api/` or `web/`.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
