# Documentation Layers

## What

Structure AI-facing documentation in two layers: a lightweight entry-point file (like `CLAUDE.md`) that's always loaded into context, and a directory of deep-dive docs (like `.claude/*.md`) that are read on demand. The entry point links to the deep-dives with a table showing what's available.

## Why

Without layered docs:
- **One giant file wastes context.** A 2000-line instruction file burns context window on sections irrelevant to the current task.
- **No docs means hallucination.** The AI fills knowledge gaps with guesses about your architecture, conventions, and APIs.
- **Docs scattered across the codebase get missed.** If the AI doesn't know a doc exists, it won't read it.

The two-layer approach gives you always-on lightweight context plus depth when needed.

## How

### Layer 1: Entry point (`CLAUDE.md` or equivalent)

Keep this concise — aim for under 200 lines. (This is a practical heuristic: ~200 lines of markdown is roughly 3-4k tokens, leaving most of the context window for actual code. Adjust based on your tool's context size.) It contains:
- One-line project description
- Build/run commands (the stuff the AI needs every session)
- Project structure overview
- Key conventions (naming, patterns, etc.)
- Table of deep-dive docs with one-line descriptions
- Git workflow settings

```markdown
# my-project

Web app for managing widgets.

## Build / Run
- `npm run dev` — start dev server
- `npm test` — run tests
- `npm run build` — production build

## Project Structure
src/
  components/    React components
  api/           API client and types
  hooks/         Custom React hooks

## Deep-dive docs
| Doc | Contents |
|-----|----------|
| [.claude/architecture.md](.claude/architecture.md) | System design, data flow |
| [.claude/api.md](.claude/api.md) | API endpoints and contracts |
| [.claude/testing.md](.claude/testing.md) | Test patterns and fixtures |
| [.claude/gotchas.md](.claude/gotchas.md) | Non-obvious behaviors and pitfalls |
```

### Layer 2: Deep-dive docs (`.claude/*.md`)

One file per topic. These are read when the AI needs them for a specific task. Each should be self-contained — someone reading just that file should understand the topic.

Good candidates for deep-dive docs:
- Architecture and data flow diagrams
- API documentation and contracts
- Testing patterns and fixture setup
- Deployment and infrastructure
- Gotchas and pitfalls (see [gotchas-docs.md](gotchas-docs.md))
- Dependency maps (see [dependency-headers.md](dependency-headers.md))

## Example

```
my-project/
  CLAUDE.md                 ← Always loaded. ~100 lines. Links to everything below.
  .claude/
    architecture.md         ← Read when working on system design
    api.md                  ← Read when working on endpoints
    testing.md              ← Read when writing or fixing tests
    gotchas.md              ← Read when hitting unexpected behavior
    deployment.md           ← Read when working on CI/CD or infra
```

The AI's workflow becomes:
1. Start of session → read `CLAUDE.md` (automatic)
2. Working on API endpoint → read `.claude/api.md` (on demand)
3. Hit a weird bug → check `.claude/gotchas.md` (on demand)

## When to skip

- **Single-file scripts or tiny projects** — just put everything in `CLAUDE.md`.
- **Projects with excellent existing docs** (e.g., well-maintained README, wiki, or docsite) — link to those from `CLAUDE.md` instead of duplicating.
