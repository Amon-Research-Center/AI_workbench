#!/usr/bin/env python3
"""
8-channel audio ADC recorder using Behringer UMC1820 (or similar).
Saves NumPy .npy file with timestamp.
"""
import numpy as np, sounddevice as sd, datetime as dt, argparse

ap = argparse.ArgumentParser()
ap.add_argument("--sr", type=int, default=96000, help="Sample rate (Hz)")
ap.add_argument("--dur", type=int, default=60, help="Duration (seconds)")
ap.add_argument("--ch",  type=int, default=8, help="Number of channels")
args = ap.parse_args()

sd.default.samplerate = args.sr
sd.default.channels   = args.ch

print(f"[INFO] Recording {args.ch} channels @ {args.sr} Hz for {args.dur} sec…")
data = sd.rec(int(args.dur*args.sr), dtype='float64')
sd.wait()

fname = f"adc_{dt.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}_{args.sr}Hz_{args.ch}ch.npy"
np.save(fname, data)
print("[INFO] Saved", fname)
