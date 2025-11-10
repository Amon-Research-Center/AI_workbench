# Hera Git Bootstrap Script in Python (for review/demo)

import os
import subprocess

# --- Environment Variables ---
vt_paths = {
    "VT": "/home/nfs/vtrust/",
    "VTT": "/home/nfs/vtrust/vt-cis",
    "VTR": "/home/nfs/vtrust/vt-transcripts-raw",
    "VTP": "/home/nfs/vtrust/vt-transcripts-processed",
    "VTL": "/home/nfs/vtrust/vt-legal",
    "VTA": "/home/nfs/vtrust/accounting",
    "VTI": "/home/nfs/vtrust/vt-ignition"
}

for key, path in vt_paths.items():
    os.environ[key] = path

# --- Git Repo Setup ---
project_dir = os.path.expanduser("~/vectortrust")
os.makedirs(project_dir, exist_ok=True)
os.chdir(project_dir)

subprocess.run(["git", "init"], check=True)
subprocess.run(["git", "config", "user.name", "Vector Trust"], check=True)
subprocess.run(["git", "config", "user.email", "vectortrust@protonmail.com"], check=True)

# Set GPG key if known
# subprocess.run(["git", "config", "user.signingkey", "YOURKEYID"], check=True)
# subprocess.run(["git", "config", "commit.gpgsign", "true"], check=True)

# Add and commit all
subprocess.run(["git", "add", "."], check=True)
subprocess.run(["git", "commit", "-m", "Initial commit: core ignition and seedpack"], check=True)

# Link remote and push (adjust URL as needed)
subprocess.run(["git", "remote", "add", "origin", "https://github.com/vectortrust/livingfield.git"], check=True)
subprocess.run(["git", "branch", "-M", "main"], check=True)
subprocess.run(["git", "push", "-u", "origin", "main"], check=True)

print("[✓] Hera repo bootstrapped successfully.")
