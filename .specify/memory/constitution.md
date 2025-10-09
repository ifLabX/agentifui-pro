# Agentifui Pro Constitution

<!--
SYNC IMPACT REPORT
==================
Version Change: Initial → 1.0.0
Rationale: Initial constitution establishment for Agentifui Pro monorepo

Modified Principles:
- NEW: I. Monorepo Consistency - Ensures frontend/backend alignment
- NEW: II. Type Safety First - TypeScript strict mode + Python type hints
- NEW: III. Test-First Development (NON-NEGOTIABLE) - Mandatory TDD with 80% coverage
- NEW: IV. English-Only Communication - All code, comments, commits in English
- NEW: V. Convention Over Configuration - Follow established patterns

Added Sections:
- Core Principles (5 principles)
- Quality Standards (testing, code quality, internationalization)
- Development Workflow (branch strategy, PR requirements, quality gates)
- Governance (versioning, compliance, amendments)

Templates Status:
✅ plan-template.md - Constitution Check section references this file
✅ spec-template.md - User stories and requirements align with principles
✅ tasks-template.md - Task structure supports TDD and parallel execution
⚠️ No command files found yet - future commands should reference this constitution

Follow-up TODOs: None - all placeholders filled with concrete values
-->

## Core Principles

### I. Monorepo Consistency

**Principle**: Frontend and backend MUST maintain structural and conceptual alignment while respecting their technical boundaries.

**Rules**:
- Shared concepts (auth, user entities, API contracts) MUST use consistent naming across stacks
- Breaking changes in API contracts require coordinated frontend/backend updates
- Port allocation is fixed: backend=8000, frontend=3000
- Environment-specific configurations MUST use separate files (.env.local, .env.production)
- No cross-stack imports - backend and frontend remain independently deployable

**Rationale**: Monorepo architecture provides coordination benefits without sacrificing independent deployability. Consistency reduces cognitive overhead when context-switching between stacks while maintaining clear separation of concerns.

### II. Type Safety First

**Principle**: All code MUST be statically typed with zero tolerance for type escape hatches.

**Rules**:
- **TypeScript (Frontend)**: Strict mode enabled, no `any` types permitted
- **Python (Backend)**: Type hints required for all function signatures and public APIs
- **Component Props**: Must be typed with interfaces, not inline types
- **API Contracts**: Shared type definitions or OpenAPI schema validation required
- Maximum cyclomatic complexity: 15 per function/method
- Type checking MUST pass before commits are allowed

**Rationale**: Type safety catches entire classes of bugs at compile time rather than runtime. Explicit types serve as machine-verified documentation and enable confident refactoring. The short-term cost of typing is recovered many times over through reduced debugging and maintenance burden.

### III. Test-First Development (NON-NEGOTIABLE)

**Principle**: Tests MUST be written before implementation code in a strict Red-Green-Refactor cycle.

**Rules**:
- Write test → Verify test fails (Red) → Implement minimum code to pass (Green) → Refactor for quality
- Backend MUST maintain minimum 80% test coverage
- Frontend tests required for all business logic and critical user flows
- Contract tests required for API boundary changes
- Integration tests required for cross-service communication
- No merging to main without all tests passing
- No disabling/skipping tests to achieve "green" status

**Rationale**: Test-First is non-negotiable because it fundamentally changes design quality - code written to be testable is better factored, more modular, and has clearer interfaces. Tests written after implementation often just verify existing behavior (good or bad) rather than driving good design. The practice catches bugs earlier when they cost 10-100x less to fix.

### IV. English-Only Communication

**Principle**: All technical communication MUST be in English to ensure global accessibility and professional standards.

**Rules**:
- Code: Variables, functions, classes, modules - English names only
- Comments: English only, minimal and purposeful (explain WHY not WHAT)
- Commits: Conventional format with English titles (body optional)
- Pull Requests: Titles, descriptions, review comments - English only
- Documentation: README, guides, API docs - English only
- User-facing content: Use i18n system (next-intl) with kebab-case keys

