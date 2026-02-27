# Dependency Headers

## What

Add a structured comment block at the top of every source file that documents what the file does, what it depends on, and what depends on it. This gives the AI instant local context about blast radius before it modifies anything.

## Why

Without dependency headers:
- **The AI modifies a file without understanding what breaks.** It changes a function signature and doesn't realize three other modules import it.
- **Refactoring is blind.** The AI has to grep the entire codebase to understand impact, which is slow and error-prone.
- **New-to-project AI sessions start slow.** The AI spends its first several turns just mapping out how files relate to each other.

With headers, the AI reads one file and immediately knows the dependency graph around it.

## How

Add this block to the top of every source file:

```
//  [Project] - [File Description]
//
//  [What this file does — 1-2 sentences]
//
//  Depends on: [list of files/modules this file imports or relies on]
//  Used by:    [list of files/modules that import or rely on this file]
```

### Rules
- Update headers when dependencies change (add/remove imports, restructure modules)
- Keep the lists accurate — stale headers are worse than no headers
- Use relative paths or module names, whichever is conventional for the project
- For files with many dependents, list the primary ones and add "(+ N others)"

### Complement with dependency maps

For the full picture, maintain a dependency map table in `.claude/` docs:

```markdown
## Dependency Map

| File | Role | Depends On | Used By |
|------|------|-----------|---------|
| auth.ts | Authentication logic | db.ts, config.ts | api.ts, middleware.ts |
| db.ts | Database connection | config.ts | auth.ts, models/*.ts |
| config.ts | Config loader | — | auth.ts, db.ts, server.ts |
```

## Example

```csharp
//  MyGame - PlayerController.cs
//
//  Handles player input, movement, and animation state.
//  Main controller for the player character entity.
//
//  Depends on: InputManager.cs, AnimationSystem.cs, PhysicsBody.cs, GameConfig.cs
//  Used by:    GameScene.cs, MultiplayerSync.cs

using MyGame.Input;
using MyGame.Animation;
...
```

```typescript
//  dashboard - api-client.ts
//
//  HTTP client wrapper for backend API calls.
//  Handles auth headers, error normalization, and retry logic.
//
//  Depends on: config.ts, auth-store.ts, types/api.ts
//  Used by:    hooks/useApi.ts, pages/*.tsx (+ 12 others)

import { getConfig } from './config';
import { authStore } from './auth-store';
...
```

## When to skip

- **Generated files** — don't add headers to files produced by code generators, bundlers, or compilers.
- **Trivial files** — a 10-line utility with one export and one consumer doesn't need the ceremony.
- **Rapid prototyping** — add headers when the code stabilizes, not while you're still figuring out the structure.
