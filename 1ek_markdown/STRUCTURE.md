# Structure & Conventions

This workspace contains multiple projects and nested Git repositories. The goal is to keep navigation predictable and reduce friction across research, code, and ops.

## Top-Level Layout
- `arl/`: Research projects under Amon Research Labs.
- `holding/`: Organization operations, templates, and shared assets.
- `Zotero/`: Citation and bibliography resources.
- `ai_memories/`: Short-term notes and scratch space.

## Numbered Folders
Projects commonly use numeric prefixes to group concerns:

- `00_meta`: high-level metadata, governance, goals
- `10_*`–`40_*`: domain assets (hardware, acquisition, notebooks)
- `50_references`: literature, citations
- `60_*`–`90_*`: processing, tools, docs, scripts
- `98_eklectic`: personal notes/scratch
- `99_Archive`: archived material

Prefer American English and correct spelling in folder names. For example, use `acquire` not `aquire`.

## Nested Git Repos
- Treat each nested repo as independent; do not move or rename its internal folders without a deliberate migration plan.
- Repo root should include a short `README.md` and a license when applicable.
- Cross-references should be relative paths or links to Git remotes.

## File Naming
- Kebab-case or snake_case for files and directories; avoid spaces.
- Use concise, descriptive names; prefer `.md` for lightweight docs.
- Avoid committing large binaries unless required; place large data under a `data/` subfolder with a `README.md` and `.gitignore`/LFS rules.

## Tooling Baseline
- Shared editor settings via `.editorconfig` at the workspace root.
- A `scripts/` folder for maintenance scripts (catalog generation, lint helpers).
- Auto-generated inventory in `docs/CATALOG.md` and machine-readable `docs/inventory.json`.

## Rename Policy
- For typos or inconsistent names inside nested repos, propose renames and apply via `git mv` within that repo to preserve history.
- For non-repo content, standard filesystem renames are acceptable.

