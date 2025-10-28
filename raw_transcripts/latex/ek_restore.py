
#!/usr/bin/env python3
"""
ek_restore.py - v2

Enhanced system restoration:
- Auto-detect snapshot tarball
- Extract to ~/snapshots/
- Check for missing components
- Reinstall packages from apt list --manual-installed
"""

import os
import shutil
import subprocess
import tarfile
import yaml
from pathlib import Path

CONFIG = "ek_recover.yaml"
SNAPSHOT_DIR = Path.home() / "snapshots"
SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

def load_config():
    with open(CONFIG, 'r') as f:
        return yaml.safe_load(f)

def unpack_snapshot_tarball():
    tarballs = sorted(Path(".").glob("ekdot_*.tar.gz"), reverse=True)
    if not tarballs:
        print("❌ No snapshot tarball found in current directory.")
        return
    latest = tarballs[0]
    print(f"📦 Unpacking snapshot: {latest}")
    with tarfile.open(latest, "r:gz") as tar:
        tar.extractall(path=SNAPSHOT_DIR)

def restore_file(src, dest):
    try:
        src_path = SNAPSHOT_DIR / Path(src).expanduser().name
        dest_path = Path(os.path.expanduser(dest))
        if not src_path.exists():
            print(f"⚠️ Missing from snapshot: {src_path}")
            return
        print(f"🔄 Restoring {dest_path} from {src_path}")
        if src_path.is_file():
            shutil.copy2(src_path, dest_path)
        elif src_path.is_dir():
            if dest_path.exists():
                shutil.rmtree(dest_path)
            shutil.copytree(src_path, dest_path)
    except Exception as e:
        print(f"⚠️ Error restoring {dest}: {e}")

def reinstall_apt_packages():
    pkgs_file = SNAPSHOT_DIR / "manual_installed_pkgs.txt"
    if pkgs_file.exists():
        print("📦 Reinstalling saved apt packages...")
        with open(pkgs_file) as f:
            pkgs = [line.strip() for line in f if line.strip()]
        subprocess.run(["sudo", "apt-get", "install", "-y"] + pkgs)
    else:
        print("⚠️ No package list found (manual_installed_pkgs.txt)")

def main():
    print("🚀 Starting ek_restore...")
    unpack_snapshot_tarball()
    cfg = load_config()
    includes = cfg.get("include", [])
    excludes = cfg.get("exclude", [])

    for path in includes:
        if path not in excludes:
            restore_file(path, path)

    reinstall_apt_packages()
    print("✅ Full system recovery routine complete.")

if __name__ == "__main__":
    main()
