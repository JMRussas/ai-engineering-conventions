# Planning Rigor

## What

Scale the depth of your plan to the risk of the task, not its size. A three-level system (Quick / Standard / Thorough) gives you a shared vocabulary with the AI for how much planning a task needs before implementation begins.

## Why

Without calibrated planning:
- **Trivial tasks get over-planned.** The AI writes a 500-word plan for a one-line config change, wasting your time reviewing it.
- **Risky tasks get under-planned.** The AI dives into a database migration with a one-sentence "I'll update the schema" and breaks things you didn't anticipate.
- **Planning is inconsistent.** Sometimes the AI plans, sometimes it doesn't. You can't predict what you'll get.

The core insight: a 3-file feature is often less risky than a 1-file auth change. Risk, not size, determines how much planning you need.

## How

### L1 — Quick (low-risk changes)

- Brief approach in a few bullet points, then execute.
- **When:** Bug fixes, config changes, adding a test, copy changes. Typically 1-2 files.
- **Plan contents:** What you're changing and why. That's it.

### L2 — Standard (moderate-risk changes)

- Written plan with file list, proposed approach, and test impact.
- **When:** New features, multi-file refactors, new endpoints, UI components. Typically 3-10 files, but risk matters more than count.
- **Plan contents:**
  - Summary of approach
  - Files to create/modify (with what changes)
  - Test impact (which existing tests break and why)
  - Open questions with proposed answers

### L3 — Thorough (security, data migrations, multi-system changes)

- Full plan with risk analysis, migration safety, rollback strategy. Implementation should be mechanical after approval.
- **When:** Auth/security changes, DB schema changes, multi-system integrations, anything touching user data.
- **Plan contents:**
  - Everything in L2, plus:
  - Risk assessment — what could break, blast radius
  - Migration safety — verify current state matches assumptions
  - Test strategy — specific tests to add, edge cases
  - Security review — for auth/data changes
  - Rollback plan — how to undo if something goes wrong

### Default levels by task type

| Task type | Default level |
|-----------|--------------|
| Bug fix, typo, config change | L1 |
| New feature, refactor, new UI page | L2 |
| Auth/security, DB migration, payment, compliance | L3 |
| User explicitly says "plan it out" | L3 |

## Example

In your AI instruction file:
```markdown
## Planning Rigor

Every non-trivial task gets a plan. Use L1/L2/L3 based on risk:
- L1 (Quick): Bug fixes, config changes. Bullet points then execute.
- L2 (Standard): Features, refactors. Written plan with file list and test impact.
- L3 (Thorough): Security, migrations. Full risk analysis and rollback plan.

You can request a level explicitly: "plan this at L2"
```

In practice:
```
You: "Add a dark mode toggle to settings"
AI: "This is L2 — new feature touching multiple files. Here's my plan:
     - Add ThemeContext with light/dark state
     - Modify Settings.tsx to add toggle component
     - Update globals.css with dark theme variables
     - 2 existing tests in Settings.test.tsx will need theme provider wrapper
     Approve?"
```

## When to skip

- Solo prototyping where you're iterating fast and throwaway is fine.
- You're the domain expert and just need the AI to type faster — you're providing the plan yourself through detailed instructions.
