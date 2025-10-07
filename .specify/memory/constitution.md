<!--
Sync Impact Report:
- Version: 2.0.0 → 2.0.1 (PATCH: restore constitution from command template corruption + formatting fixes)
- Created: 2025-10-07
- Modified sections:
  * No principle changes - this is a restoration and formatting fix
  * Fixed YYYy typo in date format specification to YYYY
  * Whitespace cleanup in checklist template
  * Improved command template formatting consistency
- Context: The constitution file was accidentally replaced with the command template content.
  This restoration preserves the complete v2.0.0 content with minor formatting improvements.
- Templates status:
  ✅ .specify/templates/spec-template.md - No changes needed (already aligned)
  ✅ .specify/templates/plan-template.md - No changes needed (already aligned)
  ✅ .specify/templates/tasks-template.md - No changes needed (already aligned)
  ✅ .specify/templates/checklist-template.md - No changes needed (already aligned)
- Commands status:
  ✅ All speckit.* commands - Minor whitespace cleanup applied
  ✅ No constitutional principle changes affecting command logic
- Follow-up:
  * None - this is a maintenance patch
-->

# Agentifui Pro Constitution

## Core Principles

### I. Specification-First Development

**Rule**: All features MUST begin with a complete specification before any implementation.

**Requirements**:
- Feature specifications MUST define WHAT and WHY, never HOW (implementation details)
- Specifications MUST be technology-agnostic and understandable by non-technical stakeholders
- Success criteria MUST be measurable and verifiable without knowing implementation
- User stories MUST be prioritized (P1, P2, P3) and independently testable
- Maximum 3 NEEDS CLARIFICATION markers allowed per specification

**Rationale**: Specifications provide a shared understanding between stakeholders and developers,
reducing rework and misalignment. Technology-agnostic specs allow for flexible implementation
choices.

### II. User-Story-Driven Organization

**Rule**: Features MUST be organized by user stories with clear priorities, not technical layers.

**Requirements**:
- Each user story MUST be independently implementable and testable
- Stories MUST be prioritized by value (P1 = MVP, P2/P3 = enhancements)
- Implementation tasks MUST be grouped by story, not by technical concern
- Each story MUST deliver standalone value that can be demonstrated

**Rationale**: User-story organization enables incremental delivery, early feedback, and MVP-first
development. It aligns technical work with business value.

### III. Dual-Stack Excellence

**Rule**: Every feature MUST maintain consistency across both frontend (Next.js/TypeScript) and
backend (FastAPI/Python) stacks.

**Requirements**:
- All APIs must be properly typed with Pydantic models on the backend
- Corresponding TypeScript interfaces required on the frontend
- Cross-stack communication follows OpenAPI standards
- Automatic type generation where possible

**Rationale**: Ensures type safety, reduces integration bugs, and maintains development velocity
across the full stack.

### IV. Quality Validation Gates

**Rule**: Each phase MUST pass quality checks before proceeding to the next.

**Requirements**:
- Specifications MUST pass quality checklist before planning (completeness, clarity, testability)
- Plans MUST pass constitution check before task generation (compliance with principles)
- Checklists MUST be reviewed before implementation starts
- All clarifications MUST be resolved before planning
- Code MUST pass automated quality gates:
  * Python: Ruff linting and formatting (120 character line length)
  * TypeScript: Dual-layer linting (oxlint + ESLint) with strict mode
  * Type hints required for all Python function signatures
  * No `any` types in TypeScript, full type coverage required

**Rationale**: Early quality gates catch issues when they're cheapest to fix, reducing downstream
rework and ensuring alignment with project standards.

### V. Test-Driven Pragmatism

**Rule**: Tests are included when explicitly required or for critical functionality.

**Requirements**:
- Tests MUST be explicitly requested in specification or feature requirements
- When included, tests MUST be written before implementation (TDD)
- **Backend**: 80% minimum coverage when tests are included
- **Frontend**: Jest + React Testing Library for behavior testing
- **Integration**: Required for API contracts, inter-service communication, shared schemas
- **Accessibility**: WCAG 2.1 AA compliance testing for all UI components
- Contract tests MUST be included for API changes affecting external consumers

**Rationale**: Pragmatic test strategy allocates testing effort where it adds most value while
maintaining high quality standards for critical functionality.

### VI. Internationalization by Design

**Rule**: All user-facing text MUST use the next-intl translation system with strict naming
conventions.

**Requirements**:
- Translation keys: kebab-case matching component naming (`sign-in`, not `SignIn`)
- Single function: Always use `t('namespace.section.key')` format
- Type safety: All translation keys are compile-time validated
- New features: Require translation namespace creation via `pnpm i18n:namespace`
- No hardcoded strings in UI components under any circumstances

**Rationale**: Enables global reach, maintains consistency, ensures type safety, and prevents
costly retrofitting of internationalization.

### VII. Phase-Structured Workflow

**Rule**: Implementation planning MUST follow structured phases with clear outputs.

**Requirements**:
- **Phase 0 (Research)**: Resolve all NEEDS CLARIFICATION, document decisions
- **Phase 1 (Design)**: Generate data-model.md, contracts/, quickstart.md
- **Phase 2 (Tasks)**: Create dependency-ordered, priority-grouped task list
- **Phase 3 (Implementation)**: Execute tasks with progress tracking and validation

