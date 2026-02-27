# AI Engineering Conventions

A curated collection of process conventions for working effectively with AI coding assistants.

These aren't theoretical — they're patterns extracted from daily AI-augmented development across multiple projects, refined through real usage. Each convention is standalone: adopt what fits your workflow, skip what doesn't.

## Who this is for

- **Individual developers** using AI assistants (Claude Code, Cursor, Copilot, etc.) who want more consistent, reliable results
- **Team leads** establishing AI workflows and wanting guardrails that don't kill velocity
- **Anyone** who's noticed that AI output quality varies wildly and suspects the problem is process, not the model

## How to use this

Each convention in `conventions/` follows the same format:

- **What** — one paragraph summary
- **Why** — what goes wrong without it
- **How** — concrete implementation
- **Example** — real config, code, or workflow snippet
- **When to skip** — not everything applies everywhere

Start with the ones that address your biggest pain points. You don't need all of them.

## Conventions

### Planning & Design
| Convention | Summary |
|-----------|---------|
| [Planning Rigor](conventions/planning-rigor.md) | Scale planning depth to risk, not task size |
| [Design Change Protocol](conventions/design-change-protocol.md) | Stop and re-plan when implementation deviates from the plan |
| [Test-First with AI](conventions/test-first-with-ai.md) | Write failing tests before asking AI to implement |

### Documentation & Knowledge
| Convention | Summary |
|-----------|---------|
| [Documentation Layers](conventions/documentation-layers.md) | Lightweight entry point + deep-dive docs on demand |
| [Dependency Headers](conventions/dependency-headers.md) | Explicit dependency maps in source files |
| [Gotchas Docs](conventions/gotchas-docs.md) | Prevent the AI from re-learning the same lessons |
| [Instruction Files](conventions/instruction-files.md) | AI config as version-controlled project artifacts |
| [Memory Discipline](conventions/memory-discipline.md) | Persistent memory that's curated, not dumped |

### Tooling & Infrastructure
| Convention | Summary |
|-----------|---------|
| [Project CLI](conventions/project-cli.md) | AI builds its own inspection and validation tools |
| [RAG-Augmented Dev](conventions/rag-augmented-dev.md) | Project-specific search indexes for accurate API knowledge |
| [Guardrail Hooks](conventions/guardrail-hooks.md) | Automated safety nets for AI-generated code |

### Process & Trust
| Convention | Summary |
|-----------|---------|
| [Incremental Trust](conventions/incremental-trust.md) | Human stays in the approval loop for irreversible actions |
| [Context Budgeting](conventions/context-budgeting.md) | Be deliberate about what the AI sees |
| [Checkpoint Commits](conventions/checkpoint-commits.md) | Frequent micro-commits for easy rollback during AI sessions |

## Reference Implementation

The `examples/` directory contains a complete working setup:

- [examples/CLAUDE.md](examples/CLAUDE.md) — A full AI instruction file incorporating many of these conventions
- [examples/cli-example.py](examples/cli-example.py) — A sample project CLI

## Contributing

Found a convention that works for you? Open a PR. The bar is:

1. You've used it in real work (not just theorized about it)
2. It follows the What/Why/How/Example/When-to-skip format
3. It's a process convention, not a tool-specific tip

## License

MIT — use these however you want.
