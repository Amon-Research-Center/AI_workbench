
#!/usr/bin/env python3
"""
ek_snapdot.py

Harvests user and system dotfiles/configs, archives them, and stages them for Git.
"""

import os
import shutil
import datetime
import subprocess
from pathlib import Path

# Paths to include in snapshot
SNAP_PATHS = [
    "~/.bashrc",
    "~/.bash_aliases",
    "~/.zshrc",
    "~/.nanorc",
    "~/.gitconfig",
    "~/.vimrc",
    "~/.ssh/config",
    "/etc/hosts",
    "/etc/network/interfaces"
]

SNAP_ROOT = Path.home() / "snapshots"
SNAP_ROOT.mkdir(parents=True, exist_ok=True)

def expand(path):
    return Path(os.path.expanduser(path)).resolve()

def collect_files():
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    bundle_dir = SNAP_ROOT / f"ekdot_{stamp}"
    bundle_dir.mkdir()
    copied = []

    for path in SNAP_PATHS:
        p = expand(path)
        if p.exists():
            try:
                dest = bundle_dir / p.name
                if p.is_file():
                    shutil.copy2(p, dest)
                    copied.append(str(dest))
                elif p.is_dir():
                    shutil.copytree(p, dest)
                    copied.append(str(dest))
            except Exception as e:
                print(f"⚠️ Could not copy {p}: {e}")

    return bundle_dir, copied

def archive(bundle_dir):
    archive_path = str(bundle_dir) + ".tar.gz"
    shutil.make_archive(str(bundle_dir), "gztar", root_dir=bundle_dir)
    return archive_path

def git_commit(archive_path):
    git_dir = "/home/nfs/vtrust/vt-cis/git"
    dest = Path(git_dir) / Path(archive_path).name
    shutil.move(archive_path, dest)
    subprocess.run(["git", "-C", git_dir, "add", dest.name], check=True)
    subprocess.run(["git", "-C", git_dir, "commit", "-m", f"dot snapshot: {dest.name}"], check=True)
    print(f"✅ Snapshot committed to git: {dest.name}")

def main():
    print("📦 Harvesting dotfiles...")
    bundle_dir, files = collect_files()
    print(f"📁 Collected: {len(files)} files")
    archive_path = archive(bundle_dir)
    print(f"🗜 Archived at: {archive_path}")
    git_commit(archive_path)

if __name__ == "__main__":
    main()
