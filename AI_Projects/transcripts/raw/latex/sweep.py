#!/usr/bin/env python3
"""Parameter sweep for ATFT 2D simulator.

Runs multiple configurations varying k (damping) and source sigma, saving
NPZ/CSV artifacts and an aggregate CSV summary.
"""
from __future__ import annotations

import csv
from pathlib import Path
import itertools as it
import subprocess


HERE = Path(__file__).resolve().parent
SIM = HERE / "atft_sim2d.py"


def run_case(nx, ny, steps, dt, dx, c, k, sigma, outstem):
    out = HERE / outstem
    cmd = [
        "python3",
        str(SIM),
        "--nx", str(nx),
        "--ny", str(ny),
        "--steps", str(steps),
        "--dt", str(dt),
        "--dx", str(dx),
        "--c", str(c),
        "--k", str(k),
        "--source", "gaussian",
        "--src-sigma", str(sigma),
        "--out", str(out),
    ]
    subprocess.check_call(cmd)
    return out


def main():
    nx = ny = 128
    steps = 500
    dt = 1e-3
    dx = 1.0
    c = 1.0
    ks = [0.0, 0.01, 0.05]
    sigmas = [2.0, 4.0, 8.0]

    summary_rows = [("out", "k", "sigma", "final_energy", "final_coh")]

    for k, sigma in it.product(ks, sigmas):
        stem = f"sweep_k{k:.3f}_sg{sigma:.1f}"
        out = run_case(nx, ny, steps, dt, dx, c, k, sigma, stem)
        # Parse last line of metrics CSV
        mfile = Path(f"{out}_metrics.csv")
        last = mfile.read_text().strip().splitlines()[-1]
        _, e, coh = last.split(",")
        summary_rows.append((str(out.name), k, sigma, float(e), float(coh)))

    with open(HERE / "sweep_summary.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerows(summary_rows)
    print("Wrote", HERE / "sweep_summary.csv")


if __name__ == "__main__":
    main()

