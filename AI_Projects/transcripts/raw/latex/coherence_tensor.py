#!/usr/bin/env python3
"""
Coherence tensor analysis
- Computes cross-spectral density (CSD) matrix
- Computes coherence matrix
- Provides Higher Order SVD (HOSVD)
"""
import numpy as np
from scipy.signal import stft, get_window

def csd_matrix(X, fs, nperseg=8192, noverlap=4096):
    chans = list(X.keys()); Z={}; f=t=None
    for k in chans:
        f,t,Z[k] = stft(X[k], fs=fs, nperseg=nperseg, noverlap=noverlap,
                        window=get_window('hann', nperseg), return_onesided=True)
    F=len(f); n=len(chans)
    S=np.zeros((F,n,n),complex); P=np.zeros((F,n))
    for i,ci in enumerate(chans):
        Zi=Z[ci]; P[:,i]=(Zi*np.conj(Zi)).mean(axis=1).real
        for j,cj in enumerate(chans):
            Zj=Z[cj]; S[:,i,j]=(Zi*np.conj(Zj)).mean(axis=1)
    C = np.abs(S)**2 / (P[:,None,:]*P[:,:,None] + 1e-18)
    return f, S, P, C, chans

def unfold(T, mode): return np.reshape(np.moveaxis(T, mode, 0), (T.shape[mode], -1))
def hosvd(T, ranks):
    U=[]; G=T.copy()
    for m in range(T.ndim):
        U_m,_,_ = np.linalg.svd(unfold(T,m), full_matrices=False)
        U.append(U_m[:,:ranks[m]])
    for m in range(T.ndim):
        G = np.tensordot(np.conj(U[m]).T, G, axes=(1,m)); G = np.moveaxis(G,0,m)
    return G,U
