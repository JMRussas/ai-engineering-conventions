# ai-engineering-conventions

A collection of process conventions for AI-augmented software development.

## Build / Run

No build step. This is a documentation-only repo.

## Project Structure

```
ai-engineering-conventions/
  README.md               Public-facing overview and convention index
  CLAUDE.md               This file — AI agent entry point
  LICENSE                 MIT license
  conventions/            Individual convention docs (one per pattern)
  examples/               Reference implementations and samples
```

## Conventions for this repo

- Each convention file follows the format: What / Why / How / Example / When to skip
- Convention file names use kebab-case: `planning-rigor.md`, not `PlanningRigor.md`
- Keep conventions standalone — someone should be able to read one file and adopt that pattern without reading anything else
- README.md table must stay in sync with the files in conventions/
- Don't add tool-specific tips (e.g., "use this Cursor setting"). Focus on process patterns that work across tools.
- Cross-reference related conventions where relevant (e.g., gotchas-docs links to rag-augmented-dev for cross-project databases)
- The examples/ directory contains a fictional reference project — keep examples internally consistent but don't claim they're real

## Git Workflow

- workflow: direct
- base_branch: main
