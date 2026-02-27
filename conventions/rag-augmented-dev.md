# RAG-Augmented Development

## What

Build project-specific search indexes (RAG — Retrieval-Augmented Generation) so the AI has accurate, searchable knowledge about your APIs, engines, frameworks, and codebases instead of relying on training data that may be outdated, incomplete, or wrong.

## Why

Without project-specific RAG:
- **The AI hallucinates API calls.** It confidently writes code using functions that don't exist, parameters that were renamed, or patterns from an older version.
- **Proprietary/internal APIs are invisible.** The AI has zero knowledge of your custom engine, internal libraries, or unpublished APIs.
- **Documentation rot goes undetected.** The AI uses patterns from its training data that worked two versions ago but are now deprecated.

RAG gives the AI a search tool for ground truth. Instead of guessing, it looks things up.

## How

### When RAG is worth the investment
- **Custom engines or frameworks** — the AI has no training data for your proprietary code
- **Rapidly evolving APIs** — the docs change faster than model training cycles
- **Large codebases** (10k+ files) — too big to fit in context, needs selective retrieval
- **Specialized domains** — game engines, embedded systems, domain-specific languages

### When RAG is overkill
- **Well-known, stable libraries** — the AI already knows React, Express, etc.
- **Small projects** — the whole codebase fits in context
- **Short-lived prototypes** — the indexing investment doesn't pay off

### Architecture pattern

```
Source material (code, docs, API specs)
    ↓
Chunker (splits into meaningful segments)
    ↓
Embeddings (semantic vectors via embedding model)
    ↓
Vector store (searchable index)
    ↓
MCP server or tool (AI queries the index)
    ↓
AI gets relevant context for its current task
```

### Key decisions

**Chunking strategy:**
- For **source code**: chunk by class/function/type — one logical unit per chunk
- For **documentation**: chunk by section/heading — preserve semantic boundaries
- For **API specs**: chunk by endpoint/type — each API surface as a unit
- Include metadata (file path, module, category) for filtering

**Embedding model:**
- Local models (e.g., `nomic-embed-text`) work well for code and avoid API costs
- Keep embeddings local for proprietary code — don't send to external APIs unless acceptable

**Practical considerations:**
- **Initial indexing:** Minutes for small codebases (< 1k files), potentially hours for large ones (10k+). Plan for this.
- **Re-indexing:** Prefer incremental re-indexing (only changed files) over full rebuilds. Full re-index on major version bumps.
- **Query latency:** 50-200ms typical for local vector stores. Adds overhead to every AI tool call.
- **Hardware:** Local embedding models strongly benefit from a GPU. CPU works but is ~10x slower for indexing. Query-time is fast either way.
- **Storage:** Vector indexes are compact — typically 100-500MB for large codebases.

**Retrieval interface:**
- Expose as an MCP server tool so the AI can search naturally during conversation
- Provide both semantic search (natural language queries) and exact lookup (type/function name)
- Support source filtering (e.g., "search only engine code" vs "search only game code")

## Example

A game project with a custom engine:

```
# Indexing pipeline
1. Parse engine C# source → extract classes, methods, enums, interfaces
2. Parse game code → same extraction
3. Parse markdown docs → chunk by heading
4. Embed all chunks with nomic-embed-text
5. Store in ChromaDB/FAISS/similar

# MCP tools exposed to AI
search_engine(query, top_k)     # Semantic search across engine code
lookup_type(name)                # Exact match by type name
search_docs(query, top_k)       # Search documentation
```

The AI's workflow becomes:
```
User: "Add a health bar to the player HUD"
AI: [searches for "health bar UI" in engine → finds ProgressBar widget]
AI: [looks up ProgressBar → gets constructor, properties, events]
AI: [searches game code for "HUD" → finds existing HUD setup pattern]
AI: [implements using actual API, not hallucinated one]
```

### Maintenance
- **Re-index when source changes.** Automate this as part of your build or CI.
- **Monitor retrieval quality.** If the AI is still hallucinating despite RAG, the chunks may be too large, too small, or poorly structured.
- **Version your index.** When the underlying API changes, stale embeddings produce wrong results.

## When to skip

- **The AI already knows your tech stack well** — standard libraries with stable APIs.
- **The project is small enough** to include all relevant code in context directly.
- **You're prototyping** and accuracy isn't critical yet — get it working first, add RAG when you scale.
