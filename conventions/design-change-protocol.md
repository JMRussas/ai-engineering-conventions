# Design Change Protocol

## What

When implementation reveals that the approved plan needs to change, the AI must stop, explain what changed and why, propose a new approach, and wait for approval before continuing. No silent deviations.

## Why

Without this protocol:
- **The AI quietly changes the design mid-implementation.** You approved Plan A but get Plan B delivered, with no explanation of why or what tradeoffs were made differently.
- **You lose architectural control.** The AI encounters a problem, makes a judgment call you wouldn't have made, and you don't find out until review — or worse, production.
- **Debugging becomes archaeology.** When something breaks, you have to reverse-engineer why the implementation doesn't match the plan you approved.

The AI isn't being malicious — it's being "helpful." It hits a snag, finds a workaround, and keeps going. But the workaround might have implications the AI doesn't see.

## How

Add this rule to your AI instruction file:

> All design decisions happen in the plan. If implementation reveals that the plan needs to change:
> 1. **Stop implementation.** Don't silently change the design.
> 2. **Explain what changed and why.** Be specific: "The plan assumed X, but Y is actually the case."
> 3. **Propose the new approach.** With the same rigor as the original plan.
> 4. **Wait for approval** before continuing.
>
> This applies to any deviation: new files not in the plan, different APIs than specified, architectural changes, or dropped/added scope.

## Example

**Without the protocol:**
```
You: "Approved. Go ahead with the Redis caching plan."
AI: [implements for 10 minutes]
AI: "Done! I used an in-memory LRU cache instead of Redis because
     the Redis client had a dependency conflict. Everything works."
You: [now has to evaluate a completely different architecture than what was approved]
```

**With the protocol:**
```
You: "Approved. Go ahead with the Redis caching plan."
AI: "Stopping — the plan assumed redis-client v4 but the project
     pins v3 which doesn't support the cluster API we need.

     Options:
     1. Upgrade redis-client to v4 (risk: breaking changes in 3 other modules)
     2. Use in-memory LRU cache instead (simpler, but no persistence across restarts)
     3. Use redis-client v3 with manual cluster handling (more code, same architecture)

     I'd recommend option 3. Which way?"
```

## When to skip

- **L1 tasks** where the "plan" is a few bullet points and the deviation is trivial (e.g., "I used `fs.readFile` instead of `fs.read` because the API is cleaner").
- **Explicit delegation:** You've told the AI "use your judgment on implementation details" — but even then, architectural changes warrant a check-in.
