# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Architecture

**Agentifui Pro** is a modern monorepo with dual-stack architecture:
- **Backend (`api/`)**: FastAPI Python application managed by `uv`
- **Frontend (`web/`)**: Next.js 15 TypeScript application managed by `pnpm`

The backend runs on port 8000 with CORS configured for Next.js development server on localhost:3000.

## Code Standards & Guidelines

### Code Comments Policy
- **Language**: All comments MUST be written in English
- **Minimalism**: Comments should be written only when absolutely necessary
- **Focus**: Explain WHY, not WHAT the code does

### Naming Conventions
- **Components** (web/): Use kebab-case for all file and directory names
- **Translation Keys**: Use kebab-case to match component naming consistency
  - Correct: `t('common.navigation.home')`, `t('auth.sign-in.email')`
  - Incorrect: `t('common.Navigation.home')`, `t('auth.SignIn.email')`
- **Consistency**: All naming should follow the same case convention throughout the project

### Commit Convention
- **Format**: Follow conventional commit format with title only
- **Title**: Required - clear, concise description of changes
- **Body**: Optional - use only for complex changes that need explanation
- **Language**: All commit messages MUST be in English

Example:
```
feat: add bundle analyzer configuration
fix: resolve TypeScript compilation errors
```

## Internationalization (i18n)

**Architecture**: Next-intl with automated namespace management and type safety

### Quick Commands
```bash
cd web
pnpm i18n:locale <locale>     # Add new language (auto-detects common names)
pnpm i18n:namespace <name>    # Add feature namespace (updates types)
```

### Development Notes
- **Single t() function**: Always use `t('namespace.section.key')` format
- **Kebab-case keys**: Match component naming (`sign-in`, not `SignIn`)  
- **Server vs Client**: Import from `next-intl/server` for server components
- **Type safety**: All translation keys are compile-time validated
- **Details**: See `web/i18n/README.md` for complete documentation

## Development Commands

### Backend Development (api/)
```bash
# Run development server with hot reload
uv run --project api dev

# Lint and format Python code
uv run --project api ruff check --fix api/
uv run --project api ruff format api/

# Check without fixing
uv run --project api ruff check api/
```

### Frontend Development (web/)
```bash
cd web

# Code quality and analysis
pnpm lint                        # Comprehensive linting (oxlint + eslint with caching)
pnpm lint-complexity             # Check code complexity (max: 15)
pnpm eslint-fix                  # ESLint with auto-fix and caching
pnpm format                      # Prettier formatting
pnpm type-check                  # TypeScript checking
pnpm quality                     # Run all quality checks (type-check + lint + format:check)

# Testing
pnpm test                        # Run Jest tests
```

## Package Management & Tooling

### Python (Backend)
- **Manager**: `uv` (modern Python package manager)
- **Runtime**: Python >=3.12
- **Linting**: Ruff with extensive ruleset (120 char line length)
- **Dependencies**: FastAPI, Uvicorn, Pydantic

### TypeScript/JavaScript (Frontend) 
- **Manager**: `pnpm@10.15.0`
- **Runtime**: Node.js >=20.0.0
- **Framework**: Next.js 15 with App Router
- **Styling**: Tailwind CSS v4 with custom theme extensions
- **Testing**: Jest with React Testing Library and Happy DOM
- **Linting**: Dual-layer approach with oxlint (fast) + ESLint (comprehensive)
- **Formatting**: Prettier with import sorting
- **Bundle Analysis**: Webpack Bundle Analyzer for performance monitoring

## Code Quality Configuration

### Python Linting (api/.ruff.toml)
- Comprehensive ruleset including security, bugbear, and style rules
- Line length: 120 characters
- Excludes migrations, .venv, __pycache__
- Per-file ignores for __init__.py, configs/, tests/

### TypeScript Linting (web/eslint.config.mjs)
- Next.js recommended config + TypeScript
- Oxlint plugin integration for enhanced performance
- Caching enabled for faster subsequent runs
- Code complexity enforcement (max: 15)

### Import Organization
Frontend uses automatic import sorting via Prettier plugin:
- React/Next.js imports first
- Third-party packages
- Internal imports by type (@/types, @/lib, @/components, etc.)
- Relative imports last

## Pre-commit Hooks

The repository uses Husky with monorepo-aware pre-commit hooks that:
- Detect which workspace (api/ or web/) has changes
- Run appropriate linters only for modified code
- Apply automatic fixes where possible
- Enforce code quality before commits

## Testing Framework

### Frontend Testing Stack
- **Jest**: Testing framework with TypeScript support
- **React Testing Library**: Component testing utilities
- **Happy DOM**: Lightweight DOM implementation for faster tests
- **Coverage**: Comprehensive test coverage reporting

### Test Configuration
- `jest.config.ts`: Jest configuration with Next.js integration
- `jest.setup.ts`: Global test setup and utilities
- `__tests__/`: Test files location

## Key Files to Understand

- `api/main.py`: FastAPI application entry point with CORS middleware
- `web/app/`: Next.js App Router pages and layouts
- `web/i18n/config.ts`: Single source of truth for i18n configuration
- `web/types/i18n.d.ts`: Auto-generated i18n type definitions
- `api/.ruff.toml`: Python linting configuration
- `web/eslint.config.mjs`: TypeScript linting configuration
- `web/tailwind.config.ts`: Tailwind CSS configuration with theme extensions
- `web/jest.config.ts`: Jest testing configuration
- Root `package.json`: Monorepo scripts and husky configuration

## Pull Request Creation Guidelines

### Before Creating PRs
- **Always read PR template first**: Before using `gh pr create` or GitHub MCP to create PRs, you MUST read `.github/pull_request_template.md` to understand the required format and checklist
- **Follow template structure**: Use the template's format including summary, type checkboxes, and issue linking
- **All PRs in English**: Ensure all PR titles, descriptions, and comments are written in English