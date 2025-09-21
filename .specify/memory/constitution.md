<!--
Sync Impact Report:
Version change: [TEMPLATE] → 1.0.0
Modified principles: Initial creation with 5 core principles
Added sections: Core Principles, Development Standards, Quality Assurance, Governance
Removed sections: None (initial creation)
Templates requiring updates:
✅ plan-template.md (Constitution Check section compatible)
✅ spec-template.md (aligned with quality requirements)
✅ tasks-template.md (aligned with testing and development flow)
Follow-up TODOs: None
-->

# Agentifui Pro Constitution

## Core Principles

### I. Dual-Stack Excellence
Every feature MUST maintain consistency across both frontend (Next.js/TypeScript) and backend (FastAPI/Python) stacks. All APIs must be properly typed with Pydantic models on the backend and corresponding TypeScript interfaces on the frontend. Cross-stack communication follows OpenAPI standards with automatic type generation.

**Rationale**: Ensures type safety, reduces integration bugs, and maintains development velocity across the full stack.

### II. Quality-First Development
Code quality is non-negotiable. All code MUST pass automated quality gates: Python code uses Ruff for linting/formatting (120 char limit), TypeScript uses dual-layer linting (oxlint + ESLint), all commits go through pre-commit hooks. No code enters main branch without quality validation.

**Rationale**: Prevents technical debt accumulation and ensures consistent, maintainable codebase across team members.

### III. Test-Driven Implementation
All new features MUST follow test-first development. Frontend components require Jest + React Testing Library tests, backend endpoints require FastAPI test client validation. Integration tests validate cross-stack communication. Tests must pass before implementation is considered complete.

**Rationale**: Ensures reliability, enables safe refactoring, and catches regressions early in development cycle.

### IV. Internationalization by Design
All user-facing text MUST use the next-intl translation system with kebab-case keys matching component naming. New features require translation namespace creation via `pnpm i18n:namespace`. No hardcoded strings in UI components.

**Rationale**: Enables global reach, maintains consistency, and prevents costly retrofitting of internationalization.

### V. Convention Consistency
All naming conventions MUST be consistently applied: kebab-case for files/directories/translation keys, conventional commits in English, comments in English only when necessary. Pattern adherence across monorepo is mandatory.

**Rationale**: Reduces cognitive load, improves team efficiency, and ensures predictable codebase navigation.

## Development Standards

All development MUST follow the established patterns documented in CLAUDE.md. Technology choices are constrained to the approved stack: Python 3.12+ with uv, Node.js 20+ with pnpm, established testing frameworks. New dependencies require architecture review and documentation updates.

## Quality Assurance

Code review is mandatory for all changes. Quality gates include: type checking (TypeScript + mypy), linting (Ruff + ESLint/oxlint), formatting (Prettier + Ruff), testing (Jest + pytest), and pre-commit hook validation. Performance monitoring via bundle analysis is required for frontend changes.

## Governance

This constitution supersedes all other development practices. Amendments require documentation updates, team approval, and migration plan for existing code. All Pull Requests must verify compliance with these principles. Complexity that violates simplicity principles must be explicitly justified.

Use CLAUDE.md for runtime development guidance and tool-specific instructions.

**Version**: 1.0.0 | **Ratified**: 2025-09-21 | **Last Amended**: 2025-09-21