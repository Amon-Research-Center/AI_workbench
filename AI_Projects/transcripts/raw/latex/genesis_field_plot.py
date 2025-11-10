
import numpy as np
import matplotlib.pyplot as plt

# Generate the linear path (pure motion)
x_line = np.linspace(0, 5, 500)
y_line = 0.5 * x_line  # Line with slope = motion

# Generate the spiral (curved response with resistance and energy input)
theta = np.linspace(0, 6 * np.pi, 1000)
r_spiral = 0.1 + 0.05 * theta
x_spiral = r_spiral * np.cos(theta)
y_spiral = r_spiral * np.sin(theta)

# Create the plot
plt.figure(figsize=(10, 8))
plt.plot(x_line, y_line, label='Linear Motion (Power)', color='red', linewidth=2)
plt.plot(x_spiral, y_spiral, label='Curved Spiral (Resistance + Energy)', color='blue', linewidth=2)

# Highlight the convergence region
plt.scatter([0], [0], color='gold', s=100, label='Point of Convergence (Genesis)', zorder=5)

# Decorations
plt.title('Convergence of Line and Curve — The Genesis Point')
plt.xlabel('Motion →')
plt.ylabel('Resistance ↑')
plt.legend()
plt.grid(True)
plt.axis('equal')
plt.tight_layout()
plt.show()
