import numpy as np
import sys

def run_bmf_simulation(timesteps=100, grid_size=100, dt=0.1):
    """
    Simulates the Base Morphogenic Field theory on a 2D grid.
    Returns the time-evolved state of the field.
    """
    # Initialize the substrate
    Psi = np.zeros((grid_size, grid_size))
    # Add an initial disturbance or 'point' in the center
    Psi[grid_size // 2, grid_size // 2] = 1.0

    # Main time evolution loop
    for t in range(timesteps):
        # Calculate operators (simplified for demo)
        # The Line Operator (approximated with a finite difference gradient)
        L = np.gradient(Psi, axis=(0, 1))

        # The Curve Operator (approximated with a finite difference Laplacian)
        C = np.gradient(L[0], axis=0) + np.gradient(L[1], axis=1)

        # The Movement Operator (simplified as a simple decay for this demo)
        M = -0.01 * Psi

        # The Resistance Operator (simplified)
        k = 0.05
        R = -k * M

        # Update the field based on the master equation (simplified for demo)
        # The master equation is d²P/dt² = C(L) + M + R + Λ
        # We approximate d²P/dt² with a simple update rule: dP/dt = C + M + R
        dPsi_dt = C + M + R

        # Update the field state using Euler's method
        Psi += dPsi_dt * dt

    return Psi

if __name__ == "__main__":
    # Check if a filename is provided as a command-line argument
    if len(sys.argv) > 1:
        output_filename = sys.argv[1]
    else:
        output_filename = "bmf_field_state.npy"
    
    print("Starting BMF simulation...")
    final_state = run_bmf_simulation(timesteps=200, grid_size=200)
    
    # Save the final state to a file that Blender can read
    np.save(output_filename, final_state)
    print(f"BMF simulation complete. Field state saved to {output_filename}")
 
