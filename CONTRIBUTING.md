# Contributing to Agentifui Pro

## Project Introduction

**Agentifui Pro** is a modern monorepo featuring:
- **Backend**: FastAPI (Python >=3.12) managed by `uv`
- **Frontend**: Next.js 15 (TypeScript) managed by `pnpm`

## Contributing Rules

### Language Requirements
- **All content MUST be in English**: comments, commits, PRs, documentation

### Commit Convention
Follow [Conventional Commits](https://www.conventionalcommits.org/):
```
feat: add user authentication
fix: resolve build errors
docs: update API guide
```

### Code Quality Standards

**Python (Backend)**:
- Line length: 120 characters
- Use Ruff for linting/formatting
- Type hints required

**TypeScript (Frontend)**:
- Maximum complexity: 15
- Strict TypeScript configuration
- Auto-sorted imports

### Workflow Requirements

1. **Issue-first**: Link PR to issue with `Fixes #<number>`
2. **Quality checks**: All linting and tests must pass
3. **Branch naming**: `feature/`, `fix/`, `docs/` prefixes
4. **Review required**: One approval needed

### Comment Policy
- Minimal comments, only when necessary
- Explain WHY, not WHAT
- Clear, concise English

---

See `CLAUDE.md` for detailed development commands and project architecture.