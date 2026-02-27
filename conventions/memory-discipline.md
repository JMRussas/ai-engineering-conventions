# Memory Discipline

## What

If your AI tool supports persistent memory across sessions, curate it actively. Define what gets saved, what doesn't, and how memory is organized. Treat memory like a knowledge base, not a journal.

## Why

Without memory discipline:
- **Memory fills with noise.** Session-specific details, half-formed conclusions, and outdated information accumulate and pollute future sessions.
- **The AI acts on stale information.** It "remembers" something from three weeks ago that's no longer true, and you don't realize it's working from outdated context.
- **Useful patterns get lost.** Important conventions and preferences get buried under session trivia.

Good memory is a compounding advantage. Bad memory is a compounding liability.

## How

### What to save
- **Stable patterns** confirmed across multiple interactions (naming conventions, preferred libraries, workflow preferences)
- **Architectural decisions** and their rationale
- **Personal preferences** for communication, tools, and workflow (memory is per-developer; team-wide conventions belong in [instruction files](instruction-files.md))
- **Solutions to recurring problems** — things the AI would otherwise re-discover each session
- **Explicit user requests** — "always use bun", "never auto-commit" (save immediately, don't wait for confirmation)

### What NOT to save
- **Session-specific context** — current task details, in-progress work, temporary state
- **Unverified conclusions** — something observed once in one file isn't a project-wide pattern
- **Anything that duplicates existing docs** — if it's in CLAUDE.md or .claude/*.md, don't also put it in memory
- **Speculative information** — "I think this might be..." doesn't belong in memory

### Organization
- **Organize by topic, not chronologically.** Memory files should be `patterns.md`, `debugging.md`, `preferences.md` — not `session-2024-01-15.md`.
- **Keep the primary memory file concise.** If your tool auto-loads a memory file into context, keep it short and link to detail files. (See [documentation-layers.md](documentation-layers.md) for the reasoning behind the ~200-line guideline.)
- **Update, don't append.** When a pattern evolves, update the existing entry. Don't add a new one that contradicts the old.
- **Prune regularly.** Remove entries that are outdated, wrong, or no longer relevant.

## Example

**Primary memory file (always loaded):**
```markdown
# Memory

## User Preferences
- Uses bun instead of npm for all JS projects
- Prefers functional components over class components in React
- Wants explicit error messages, not generic "something went wrong"

## Cross-project Patterns
- All projects use the documentation layers pattern (CLAUDE.md + .claude/*.md)
- Python projects target 3.11+ unless specified otherwise
- See debugging.md for common issues and fixes
```

**Topic file (loaded on demand):**
```markdown
# Debugging Patterns

## C# / Unity
- NullReferenceException in OnDestroy: check for destroyed singleton references
- IL2CPP builds fail silently with generic virtual methods — use concrete types

## TypeScript
- ESM/CJS interop: use `import type` for type-only imports to avoid runtime issues
- Vite proxy config doesn't support WebSocket by default — add `ws: true`
```

## When to skip

- **Your AI tool doesn't support persistent memory.** (But consider instruction files as a substitute — see [instruction-files.md](instruction-files.md).)
- **Short-lived projects** where you won't have multiple sessions.
- **Team settings** where memory could drift between team members' AI instances — use shared instruction files instead.
