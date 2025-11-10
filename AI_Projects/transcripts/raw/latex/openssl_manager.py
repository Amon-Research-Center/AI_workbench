#!/usr/bin/env python3
# openssl_manager.py
import argparse, os, platform, shutil, subprocess, sys, time, json
from pathlib import Path

try:
    import yaml  # optional
except Exception:
    yaml = None

OS = platform.system().lower()

PKG_SYSTEMS = {
    "linux-apt": ["apt-get", "install", "-y", "openssl"],
    "linux-dnf": ["dnf", "install", "-y", "openssl"],
    "linux-yum": ["yum", "install", "-y", "openssl"],
    "mac-brew":  ["brew", "install", "openssl"]
}

def run(cmd, check=True):
    return subprocess.run(cmd, text=True, capture_output=True, check=check)

def sudo_wrap(cmd):
    if os.geteuid() == 0:
        return cmd
    return ["sudo"] + cmd

def detect_pkg_mgr():
    if OS == "darwin":
        return "mac-brew" if shutil.which("brew") else None
    # Linux
    if shutil.which("apt-get"):
        return "linux-apt"
    if shutil.which("dnf"):
        return "linux-dnf"
    if shutil.which("yum"):
        return "linux-yum"
    return None

def which_openssl():
    for p in ["openssl"]:
        w = shutil.which(p)
        if w:
            return w
    return None

def openssl_version():
    exe = which_openssl()
    if not exe:
        return None, None
    r = run([exe, "version"], check=False)
    vline = r.stdout.strip()
    return exe, vline

def install_openssl():
    mgr = detect_pkg_mgr()
    if not mgr:
        print("Unsupported platform or missing package manager."); return 1
    cmd = PKG_SYSTEMS[mgr]
    print(f"Installing OpenSSL via {mgr} …")
    r = run(sudo_wrap(cmd), check=False)
    print(r.stdout or r.stderr)
    return r.returncode

def uninstall_openssl():
    mgr = detect_pkg_mgr()
    if not mgr:
        print("Unsupported platform or missing package manager."); return 1
    if mgr == "linux-apt":
        cmd = ["apt-get", "remove", "-y", "openssl"]
    elif mgr in ("linux-dnf", "linux-yum"):
        cmd = ["dnf" if mgr=="linux-dnf" else "yum", "remove", "-y", "openssl"]
    elif mgr == "mac-brew":
        cmd = ["brew", "uninstall", "openssl"]  # could be openssl@3
    else:
        print("Unknown manager."); return 1
    print(f"Uninstalling OpenSSL via {mgr} …")
    r = run(sudo_wrap(cmd), check=False)
    print(r.stdout or r.stderr)
    return r.returncode

def reinstall_openssl():
    rc1 = uninstall_openssl()
    rc2 = install_openssl() if rc1 == 0 else 1
    return rc1 or rc2

def load_config(path):
    if not path:
        return {}
    p = Path(path)
    if not p.exists():
        print(f"Config not found: {path}"); return {}
    try:
        if p.suffix.lower() in (".yaml", ".yml"):
            if not yaml:
                print("PyYAML not available; install pyyaml or use JSON."); return {}
            with open(p, "r") as f:
                return yaml.safe_load(f) or {}
        else:
            with open(p, "r") as f:
                return json.load(f)
    except Exception as e:
        print(f"Config parse error: {e}")
        return {}

def backup(path):
    src = Path(path)
    if not src.exists():
        return None
    ts = time.strftime("%Y%m%d-%H%M%S")
    dst = src.with_suffix(src.suffix + f".bak.{ts}")
    shutil.copy2(src, dst)
    return str(dst)

def find_openssl_conf(custom=None):
    if custom:
        return custom
    # Common locations
    candidates = [
        "/etc/ssl/openssl.cnf",
        "/etc/openssl/openssl.cnf",
        "/usr/local/etc/openssl/openssl.cnf",
        "/usr/local/ssl/openssl.cnf",
        "/opt/homebrew/etc/openssl/openssl.cnf",
        "/opt/homebrew/etc/openssl@3/openssl.cnf",
    ]
    for c in candidates:
        if Path(c).exists():
            return c
    # Fallback via openssl version -d (OPENSSLDIR)
    exe = which_openssl()
    if exe:
        r = run([exe, "version", "-d"], check=False)
        out = r.stdout.strip()
        # format: OPENSSLDIR: "/etc/ssl"
        if ":" in out:
            d = out.split(":", 1)[1].strip().strip('"')
            guess = os.path.join(d, "openssl.cnf")
            if Path(guess).exists():
                return guess
    return None

