# Checkpoint Commits

## What

Make frequent micro-commits during AI-assisted development to create restore points. When the AI takes a wrong turn (and it will), you roll back to the last good state instead of manually untangling changes across multiple files.

## Why

Without checkpoint commits:
- **Wrong turns are expensive.** The AI modifies 8 files, you realize the approach is wrong, and now you're manually reverting or diffing to figure out what changed.
- **Good work gets lost in bad work.** The AI correctly implements steps 1-3, then breaks everything at step 4. Without a checkpoint after step 3, you lose the good work when you revert.
- **You're afraid to let the AI try things.** The cost of failure is so high (manual cleanup) that you over-constrain the AI instead of letting it explore.

Checkpoint commits make AI-assisted work low-risk. Try something, commit if it works, revert if it doesn't.

## How

### The workflow

```
1. AI completes a logical unit of work (one function, one file, one step)
2. You verify it looks right (quick scan, run tests)
3. Commit: "checkpoint: add user validation logic"
4. AI continues to next step
5. Something goes wrong at step N
6. git reset HEAD~1  (or however many checkpoints back — unstages and keeps files)
7. Try again from the last good state
```

### Commit conventions

Use a prefix to distinguish checkpoints from "real" commits:

```
checkpoint: add auth middleware
checkpoint: wire up login endpoint
checkpoint: add error handling to auth flow
```

Before merging or pushing, squash checkpoints into meaningful commits:

```bash
# Squash last 5 checkpoints into one commit
git reset --soft HEAD~5
git commit -m "feat: add authentication system"
```

### When to checkpoint

- After each **logical step** in a multi-step task
- After the AI **successfully modifies a file** and tests still pass
- Before the AI starts **something risky** (refactoring, changing interfaces)
- When you think "this is good so far, I don't want to lose it"

### When NOT to checkpoint

- After every single line change (too granular, creates noise)
- When the code doesn't compile or tests don't pass (don't checkpoint broken states)

### Quick commands

```bash
# Fast checkpoint (stage specific files, or -A if you'll squash before pushing)
git add <files> && git commit -m "checkpoint: [description]"

# See checkpoint history
git log --oneline -10

# Undo last checkpoint (keeps changes as unstaged files)
git reset HEAD~1

# Undo to specific checkpoint
git log --oneline  # find the hash
git reset <hash>

# Squash all checkpoints into one commit (--soft keeps changes staged)
git reset --soft <first-checkpoint-parent-hash>
git commit -m "feat: meaningful description"
```

**`git reset` modes:**
- `git reset <hash>` (default `--mixed`) — undoes commits, keeps changes as unstaged files. Use for retrying.
- `git reset --soft <hash>` — undoes commits, keeps changes staged. Use for squashing.
- `git reset --hard <hash>` — undoes commits and discards all changes. Use when you want to throw away work entirely.

### Branch strategy

Checkpoint commits are safest on **feature branches**. On main (direct workflow), squashing rewrites history — only safe if you haven't pushed the intermediate checkpoints. If using `workflow: direct`, checkpoint locally and squash before your first push.

## Example

```
Session: Adding a search feature

[AI adds SearchBar component]
→ git commit -m "checkpoint: add SearchBar component"

[AI adds search API endpoint]
→ git commit -m "checkpoint: add /api/search endpoint"

[AI adds search results page]
→ git commit -m "checkpoint: add SearchResults page"

[AI tries to add autocomplete — breaks the SearchBar]
→ git reset HEAD~1   ← undo last checkpoint, back to working SearchResults
→ "Let's try a different approach to autocomplete"

[AI adds autocomplete correctly this time]
→ git commit -m "checkpoint: add autocomplete to SearchBar"

[Ready to push]
→ git reset --soft HEAD~4
→ git commit -m "feat: add search with autocomplete"
→ git push
```

## When to skip

- **Trivial changes** (one-file, one-function) where there's nothing to checkpoint.
- **You're using a tool with built-in undo** (some IDE-integrated AI tools track changes automatically).
- **Solo rapid prototyping** — but even here, one checkpoint before a risky step costs almost nothing and can save significant cleanup time.
