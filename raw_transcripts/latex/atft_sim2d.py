#!/usr/bin/env python3
"""
ATFT 2D damped wave-like simulator with simple metrics.

Equation:
  d2P/dt2 = c^2 * Laplacian(P) - k * dP/dt + S(x,y,t)

Maps ATFT operators to numerical terms:
  C -> Laplacian, M -> dP/dt, R -> damping, P-hat -> localized source S

Saves results to NPZ and optional CSV metrics per time step.
"""
from __future__ import annotations

import argparse
import csv
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

import numpy as np


@dataclass
class Params:
    nx: int = 128
    ny: int = 128
    steps: int = 1000
    dt: float = 1e-3
    dx: float = 1.0
    c: float = 1.0
    k: float = 0.02
    source: str = "gaussian"  # gaussian|none|impulse
    src_amp: float = 1.0
    src_sigma: float = 3.0
    out: str = "run"
    save_pgm: bool = False
    check_energy: bool = False


def laplacian(u: np.ndarray, dx: float) -> np.ndarray:
    return (
        -4 * u
        + np.roll(u, 1, axis=0)
        + np.roll(u, -1, axis=0)
        + np.roll(u, 1, axis=1)
        + np.roll(u, -1, axis=1)
    ) / (dx * dx)


def gaussian_source(shape: Tuple[int, int], amp: float, sigma: float) -> np.ndarray:
    ny, nx = shape
    y = np.arange(ny) - ny / 2.0
    x = np.arange(nx) - nx / 2.0
    X, Y = np.meshgrid(x, y)
    return amp * np.exp(-(X**2 + Y**2) / (2 * sigma * sigma))


def coherence_proxy(u: np.ndarray) -> float:
    """Return a crude spatial coherence proxy from power spectrum peakiness.

    1. FFT2 -> power spectrum
    2. Ratio of top-bin power to mean power (excluding DC)
    """
    U = np.fft.rfft2(u)
    P = (U * np.conj(U)).real
    # exclude DC
    mean = P[1:, 1:].mean() if P.shape[0] > 1 and P.shape[1] > 1 else P.mean()
    peak = P.max()
    return float(peak / (mean + 1e-12))


def energy_like(u: np.ndarray, v: np.ndarray, c: float, dx: float) -> float:
    grad2 = np.sum((np.roll(u, -1, 0) - u) ** 2 + (np.roll(u, -1, 1) - u) ** 2)
    return 0.5 * (np.sum(v * v) + (c * c / (dx * dx)) * grad2)


def save_pgm_image(u: np.ndarray, path: str) -> None:
    arr = u.copy()
    arr -= arr.min()
    if arr.max() > 0:
        arr /= arr.max()
    img = (arr * 255.0).astype(np.uint8)
    h, w = img.shape
    with open(path, "wb") as f:
        f.write(f"P5\n{w} {h}\n255\n".encode("ascii"))
        f.write(img.tobytes())


def run(p: Params) -> None:
    ny, nx = p.ny, p.nx
    u_prev = np.zeros((ny, nx), dtype=np.float64)
    u = np.zeros_like(u_prev)
    v = np.zeros_like(u_prev)  # velocity dP/dt

    if p.source == "gaussian":
        S = gaussian_source((ny, nx), p.src_amp, p.src_sigma)
    else:
        S = np.zeros_like(u)

    dt = p.dt
    c2 = p.c * p.c
    k = p.k
    dx = p.dx

    metrics_rows = []

    for t in range(p.steps):
        lap = laplacian(u, dx)
        a = c2 * lap - k * v + S  # acceleration
        v = v + dt * a
        u = u + dt * v

        if (t % max(1, p.steps // 100)) == 0 or t == p.steps - 1:
            e = energy_like(u, v, p.c, dx)
            coh = coherence_proxy(u)
            metrics_rows.append((t, e, coh))

    out = Path(p.out)
    np.savez_compressed(
        f"{out}.npz",
        u=u,
        v=v,
        params=p.__dict__,
        metrics=np.array(metrics_rows, dtype=np.float64),
    )
    with open(f"{out}_metrics.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["step", "energy_like", "coherence_proxy"])
        w.writerows(metrics_rows)

    if p.save_pgm:
        save_pgm_image(u, f"{out}.pgm")

    if p.check_energy:
        energies = np.array([row[1] for row in metrics_rows], dtype=float)
        rel_std = float(energies.std() / (energies.mean() + 1e-12))
        msg = f"Relative energy std (should be ~0 if k=0): {rel_std:.3e}\n"
        Path(f"{out}_energy_check.txt").write_text(msg)
        print(msg.strip())

    print(f"Saved {out}.npz and {out}_metrics.csv")


def parse_args() -> Params:
    ap = argparse.ArgumentParser()
    ap.add_argument("--nx", type=int, default=128)
    ap.add_argument("--ny", type=int, default=128)
    ap.add_argument("--steps", type=int, default=1000)
    ap.add_argument("--dt", type=float, default=1e-3)
    ap.add_argument("--dx", type=float, default=1.0)
    ap.add_argument("--c", type=float, default=1.0)
    ap.add_argument("--k", type=float, default=0.02)
    ap.add_argument("--source", choices=["gaussian", "none"], default="gaussian")
    ap.add_argument("--src-amp", type=float, default=1.0)
    ap.add_argument("--src-sigma", type=float, default=3.0)
    ap.add_argument("--out", type=str, default="run")
    ap.add_argument("--save-pgm", action="store_true")
    ap.add_argument("--check-energy", action="store_true")
    a = ap.parse_args()
    return Params(
        nx=a.nx,
        ny=a.ny,
        steps=a.steps,
        dt=a.dt,
        dx=a.dx,
        c=a.c,
        k=a.k,
        source=a.source,
        src_amp=a.src_amp,
        src_sigma=a.src_sigma,
        out=a.out,
        save_pgm=a.save_pgm,
        check_energy=a.check_energy,
    )


if __name__ == "__main__":
    run(parse_args())
