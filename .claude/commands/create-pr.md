---
description: Create a pull request with automated quality validation and conventional commit formatting
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Goal

Create a well-formatted pull request that follows project conventions, passes all quality checks, and includes comprehensive context for reviewers.

## Execution Steps

### 1. Validate Git State

Check current repository status and branch:

```bash
git status
git branch --show-current
```

**Validation Rules:**
- **HALT** if on `main` or `master` branch → "Cannot create PR from main/master. Switch to a feature branch first."
- **HALT** if working directory has unstaged changes → "Uncommitted changes detected. Commit or stash them first."
- **WARN** if ahead of origin → Suggest pushing commits before PR creation
- **VERIFY** current branch has commits not in main/master

### 2. Extract PR Context

Gather information for PR creation:

**From Git History:**
```bash
# Get commits not in main
git log main..HEAD --oneline

# Get commit messages for PR description
git log main..HEAD --format="%s%n%b" --reverse
```

**From Branch Name:**
- Extract issue number if present (e.g., `feature/123-auth` → `#123`)
- Infer feature type from prefix: `feature/`, `fix/`, `refactor/`, `docs/`

**From User Arguments:**
- Parse `$ARGUMENTS` for:
  - PR title override
  - Issue references (`#123`, `Fixes #456`)
  - Additional context or description
  - Flags: `--draft`, `--base <branch>`, `--no-checks`

### 3. Run Quality Checks

Execute project-specific quality validation:

**For Backend Changes (api/ directory):**
```bash
cd api
uv run ruff check . --fix
uv run mypy .
uv run pytest --cov --cov-report=term-missing
```

**For Frontend Changes (web/ directory):**
```bash
cd web
pnpm fix
pnpm type-check
pnpm test
```

**Quality Gates:**
- **CRITICAL**: If `--no-checks` flag NOT provided:
  - All linters must pass (ruff, ESLint)
  - All type checks must pass (mypy, TypeScript)
  - All tests must pass
  - **HALT** on any failure with clear error report
- **SKIP**: If `--no-checks` flag provided → Proceed with warning

### 4. Generate PR Title and Description

**Title Format:**
Follow conventional commits pattern from most recent commit or infer from changes:
```
<type>: <description>

Types: feat, fix, refactor, docs, test, chore, perf, style, ci
```

**Extract from commits:**
- If all commits have same type → Use that type
- If mixed → Ask user to clarify or use most common type
- Character limit: 72 characters max

**Description Structure:**
Use template from `.github/pull_request_template.md`:

1. **Overview**: Synthesize commit messages into coherent summary
2. **Changes**: Bullet list of key modifications
3. **Testing**: How changes were validated
4. **Issue Links**: Auto-detect from commits or branch name
5. **Checklist**: Pre-fill based on changes detected

### 5. Detect Issue References

Search for issue references in:
- Branch name pattern: `feature/123-*` or `fix/456-*`
- Commit messages: `#123`, `Fixes #456`, `Closes #789`
- User arguments: Explicit issue references

**Link Format:**
- If issue found → Add `Fixes #<number>` to description
- If multiple issues → List all with appropriate keywords
- If no issue → Omit issue section

### 6. Build PR Description

Synthesize final PR body following this template:

```markdown
## Overview
<Synthesized summary from commits and context>

## Changes
<Bullet list of key changes organized by area>
- **Backend**: <changes>
- **Frontend**: <changes>
- **Tests**: <changes>
- **Documentation**: <changes>

## Testing
<How the changes were validated>
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Type checking passes

## Related Issues
<If applicable>
Fixes #<issue-number>

## Additional Context
<Any relevant information for reviewers>

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings introduced
- [ ] Tests added/updated
- [ ] All quality checks pass
```

### 7. Create Pull Request

Use GitHub CLI to create PR:

```bash
gh pr create \
  --title "<generated-title>" \
  --body "$(cat <<'EOF'
<generated-description>
EOF
)" \
  --base main \
  [--draft if requested] \
  [--reviewer <if specified>] \
  [--label <if inferred>]
```

**Base Branch Selection:**
- Default: `main`
- Override with `--base <branch>` from user arguments
- Validate base branch exists before creation

**Draft Mode:**
- Enable with `--draft` flag in arguments
- Useful for WIP or early feedback requests

### 8. Post-Creation Actions

After successful PR creation:

1. **Display PR URL**: Show clickable link to created PR
2. **Show PR Summary**:
   ```
   ✅ Pull Request Created Successfully

   Title: feat: add user authentication
   Base:  main ← feature/auth-system
   URL:   https://github.com/user/repo/pull/123

   Quality Checks: ✅ All Passed
   - Linting: ✅
   - Type Check: ✅
   - Tests: ✅

   Next Steps:
   - Review the PR description and make any necessary edits
   - Request reviews from team members
   - Monitor CI/CD pipeline status
   ```

