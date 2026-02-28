# Context Budgeting

## What

Be deliberate about what information the AI sees during a task. Too much context is as harmful as too little — it causes the AI to lose focus, weight irrelevant details, and miss what matters. Budget your context like you'd budget memory in a constrained system.

## Why

Without context budgeting:
- **The AI drowns in noise.** You paste 5 files into the prompt when it only needs 2. The AI tries to account for all of them and makes worse decisions.
- **Important details get diluted.** Critical constraints buried in page 3 of context get less attention than whatever's at the top.
- **Conversations drift.** Long sessions accumulate stale context — assumptions from turn 5 that were corrected at turn 20 still influence behavior.
- **You hit context limits.** The window fills with irrelevant code, leaving no room for the actual work.

## How

### Principle: show what's relevant, hide what's not

Before giving the AI context, ask: "Does it need this to do the current task?"

| Context type | Include? |
|-------------|----------|
| Files being modified | Always |
| Files that import/depend on modified files | Usually |
| Project conventions (instruction file) | Always (keep it short) |
| Unrelated files "for reference" | Rarely |
| Full conversation history from a different task | Never |

### Strategies

**1. Layered documentation (see [documentation-layers.md](documentation-layers.md))**
- Always-loaded: lightweight entry point (keep it concise — see that doc for sizing guidance)
- On-demand: deep-dive docs loaded only when relevant

**2. Fresh conversations for fresh tasks**
- Start a new conversation when switching tasks. Don't carry stale context.
- Rule of thumb: if you're past ~30 turns or the conversation has shifted topics significantly, start fresh.

**3. Focused file inclusion**
- Don't dump entire files when the AI only needs a section.
- Point the AI to specific functions or line ranges.
- Use dependency headers to help the AI identify what else to read.

**4. Prune conversation context**
- If you've been debugging and the AI has tried 5 wrong approaches, summarize the findings and start a new conversation with just the summary. The old wrong turns actively hurt by biasing the AI.

**5. Separate research from implementation**
- Use one conversation to explore/understand the codebase.
- Start a fresh conversation for implementation, providing only the conclusions from research.

### Context window hygiene signals

**Start a new conversation when:**
- You've switched to a fundamentally different task
- The AI keeps making the same mistake despite corrections (context is polluted)
- You've been going for 30+ turns
- The AI starts referencing things from earlier that are no longer relevant

**Stay in the current conversation when:**
- You're iterating on the same feature
- Each turn builds on the previous one
- The AI's context is accurate and helpful

## Example

**Over-budgeted (bad):**
```
"Here's my entire src/ directory (47 files). Add a logout button to the navbar."
→ AI is overwhelmed, may modify the wrong files, loses focus
```

**Well-budgeted (good):**
```
"Here's Navbar.tsx, auth-store.ts, and the route definitions.
 Add a logout button that calls auth-store's logout() and redirects to /login."
→ AI has exactly what it needs, produces focused output
```

**Context pollution (bad):**
```
[Turn 1-15: debugging a database issue]
[Turn 16: "OK forget that, let's add a new API endpoint"]
→ AI is still biased by the database debugging context
```

**Fresh start (good):**
```
[New conversation]
"I need a new API endpoint for /api/widgets. Here's the existing
 endpoint pattern from handlers/users.ts and the relevant types."
→ AI starts clean with only relevant context
```

## When to skip

- **Your AI tool handles context automatically** with features like codebase indexing that dynamically retrieve relevant files.
- **Very short sessions** (1-3 turns) where context bloat isn't a risk.
- **Exploration/learning sessions** where breadth of context is the point.
