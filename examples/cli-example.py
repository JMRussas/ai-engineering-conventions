#!/usr/bin/env python3
"""
Example Project CLI — AI inspection and validation tools.

This is a sample CLI showing how a project-specific CLI might look.
Real CLIs grow organically as the AI discovers what queries it needs.
Commands here are illustrative — your project's commands will be different.

Usage:
    python tools/cli.py deps --module MODULE
    python tools/cli.py check-config
    python tools/cli.py find-type TYPE_NAME
    python tools/cli.py api-routes
"""

import argparse
import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
SRC_DIR = PROJECT_ROOT / "src"


def cmd_deps(args):
    """Show what a module imports and what imports it."""
    target = args.module
    imports_from = []  # What this module depends on
    imported_by = []   # What depends on this module

    for ts_file in SRC_DIR.rglob("*.ts*"):
        relative = ts_file.relative_to(SRC_DIR)
        content = ts_file.read_text(encoding="utf-8", errors="replace")

        # Check if this file imports the target (match path segment, not substring)
        if re.search(rf"""from\s+['"].*\b{re.escape(target)}\b""", content):
            if not any(part == target for part in relative.parts):
                imported_by.append(str(relative))

        # Check if the target file imports from elsewhere (match path segment)
        if any(part == target or part.startswith(target + ".") for part in relative.parts):
            for match in re.finditer(r"""from\s+['"]([^'"]+)['"]""", content):
                imports_from.append(match.group(1))

    print(f"\n{target} depends on:")
    for dep in sorted(set(imports_from)):
        print(f"  {dep}")

    print(f"\nImported by:")
    for dep in sorted(set(imported_by)):
        print(f"  {dep}")


def cmd_check_config(args):
    """Validate that config.ts references match .env.example."""
    config_file = SRC_DIR / "config.ts"
    env_example = PROJECT_ROOT / ".env.example"

    if not config_file.exists():
        print("ERROR: src/config.ts not found")
        sys.exit(1)

    config_content = config_file.read_text(encoding="utf-8")
    config_vars = set(re.findall(r"process\.env\.(\w+)", config_content))

    if env_example.exists():
        env_content = env_example.read_text(encoding="utf-8")
        env_vars = set(re.findall(r"^(\w+)=", env_content, re.MULTILINE))

        missing_from_env = config_vars - env_vars
        unused_in_env = env_vars - config_vars

        if missing_from_env:
            print("Config vars NOT in .env.example:")
            for var in sorted(missing_from_env):
                print(f"  {var}")

        if unused_in_env:
            print("Env vars NOT referenced in config.ts:")
            for var in sorted(unused_in_env):
                print(f"  {var}")

        if not missing_from_env and not unused_in_env:
            print("Config and .env.example are in sync.")
    else:
        print(f"Config references {len(config_vars)} env vars (no .env.example to check against)")
        for var in sorted(config_vars):
            print(f"  {var}")


def cmd_find_type(args):
    """Find where a type/interface/class is defined."""
    target = args.name
    pattern = re.compile(
        rf"(export\s+)?(type|interface|class|enum)\s+{re.escape(target)}\b"
    )

    found = []
    for ts_file in SRC_DIR.rglob("*.ts*"):
        content = ts_file.read_text(encoding="utf-8", errors="replace")
        for i, line in enumerate(content.splitlines(), 1):
            if pattern.search(line):
                found.append((ts_file.relative_to(PROJECT_ROOT), i, line.strip()))

    if found:
        for path, line_num, line in found:
            print(f"{path}:{line_num}  {line}")
    else:
        print(f"Type '{target}' not found in src/")


def cmd_api_routes(args):
    """List all API route definitions."""
    route_pattern = re.compile(
        r"""(app|router)\.(get|post|put|patch|delete)\s*\(\s*['"]([^'"]+)['"]"""
    )

    routes = []
    for ts_file in SRC_DIR.rglob("*.ts*"):
        content = ts_file.read_text(encoding="utf-8", errors="replace")
        for match in route_pattern.finditer(content):
            method = match.group(2).upper()
            path = match.group(3)
            routes.append((method, path, ts_file.relative_to(PROJECT_ROOT)))

    if routes:
        for method, path, file in sorted(routes, key=lambda r: r[1]):
            print(f"  {method:7s} {path:30s}  ({file})")
    else:
        print("No route definitions found.")


def main():
    parser = argparse.ArgumentParser(
        description="Project CLI — AI inspection and validation tools"
    )
    sub = parser.add_subparsers(dest="command")

    p_deps = sub.add_parser("deps", help="Show module dependencies")
    p_deps.add_argument("--module", required=True, help="Module name to inspect")

    sub.add_parser("check-config", help="Validate config vs .env.example")

    p_find = sub.add_parser("find-type", help="Find type/interface/class definition")
    p_find.add_argument("name", help="Type name to search for")

    sub.add_parser("api-routes", help="List all API route definitions")

    args = parser.parse_args()

    commands = {
        "deps": cmd_deps,
        "check-config": cmd_check_config,
        "find-type": cmd_find_type,
        "api-routes": cmd_api_routes,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
