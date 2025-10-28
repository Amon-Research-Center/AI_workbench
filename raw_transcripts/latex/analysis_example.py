#!/usr/bin/env python3
"""Example: load multichannel .npy, compute coherence, and print summary."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import numpy as np

from coherence_metrics import coherence_matrix


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("infile")
    ap.add_argument("--fs", type=float, default=96000.0)
    ap.add_argument("--nperseg", type=int, default=4096)
    ap.add_argument("--out", default="analysis")
    a = ap.parse_args()

    X = np.load(a.infile)
    f, C, P = coherence_matrix(X, a.fs, a.nperseg)
    out = Path(a.out)
    np.savez_compressed(f"{out}.npz", freqs=f, coherence=C, psd=P)
    # Print top pair coherence
    ch = X.shape[1]
    best = (None, -1.0, None)
    for i in range(ch):
        for j in range(i + 1, ch):
            idx = int(np.argmax(C[i, j]))
            val = float(C[i, j, idx])
            if val > best[1]:
                best = ((i, j), val, float(f[idx]))
    Path(f"{out}.json").write_text(json.dumps({"best_pair": best[0], "C_max": best[1], "f_max": best[2]}, indent=2))
    print("Best pair:", best)


if __name__ == "__main__":
    main()

