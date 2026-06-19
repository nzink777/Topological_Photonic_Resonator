import numpy as np
import matplotlib
matplotlib.use('Agg') # This tells matplotlib to save files instead of trying to open a window
import matplotlib.pyplot as plt

def plot_64_lattice():
    """
    Visualizes the 64-sector lattice discretization for the waveguide.
    """
    # 8x8 grid represents the 64 states (2^6)
    grid = np.arange(64).reshape(8, 8)
    
    plt.figure(figsize=(6, 6))
    plt.imshow(grid, cmap='viridis', origin='upper')
    plt.colorbar(label='State ID')
    plt.title("Cornucopia 64-State Lattice Projection")
    plt.grid(True, color='white', linestyle='-', linewidth=2)
    plt.xticks([])
    plt.yticks([])
    plt.show()

plot_64_lattice()
