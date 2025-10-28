#!/usr/bin/env python3
"""Curate transcripts into a stable mirror with a manifest and index.

Creates symlinks under vtrust/curation/transcripts/ with slugified filenames
pointing to originals scattered across the workspace. Generates:
- vtrust/curation/transcripts/manifest.json
- vtrust/curation/transcripts/manifest.csv
- vtrust/docs/transcripts_index.md

Heuristics:
- Include text-like files (.txt, .md) whose path contains 'transcripts', or
  filenames that look like dated logs (e.g., starting with digits), or known
  keywords discovered in this workspace (e.g., 'the_beginning').
- Skip hidden files and .git directories.
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
CUR = ROOT / "curation" / "transcripts"
DOCS = ROOT / "docs"


TEXT_EXT = {".txt", ".md"}
KEYWORDS = {"transcripts", "the_beginning"}
DATE_RE = re.compile(r"^(\d{6,8}|\d{4}-?\d{2}-?\d{2})")
TIME_RE = re.compile(r"(\d{8})(\d{4})")


def sha256_file(p: Path, chunk_size: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        while True:
            b = f.read(chunk_size)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def slugify(name: str) -> str:
    # Lowercase, replace spaces/quotes with underscores, remove weird chars
    s = name.strip().lower()
    s = s.replace("\"", "").replace("'", "")
    s = re.sub(r"\s+", "_", s)
    s = re.sub(r"[^a-z0-9._-]", "", s)
    return s


@dataclass
class Entry:
    src: str
    link: str
    size: int
    sha256: str
    ext: str
    inferred_date: str | None
    ai: str | None


def should_include(path: Path) -> bool:
    if path.suffix.lower() not in TEXT_EXT:
        return False
    pstr = str(path).lower()
    if any(k in pstr for k in KEYWORDS):
        return True
    if DATE_RE.match(path.name):
        return True
    if "/transcripts/" in pstr:
        return True
    return False


def find_candidates(root: Path) -> Iterable[Path]:
    for base, dnames, fnames in os.walk(root):
        dnames[:] = [d for d in dnames if not d.startswith(".") and d != ".git"]
        for fn in fnames:
            if fn.startswith("."):
                continue
            p = Path(base) / fn
            if should_include(p):
                yield p


def main() -> None:
    CUR.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)

    seen_hashes: dict[str, int] = {}
    entries: list[Entry] = []

    for src in sorted(find_candidates(ROOT)):
        try:
            size = src.stat().st_size
        except FileNotFoundError:
            continue
        if size == 0:
            continue
        h = sha256_file(src)
        ext = src.suffix.lower() or ""
        base_slug = slugify(src.stem)
        # Ensure uniqueness by hashing duplicate content
        idx = seen_hashes.get(h, 0)
        link_name = f"{base_slug}{('-'+str(idx)) if idx else ''}{ext}"
        # Avoid collisions on disk
        while (CUR / link_name).exists():
            idx += 1
            link_name = f"{base_slug}-{idx}{ext}"
        seen_hashes[h] = idx + 1

        link_path = CUR / link_name
        # Create/refresh symlink
        if link_path.is_symlink() or link_path.exists():
            link_path.unlink()
        try:
            link_path.symlink_to(src)
        except Exception:
            # Fallback to relative symlink if needed
            try:
                link_path.symlink_to(os.path.relpath(src, CUR))
            except Exception:
                # As a last resort, skip linking but still record
                pass

        inferred_date = None
        m = DATE_RE.match(src.name)
        if m:
            inferred_date = m.group(1)
            if len(inferred_date) == 6:
                inferred_date = '20' + inferred_date  # naive year expansion

        # Infer AI label from file head
        ai = None
        try:
            head = (Path(ROOT / src).read_text(encoding='utf-8', errors='ignore'))[:2000].lower()
            if 'chatgpt said' in head or 'chatgpt' in head:
                ai = 'chatgpt'
            elif 'claude' in head:
                ai = 'claude'
            elif 'mistral' in head:
                ai = 'mistral'
            elif 'llama' in head:
                ai = 'llama'
            elif 'modulus sage' in head or 'sage said' in head:
                ai = 'sage'
        except Exception:
            pass

        entries.append(
            Entry(
                src=str(src.relative_to(ROOT)),
                link=str(link_path.relative_to(ROOT)),
                size=size,
                sha256=h,
                ext=ext.lstrip("."),
                inferred_date=inferred_date,
                ai=ai,
            )
        )

    # Write manifest.json
    (CUR / "manifest.json").write_text(
        json.dumps([asdict(e) for e in entries], indent=2), encoding="utf-8"
    )
    # Write manifest.csv
    with (CUR / "manifest.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["src", "link", "size", "sha256", "ext", "inferred_date"])
        for e in entries:
            w.writerow([e.src, e.link, e.size, e.sha256, e.ext, e.inferred_date or ""])

    # Chronological index (by inferred date)
    try:
        e_sorted = sorted(entries, key=lambda e: ((e.inferred_date or '99999999'), (e.ai or 'zzz'), e.src))
    except Exception:
        e_sorted = entries
    lines = ["# Transcripts Index (Chronological)\n", "Sorted by inferred date and AI tag.\n"]
    for e in e_sorted:
        tag = f" [{e.ai}]" if e.ai else ""
        lines.append(f"- `{e.link}` (from `{e.src}`, {e.size} bytes){tag}")
    (DOCS / "transcripts_index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Extract suggestions and AI vision statements (heuristics)
    sugg, vision = [], []
    SUGG_PAT = re.compile(r"\b(should|recommend|suggest|could|next step|improve|fix|rename|normalize|standardize|derive|prove)\b", re.I)
    VISION_PAT = re.compile(r"\b(this (work|theory)|we (present|propose)|goal:|aims to|cmci|amon\W*turing|dissertation|unified)\b", re.I)
    for e in e_sorted:
        p = ROOT / e.src
        try:
            txt = p.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        for line in txt.splitlines():
            if SUGG_PAT.search(line):
                sugg.append(f"- {e.inferred_date or ''} {e.ai or ''} {line.strip()}")
            if VISION_PAT.search(line):
                vision.append(f"- {e.inferred_date or ''} {e.ai or ''} {line.strip()}")
    (DOCS / "suggestions.md").write_text("\n".join(["# Suggestions Extracted\n"] + sugg) + "\n", encoding='utf-8')
    (DOCS / "ai_vision.md").write_text("\n".join(["# AI Vision Statements\n"] + vision) + "\n", encoding='utf-8')

    print(f"Curated {len(entries)} transcripts → {CUR.relative_to(ROOT)} (chronological + summaries)")


if __name__ == "__main__":
    main()
