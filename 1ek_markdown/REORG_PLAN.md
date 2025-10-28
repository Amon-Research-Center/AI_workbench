# Reorganization Plan

This plan establishes conventions, documents the current state, and proposes safe next steps.

## Phase 1 — Baseline (in this change)
- Add workspace `README.md` and `docs/STRUCTURE.md`.
- Add `.editorconfig` to unify basic formatting.
- Add maintenance scripts under `scripts/`:
  - `gen_catalog.py`: generates `docs/CATALOG.md` and `docs/inventory.json`.
  - `check_naming.py`: flags suspicious names (e.g., `aquire` vs `acquire`).

## Phase 2 — Catalog and Audit
- Run catalog generation and review nested repositories and key docs.
- Compile rename candidates and path risks (especially inside Git repos).

## Phase 3 — Targeted Renames
- For non-repo content: apply direct renames.
- For nested repos: use `git mv` inside each repo and update references.

## Phase 4 — Polishing
- Add missing `README.md` at repo roots and important subfolders.
- Add per-repo tooling configs where helpful.

Changes in Phase 3 require explicit confirmation because they modify nested Git repositories.

