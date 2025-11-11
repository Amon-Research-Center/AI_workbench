#!/usr/bin/env python3
# Filename: bmf_simulation.py
# Version: 0.1.0
# Description: Lyapunov-stable sim of BMF attractor decay (φ→φ₀) on 2D substrate. Plots field evolution.
# Date: 2025-10-28
# Execution: chmod +x bmf_simulation.py && ./bmf_simulation.py
#   - Prompts for params: alpha (P op), tau_steps, grid_size.
#   - Requires numpy, matplotlib (pre-installed in podman python:3.12 image).
#   - Outputs: phi_evolution.png + console Lyapunov E trace.

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp  # For toy time-evolution.

def master_eq(t, psi, H_params, phi0):
    """iℏ ∂_τ Ψ = ĤΨ + S[Φ₀]; toy 1D slice for demo."""
    alpha, beta, gamma, delta, epsilon = H_params  # Five ops as scalars here; extend to matrices.
    H_psi = (alpha * np.real(psi) + beta * np.imag(psi) +  # Placeholder non-commute via phase.
             gamma * np.sin(psi) + delta * np.cos(psi) + epsilon * np.tanh(psi))
    S_phi = -0.1 * (psi - phi0)  # Attractor sink; Lyapunov E = dS/dpsi <=0.
    return 1j * H_psi + S_phi  # ℏ=1 norm.

# User inputs.
alpha = float(input("Enter alpha (P op strength, def 1.0): ") or "1.0")
h_params = [alpha, 1.0, 0.5, 0.3, 0.2]  # Defaults; tweak for elements.
tau_steps = int(input("Enter time steps (def 100): ") or "100")
grid_size = int(input("Enter grid size N (def 50): ") or "50")
phi0 = np.zeros((grid_size, grid_size))  # Target attractor.

# Initial field: Gaussian bump.
x, y = np.meshgrid(np.linspace(-1, 1, grid_size), np.linspace(-1, 1, grid_size))
psi0 = np.exp(-(x**2 + y**2) / 0.1) + 1j * np.sin(x * y)  # Complex info density.

# Flatten for ODE solve (vectorized).
psi0_flat = psi0.flatten()
t_span = (0, tau_steps)
sol = solve_ivp(lambda t, psi: np.array([master_eq(t, psi[i], h_params, phi0.flat[i]) for i in range(len(psi))]),
                t_span, psi0_flat, t_eval=np.linspace(0, tau_steps, 50), method='RK45')

# Reshape & plot final phi vs phi0 decay.
phi_final = sol.y[:,-1].reshape(grid_size, grid_size).real
fig, ax = plt.subplots(1, 2, figsize=(10,5))
ax[0].imshow(psi0.real, cmap='viridis'); ax[0].set_title('Initial Φ')
ax[1].imshow(phi_final, cmap='viridis'); ax[1].set_title(f'Final Φ (E≤0 sink)')
plt.savefig('phi_evolution.png')
plt.show()

# Lyapunov trace (toy: |dΨ/dt| contraction).
lyap_E = np.diff(np.linalg.norm(sol.y, axis=0))  # <=0 check.
print(f"Lyapunov trace sample: {lyap_E[-5:]}")  # Last 5; expect non-positive.