DEFAULT_CONF_SNIPPET = """\
# Added by openssl_manager.py
openssl_conf = default_conf

[default_conf]
ssl_conf = ssl_sect
providers = provider_sect

[provider_sect]
default = default_sect
legacy = legacy_sect

[default_sect]
activate = 1

[legacy_sect]
activate = 0

[ssl_sect]
system_default = ssl_default_sect

[ssl_default_sect]
MinProtocol = TLSv1.2
CipherString = DEFAULT:@SECLEVEL=2
"""

def ensure_line(s, key, value):
    out = []
    found = False
    for line in s.splitlines():
        if line.strip().startswith(key):
            out.append(f"{key} = {value}")
            found = True
        else:
            out.append(line)
    if not found:
        out.append(f"{key} = {value}")
    return "\n".join(out) + "\n"

def configure_openssl(cfg):
    conf_path = find_openssl_conf(cfg.get("openssl_conf"))
    if not conf_path:
        print("openssl.cnf not found."); return 1
    print(f"Using conf: {conf_path}")
    b = backup(conf_path)
    if b: print(f"Backup: {b}")

    text = Path(conf_path).read_text()

    # Ensure root directive present
    if "openssl_conf" not in text:
        text = text.rstrip() + "\n\n" + DEFAULT_CONF_SNIPPET

    # Apply overrides from cfg.ssl (if provided)
    ssl = (cfg.get("ssl") or {})
    min_proto = ssl.get("min_protocol")  # e.g., TLSv1.2, TLSv1.3
    cipher = ssl.get("cipher_string")    # e.g., "DEFAULT:@SECLEVEL=2"
    seclvl = ssl.get("security_level")   # 0-5, if provided, overwrite in CipherString

    # Remodel [ssl_default_sect]
    # Simple replace: adjust MinProtocol and CipherString lines anywhere they appear
    def replace_kv(block_text, k, v):
        return ensure_line(block_text, k, v)

    if min_proto:
        text = text.replace("MinProtocol = TLSv1.2", f"MinProtocol = {min_proto}")
        # fallback if line not matched:
        text = ensure_line(text, "MinProtocol", min_proto)

    if cipher:
        text = text.replace("CipherString = DEFAULT:@SECLEVEL=2", f"CipherString = {cipher}")
        text = ensure_line(text, "CipherString", cipher)

    if seclvl is not None:
        # naive adjust in CipherString if @SECLEVEL appears
        lines = []
        for line in text.splitlines():
            if line.strip().startswith("CipherString"):
                # try to normalize seclevel
                if "@SECLEVEL=" in line:
                    pre = line.split("@SECLEVEL=")[0]
                    lines.append(pre + f"@SECLEVEL={int(seclvl)}")
                else:
                    lines.append(line + f"@SECLEVEL={int(seclvl)}")
            else:
                lines.append(line)
        text = "\n".join(lines) + "\n"

    Path(conf_path).write_text(text)
    print("Configuration applied.")
    return 0

def reconfigure_openssl(cfg):
    return configure_openssl(cfg)

def show_status():
    exe, ver = openssl_version()
    print(f"openssl path: {exe or 'not found'}")
    print(f"openssl version: {ver or 'n/a'}")
    conf = find_openssl_conf(None)
    print(f"openssl.cnf: {conf or 'not found'}")

def menu(cfg):
    actions = {
        "1": ("Show status", lambda: (show_status(), 0)[1]),
        "2": ("Install", install_openssl),
        "3": ("Uninstall", uninstall_openssl),
        "4": ("Reinstall", reinstall_openssl),
        "5": ("Configure", lambda: configure_openssl(cfg)),
        "6": ("Reconfigure", lambda: reconfigure_openssl(cfg)),
        "0": ("Exit", lambda: sys.exit(0)),
    }
    while True:
        print("\nOpenSSL Manager")
        for k in sorted(actions.keys()):
            print(f" {k}) {actions[k][0]}")
        choice = input("> ").strip()
        fn = actions.get(choice)
        if not fn:
            print("Invalid."); continue
        rc = fn[1]()
        if rc not in (0, None):
            print(f"Return code: {rc}")

def parse_args():
    ap = argparse.ArgumentParser(description="Modular OpenSSL controller")
    ap.add_argument("--config", help="Path to JSON or YAML config")
    ap.add_argument("--noninteractive", action="store_true", help="Run and exit after --action")
    ap.add_argument("--action", choices=["status","install","uninstall","reinstall","configure","reconfigure"])
    return ap.parse_args()

def main():
    args = parse_args()
    cfg = load_config(args.config)
    if args.noninteractive and args.action:
        actions = {
            "status": lambda: (show_status(), 0)[1],
            "install": install_openssl,
            "uninstall": uninstall_openssl,
            "reinstall": reinstall_openssl,
            "configure": lambda: configure_openssl(cfg),
            "reconfigure": lambda: reconfigure_openssl(cfg),
        }
        rc = actions[args.action]()
        sys.exit(rc if isinstance(rc, int) else 0)
    menu(cfg)

if __name__ == "__main__":
    main()
