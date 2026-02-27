# Example CLAUDE.md — Reference Implementation

This is a complete AI instruction file that incorporates conventions from this repository.
It's a real, working config — not a template. Adapt what's useful, drop what doesn't fit.

---

# my-project

Web application for managing and visualizing sensor data.

## Build / Run

- `npm run dev` — start dev server (Vite, port 3000)
- `npm test` — run Jest test suite
- `npm run build` — production build to dist/
- `npm run lint` — ESLint + Prettier check
- `python tools/cli.py --help` — project CLI for inspection and validation

## Project Structure

```
my-project/
  CLAUDE.md              This file
  .claude/
    architecture.md      System design, data flow, component hierarchy
    api.md               REST API endpoints and contracts
    testing.md           Test patterns, fixtures, mock setup
    gotchas.md           Non-obvious behaviors and pitfalls
  src/
    components/          React components (one per file)
    hooks/               Custom React hooks
    api/                 API client, types, error handling
    store/               Zustand stores
    pages/               Route-level page components
    utils/               Shared utilities
  tools/
    cli.py               AI-extensible project CLI
```

## Conventions

- **Naming:** PascalCase for components/types, camelCase for functions/variables, kebab-case for file names
- **Components:** Functional components only. Props interface named `{Component}Props`.
- **State:** Zustand stores in src/store/. No prop drilling past 2 levels.
- **API calls:** Always go through src/api/client.ts. Never call fetch directly.
- **Error handling:** API errors throw `ApiError` (src/api/errors.ts). Components catch with error boundaries.
- **Config:** All config in src/config.ts, loaded from environment variables. Never hardcoded.

## Deep-dive docs

| Doc | Contents |
|-----|----------|
| [.claude/architecture.md](.claude/architecture.md) | System design, data flow, component hierarchy |
| [.claude/api.md](.claude/api.md) | REST endpoints, request/response contracts |
| [.claude/testing.md](.claude/testing.md) | Test patterns, fixtures, common mock setup |
| [.claude/gotchas.md](.claude/gotchas.md) | Non-obvious behaviors, framework quirks |

## Git Workflow

- workflow: pr
- base_branch: main
- branch_protection: yes
- ci_gate: required
- squash_merge: yes

## Planning Rigor

Every non-trivial task gets a plan. Scale depth to risk:

- **L1 (Quick):** Bug fixes, config changes. Bullet points then execute.
- **L2 (Standard):** Features, refactors. Written plan with file list and test impact.
- **L3 (Thorough):** Security, migrations. Full risk analysis, rollback plan.

If implementation reveals the plan needs to change: stop, explain, propose new approach, wait for approval.

## Gotchas

See [.claude/gotchas.md](.claude/gotchas.md) for the full list. Key ones:

- Vite HMR breaks silently with circular imports — use `npx madge --circular src/`
- Zustand `set()` is async in React 18 strict mode — don't read state immediately after setting
- The API returns dates as Unix timestamps, not ISO strings — always use `fromTimestamp()` util
