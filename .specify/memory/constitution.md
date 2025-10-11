<!--
Sync Impact Report:
Version change: 1.1.0 → 1.2.0
Modified principles:
- I. Dual-Stack Excellence (enhanced with Turbopack and development server specifications)
- III. Test-Driven Implementation (clarified test organization and location standards)
Added sections:
- VI. Professional Communication Standards (new principle for code quality and collaboration)
Removed sections: None
Templates requiring updates:
✅ plan-template.md (updated Constitution Check references)
✅ spec-template.md (aligned quality requirements)
✅ tasks-template.md (enhanced test organization guidelines)
✅ agent-file-template.md (synchronized with current constitution)
✅ CLAUDE.md (runtime guidance updated with latest standards)
Follow-up TODOs: None
-->

# Agentifui Pro Constitution

## Core Principles

### I. Dual-Stack Excellence
Every feature MUST maintain consistency across both frontend (Next.js/TypeScript) and backend (FastAPI/Python) stacks. All APIs must be properly typed with Pydantic models on the backend and corresponding TypeScript interfaces on the frontend. Cross-stack communication follows OpenAPI standards with automatic type generation.

**Development Environment**: Frontend development uses Turbopack (enabled by default) for optimal hot reload performance. Backend runs on port 8000, frontend on port 3000.

**Rationale**: Ensures type safety, reduces integration bugs, maintains development velocity across the full stack, and provides optimal developer experience with fast iteration cycles.

### II. Quality-First Development
Code quality is non-negotiable. All code MUST pass automated quality gates before entering the main branch:
- Python: Ruff linting and formatting (120 character line length)
- TypeScript: Dual-layer linting (oxlint + ESLint) with strict mode enabled
- Pre-commit hooks: Automated quality validation on all commits
- Type hints: Required for all Python function signatures and public functions/classes
- Type safety: No `any` types in TypeScript, full type coverage required
- Docstrings: Required for all public Python functions and classes
- Maximum cyclomatic complexity: 15 for TypeScript code

**Rationale**: Prevents technical debt accumulation and ensures consistent, maintainable codebase across team members.

### III. Test-Driven Implementation
All new features MUST follow test-first development with mandatory coverage requirements:
- Frontend: Jest + React Testing Library for component testing
- Backend: FastAPI test client for endpoint validation (minimum 80% coverage)
- Integration: Cross-stack communication validation tests required
- Accessibility: WCAG 2.1 AA compliance testing for all UI components
- Tests MUST pass before implementation is considered complete

**Test Organization Standards**:
- All tests MUST be in dedicated test directories (`tests/`, `__tests__/`, or `test/`)
- NEVER create test files next to source files (e.g., no `auth.test.js` next to `auth.js`)
- Backend tests: `api/tests/` directory structure (contract/, integration/, unit/)
- Frontend tests: `web/__tests__/` or `web/tests/` directory structure
- Check for existing test directories before creating new ones

**Rationale**: Ensures reliability, enables safe refactoring, catches regressions early in development cycle, maintains high code quality standards, and keeps codebase organized and navigable.

### IV. Internationalization by Design
All user-facing text MUST use the next-intl translation system with strict naming conventions:
- Translation keys: kebab-case matching component naming (`sign-in`, not `SignIn`)
- Single function: Always use `t('namespace.section.key')` format
- Server components: Import from `next-intl/server`
- Type safety: All translation keys are compile-time validated
- New features: Require translation namespace creation via `pnpm i18n:namespace`
- No hardcoded strings in UI components under any circumstances

**Rationale**: Enables global reach, maintains consistency, ensures type safety, and prevents costly retrofitting of internationalization.

### V. Convention Consistency
All naming conventions MUST be consistently applied across the monorepo:
- Files/directories: kebab-case for all frontend files and directories
- Translation keys: kebab-case matching component naming
- Commit messages: Conventional commit format in English (title required, body optional)
- Code comments: English only, minimal and purposeful (explain WHY, not WHAT)
- Import organization: Automatic sorting via Prettier plugin (React/Next.js → third-party → internal → relative)

**Rationale**: Reduces cognitive load, improves team efficiency, ensures predictable codebase navigation, and maintains professional communication standards.

### VI. Professional Communication Standards
All project communication and content MUST maintain professional standards:
- Language: All content in English (comments, commits, PRs, documentation)
- Code artifacts: Remove all `console.log` statements and `TODO` comments before PR submission
- Security: Never commit secrets or credentials - use environment variables exclusively
- Error handling: Use specific exceptions in Python, never bare `except:`
- Async operations: Prefer async/await for I/O operations in both Python and TypeScript

**Rationale**: Ensures global team collaboration, maintains production-ready code quality, prevents security vulnerabilities, and establishes consistent error handling patterns.

