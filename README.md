# AI Engineering Conventions

A curated collection of process conventions for working effectively with AI coding assistants.

These aren't theoretical — they're patterns extracted from daily AI-augmented development across multiple projects, refined through real usage. Each convention is standalone: adopt what fits your workflow, skip what doesn't.

## Who this is for

- **Individual developers** using agentic AI workflows (Claude Code, Cursor Composer, Aider, etc.) who want more consistent, reliable results. Many patterns also apply to autocomplete-style assistants (Copilot, etc.).
- **Team leads** establishing AI workflows and wanting guardrails that don't kill velocity
- **Anyone** who's noticed that AI output quality varies wildly and suspects the problem is process, not the model

These conventions assume a single-developer-single-agent workflow. Multi-agent scenarios (multiple AI sessions, team members with different AI tools) may need adaptation.

> **Note:** Examples in this repo use Claude Code conventions (CLAUDE.md, .claude/ directory), but the patterns themselves are tool-agnostic. Adapt the filenames and mechanics to your tool.

## How to use this

Each convention in `conventions/` follows the same format:

- **What** — one paragraph summary
- **Why** — what goes wrong without it
- **How** — concrete implementation
- **Example** — real config, code, or workflow snippet
- **When to skip** — not everything applies everywhere

Start with the ones that address your biggest pain points. You don't need all of them.

**New to AI-augmented development?** Start with these three:
1. [Instruction Files](conventions/instruction-files.md) — foundational; everything else builds on this
2. [Checkpoint Commits](conventions/checkpoint-commits.md) — immediate safety net, zero setup cost
3. [Planning Rigor](conventions/planning-rigor.md) — prevents the most common failure mode (AI builds the wrong thing)

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

## Convention interactions

Some conventions create productive tension with each other. This is by design — you resolve the tension based on your context.

| Convention A | Convention B | Tension | Resolution |
|-------------|-------------|---------|------------|
| Checkpoint Commits | Guardrail Hooks | Hooks slow down rapid checkpointing | Skip hooks for checkpoints (`--no-verify`), rely on CI before merge |
| Context Budgeting | RAG-Augmented Dev | RAG retrieval can expand context | Set `top_k` low, filter by source; RAG replaces context, not adds to it |
| Test-First | Incremental Trust | Should the AI run tests freely? | Yes — running tests is local and reversible, always in the "free" trust tier |
| Design Change Protocol | Planning Rigor L1 | L1 says "just go"; protocol says "stop on deviations" | Protocol only applies to L2+ tasks. L1 deviations are expected and fine. |

## Contributing

Found a convention that works for you? Open a PR. The bar is:

1. You've used it in real work (not just theorized about it)
2. It follows the What/Why/How/Example/When-to-skip format
3. It's a process convention, not a tool-specific tip

## License

MIT — use these however you want.
