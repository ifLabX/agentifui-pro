# Spec-Kit Workflow

Spec-Driven Development (SDD) for Agentifui Pro, powered by [spec-kit v0.0.57](https://github.com/github/spec-kit).

## Quick Start

### 1. Define Project Principles (`/speckit.constitution`)

Establish or update your project's constitutional principles:

```
/speckit.constitution
```

### 2. Create Feature Specification (`/speckit.specify`)

Describe **what** you want to build in natural language:

```
/speckit.specify Build a user authentication system with email/password login,
password reset functionality, and user profile management.
```

**What this does**:
- Creates feature branch and directory structure
- Generates specification with quality validation
- Creates requirements checklist automatically
- Limits clarifications to 3 critical questions max

### 3. Clarify Ambiguities (`/speckit.clarify`)

Resolve underspecified areas interactively (optional but recommended):

```
/speckit.clarify
```

**What this does**:
- Identifies ambiguous requirements
- Asks up to 10 targeted clarification questions (max 5 at a time)
- Updates spec with answers in real-time
- Validates completeness before proceeding

### 4. Create Technical Plan (`/speckit.plan`)

Define **how** to implement with structured phases:

```
/speckit.plan Use FastAPI for backend authentication with JWT tokens,
bcrypt for password hashing, and Next.js frontend with
server-side session management.
```

**What this does**:
- **Phase 0**: Research and resolve technical unknowns
- **Phase 1**: Generate data-model.md, contracts/, quickstart.md
- Constitution check validation
- Updates AI agent context automatically

### 5. Generate Task List (`/speckit.tasks`)

Create priority-grouped, dependency-ordered tasks:

```
/speckit.tasks
```

**What this does**:
- Organizes tasks by user story priority (P1, P2, P3)
- Each story is independently implementable and testable
- Marks parallelizable tasks with [P]
- Tests are optional (included only when specified)
- Generates MVP-first implementation strategy

### 6. Execute Implementation (`/speckit.implement`)

Run the implementation with validation:

```
/speckit.implement
```

**What this does**:
- Checks all checklists are complete (or prompts to proceed)
- Executes tasks phase by phase
- Tracks progress and marks completed tasks
- Validates implementation against specification

### 7. Quality Analysis (`/speckit.analyze`)

Cross-artifact consistency validation (optional):

```
/speckit.analyze
```

**What this does**:
- Validates spec.md, plan.md, and tasks.md consistency
- Checks constitution compliance (flags violations as CRITICAL)
- Identifies coverage gaps and ambiguities
- Provides remediation recommendations

### 8. Custom Checklists (`/speckit.checklist`)

Generate custom quality checklists (optional):

```
/speckit.checklist Create a security checklist for authentication features
```

## Directory Structure

```
.specify/
├── memory/
│   └── constitution.md              # Project constitutional principles
├── scripts/bash/                    # Automation scripts
│   ├── check-prerequisites.sh       # Unified prerequisite validation
│   ├── common.sh                    # Shared functions library
│   ├── create-new-feature.sh        # Feature initialization
│   ├── setup-plan.sh                # Planning environment setup
│   └── update-agent-context.sh      # AI agent context updater
├── templates/                       # Workflow templates
│   ├── spec-template.md             # Feature specification template
│   ├── plan-template.md             # Implementation plan template
│   ├── tasks-template.md            # Task list template
│   └── checklist-template.md        # Quality checklist template
└── specs/                           # Generated specifications (auto-created)
    └── ###-feature-name/
        ├── spec.md                  # Feature specification
        ├── plan.md                  # Implementation plan
        ├── tasks.md                 # Task list
        ├── research.md              # Phase 0 research (optional)
        ├── data-model.md            # Phase 1 data model (optional)
        ├── contracts/               # Phase 1 API contracts (optional)
        ├── quickstart.md            # Phase 1 quickstart guide (optional)
        └── checklists/              # Custom checklists (optional)
```

## Workflow Comparison

### Legacy Commands (Removed)
```
❌ /specify → /clarify → /plan → /tasks → /implement
```

### Spec-Kit v0.0.57 (Current)
```
✅ /speckit.constitution → /speckit.specify → /speckit.clarify →
   /speckit.plan → /speckit.tasks → /speckit.implement →
   /speckit.analyze (optional) + /speckit.checklist (optional)
```

## Key Differences

| Feature | Legacy | Spec-Kit v0.0.57 |
|---------|--------|------------------|
| **Quality Validation** | None | Automatic checklist generation |
| **Clarifications** | Unlimited | Max 3 NEEDS CLARIFICATION markers |
| **Task Organization** | Technical layers | User story priorities (P1/P2/P3) |
| **Testing** | Mandatory | Optional (only when needed) |
| **Workflow Structure** | Linear | Phase-based (Phase 0/1/2/3) |
| **Constitution Check** | Manual | Automated in every analysis |

## Integration with Agentifui Pro

This spec-kit setup is configured to work with:
- **Backend**: FastAPI (Python 3.12+) in `/api`, managed by `uv`
- **Frontend**: Next.js 15 (TypeScript/React 19) in `/web`, managed by `pnpm`
- **Database**: PostgreSQL 18+ (native uuidv7 support)
- **AI Agent**: Claude Code with constitutional guidance
- **Quality**: Dual-layer linting (Ruff + oxlint/ESLint), pre-commit hooks

## Best Practices

### Specification Phase
- Start with clear, natural language feature descriptions
- Focus on WHAT and WHY, never HOW (implementation details)
- Prioritize user stories by value (P1 = MVP first)
- Limit clarifications to truly critical questions (≤3)
- Ensure specifications are technology-agnostic

### Planning Phase
- Include technical constraints and stack preferences
- Document research decisions in research.md
- Generate complete API contracts in contracts/
- Create realistic quickstart scenarios
- Run constitution check before task generation

### Implementation Phase
- Review and complete all checklists before starting
- Work on P1 stories first (MVP-first approach)
- Execute tasks in dependency order
- Mark tasks complete as you finish them
- Validate against original specification

### Quality Phase
- Run `/speckit.analyze` before major milestones
- Address CRITICAL constitution violations immediately
- Keep specifications and implementation in sync
- Use custom checklists for domain-specific quality

## Constitution Highlights

Agentifui Pro follows 9 core principles:

1. **Specification-First Development** - Complete specs before any code
2. **User-Story-Driven Organization** - Organize by value, not technical layers
3. **Dual-Stack Excellence** - Type-safe frontend + backend integration
4. **Quality Validation Gates** - Automated quality checks at every phase
5. **Test-Driven Pragmatism** - Tests only when needed, TDD when included
6. **Internationalization by Design** - next-intl with kebab-case keys
7. **Phase-Structured Workflow** - Research → Design → Tasks → Implementation
8. **Convention Consistency** - Uniform naming, commits, and code style
9. **Constitution Authority** - Principles are non-negotiable, tool-enforced

See `.specify/memory/constitution.md` for complete details.

## Common Workflows

### Starting a New Feature
```bash
/speckit.specify "Add real-time notifications for user activities"
# Follow prompts, answer clarification questions
/speckit.plan "Use WebSocket with FastAPI, Next.js client with EventSource"
/speckit.tasks
/speckit.implement
```

### Improving an Existing Feature
```bash
/speckit.analyze  # Check current state
/speckit.specify "Enhance notification system with email digest option"
# Continue with plan → tasks → implement
```

### Adding Custom Quality Checks
```bash
/speckit.checklist Create performance checklist for API endpoints
# Review and complete checklist items
/speckit.implement  # Checklist validation included
```

## Troubleshooting

**Q: "No critical ambiguities detected" but specification seems incomplete**
- This is expected for well-defined features
- Run `/speckit.clarify` again if you identify gaps later
- Remember: limit is 3 NEEDS CLARIFICATION markers

**Q: Implementation fails checklist validation**
- Complete all checklist items before proceeding
- Or explicitly confirm to proceed anyway (not recommended)
- Use `/speckit.checklist` to generate additional quality checks

**Q: Constitution violations flagged as CRITICAL**
- These MUST be resolved, not waived
- Update specification/plan to comply with principles
- Or propose constitution amendment (requires justification)

**Q: Tasks seem too granular/not granular enough**
- Adjust level of detail in plan.md before running `/speckit.tasks`
- Use data-model.md and contracts/ for better task generation
- Re-run `/speckit.tasks` after plan updates

## Resources

- [Spec-Kit GitHub Repository](https://github.com/github/spec-kit)
- [Spec-Kit v0.0.57 Documentation](https://github.com/github/spec-kit/blob/v0.0.57/README.md)
- [Agentifui Pro Constitution](.specify/memory/constitution.md)
- [Project CLAUDE.md](../CLAUDE.md) - AI agent guidance
- [Pull Request Template](../.github/pull_request_template.md)

## Contributing

When adding new commands or templates:
1. Follow spec-kit v0.0.57 conventions
2. Update constitution if adding new principles
3. Ensure backward compatibility with existing features
4. Document changes in Sync Impact Report
5. Use conventional commit format

For questions or issues, refer to the constitution or create an issue.
