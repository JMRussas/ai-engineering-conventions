# Incremental Trust

## What

Design your AI workflow so that the human stays in the approval loop for actions that are irreversible, affect shared systems, or have significant blast radius. The AI can freely take local, reversible actions (editing files, running tests) but must get explicit approval before crossing trust boundaries.

## Why

Without an incremental trust model:
- **One bad AI action destroys hours of work.** A force-push, a dropped table, a deleted branch — the AI was "helping" but caused irreversible damage.
- **You either over-restrict or under-restrict.** Without clear boundaries, you end up either approving every file edit (slow) or letting the AI push to production (dangerous).
- **Trust erodes after incidents.** One bad experience makes you distrust the AI for everything, even things it handles well.

The goal is maximum AI autonomy *within safe boundaries*, with human checkpoints at the boundaries.

## How

### Define trust boundaries

Categorize actions into tiers:

| Tier | Examples | AI can do freely? |
|------|---------|-------------------|
| **Local, reversible** | Edit files, run tests, read code, create branches | Yes |
| **Local, hard to reverse** | Delete files, reset git state, modify config | Ask first |
| **Shared systems** | Push code, create PRs, comment on issues | Ask first |
| **Destructive** | Force push, drop tables, delete branches, deploy | Always ask, explain risks |

### Implement in your AI instruction file

```markdown
## Trust Boundaries

You can freely:
- Read and edit files
- Run tests and build commands
- Create local branches
- Search and explore the codebase

Always ask before:
- Pushing to remote
- Creating or commenting on PRs/issues
- Deleting files or branches
- Running destructive git commands (reset --hard, push --force)
- Modifying CI/CD pipelines
- Any action visible to other team members

Never:
- Force-push to main/master
- Commit secrets or credentials
- Merge PRs (human merges)
- Deploy to production
```

### The escalation pattern

When the AI hits a trust boundary, it should:
1. **State what it wants to do** and why
2. **Describe the blast radius** — what could go wrong
3. **Wait for approval** — don't proceed on assumption
4. **Confirm the outcome** after taking the action

## Example

**Good — AI respects trust boundary:**
```
AI: "The feature branch is ready. I'd like to push and create a PR.
     This will:
     - Push branch 'feature/dark-mode' to origin
     - Create a PR against main with the changes we discussed
     Should I go ahead?"
```

**Bad — AI crosses boundary silently:**
```
AI: "Done! I've pushed the changes and created PR #47.
     Here's the link: ..."
You: [didn't want it pushed yet, had more changes to make]
```

**Calibrating over time:**
```
You: "For this session, you can push freely — I'll review in GitHub."
AI: [pushes without asking for the rest of the session]
AI: [next session, goes back to asking — session-level trust doesn't persist]
```

## When to skip

- **Solo prototyping** on a throwaway repo where nothing is shared and everything is expendable.
- **Fully automated pipelines** where the AI operates within a sandboxed CI environment with its own safety nets (branch protection, required reviews, etc.).
- **Explicit delegation** — you've told the AI to handle everything end-to-end and you'll review the PR.
