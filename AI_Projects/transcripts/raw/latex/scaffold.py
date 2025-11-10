# BMF Sage + LaTeX Scaffold (Jupyter, SageMath kernel)
# Author: Christopher R. Amon (ORCID: 0000-0001-9133-7677)
# Use: Run cell-by-cell in Jupyter with the **SageMath** kernel.

#%% [1] Symbols & Operators
var('x y t a_c a_m a_r k Lambda sigma omega')
P = function('P')(x,y,t)

# core operators
gradP = (diff(P,x), diff(P,y))                 # ∇P
lapP  = diff(P,x,2) + diff(P,y,2)              # ∇²P  (curvature)
Mop   = diff(P,t)                               # ∂P/∂t (movement)
Rop   = -k*diff(P,t)                            # −k ∂P/∂t (resistance)

# master equation (LHS = 0)
Master = diff(P,t,2) - (a_c*lapP + a_m*Mop + a_r*Rop + Lambda)

show(Master)
print("LaTeX Master:")
print(latex(Master))

#%% [2] Test Field & Residual (Gaussian pulse)
assume(sigma>0, omega>0)
Ptest = exp(-(x^2 + y^2)/sigma^2) * cos(omega*t)
Res   = Master.subs({P:Ptest}).simplify_full()
show(Res)
print("LaTeX Residual:")
print(latex(Res))

#%% [3] Pretty Printer: dump key objects to a .tex snippet
def dump_tex(fname, items):
    with open(fname, 'w') as f:
        for name,expr in items:
            f.write("% --- %s ---\n"%name)
            f.write(latex(expr)+"\n\n")
    print("Wrote:", fname)

_ = dump_tex('bmf_equations.tex', [
    ("Gradient",  vector(gradP)),
    ("Laplacian", lapP),
    ("Movement",  Mop),
    ("Resistance",Rop),
    ("MasterEq",  Master),
    ("Residual_Ptest", Res)
])

#%% [4] Eye Candy: 2D/3D plots at t=0
subs0 = {a_c:1, a_m:1, a_r:1, k:0.12, Lambda:0, sigma:6, omega:0.5, t:0}
P0    = Ptest.subs(subs0)

# 2D heatmap
hm = density_plot(P0, (x,-30,30), (y,-30,30), cmap='magma', plot_points=200)
show(hm)

# 3D surface
sf = plot3d(P0, (x,-20,20), (y,-20,20), color='purple', opacity=0.85, plot_points=100)
show(sf)

#%% [5] Coherence Σ(x,y,t): 1/(1+|∇P|) at t=0
Px = diff(Ptest,x).subs(subs0)
Py = diff(Ptest,y).subs(subs0)
Sigma0 = 1/(1+sqrt(Px^2 + Py^2))

hmS = density_plot(Sigma0, (x,-30,30), (y,-30,30), cmap='viridis', plot_points=200)
show(hmS)

sfS = plot3d(Sigma0, (x,-20,20), (y,-20,20), color='forestgreen', opacity=0.85, plot_points=100)
show(sfS)

#%% [6] Time Slice Animation (gif) for P(x,y,t)
# Note: Keep domain moderate for speed; generates bmf_pulse.gif
frames = []
T0, T1, N = 0, 60, 30
for i in range(N+1):
    ti = T0 + (T1-T0)*i/N
    Pi = Ptest.subs(subs0).subs({t:ti})
    frames.append(density_plot(Pi, (x,-20,20), (y,-20,20), cmap='magma', plot_points=120))
ani = animate(frames)
ani.save('bmf_pulse.gif', delay=6)
print('Saved: bmf_pulse.gif')

#%% [7] Parameter Sweep (ω vs σ) — small grid of thumbnails
sigmas = [4,6,9]
omegas = [0.3,0.6,1.0]
thumbs = []
for s in sigmas:
    row=[]
    for w in omegas:
        Pi = Ptest.subs({sigma:s, omega:w, t:0})
        row.append(density_plot(Pi, (x,-20,20), (y,-20,20), cmap='magma', plot_points=120))
    thumbs.append(sum(row))
show(sum(thumbs))

#%% [8] Export static images
hm.save('bmf_P_t0.png', dpi=180)
hmS.save('bmf_Sigma_t0.png', dpi=180)
print('Saved: bmf_P_t0.png, bmf_Sigma_t0.png')

#%% [9] Minimal LaTeX doc template to include bmf_equations.tex
texdoc = r"""
\documentclass[11pt]{article}
\usepackage{amsmath, amssymb, amsthm}
\usepackage{geometry}
\usepackage{hyperref}
\geometry{margin=1in}
\title{BMF Operators and Coherence Snapshot}
\author{Christopher R. Amon (ORCID: 0000-0001-9133-7677)}
\begin{document}\maketitle
\section*{Core Objects}
\input{bmf_equations.tex}
\end{document}
"""
with open('bmf_equations_doc.tex','w') as f:
    f.write(texdoc)
print('Wrote: bmf_equations_doc.tex (compile with pdflatex)')
