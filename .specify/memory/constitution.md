<!--
Sync Impact Report:
Version change: 1.0.1 → 1.1.0
Modified principles:
- I. Dual-Stack Excellence (enhanced with OpenAPI automation and type generation details)
- II. Quality-First Development (expanded with detailed quality gate requirements)
- III. Test-Driven Implementation (added specific coverage targets and accessibility standards)
- IV. Internationalization by Design (enhanced with type safety and namespace requirements)
- V. Convention Consistency (expanded with commit, comment, and import organization policies)
Added sections:
- Spec-Kit Workflow integration in Development Standards
- Enhanced PR requirements in Quality Assurance
Removed sections: None
Templates requiring updates:
✅ plan-template.md (Constitution Check section aligned)
✅ spec-template.md (quality requirements aligned)
✅ tasks-template.md (testing and TDD workflow aligned)
✅ agent-file-template.md (update-agent-context.sh compatible)
✅ CLAUDE.md (runtime guidance synchronized)
✅ .specify/README.md (spec-kit workflow documented)
Follow-up TODOs: None
-->

# Agentifui Pro Constitution

## Core Principles

### I. Dual-Stack Excellence
Every feature MUST maintain consistency across both frontend (Next.js/TypeScript) and backend (FastAPI/Python) stacks. All APIs must be properly typed with Pydantic models on the backend and corresponding TypeScript interfaces on the frontend. Cross-stack communication follows OpenAPI standards with automatic type generation.

**Rationale**: Ensures type safety, reduces integration bugs, and maintains development velocity across the full stack.

### II. Quality-First Development
Code quality is non-negotiable. All code MUST pass automated quality gates before entering the main branch:
- Python: Ruff linting and formatting (120 character line length)
- TypeScript: Dual-layer linting (oxlint + ESLint) with strict mode
- Pre-commit hooks: Automated quality validation on all commits
- Type hints: Required for all Python function signatures
- Type safety: No `any` types in TypeScript, full type coverage required

**Rationale**: Prevents technical debt accumulation and ensures consistent, maintainable codebase across team members.

### III. Test-Driven Implementation
All new features MUST follow test-first development with mandatory coverage requirements:
- Frontend: Jest + React Testing Library for component testing
- Backend: FastAPI test client for endpoint validation (minimum 80% coverage)
- Integration: Cross-stack communication validation tests required
- Accessibility: WCAG 2.1 AA compliance testing for all UI components
- Tests must pass before implementation is considered complete

**Rationale**: Ensures reliability, enables safe refactoring, catches regressions early in development cycle, and maintains high code quality standards.

### IV. Internationalization by Design
All user-facing text MUST use the next-intl translation system with strict naming conventions:
- Translation keys: kebab-case matching component naming (`sign-in`, not `SignIn`)
- Single function: Always use `t('namespace.section.key')` format
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

## Development Standards

### Technology Stack
All development MUST follow the established patterns documented in agent-specific context files. Technology stack is constrained to approved choices:
- Backend: Python 3.12+ with uv package manager, FastAPI framework
- Frontend: Node.js 20+ with pnpm, Next.js 15 with App Router, React 19
- Database: PostgreSQL 18+ (required for native `uuidv7()` function support)
- Testing: pytest (backend), Jest + React Testing Library (frontend)

### Spec-Kit Workflow
All features MUST follow the Spec-Driven Development workflow:
1. **Feature Specification** (`/specify`): Define WHAT the feature does in natural language
2. **Implementation Planning** (`/plan`): Define HOW to implement with technical details
3. **Task Generation** (`/tasks`): Generate ordered, dependency-aware task lists
4. **Implementation**: Execute tasks following TDD principles and constitutional guidelines

Feature specifications are stored in `.specify/specs/###-feature-name/` with spec.md, plan.md, and tasks.md files. The constitution is referenced in all implementation plans via the Constitution Check section.

### Architecture Patterns
New dependencies require architecture review and documentation updates. All features must integrate with existing architecture patterns:
- Backend: FastAPI dependency injection for database sessions, async/await for I/O operations
- Frontend: Server Components preferred over Client Components, proper use of React hooks
- Database: Alembic migrations for all schema changes (never edit applied migrations)
- Error handling: Structured error responses with request tracing

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
All Pull Requests must meet quality requirements before merge:
- All automated checks passing (linting, type checking, tests)
- No debugging artifacts (`console.log`, `TODO` comments in implementation code)
- Documentation updated for public API changes
- Breaking changes explicitly marked and justified
- PR template followed (summary, type checkboxes, issue linking)
- All PR content in English (titles, descriptions, comments)

### Testing Standards
- Test isolation: Each test must be independent with automatic cache reset
- Database tests: Use PostgreSQL 18+ (real database, not SQLite mocks)
- Component testing: Test behavior, not implementation details
- User interaction: Test user flows and accessibility, not just rendering

## Governance

This constitution supersedes all other development practices and establishes project-wide standards. Amendments require documentation updates, team approval, and migration plan for existing code.

### Compliance
All Pull Requests must verify compliance with constitutional principles. Complexity that violates simplicity principles must be explicitly justified in the Complexity Tracking section of implementation plans (`.specify/specs/###-feature-name/plan.md`).

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

All amendments must update the Sync Impact Report and propagate changes to dependent templates in `.specify/templates/`.

**Version**: 1.1.0 | **Ratified**: 2025-09-21 | **Last Amended**: 2025-10-05