3. **Suggest Next Actions**:
   - Add reviewers: `gh pr edit <number> --add-reviewer <username>`
   - Add labels: `gh pr edit <number> --add-label <label>`
   - Convert to draft: `gh pr ready --undo <number>`

## Operating Principles

### Safety First
- **NEVER create PR from main/master branch**
- **ALWAYS verify clean working directory**
- **REQUIRE quality checks pass** (unless `--no-checks` explicitly provided)
- **VALIDATE base branch exists** before creation

### Quality Standards
- **Conventional Commits**: Enforce standard commit message format
- **Complete Testing**: All tests must pass before PR creation
- **Type Safety**: No type errors allowed in production code
- **Code Style**: Automated formatting applied before PR

### User Experience
- **Clear Error Messages**: Explain what failed and how to fix
- **Actionable Output**: Provide next steps and useful commands
- **Progress Visibility**: Show what's being validated in real-time
- **Smart Defaults**: Infer context from git history and branch names

### Token Efficiency
- **Minimal File Reading**: Only read necessary files (PR template, git log)
- **Batched Commands**: Run quality checks in parallel where possible
- **Smart Caching**: Reuse git log and status information
- **Progressive Disclosure**: Show summary first, details on request

## Error Handling

### Common Failure Scenarios

**On Main Branch:**
```
❌ Cannot create PR from main/master branch

Current branch: main

Action Required:
1. Create a feature branch: git checkout -b feature/my-feature
2. Make your changes and commit
3. Run /create-pr again
```

**Uncommitted Changes:**
```
❌ Uncommitted changes detected

Modified files:
- api/app/main.py
- web/src/components/Header.tsx

Action Required:
1. Commit changes: git add . && git commit -m "your message"
   OR
2. Stash changes: git stash
3. Run /create-pr again
```

**Quality Checks Failed:**
```
❌ Quality checks failed - cannot create PR

Backend Checks:
✅ Linting (ruff): Passed
❌ Type Check (mypy): 3 errors found
✅ Tests (pytest): Passed

Action Required:
1. Fix type errors reported above
2. Run checks again: cd api && uv run mypy .
3. Use --no-checks flag to bypass (NOT recommended)
```

**No Commits to PR:**
```
❌ No new commits found

Current branch has no commits ahead of main.

Action Required:
1. Make changes and commit them
2. Ensure commits are not already in main
```

## Examples

### Basic PR Creation
```
/create-pr
```
- Auto-detects changes, runs quality checks
- Generates title from recent commits
- Creates PR with full description
- Links issues if found in branch/commits

### PR with Custom Title and Issue
```
/create-pr "feat: implement OAuth2 authentication" Fixes #123
```
- Uses provided title instead of auto-generation
- Links to issue #123 with "Fixes" keyword
- Runs quality checks
- Creates PR with custom context

### Draft PR Without Quality Checks
```
/create-pr --draft --no-checks
```
- Creates draft PR (work in progress)
- Skips quality validation (for early feedback)
- Still validates git state and generates description
- Warns about skipped checks

### PR to Different Base Branch
```
/create-pr --base develop
```
- Creates PR targeting `develop` instead of `main`
- Useful for feature branch workflows
- Validates base branch exists

### PR with Specific Reviewers
```
/create-pr --reviewer alice,bob
```
- Creates PR and requests reviews from alice and bob
- Uses GitHub usernames
- Can combine with other flags

## Integration with Project Standards

### Monorepo Awareness
- **Detects scope**: Identifies if changes are backend, frontend, or both
- **Targeted checks**: Runs only relevant quality checks for changed areas
- **Smart labeling**: Suggests labels based on changed directories

### Conventional Commits
- **Enforces format**: `<type>: <description>`
- **Validates types**: feat, fix, refactor, docs, test, chore, perf, style, ci
- **Character limits**: Max 72 chars for title

### i18n Compliance
- **Checks translation keys**: Validates kebab-case format in translations
- **Warns on hardcoded strings**: Suggests using `t()` for user-facing text

### Testing Requirements
- **Backend**: Minimum 80% coverage required
- **Frontend**: All tests must pass, type-check clean
- **E2E**: Suggests running Playwright tests for UI changes

## Boundaries

**Will:**
- Validate git state and enforce branch safety rules
- Run comprehensive quality checks before PR creation
- Generate well-formatted PR descriptions following project templates
- Auto-detect and link related issues from commits and branch names
- Provide clear error messages with actionable remediation steps

**Will Not:**
- Create PRs from main/master branches (safety violation)
- Bypass quality checks without explicit `--no-checks` flag
- Modify code to fix quality issues automatically (user must fix)
- Push commits to remote (user should review before pushing)
- Merge or approve PRs (separate review process)
- Invent issue numbers or commit messages that don't exist
