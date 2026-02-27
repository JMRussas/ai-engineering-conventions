# Gotchas Docs

## What

Maintain a "Gotchas & Pitfalls" document per project that records non-obvious behaviors, engine quirks, API footguns, and things that don't work the way you'd expect. The AI reads this before working so it doesn't re-learn the same lessons every session.

## Why

Without gotchas docs:
- **The AI makes the same mistake every session.** It tries an approach, hits a quirk, works around it — then does the exact same thing next time because conversation context is gone.
- **Onboarding is expensive.** Every new AI session (or new team member) pays the full cost of discovering project-specific pitfalls.
- **Tribal knowledge stays tribal.** The gotcha lives in someone's head or a Slack thread, not where the AI can find it.

This is one of the highest-ROI conventions because it directly eliminates repeated failures.

## How

Create a file at `.claude/gotchas.md` (or similar path the AI reads on demand):

### Format

```markdown
# Gotchas & Pitfalls

## [Category]

### [Short description of the gotcha]
**Symptom:** What you see when you hit this.
**Cause:** Why it happens.
**Fix:** What to do instead.
```

### Rules
- Add a gotcha **the first time** something non-obvious bites you — don't wait for it to happen twice
- Keep entries short — 3-5 lines each. This isn't a blog post.
- Categorize by area (API, build system, testing, deployment, etc.)
- Remove gotchas when the underlying issue is fixed
- Review periodically — stale gotchas erode trust in the document

### When to add entries
- The AI tries something that should work but doesn't
- A library/framework has undocumented behavior you discovered
- A test passes locally but fails in CI for non-obvious reasons
- A configuration value has a surprising default
- An API behaves differently than its documentation suggests

## Example

```markdown
# Gotchas & Pitfalls

## Build System

### Vite HMR breaks with circular imports
**Symptom:** Hot reload stops working silently. No error in console.
**Cause:** Vite's HMR can't resolve circular dependency chains.
**Fix:** Break the cycle with a shared types file. Run `npx madge --circular src/` to detect.

## API

### Auth token refresh race condition
**Symptom:** Intermittent 401 errors under load, even with valid refresh tokens.
**Cause:** Multiple concurrent requests all try to refresh the token simultaneously.
**Fix:** Use a mutex/queue pattern — first request refreshes, others wait for the result.

## Testing

### Jest timer mocks don't work with async/await
**Symptom:** `jest.advanceTimersByTime()` has no effect on `await sleep(1000)`.
**Cause:** Jest fake timers replace `setTimeout` but not the Promise microtask queue.
**Fix:** Use `jest.advanceTimersByTimeAsync()` (Jest 29.5+) or `await jest.runAllTimersAsync()`.

## Database

### Prisma migrations fail on manually-created databases
**Symptom:** Migration fails with "table already exists" on existing databases.
**Cause:** `prisma migrate dev` expects to manage schema via its migration history table. Running it against a DB that was set up manually (without migrations) means the history is empty but the tables exist.
**Fix:** Use `prisma migrate resolve --applied <migration_name>` to mark existing migrations as already applied.
```

## Cross-project gotchas

For patterns that recur across multiple projects, consider maintaining a separate cross-project gotchas database. This is different from per-project gotchas — it captures language-level, framework-level, or tool-level pitfalls:

- "AI always forgets to handle the null case in C# nullable reference types"
- "AI generates Python 3.9 syntax when the project targets 3.8"
- "AI assumes Jest globals are available without importing in Vitest projects"

This can live in a shared repo or a RAG-indexed knowledge base for retrieval across projects.

## When to skip

- **Early prototyping** — defer until the code stabilizes, but adopt before it's shared or promoted beyond throwaway status.
- **Projects with zero surprises** — if the tech stack is vanilla and well-documented, you may not accumulate gotchas worth recording. (But you probably will.)
