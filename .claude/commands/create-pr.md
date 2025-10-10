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

### 1. Detect Default Branch and Validate Git State

```bash
# Detect repository's default branch
DEFAULT_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')
DEFAULT_BRANCH=${DEFAULT_BRANCH:-main}

# Check current state
CURRENT_BRANCH=$(git branch --show-current)
git status --short
```

**Validation:**
- **HALT** if on `$DEFAULT_BRANCH` → "Cannot create PR from default branch. Create feature branch first."
- **HALT** if uncommitted changes → "Commit or stash changes first."
- **VERIFY** current branch has commits: `git log $DEFAULT_BRANCH..HEAD --oneline`

### 2. Detect Changes and Parse Arguments

```bash
# Detect monorepo scope
CHANGED_FILES=$(git diff --name-only $DEFAULT_BRANCH..HEAD)
HAS_BACKEND=$(echo "$CHANGED_FILES" | grep -q "^api/" && echo "true" || echo "false")
HAS_FRONTEND=$(echo "$CHANGED_FILES" | grep -q "^web/" && echo "true" || echo "false")

# Get commits for PR description
git log $DEFAULT_BRANCH..HEAD --format="%s%n%b" --reverse
```

**Parse `$ARGUMENTS`:**
- PR title (first quoted string)
- Issue refs: `#123`, `Fixes #456`, `Closes #789`
- Flags: `--draft`, `--base <branch>`, `--no-checks`, `--remote <name|url>`, `--reviewer <users>`
- Branch name: Extract issue number from `feature/123-*` pattern

### 3. Run Quality Checks

**Backend** (if `$HAS_BACKEND == true`):
```bash
(cd api && uv run ruff check . && uv run mypy . && uv run pytest --cov --cov-report=term-missing --cov-fail-under=80)
```

**Frontend** (if `$HAS_FRONTEND == true`):
```bash
(cd web && pnpm lint && pnpm type-check && pnpm test && pnpm i18n:check)
```

**Gates:** Skip if `--no-checks`, halt on failure, all commands chained with `&&`

### 4. Generate PR Title and Description

**Title** (72 char max): `<type>: <description>`
Types: `feat|fix|refactor|docs|test|chore|perf|style|ci`

**Description Template:**
```markdown
## Summary
<Synthesize commit messages>

<If issue>Fixes #<number></If>

## Type
- [ ] 🐛 Bug | [ ] ✨ Feature | [ ] 💥 Breaking | [x] 📚 Docs | [ ] ♻️ Refactor | [ ] ⚡ Performance

## Changes
<Backend/Frontend/Tests/Docs organized by scope>

## Testing
- [x] Quality checks passed
- [ ] Manual testing completed
```

### 5. Push to Remote

```bash
REMOTE=${REMOTE_ARG:-origin}

# Handle URL remote
if [[ $REMOTE =~ ^https?:// ]]; then
  git remote add temp-pr-remote $REMOTE
  REMOTE="temp-pr-remote"
elif ! git remote | grep -q "^${REMOTE}$"; then
  echo "❌ Remote '$REMOTE' not found. Available: $(git remote | tr '\n' ', ')"
  exit 1
fi

git push -u $REMOTE $CURRENT_BRANCH
[[ $REMOTE == "temp-pr-remote" ]] && git remote remove temp-pr-remote
```

### 6. Create Pull Request

```bash
gh pr create \
  --title "<generated-title>" \
  --body "<generated-description>" \
  --base ${BASE_BRANCH:-$DEFAULT_BRANCH} \
  ${DRAFT_FLAG:+--draft} \
  ${REVIEWERS:+--reviewer "$REVIEWERS"}
```

### 7. Display Results

```
✅ Pull Request Created Successfully

Title: <type>: <description>
Base:  $DEFAULT_BRANCH ← $CURRENT_BRANCH
URL:   <github-pr-url>
Remote: <remote-name>

Quality Checks: ✅ All Passed
${HAS_BACKEND:+- Backend: Ruff, Mypy, Pytest (≥80%)}
${HAS_FRONTEND:+- Frontend: ESLint, TypeScript, Tests, i18n}

Next: Review PR, monitor CI, add labels with gh pr edit <num> --add-label <label>
```

## Error Handling

**On Default Branch:** `❌ Cannot create PR from '$DEFAULT_BRANCH'. Action: git checkout -b feature/name`

**Uncommitted Changes:** `❌ Uncommitted changes. Action: git add . && git commit OR git stash`

**Quality Failed:** `❌ <Scope>: <Check> failed. Action: Fix errors or use --no-checks`

**Remote Not Found:** `❌ Remote '<name>' not found. Available: <list>. Action: Use existing or add remote`

## Usage Examples

```bash
# Basic
/create-pr

# Custom title + issue
/create-pr "feat: implement OAuth2" Fixes #123

# Draft, skip checks
/create-pr --draft --no-checks

# Custom remote + base
/create-pr --remote upstream --base develop

# URL remote
/create-pr --remote https://github.com/org/repo.git

# With reviewers
/create-pr --reviewer alice,bob

# Combined
/create-pr "feat: add feature" --remote upstream --base develop --draft --reviewer alice
```

## Project Integration

**Monorepo:** Detects changes via `git diff --name-only`, runs targeted checks (api/ or web/)

**Quality:**
- Backend: Ruff, Mypy, Pytest ≥80% coverage
- Frontend: ESLint+Prettier, TypeScript strict, Tests, i18n kebab-case validation

**i18n:** Validates `t('auth.sign-in.email')` kebab-case format, checks hardcoded strings

## Boundaries

**Will:** Detect default branch dynamically, run targeted quality checks, push to any remote (named/URL), enforce 80% coverage, validate i18n, generate conventional commit PRs

**Will Not:** Create PRs from default branch, bypass checks without `--no-checks`, force push without awareness, add permanent URL remotes, auto-fix code issues
