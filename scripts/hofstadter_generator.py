import numpy as np
import matplotlib.pyplot as plt

def generate_hofstadter(q_range=64):
    """
    Generates the Hofstadter Butterfly spectrum for a 64-state lattice.
    """
    energies = []
    fluxes = []
    
    for q in range(1, q_range + 1):
        for p in range(q):
            # Hofstadter model Hamiltonian
            # Using the tight-binding approximation for a magnetic lattice
            diag = 2 * np.cos(2 * np.pi * p / q * np.arange(q))
            off_diag = np.ones(q - 1)
            mat = np.diag(diag) + np.diag(off_diag, k=1) + np.diag(off_diag, k=-1)
            mat[0, q-1] = 1
            mat[q-1, 0] = 1
            
            e = np.linalg.eigvalsh(mat)
            energies.extend(e)
            fluxes.extend([p/q] * len(e))
            
    return fluxes, energies

fluxes, energies = generate_hofstadter()

plt.figure(figsize=(10, 6))
plt.scatter(fluxes, energies, s=0.1, color='blue')
plt.title("Cornucopia Lattice: Hofstadter Energy Spectrum (N=64)")
plt.xlabel("Magnetic Flux ($\phi / \phi_0$)")
plt.ylabel("Energy (E/t)")
plt.show()
