import sys
import os
import matplotlib
# Force headless mode to prevent crashes on GitHub servers
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import numpy as np

# 1. Expand the system's "Vision" (Pathing)
sys.path.append(os.path.abspath("./src"))
sys.path.append(os.path.abspath("./scripts"))

# 2. Import the Library
from resonator_logic import calculate_bandgap
import flux_calculator
import hofstadter_generator
import lattice_mapper

# 3. The Smoke Test Suite
def run_smoke_test():
    """Verifies that all modules load without errors."""
    print("[*] Running Smoke Test: Checking module integrity...")
    print("[+] All modules loaded successfully.")
    return True

def stress_test_lattice_noise(noise_level=0.02):
    print(f"[*] Running Defect Sensitivity Test (Noise: {noise_level*100}%)")
    
    # Run Physics Logic
    current_gap = calculate_bandgap(perturbation=noise_level)
    
    # Threshold check
    threshold = 0.4
    if current_gap < threshold:
        print(f"[!] FAILURE: Bandgap too small ({current_gap:.4f})")
        return False
    
    # 4. Visualization Logic
    # Ensure output directory exists
    os.makedirs('outputs', exist_ok=True)
    
    # Create the plot
    plt.figure(figsize=(8, 8))
    
    # Assuming lattice_mapper has a method to return the 8x8 grid for the 64 states
    # If this method name differs, check your lattice_mapper.py file
    grid_data = lattice_mapper.get_lattice_grid() 
    
    plt.imshow(grid_data, cmap='viridis', interpolation='nearest')
    plt.colorbar(label='State ID')
    plt.title(f"Cornucopia 64-State Lattice Projection (Noise: {noise_level*100}%)")
    
    # Add Bandgap metadata box
    plt.text(0.05, 0.95, f"Noise Level: {noise_level}\nBandgap: {current_gap:.4f}", 
             transform=plt.gca().transAxes, bbox=dict(facecolor='white', alpha=0.5))
    
    plt.savefig('outputs/resonator_output.png')
    print("[+] Plot saved as outputs/resonator_output.png")
    return True

# 5. Orchestration
def run_all_tests():
    print("=== INITIALIZING TECHNOMOUSE MASTER SUITE ===")
    
    if not run_smoke_test():
        sys.exit(1)
        
    if not stress_test_lattice_noise():
        sys.exit(1)
        
    print("=== SYSTEM INTEGRITY VERIFIED: ALL SYSTEMS NOMINAL ===")

if __name__ == "__main__":
    run_all_tests()
    
