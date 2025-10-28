# FILE: basic-field.py  
# VERSION: 1.0
# DESCRIPTION: Ultra-simple AFT field visualization - no hanging, just works
# AUTHOR: Christopher R. Amon - Amon Research Labs
# CREATED: 2025-09-11

import numpy as np
import matplotlib.pyplot as plt

# Simple field equation
x = np.linspace(-3, 3, 30)
y = np.linspace(-3, 3, 30)
X, Y = np.meshgrid(x, y)

# AFT field: ψ(x,y) = e^(-(x²+y²)/2) * cos(x+y)  
Z = np.exp(-(X**2 + Y**2)/2) * np.cos(X + Y)

# Simple contour plot
plt.figure(figsize=(8, 6))
plt.contourf(X, Y, Z, levels=15, cmap='plasma')
plt.colorbar(label='Field Strength')
plt.title('AFT Morphogenic Field')
plt.xlabel('X')
plt.ylabel('Y')
plt.savefig('aft_field_basic.png', dpi=150)
plt.show()

print("SUCCESS: Basic field visualization created!")
print("File saved: aft_field_basic.png")
print("Visual system working!")