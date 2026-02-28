# Instruction Files

## What

Treat your AI instruction file (CLAUDE.md, .cursor/rules/, .github/copilot-instructions.md, etc.) as a version-controlled project artifact. Check it into the repo, review changes like code, and iterate on it as the project evolves.

## Why

Without version-controlled instruction files:
- **AI behavior is inconsistent across team members.** Everyone has different prompts, different conventions, different expectations — the same codebase gets worked on in completely different styles.
- **Knowledge is ephemeral.** Conventions live in people's heads or one-off prompts. New team members (or new AI sessions) start from zero.
- **There's no feedback loop.** When the AI consistently makes a mistake, there's no mechanism to fix it permanently — you just correct it again next time.

Instruction files are the bridge between "I want the AI to do X" and "the AI consistently does X."

## How

### Create the file
Most AI tools look for a specific filename:
- **Claude Code:** `CLAUDE.md` at project root
- **Cursor:** `.cursor/rules/` directory (previously `.cursorrules`, now deprecated). Tool-specific filenames change frequently — check your tool's current docs.
- **GitHub Copilot:** `.github/copilot-instructions.md`
- **Generic:** Any file you paste into system prompts

### What to include
- Project description (one line)
- Build/run/test commands
- Project structure overview
- Naming conventions and code style
- Architecture patterns to follow
- Common mistakes to avoid
- Links to deeper documentation

### What NOT to include
- Lengthy tutorials or explanations (link to docs instead)
- Information that changes frequently (use dynamic sources like CLI tools)
- Secrets or credentials (obviously)
- Personal preferences that wouldn't apply to the whole team (those belong in per-developer [memory](memory-discipline.md), not shared instruction files)

### Treat it like code
- **Review changes.** When someone updates the instruction file, review the PR like any other code change. A bad instruction can cause systematic errors.
- **Test changes.** After modifying instructions, test that the AI actually behaves differently. Instructions that the AI ignores are worse than no instructions (false confidence).
- **Keep it current.** Stale instructions cause the AI to fight against the actual codebase. Update when architecture changes.

## Example

```markdown
# my-api

REST API for the widget management platform.

## Build / Run
- `cargo build` — compile
- `cargo test` — run all tests
- `cargo run` — start server on :8080

## Conventions
- Error types go in src/errors.rs, one enum per module
- All endpoints return Result<Json<T>, ApiError>
- Use `tracing` for logging, not `println!` or `log`
- Database queries go through the repository pattern (src/repos/)
- Tests use the `TestDb` fixture from tests/common/mod.rs

## Architecture
- src/handlers/ — HTTP handlers, one file per resource
- src/repos/ — Database access layer
- src/models/ — Domain types and validation
- src/errors.rs — Error types and conversions

## Don't
- Don't use `unwrap()` in production code — use `?` or explicit error handling
- Don't add new dependencies without checking if an existing one covers the use case
- Don't write SQL strings directly — use the query builder in src/db/mod.rs
```

## When to skip

- **Solo throwaway projects** where you're the only one and it's short-lived.
- **You're using the AI for a one-off question**, not ongoing development on a project.
