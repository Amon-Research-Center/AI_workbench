#!/usr/bin/env python3
"""Compute pairwise magnitude-squared coherence from multi-channel data.

Input: Numpy .npy file produced by acquisition (shape: samples x channels).
Output: NPZ with frequency axis and coherence matrix per pair; JSON summary.

Implements a basic Welch periodogram with numpy only.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Tuple

import numpy as np


def welch(x: np.ndarray, fs: float, nperseg: int) -> Tuple[np.ndarray, np.ndarray]:
    step = nperseg // 2
    n = x.shape[0]
    window = np.hanning(nperseg)
    scale = (window**2).sum()
    segs = []
    for start in range(0, n - nperseg + 1, step):
        seg = x[start : start + nperseg]
        segs.append(np.fft.rfft(window * seg))
    if not segs:
        raise ValueError("Signal too short for nperseg")
    S = np.stack(segs)
    Pxx = (np.abs(S) ** 2).mean(axis=0) / scale
    freqs = np.fft.rfftfreq(nperseg, d=1.0 / fs)
    return freqs, Pxx


def coherence_matrix(X: np.ndarray, fs: float, nperseg: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    # X: samples x channels
    freqs = None
    P = []
    for ch in range(X.shape[1]):
        f, Pxx = welch(X[:, ch], fs, nperseg)
        P.append(Pxx)
        if freqs is None:
            freqs = f
    P = np.array(P)  # channels x freqs

    # Cross-spectra via Welch on products
    step = nperseg // 2
    n = X.shape[0]
    window = np.hanning(nperseg)
    scale = (window**2).sum()
    segs = []
    for start in range(0, n - nperseg + 1, step):
        seg = X[start : start + nperseg] * window[:, None]
        S = np.fft.rfft(seg, axis=0)  # freqs x channels
        segs.append(S)
    Sstack = np.stack(segs)  # segments x freqs x channels

    # Coherence for each pair at each freq
    ch = X.shape[1]
    C = np.zeros((ch, ch, freqs.shape[0]), dtype=np.float64)
    for i in range(ch):
        for j in range(ch):
            Pxy = (Sstack[:, :, i] * np.conj(Sstack[:, :, j])).mean(axis=0) / scale
            C[i, j, :] = (np.abs(Pxy) ** 2) / (P[i] * P[j] + 1e-18)

    return freqs, C, P


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("infile", help="Input .npy (samples x channels)")
    ap.add_argument("--fs", type=float, default=96000.0, help="Sampling rate Hz")
    ap.add_argument("--nperseg", type=int, default=4096)
    ap.add_argument("--out", type=str, default="coh")
    a = ap.parse_args()

    X = np.load(a.infile)
    if X.ndim != 2:
        raise ValueError("Expected 2D array (samples x channels)")

    freqs, C, P = coherence_matrix(X, a.fs, a.nperseg)

    np.savez_compressed(f"{a.out}.npz", freqs=freqs, coherence=C, psd=P)
    # Simple summary: max coherence per pair and its frequency
    ch = X.shape[1]
    summary = {"pairs": []}
    for i in range(ch):
        for j in range(i + 1, ch):
            idx = int(np.argmax(C[i, j]))
            summary["pairs"].append({
                "i": i, "j": j, "f_max": float(freqs[idx]), "C_max": float(C[i, j, idx])
            })
    Path(f"{a.out}.json").write_text(json.dumps(summary, indent=2))
    print(f"Wrote {a.out}.npz and {a.out}.json")


if __name__ == "__main__":
    main()

