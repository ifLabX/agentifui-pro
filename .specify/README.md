# Spec-Kit Workflow

This directory contains the spec-kit configuration for Agentifui Pro, enabling Spec-Driven Development (SDD) workflow.

## Core Commands

### 1. Define Application Features (`/specify`)
Describe **what** you want to build in natural language:

```
/specify Build a user authentication system with email/password login, 
password reset functionality, and user profile management.
```

### 2. Create Technical Plan (`/plan`)
Define **how** to implement the feature with technical details:

```
/plan Use FastAPI for backend authentication with JWT tokens, 
bcrypt for password hashing, and Next.js frontend with 
server-side session management.
```

### 3. Execute Implementation (`implement`)
Run the implementation based on the generated plan:

```bash
implement specs/002-auth-system/plan.md
```

## Directory Structure

```
.specify/
├── memory/
│   └── constitution.md          # Project constitution and guidelines
├── scripts/bash/               # Automation scripts
│   ├── common.sh
│   ├── setup-plan.sh
│   ├── check-task-prerequisites.sh
│   ├── create-new-feature.sh
│   └── update-agent-context.sh
├── templates/                  # Template files
│   ├── spec-template.md
│   ├── plan-template.md
│   ├── tasks-template.md
│   └── agent-file-template.md
└── specs/                      # Generated specifications (auto-created)
    └── 001-feature-name/
        ├── spec.md
        ├── plan.md
        └── tasks.md
```

## Workflow Example

1. **Specify Feature**:
   ```
   /specify Create a task management dashboard with drag-and-drop 
   Kanban boards, real-time updates, and team collaboration features.
   ```

2. **Plan Implementation**:
   ```
   /plan Use Next.js 15 with App Router, FastAPI backend, 
   PostgreSQL database, and WebSocket for real-time updates.
   ```

3. **Execute**:
   ```bash
   implement specs/003-task-dashboard/plan.md
   ```

## Integration with Current Project

This spec-kit setup is configured to work with:
- **Backend**: FastAPI (Python) in `/api`
- **Frontend**: Next.js 15 (TypeScript) in `/web`
- **AI Agent**: Claude Code integration
- **Scripts**: Bash automation for streamlined workflow

## Best Practices

- Start with clear feature descriptions using `/specify`
- Include technical constraints and stack preferences in `/plan`
- Review generated specifications before implementation
- Use the constitution to maintain consistency across features
- Leverage automation scripts for repetitive tasks

For more details, see the [official spec-kit documentation](https://github.com/github/spec-kit).