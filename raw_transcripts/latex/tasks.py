#!/usr/bin/env python3
"""Task loader/reporter.

Reads tasks from `/home/nfs/codex_review/todo.json` (or vtrust/tasks.yaml if present),
resolves all `paths` relative to the vtrust root, validates existence, and
generates a report and `docs/TASKS.md` for easy viewing.

Schema (JSON/YAML):
  tasks: [
    {
      id: "ATFT-001",
      title: "Fill operator units table",
      desc: "Add units/commutators; update list of symbols",
      repo: "arl/arl-atft",
      paths: ["arl/arl-atft/docs/dissertation/main.tex", "arl/arl-atft/math/operators.ipynb"],
      priority: "high|med|low",
      status: "todo|in_progress|blocked|done",
      due: "2025-09-01",
      tags: ["theory","docs"],
      acceptance_criteria: ["Units consistent", "Symbols updated"],
      artifacts: ["docs/dissertation/main.pdf"]
    }
  ]
"""
from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List

try:
    import yaml  # type: ignore
except Exception:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def load_tasks() -> List[dict]:
    # Preferred: codex_review/todo.json
    json_path = Path("/home/nfs/codex_review/todo.json")
    if json_path.exists():
        data = json.loads(json_path.read_text())
        if isinstance(data, dict) and "tasks" in data:
            return list(data["tasks"])  # type: ignore
        if isinstance(data, list):
            return list(data)  # type: ignore
        print("Unrecognized JSON schema in todo.json", file=sys.stderr)
        return []

    # Fallback: vtrust/tasks.yaml
    yml = ROOT / "tasks.yaml"
    if yml.exists() and yaml is not None:
        data = yaml.safe_load(yml.read_text())
        if isinstance(data, dict) and "tasks" in data:
            return list(data["tasks"])  # type: ignore
        if isinstance(data, list):
            return list(data)  # type: ignore

    return []


def resolve_paths(paths: List[str]) -> List[tuple[str, str, bool]]:
    out: List[tuple[str, str, bool]] = []
    for p in paths:
        rp = (ROOT / p).resolve()
        out.append((p, str(rp), rp.exists()))
    return out


def main() -> None:
    tasks = load_tasks()
    lines = ["# Tasks\n"]
    missing_total = 0
    for i, t in enumerate(tasks, 1):
        tid = t.get("id") or f"TASK-{i:03d}"
        title = t.get("title") or t.get("name") or "Untitled"
        pr = t.get("priority", "")
        st = t.get("status", "")
        paths = t.get("paths") or ([t.get("path")] if t.get("path") else [])
        res = resolve_paths([p for p in paths if p])
        miss = sum(1 for _, _, ok in res if not ok)
        missing_total += miss
        lines.append(f"- {tid}: {title} [priority={pr} status={st}]")
        for relp, absp, ok in res:
            lines.append(f"  - `{relp}` → {'OK' if ok else 'MISSING'}")
        ac = t.get("acceptance_criteria") or []
        for a in ac:
            lines.append(f"  - [ ] {a}")
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "TASKS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {DOCS / 'TASKS.md'}; tasks: {len(tasks)}, missing paths: {missing_total}")


if __name__ == "__main__":
    main()

