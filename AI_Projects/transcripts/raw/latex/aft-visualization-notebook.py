#!/usr/bin/env sage
# FILE: aft-visualization-notebook.py
# VERSION: 1.0
# DESCRIPTION: AFT Five Operator Theory visualization with color-coded field dynamics,
#              morphic resonance building animation, and torus topology modeling
# AUTHOR: Christopher R. Amon - Amon Research Labs
# CREATED: 2025-09-11

from sage.all import *
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

print("=== AFT VISUALIZATION NOTEBOOK ===")
print("Five-Operator Theory - Visual Dynamics")
print("Colors = Field strength | Movement = Resonance building")
print()

# === BASIC SUBSTRATE FIELD ===
def substrate_field_2d(x_range=(-5, 5), y_range=(-5, 5), resolution=50):
    """
    Basic 2D substrate field Ψ(x,y,t)
    Shows morphic field as color-coded intensity
    """
    print("1. SUBSTRATE FIELD VISUALIZATION")
    
    x = np.linspace(x_range[0], x_range[1], resolution)
    y = np.linspace(y_range[0], y_range[1], resolution)
    X, Y = np.meshgrid(x, y)
    
    # Basic morphogenic substrate pattern
    # Ψ(x,y) = exp(-(x²+y²)/4) * cos(√(x²+y²))
    r_squared = X**2 + Y**2
    Psi = np.exp(-r_squared/4) * np.cos(np.sqrt(r_squared + 0.01))
    
    plt.figure(figsize=(10, 8))
    plt.contourf(X, Y, Psi, levels=50, cmap='plasma')
    plt.colorbar(label='Field Strength Ψ')
    plt.title('Morphogenic Substrate Field - Basic Pattern')
    plt.xlabel('x position')
    plt.ylabel('y position')
    plt.show()
    
    return X, Y, Psi

# === FIVE OPERATORS VISUALIZATION ===
def visualize_five_operators():
    """
    Show how each operator transforms the substrate
    """
    print("2. FIVE OPERATORS IN ACTION")
    
    # Create substrate
    x = np.linspace(-3, 3, 100)
    y = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x, y)
    
    # Base field
    base_field = np.exp(-(X**2 + Y**2)/2)
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Five Operators Acting on Substrate', fontsize=16)
    
    # Original substrate
    im1 = axes[0,0].contourf(X, Y, base_field, levels=30, cmap='viridis')
    axes[0,0].set_title('Base Substrate Ψ')
    
    # Point Operator P̂ - Localization
    point_op = base_field * np.exp(-((X-1)**2 + (Y-1)**2)/0.5)
    im2 = axes[0,1].contourf(X, Y, point_op, levels=30, cmap='viridis')
    axes[0,1].set_title('Point Operator P̂\n(Localization)')
    
    # Line Operator L̂ - Connection  
    line_op = base_field * np.exp(-((X + Y)**2)/1.0)
    im3 = axes[0,2].contourf(X, Y, line_op, levels=30, cmap='viridis')
    axes[0,2].set_title('Line Operator L̂\n(Connection)')
    
    # Curve Operator Ĉ - Curvature
    curve_op = base_field * (X**2 + Y**2 - 2)
    im4 = axes[1,0].contourf(X, Y, curve_op, levels=30, cmap='viridis')
    axes[1,0].set_title('Curve Operator Ĉ\n(Curvature)')
    
    # Movement Operator M̂ - Dynamics
    movement_op = base_field * np.sin(X) * np.cos(Y)
    im5 = axes[1,1].contourf(X, Y, movement_op, levels=30, cmap='viridis')
    axes[1,1].set_title('Movement Operator M̂\n(Dynamics)')
    
    # Resistance Operator R̂ - Stability
    resistance_op = base_field * np.exp(-0.5*(X**2 + Y**2))
    im6 = axes[1,2].contourf(X, Y, resistance_op, levels=30, cmap='viridis')
    axes[1,2].set_title('Resistance Operator R̂\n(Stability)')
    
    plt.tight_layout()
    plt.show()