Each phase MUST produce artifacts before the next phase begins.

**Rationale**: Structured phases ensure thorough planning before coding, reducing technical debt
and architectural rework.

### VIII. Convention Consistency

**Rule**: All naming conventions MUST be consistently applied across the monorepo.

**Requirements**:
- Files/directories: kebab-case for all frontend files and directories
- Translation keys: kebab-case matching component naming
- Commit messages: Conventional commit format in English (title required, body optional)
- Code comments: English only, minimal and purposeful (explain WHY, not WHAT)
- Import organization: Automatic sorting via Prettier plugin (React/Next.js → third-party →
  internal → relative)

**Rationale**: Reduces cognitive load, improves team efficiency, ensures predictable codebase
navigation, and maintains professional communication standards.

### IX. Constitution Authority

**Rule**: This constitution is NON-NEGOTIABLE and supersedes all other practices.

**Requirements**:
- All specifications, plans, and tasks MUST comply with constitutional principles
- Constitution violations are automatically CRITICAL and block implementation
- Constitution amendments require explicit update, version bump, and propagation
- Analysis tools MUST check for constitution compliance

**Rationale**: Constitutional authority ensures consistent quality and prevents ad-hoc deviations
that accumulate technical debt.

## Development Standards

### Technology Stack

**Backend**: Python 3.12+ with uv package manager, FastAPI framework
- Ruff linting with 120 char line length
- Type hints required for all function signatures
- Async patterns preferred for I/O operations
- PostgreSQL 18+ required (native `uuidv7()` function support)
- Alembic migrations for all schema changes

**Frontend**: Node.js 20+ with pnpm, Next.js 15 with App Router, React 19
- Strict TypeScript mode enabled
- App Router only (no Pages Router)
- Kebab-case for files and translation keys
- Maximum cyclomatic complexity: 15
- Server Components preferred over Client Components

### Security Requirements

- No secrets in code (environment variables only)
- Input validation with Pydantic/Zod
- No raw SQL with user input (ORM only)
- CORS properly configured
- JWT authentication with proper expiration
- Rate limiting for public endpoints

### Pre-commit Quality Gates

- Husky hooks enforce quality before commits
- Workspace-aware linting (api/ or web/)
- Automatic fixes applied where possible
- Commits blocked if quality checks fail

## Spec-Kit Workflow

All features MUST follow the Spec-Driven Development workflow:

1. `/speckit.constitution` - Define or update project principles
2. `/speckit.specify` - Create feature specification with quality validation
3. `/speckit.clarify` - Resolve ambiguities (≤3 clarifications, interactive)
4. `/speckit.plan` - Execute Phase 0/1, generate design artifacts
5. `/speckit.tasks` - Generate priority-grouped task list
6. `/speckit.implement` - Execute implementation with checklist validation
7. `/speckit.analyze` - Cross-artifact consistency analysis (optional)
8. `/speckit.checklist` - Custom quality checklists (optional)

Feature specifications are stored in `specs/###-feature-name/` with spec.md, plan.md, tasks.md,
and optional artifacts (research.md, data-model.md, contracts/, quickstart.md).

## Quality Assurance

### Pull Request Requirements

Before creating PRs:
- Read `.github/pull_request_template.md` to understand required format
- Follow template structure (summary, type checkboxes, issue linking)
- All PR titles, descriptions, and comments MUST be in English

Quality requirements:
- All checks must pass (linting, type checking, tests)
- No console.log statements
- No TODO comments (create issues instead)
- Documentation updates for public API changes
- Breaking changes explicitly marked and justified

### Code Review

- Code review is mandatory for all changes
- Type checking: TypeScript strict mode + Python type hints
- Performance monitoring: Bundle analysis for frontend changes
- Test isolation: Each test independent with automatic cache reset

## Governance

### Amendment Process

1. Propose change with rationale and version bump type (MAJOR/MINOR/PATCH)
2. Validate impact on templates, commands, and existing features
3. Update constitution and propagate changes to dependent artifacts
4. Create Sync Impact Report documenting all changes
5. Commit with clear message: `docs: amend constitution to vX.Y.Z (description)`

### Versioning Policy

- **MAJOR**: Backward-incompatible principle removals or redefinitions
- **MINOR**: New principles or materially expanded guidance
- **PATCH**: Clarifications, wording fixes, non-semantic refinements

### Compliance Review

- All PRs MUST verify constitution compliance
- `/speckit.analyze` MUST flag constitution violations as CRITICAL
- Violations MUST be resolved before merge, not waived
- Constitution principles MUST be enforced by tooling, not manual review
- Complexity violations must be explicitly justified in plan.md Complexity Tracking section

### Runtime Guidance

Development guidance is provided through:
- `CLAUDE.md` - Project-specific AI agent instructions
- `.specify/templates/` - Workflow templates for specs, plans, tasks, checklists
- `.specify/scripts/bash/` - Automation scripts for prerequisite checking and setup

**Version**: 2.0.1 | **Ratified**: 2025-09-21 | **Last Amended**: 2025-10-07
