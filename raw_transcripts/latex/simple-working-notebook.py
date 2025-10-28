# FILE: simple-working-notebook.py
# VERSION: 1.0
# DESCRIPTION: Simple working visualization - basic equation to 3D plot that just WORKS
# AUTHOR: Christopher R. Amon - Amon Research Labs
# CREATED: 2025-09-11

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

print("=== SIMPLE WORKING VISUALIZATION ===")
print("Basic AFT equation → 3D plot → ready for Blender")
print()

# Simple field equation that works
def simple_field(x, y, t=0):
    """
    Simple AFT field: combines all operators in basic form
    ψ(x,y) = e^(-(x²+y²)/4) * cos(√(x²+y²))
    """
    r_squared = x**2 + y**2
    return np.exp(-r_squared/4) * np.cos(np.sqrt(r_squared + 0.01))

# Create grid
x = np.linspace(-5, 5, 50)
y = np.linspace(-5, 5, 50)
X, Y = np.meshgrid(x, y)

# Calculate field
Z = simple_field(X, Y)

# Create 3D plot
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')

# Surface plot
surface = ax.plot_surface(X, Y, Z, cmap='plasma', alpha=0.8)

# Make it look good
ax.set_xlabel('X Position')
ax.set_ylabel('Y Position') 
ax.set_zlabel('Field Strength')
ax.set_title('AFT Morphogenic Field - 3D Visualization')

# Add colorbar
plt.colorbar(surface, shrink=0.5, aspect=5)

plt.show()

print("SUCCESS: Basic 3D field visualization working!")
print()

# Save data for Blender import
print("Saving data for Blender...")
np.savetxt('field_data_x.csv', X, delimiter=',')
np.savetxt('field_data_y.csv', Y, delimiter=',')  
np.savetxt('field_data_z.csv', Z, delimiter=',')
print("Files saved: field_data_x.csv, field_data_y.csv, field_data_z.csv")
print()

# Create simple animation frames
print("Creating animation frames...")
for frame in range(5):
    t = frame * 0.5
    Z_anim = simple_field(X, Y, t) * np.cos(t)
    
    fig2 = plt.figure(figsize=(10, 8))
    plt.contourf(X, Y, Z_anim, levels=20, cmap='plasma')
    plt.colorbar()
    plt.title(f'AFT Field Evolution - Frame {frame}')
    plt.savefig(f'aft_frame_{frame:02d}.png', dpi=150)
    plt.close()

print("Animation frames saved: aft_frame_00.png to aft_frame_04.png")
print()

print("=== SYSTEM IS WORKING ===")
print("✅ Equation implemented")
print("✅ 3D visualization created") 
print("✅ Data exported for Blender")
print("✅ Animation frames generated")
print()
print("Next: Import field_data_*.csv into Blender as mesh")
print("Visual system is UP and SMOOTH!")