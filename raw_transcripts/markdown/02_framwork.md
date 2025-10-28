# 2. Mathematical Framework (Operators & Substrate)

## 2.1 State Space and Fields
- **Primary state**: $\Psi(\mathbf{x}, t)$ — define function space or lattice.
- **Substrate**: $\Phi_0(\mathbf{x})$ — specify regularity & boundary behavior.
- **Domain** $\Omega$ and inner product/norm.
> **TODO**: 2–3 sentence physical meaning of $\Psi$ and $\Phi_0$.

## 2.2 Operator Set
- $\hat P$ — Propagation/transport  • **Domain/Props/Units**: ___
- $\hat L$ — Local coupling         • **Domain/Props/Units**: ___
- $\hat C$ — Constraint/projection  • **Domain/Props/Units**: ___
- $\hat M$ — Memory/hysteresis      • **Domain/Props/Units**: ___
- $\hat R$ — Resonance/selection    • **Domain/Props/Units**: ___

## 2.3 Master Evolution Equation
\[
\frac{\partial \Psi}{\partial t}
= \hat P \Psi + \hat L(\Psi, \Phi_0) + \hat C\,\Psi + \hat M[\Psi](t) + \hat R(\Psi).
\]
> **TODO:** Replace with your exact form (or write discrete-time map).

## 2.4 Well-posedness
Spaces, local existence (Lipschitz/semigroups), energy/Lyapunov, stability, BCs.
> **TODO:** one-paragraph proof sketch.

## 2.5 Non-dimensionalization & Units
| Symbol | Meaning | Units | Scale | Non-dim | Notes |
|---|---|---|---|---|---|
| $\Psi$ |  |  |  |  |  |
| $\Phi_0$ |  |  |  |  |  |
| $\hat P$ |  |  |  |  |  |
...

## 2.6 Limiting Regimes & Recoveries
Turing-like RD • Schrödinger-like • Curvature-emergence (details in App. A)

## Imported current definitions (verbatim snippets)
> (Auto-pulled from `chap1.txt` for you to prune/refine.)