**Rationale**: English is the lingua franca of software development. Consistent language use enables global collaboration, code reuse across projects, and easier onboarding. Comments in other languages create barriers for international teams and limit knowledge sharing.

### V. Convention Over Configuration

**Principle**: Follow established project patterns and conventions unless there is compelling reason to deviate.

**Rules**:
- **Frontend Naming**: Kebab-case for all files and directories
- **Backend Naming**: Snake_case for Python modules, PascalCase for classes
- **Translation Keys**: Kebab-case format `t('namespace.section.key')`
- **Line Length**: 120 characters for Python, Prettier defaults for TypeScript
- **Import Organization**: Automatic via tools (Prettier plugin for TS, Ruff for Python)
- Check existing patterns before adding new files or structures
- Document deviations in PR descriptions with clear rationale

**Rationale**: Consistency reduces cognitive load and makes codebases scannable. Developers spend more time reading code than writing it - predictable structure accelerates comprehension. Conventions encode accumulated team wisdom and prevent bikeshedding on solved problems.

## Quality Standards

### Testing Requirements

**Backend (Python + pytest)**:
- Minimum 80% code coverage enforced
- Test categories: unit (fast, isolated), integration (database/external services), contract (API boundaries)
- Async operations MUST be tested with pytest-asyncio
- Use specific exception assertions, never bare `except:`
- Mock external dependencies, never call real third-party APIs in tests

**Frontend (TypeScript + Jest)**:
- Business logic MUST have unit tests
- Critical user flows MUST have integration tests
- Component props and state transitions MUST be tested
- No snapshot tests as primary validation (too brittle)
- Use React Testing Library principles (test behavior not implementation)

### Code Quality Gates

**Linting & Formatting**:
- Backend: Ruff (check + format) MUST pass with zero warnings
- Frontend: ESLint + Oxlint dual-layer MUST pass with zero warnings
- Formatting: Automatic via pre-commit hooks (Prettier for TS, Ruff for Python)
- No commits allowed with linting failures

**Type Checking**:
- Backend: mypy (or equivalent) MUST pass for all typed code
- Frontend: `pnpm type-check` MUST pass with zero errors
- No gradual typing escape hatches (no `# type: ignore` without documented justification)

**Code Review**:
- All PRs require approval from at least one team member
- Reviewers MUST verify constitution compliance
- Complexity violations MUST be justified with specific rationale
- No console.log or TODO comments in merged code

### Internationalization (i18n)

**Requirements**:
- All user-facing text MUST use next-intl translation system
- Translation keys use kebab-case: `t('common.navigation.home')`
- Server components import from `next-intl/server`, client components from `next-intl`
- New languages: `pnpm i18n:locale <locale>` (adds language files)
- New features: `pnpm i18n:namespace <name>` (creates feature translation namespace)

**Structure**:
```
web/messages/
├── en.json          # English (default)
├── zh-CN.json       # Simplified Chinese
└── [locale].json    # Additional languages
```

## Development Workflow

### Branch Strategy

**Branch Types**:
- `main`: Production-ready code, protected, requires PR
- `feature/###-name`: Feature branches from main
- `fix/###-name`: Bug fix branches from main
- `refactor/name`: Refactoring branches from main

**Branch Naming**:
- Use issue number prefix when available: `feature/42-user-auth`
- Use descriptive kebab-case: `feature/add-dark-mode`
- Keep names concise but meaningful

### Pull Request Requirements

**Before Creating PR**:
- Read `.github/pull_request_template.md` and follow structure
- Link to issue with `Fixes #<number>` or `Closes #<number>`
- Ensure all quality checks pass (lint, type-check, tests)
- Remove debug code (console.log, print statements, debugger)
- Remove TODO comments (convert to issues or complete)
- Verify i18n keys follow kebab-case convention

**PR Content**:
- Title: Conventional commit format (`feat:`, `fix:`, `refactor:`, etc.)
- Description: English only, context and approach summary
- Screenshots: For UI changes
- Breaking changes: Clearly documented with migration path
- Test evidence: Coverage reports or test execution confirmation