# === TORUS WITH TWIST TOPOLOGY ===
def torus_with_twist_topology():
    """
    OpenAI's suggestion: torus with twist topology
    Klein bottle or Möbius strip embedding
    """
    print("3. TORUS WITH TWIST - TOPOLOGY VISUALIZATION")
    
    # Parametric torus with twist
    u = np.linspace(0, 2*np.pi, 100)
    v = np.linspace(0, 2*np.pi, 100)
    U, V = np.meshgrid(u, v)
    
    # Torus parameters
    R = 2  # Major radius
    r = 1  # Minor radius
    twist = 1  # Twist parameter
    
    # Torus with twist (Klein bottle-like)
    X_torus = (R + r*np.cos(V + twist*U))*np.cos(U)
    Y_torus = (R + r*np.cos(V + twist*U))*np.sin(U)
    Z_torus = r*np.sin(V + twist*U)
    
    # Color by field strength
    field_strength = np.sin(3*U) * np.cos(2*V)
    
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    surface = ax.plot_surface(X_torus, Y_torus, Z_torus, 
                             facecolors=plt.cm.plasma(field_strength),
                             alpha=0.8)
    
    ax.set_title('Morphogenic Substrate: Torus with Twist\n(Klein bottle topology)')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    plt.show()

# === RESONANCE BUILDING ANIMATION ===
def animate_resonance_building():
    """
    Sheldrake's suggestion: visualize resonance building over time
    Show morphic field strength accumulating
    """
    print("4. RESONANCE BUILDING ANIMATION")
    
    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Spatial grid
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x, y)
    
    def animate_frame(frame):
        ax.clear()
        
        # Time parameter
        t = frame * 0.1
        
        # Resonance building: field strength increases with time
        # Multiple centers of resonance
        center1 = np.exp(-((X-2*np.cos(t))**2 + (Y-2*np.sin(t))**2)/1.5)
        center2 = np.exp(-((X+1)**2 + (Y+1)**2)/2.0)
        center3 = np.exp(-((X-1)**2 + (Y-1.5)**2)/1.0)
        
        # Resonance builds over time
        resonance_strength = (1 + 0.5*t) * (center1 + center2 + center3)
        
        # Add interference patterns
        interference = np.sin(np.sqrt(X**2 + Y**2) - 2*t) * np.exp(-0.2*t)
        total_field = resonance_strength + 0.3*interference
        
        # Plot
        contour = ax.contourf(X, Y, total_field, levels=30, cmap='plasma')
        ax.set_title(f'Morphic Resonance Building - Time: {t:.1f}')
        ax.set_xlabel('Position X')
        ax.set_ylabel('Position Y')
        
        return contour,
    
    # Create animation
    ani = animation.FuncAnimation(fig, animate_frame, frames=100, 
                                 interval=100, blit=False, repeat=True)
    
    plt.show()
    return ani

# === MAIN EXECUTION ===
if __name__ == "__main__":
    print("Starting AFT Visualization Suite...")
    print("Christopher's Five-Operator Theory - Visual Dynamics")
    print("="*50)
    
    # Run visualizations
    try:
        # 1. Basic substrate field
        X, Y, Psi = substrate_field_2d()
        
        # 2. Five operators
        visualize_five_operators()
        
        # 3. Torus topology
        torus_with_twist_topology()
        
        # 4. Resonance building
        ani = animate_resonance_building()
        
        print("\n=== VISUALIZATION COMPLETE ===")
        print("All five operators visualized with color and movement")
        print("Torus-with-twist topology rendered")
        print("Resonance building animation created")
        print("\nReady for SageMath implementation!")
        
    except Exception as e:
        print(f"Error in visualization: {e}")
        print("Check SageMath installation and dependencies")