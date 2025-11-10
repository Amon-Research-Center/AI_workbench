#!/usr/bin/env python3
"""Check for common naming issues and style violations.

Current checks:
- misspelling: 'aquire' -> 'acquire'
- spaces in filenames/dirs
"""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT))
    except Exception:
        return str(p)


def main() -> None:
    issues = []
    for base, dnames, fnames in os.walk(ROOT):
        # Skip hidden directories
        dnames[:] = [d for d in dnames if not d.startswith('.')]

        # Skip third-party assets where filenames are canonical
        if Path(base).resolve().is_relative_to((ROOT / 'Zotero').resolve()):
            continue
        # Check directory names
        for d in dnames:
            p = Path(base) / d
            name = d
            if ' aquire ' in f' {name.lower()} ' or name.lower().endswith('aquire') or name.lower().startswith('aquire') or 'aquire_' in name.lower() or '_aquire' in name.lower():
                issues.append(("rename", rel(p), "typo 'aquire' -> 'acquire'"))
            if ' ' in name:
                issues.append(("rename", rel(p), "contains spaces"))

        # Check files
        for f in fnames:
            if f.startswith('.'):
                continue
            p = Path(base) / f
            name = f
            if 'aquire' in name.lower():
                issues.append(("rename", rel(p), "typo 'aquire' -> 'acquire'"))
            if ' ' in name:
                issues.append(("rename", rel(p), "contains spaces"))

    if not issues:
        print("No naming issues found.")
        return

    print("Naming issues found (proposal):")
    for kind, path, note in sorted(issues, key=lambda t: (t[0], t[1])):
        print(f"- {kind:6s} {path}  # {note}")


if __name__ == "__main__":
    main()