### Quality Gates

**Pre-Commit**:
- Automated formatting (Prettier, Ruff)
- Linting (ESLint, Oxlint, Ruff)
- Type checking (TypeScript strict mode, Python type hints)

**Pre-Push**:
- All tests passing
- No linting errors
- Type checking passing
- Build succeeds

**Pre-Merge**:
- PR approval from reviewer
- CI pipeline green (all checks passing)
- No unresolved review comments
- Branch up-to-date with main

## Technical Constraints

### Required Technology Versions

**Backend**:
- Python ≥3.12 (required)
- PostgreSQL ≥18 (uses native `uuidv7()` function)
- FastAPI (latest stable)
- uv (package management)

**Frontend**:
- Node.js ≥20.0.0 (required)
- pnpm@10.17.0 (exact version for workspace management)
- Next.js 15 with App Router only (no Pages Router)
- React 19
- TypeScript 5.x in strict mode

### Architecture Constraints

**Frontend**:
- Prefer Server Components over Client Components (RSC-first approach)
- Client Components only when necessary (interactivity, hooks, browser APIs)
- No Pages Router patterns - App Router only
- Route handlers in `app/api/` for API routes

**Backend**:
- Prefer async/await for I/O operations (database, HTTP, file system)
- Use Pydantic models for request/response validation
- Alembic for database migrations
- Environment variables for configuration (no secrets in code)

**Database**:
- PostgreSQL 18+ required (native UUID v7 support)
- Alembic migrations for schema changes
- Foreign key constraints enforced
- Indexing strategy documented for performance-critical queries

### Security Requirements

**Secrets Management**:
- No secrets, API keys, or credentials in code or version control
- Use environment variables (.env.local for development, platform-specific for production)
- .env files MUST be in .gitignore
- Document required environment variables in .env.example

**Code Security**:
- No SQL injection vulnerabilities (use parameterized queries/ORMs)
- Input validation on all API endpoints (Pydantic models)
- Output encoding to prevent XSS
- CORS configured appropriately for production
- Authentication/authorization required for protected endpoints

## Governance

### Constitution Authority

This constitution supersedes all other development practices and guidelines. When conflicts arise between this document and other sources (README, team conventions, external style guides), this constitution takes precedence.

### Amendment Process

**Minor Amendments** (clarifications, wording improvements, non-semantic changes):
- Propose change in PR with clear rationale
- Team discussion and approval
- Update constitution and increment PATCH version
- Communicate changes to team

**Major Amendments** (new principles, removed constraints, breaking changes):
- Create RFC (Request for Comments) document with proposal
- Team review period (minimum 1 week)
- Approval from majority of active contributors
- Create migration plan for affected code
- Update constitution and increment MAJOR or MINOR version
- Communicate changes and migration plan to team

### Versioning Policy

Constitution uses semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Backward-incompatible changes (principle removals, complete redefinitions)
- **MINOR**: New principles added, sections materially expanded, new requirements
- **PATCH**: Clarifications, wording improvements, typo fixes, formatting

### Compliance Review

**Code Review Checklist**:
- Does this PR follow the Core Principles?
- Are type hints/interfaces properly defined?
- Were tests written before implementation?
- Is English used consistently?
- Do naming conventions match project standards?
- Are quality gates passing?

**Complexity Justification**:
When violating constitution principles (e.g., exceeding complexity limits, using `any` types, skipping tests):
- Document specific rationale in PR description
- Propose plan to remove violation in future
- Get explicit approval from reviewers
- Add technical debt issue if deferring remediation

### Runtime Development Guidance

For AI-assisted development (Claude Code, GitHub Copilot, etc.), refer to:
- `CLAUDE.md` - Claude Code specific guidance and commands
- `.github/pull_request_template.md` - PR structure requirements
- Individual service READMEs - Service-specific setup and conventions

**Version**: 1.0.0 | **Ratified**: 2025-01-09 | **Last Amended**: 2025-01-09
