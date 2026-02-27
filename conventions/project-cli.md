# Project CLI

## What

Every non-trivial project gets a `tools/cli.py` that the AI can run and extend. This is the AI's live window into the codebase — complementing static docs (what the architecture *should be*) and search indexes (pre-indexed content) with dynamic queries against the code *as it currently exists*.

## Why

Without a project CLI:
- **The AI runs ad-hoc shell commands** to inspect project state — messy, unrepeatable, and often wrong on the first try.
- **Validation is manual.** You tell the AI to check something, it cobbles together a one-liner, and neither of you can easily repeat it.
- **Knowledge is lost.** The AI discovers how to query something useful, but that knowledge lives only in the conversation and is gone next session.

The key insight: if the AI would ask the same question about your project twice, that question belongs as a CLI command. A 5-line function that checks an invariant is a perfectly valid command.

## How

### Philosophy
- **Commands are project-specific.** The AI adds commands as it discovers what information it needs. There is no universal command set.
- **Introspection and validation.** Commands serve two purposes: querying project state and validating behavior.
- **Commands are reusable queries.** Formalize ad-hoc questions into repeatable commands.
- **Read-only and test commands only.** The CLI observes and validates — it does not mutate project state.
- **Non-Python projects still use Python.** Python is always available. The CLI inspects source files as text.

### When to create it
When the AI starts a session and finds itself repeatedly running ad-hoc queries, that's the signal. Don't pre-create empty CLIs.

### Structure
```python
#!/usr/bin/env python3
"""Project CLI — AI inspection and validation tools."""

import argparse
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

def cmd_deps(args):
    """Show dependency graph for a module."""
    # Project-specific: parse imports, show what depends on what
    ...

def cmd_check_config(args):
    """Validate config files against schema."""
    # Project-specific: load config, check required keys
    ...

def cmd_test_invariant(args):
    """Verify a specific project invariant holds."""
    # Project-specific: whatever you need to check
    ...

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command")

    p_deps = sub.add_parser("deps", help="Show dependency graph")
    p_deps.add_argument("--module", required=True, help="Module name to inspect")
    sub.add_parser("check-config", help="Validate config files")
    p_inv = sub.add_parser("test-invariant", help="Verify project invariants")
    p_inv.add_argument("name", help="Invariant to check")

    args = parser.parse_args()
    commands = {"deps": cmd_deps, "check-config": cmd_check_config,
                "test-invariant": cmd_test_invariant}

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
```

### Integration with planning
- **L2 plans** include "CLI commands to add" — what new queries would help validate this change
- **L3 test strategies** include "CLI commands that validate the change"

## Example

Real commands from a game engine project CLI:
```
python tools/cli.py deps --module Graphics    # What does Graphics depend on?
python tools/cli.py find-type ContainerStyle  # Where is this type defined?
python tools/cli.py check-thread-safety       # Which components lack thread-safety docs?
python tools/cli.py validate-assets           # Do all referenced assets exist?
```

## When to skip

- **Throwaway projects** or prototypes with a lifespan of days.
- **Tiny projects** where the entire codebase fits in one or two files — ad-hoc queries are fine.
- **Projects with existing comprehensive tooling** (e.g., a mature CLI framework or task runner that already covers inspection needs).