## Development Standards

### Technology Stack
All development MUST follow the established patterns documented in agent-specific context files. Technology stack is constrained to approved choices:
- Backend: Python 3.12+ with uv package manager, FastAPI framework
- Frontend: Node.js 20+ with pnpm@10.17.0, Next.js 15 with App Router, React 19
- Database: PostgreSQL 18+ (required for native `uuidv7()` function support)
- Testing: pytest (backend), Jest + React Testing Library (frontend)
- Styling: Tailwind CSS v4 utility-first framework

### Spec-Kit Workflow
All features MUST follow the Spec-Driven Development workflow:
1. **Feature Specification** (`/speckit.specify`): Define WHAT the feature does in natural language
2. **Implementation Planning** (`/speckit.plan`): Define HOW to implement with technical details
3. **Task Generation** (`/speckit.tasks`): Generate ordered, dependency-aware task lists
4. **Implementation** (`/speckit.implement`): Execute tasks following TDD principles and constitutional guidelines

Feature specifications are stored in `.specify/specs/###-feature-name/` with spec.md, plan.md, and tasks.md files. The constitution is referenced in all implementation plans via the Constitution Check section.

### Architecture Patterns
New dependencies require architecture review and documentation updates. All features must integrate with existing architecture patterns:
- Backend: FastAPI dependency injection for database sessions, async/await for I/O operations
- Frontend: Server Components preferred over Client Components, proper use of React hooks
- Database: Alembic migrations for all schema changes (never edit applied migrations)
- Error handling: Structured error responses with request tracing
- Routing: Next.js App Router only (no Pages Router)

## Quality Assurance

### Quality Gates
Code review is mandatory for all changes. Quality gates enforce multiple validation layers:
- Type checking: TypeScript strict mode + Python type hints on all function signatures
- Linting: Ruff (Python) + ESLint/oxlint (TypeScript) with caching enabled
- Formatting: Prettier (frontend) + Ruff (backend) with automatic import sorting
- Testing: Minimum 80% backend coverage, accessibility testing for all UI components
- Pre-commit validation: Husky with monorepo-aware hooks (workspace-specific linting)
- Performance monitoring: Bundle analysis required for frontend changes

### Pull Request Requirements
All Pull Requests MUST meet quality requirements before merge:
- Read `.github/pull_request_template.md` before creating PR
- All automated checks passing (linting, type checking, tests)
- No debugging artifacts (`console.log`, `TODO` comments in implementation code)
- Documentation updated for public API changes
- Breaking changes explicitly marked and justified
- PR template followed (summary, type checkboxes, issue linking with `Fixes #<number>`)
- All PR content in English (titles, descriptions, comments)

### Testing Standards
- Test isolation: Each test must be independent with automatic cache reset
- Database tests: Use PostgreSQL 18+ (real database, not SQLite mocks)
- Component testing: Test behavior, not implementation details
- User interaction: Test user flows and accessibility, not just rendering
- Test organization: All tests in dedicated directories, never next to source files

## Governance

This constitution supersedes all other development practices and establishes project-wide standards. Amendments require documentation updates, team approval, and migration plan for existing code.

### Compliance
All Pull Requests MUST verify compliance with constitutional principles. Complexity that violates simplicity principles must be explicitly justified in the Complexity Tracking section of implementation plans (`.specify/specs/###-feature-name/plan.md`).

### Agent-Specific Guidance
Use agent-specific context files for runtime development guidance and tool-specific instructions. These files are automatically updated by `.specify/scripts/bash/update-agent-context.sh` based on feature specifications:
- Claude Code: `CLAUDE.md`
- Gemini CLI: `GEMINI.md`
- GitHub Copilot: `.github/copilot-instructions.md`
- Cursor IDE: `.cursor/rules/specify-rules.mdc`
- Qwen Code: `QWEN.md`
- opencode/Codex: `AGENTS.md`
- Windsurf: `.windsurf/rules/specify-rules.md`
- Kilo Code: `.kilocode/rules/specify-rules.md`
- Auggie CLI: `.augment/rules/specify-rules.md`
- Roo Code: `.roo/rules/specify-rules.md`
- Amazon Q: `AGENTS.md`

### Amendment Process
Constitutional amendments follow semantic versioning:
- **MAJOR**: Backward incompatible governance/principle removals or redefinitions
- **MINOR**: New principles/sections added or materially expanded guidance
- **PATCH**: Clarifications, wording fixes, non-semantic refinements

All amendments MUST update the Sync Impact Report and propagate changes to dependent templates in `.specify/templates/`.

**Version**: 1.2.0 | **Ratified**: 2025-09-21 | **Last Amended**: 2025-10-11
