# Agentifui Pro

A modern full-stack monorepo with enterprise-grade tooling and development practices.

## Architecture

**Dual-stack monorepo** with:

- **Backend (`api/`)**: FastAPI + Python >=3.11 managed by `uv`
- **Frontend (`web/`)**: Next.js 15 + TypeScript + React 19 managed by `pnpm`

## Tech Stack

### Backend

- **FastAPI**: Modern Python web framework
- **uv**: Ultra-fast Python package manager
- **Ruff**: Lightning-fast Python linter and formatter
- **Pydantic**: Data validation and settings management

### Frontend

- **Next.js 15**: React framework with App Router
- **TypeScript**: Static type checking
- **Tailwind CSS v4**: Utility-first CSS framework
- **Jest**: Testing framework with React Testing Library
- **ESLint + Oxlint**: Dual-layer linting for performance

## Quick Start

### Prerequisites

- Node.js ≥20.0.0
- Python ≥3.11
- pnpm@10.17.0

### Backend

```bash
cd api
uv run --project api dev
```

### Frontend

```bash
cd web
pnpm dev
pnpm test
```

## Development Scripts

See project documentation for comprehensive command reference and development guidelines.

## Code Standards

- **Comments**: English only, minimal and purposeful
- **Commits**: Conventional format, English titles only
- **Code Quality**: Enforced via pre-commit hooks and CI
