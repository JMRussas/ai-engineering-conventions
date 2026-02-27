# Guardrail Hooks

## What

Use pre-commit hooks, CI checks, and automated linting as safety nets for AI-generated code. These catch systematic mistakes the AI makes regardless of how good your instructions are — wrong formatting, type errors, accidental secret inclusion, and style violations.

## Why

Without automated guardrails:
- **Style violations slip through.** The AI doesn't always follow your linting rules, especially in languages where multiple styles are valid.
- **Type errors accumulate.** The AI writes code that looks correct but has subtle type mismatches that only the compiler catches.
- **Secrets get committed.** The AI might include API keys from environment context, example credentials from docs, or placeholder secrets.
- **Review burden increases.** You're manually catching things that a linter would catch in milliseconds.

Guardrails don't replace review — they handle the mechanical checks so you can focus on logic and design.

## How

### Pre-commit hooks (local, instant feedback)

Use a framework like `husky` (JS), `pre-commit` (Python), or `lefthook` (language-agnostic) to run checks before every commit:

```yaml
# .pre-commit-config.yaml (Python ecosystem)
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    hooks:
      - id: check-added-large-files    # AI sometimes generates large test fixtures
      - id: detect-private-key          # Catch accidental key inclusion
      - id: check-merge-conflict        # Catch unresolved markers
      - id: trailing-whitespace
  - repo: https://github.com/astral-sh/ruff-pre-commit
    hooks:
      - id: ruff                        # Linting
      - id: ruff-format                 # Formatting
  - repo: local
    hooks:
      - id: typecheck
        name: Type check
        entry: mypy src/
        language: system
        pass_filenames: false
```

```json
// package.json (JS/TS ecosystem with husky + lint-staged)
{
  "lint-staged": {
    "*.{ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{json,md}": ["prettier --write"]
  }
}
```

### AI-specific guardrails worth adding

| Check | What it catches |
|-------|----------------|
| Secret scanner (gitleaks, trufflehog) | AI including credentials from context |
| Large file check | AI generating enormous test fixtures or data files |
| Import sorting | AI using inconsistent import ordering |
| Dead code detection | AI leaving unused variables/imports |
| License header check | AI omitting required headers |
| Dependency audit | AI adding packages with known vulnerabilities |

### Claude Code hooks (tool-specific)

Claude Code supports hooks that run in response to AI actions:

```json
// .claude/settings.json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "command": "echo 'Review: AI is modifying files'"
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "command": "echo 'AI ran a shell command'"
      }
    ]
  }
}
```

### CI guardrails (shared, authoritative)

Pre-commit hooks can be skipped. CI can't (if configured as required):

- Run the same linting/formatting checks in CI
- Add integration tests that catch AI-generated code with wrong assumptions
- Use branch protection to require passing CI before merge

## Example

A typical guardrail stack:

```
AI writes code
    ↓
Pre-commit hooks run:
  ✓ ESLint (no lint errors)
  ✓ Prettier (formatting fixed)
  ✓ TypeScript compiler (no type errors)
  ✗ gitleaks (found API key in test file!)  ← blocked
    ↓
AI removes the API key, commits again
    ↓
All hooks pass → commit succeeds
    ↓
Push to remote → CI runs:
  ✓ Full test suite
  ✓ Build succeeds
  ✓ No security vulnerabilities in deps
    ↓
PR is ready for human review (logic and design, not formatting)
```

## When to skip

- **Throwaway scripts** or one-off automation where the code won't be maintained.
- **Very early prototyping** where you're iterating faster than hooks can run — but add them before the code goes anywhere shared.
- **Projects with no build system** (pure shell scripts, config files) where hooks add more friction than value.
