
#!/usr/bin/env python3
"""
pts_sysinfo_capture.py

Runs phoronix-test-suite system-info and stores the output.
Ensures dependencies are installed and system is ready.
"""

import subprocess
import shutil
import os
import sys

def is_installed(cmd):
    return shutil.which(cmd) is not None

def install_deps():
    deps = ["php-cli", "php-xml", "phoronix-test-suite"]
    for pkg in deps:
        print(f"🔧 Ensuring {pkg} is installed...")
        subprocess.run(["sudo", "apt-get", "install", "-y", pkg], check=True)

def run_pts_sysinfo(output_path="hera_info.txt"):
    with open(output_path, "w") as f:
        subprocess.run(["phoronix-test-suite", "system-info"], stdout=f, check=True)
    print(f"✅ System info written to {output_path}")

def main():
    print("📦 PTS SysInfo Capture Start")
    if not is_installed("phoronix-test-suite"):
        print("❗ PTS not found. Installing dependencies...")
        install_deps()

    run_pts_sysinfo()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
