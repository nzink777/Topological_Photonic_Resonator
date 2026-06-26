import sys
import os
import matplotlib
matplotlib.use('Agg') # Essential for CI/CD headless execution
import matplotlib.pyplot as plt

# 1. Expand the system's "Vision"
sys.path.append(os.path.abspath("./src"))
sys.path.append(os.path.abspath("./scripts"))

# 2. Import the Library
from resonator_logic import calculate_bandgap
import flux_calculator
import hofstadter_generator
import lattice_mapper
def stress_test_lattice_noise(noise_level=0.02):
    print(f"[*] Running Defect Sensitivity Test (Noise: {noise_level*100}%)")
    
    # 1. Perform calculation
    current_gap = calculate_bandgap(perturbation=noise_level)
    
    # 2. Add Visualization (The "Painting" step)
    # Assuming lattice_mapper provides a way to get the grid data
    lattice_data = lattice_mapper.get_current_grid() 
    plt.figure(figsize=(8, 6))
    plt.imshow(lattice_data, cmap='viridis', interpolation='nearest')
    plt.colorbar(label='State ID')
    plt.title(f"Lattice Projection (Noise: {noise_level*100}%)")
    
    # 3. Add the validation text you currently have
    threshold = 0.4
    if current_gap < threshold:
        print(f"[!] FAILURE: Bandgap too small ({current_gap:.4f})")
        return False
    
    # Add status to the plot
    plt.text(0.05, 0.95, f"Noise: {noise_level}\nBandgap: {current_gap:.4f}", 
             transform=plt.gca().transAxes, bbox=dict(facecolor='white', alpha=0.5))
             
    return True


# 3. Visualization Helper
def generate_visual_report(noise_level, bandgap_result):
    """Generates and saves a labeled visualization in the outputs folder."""
    os.makedirs('outputs', exist_ok=True)
    
    plt.figure(figsize=(8, 6))
    plt.title(f"Lattice Projection (Noise: {noise_level*100}%)")
    
    # Burn the test parameters directly onto the image
    plt.text(0.05, 0.95, f"Noise Level: {noise_level}\nBandgap: {bandgap_result:.4f}", 
             transform=plt.gca().transAxes, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))
    
    output_path = 'outputs/resonator_output.png'
    plt.savefig(output_path)
    print(f"[+] Report saved to {output_path}")

# 4. The Smoke Test Suite
def run_smoke_test():
    """Verifies that all modules load without errors."""
    print("[*] Running Smoke Test: Checking module integrity...")
    print("[+] All modules loaded successfully.")
    return True

def stress_test_lattice_noise(noise_level=0.02):
    print(f"[*] Running Defect Sensitivity Test (Noise: {noise_level*100}%)")
    current_gap = calculate_bandgap(perturbation=noise_level)
    
    # Save the visual report
    generate_visual_report(noise_level, current_gap)
    
    threshold = 0.4
    if current_gap < threshold:
        print(f"[!] FAILURE: Bandgap too small ({current_gap:.4f})")
        return False
    return True

# 5. Orchestration
def run_all_tests():
    print("=== INITIALIZING MASTER SUITE ===")
    
    # Check 1: Loading
    if not run_smoke_test():
        sys.exit(1)
        
    # Check 2: Physics Integrity
    if not stress_test_lattice_noise():
        sys.exit(1)
        
    print("=== SYSTEM INTEGRITY VERIFIED: ALL SYSTEMS NOMINAL ===")

if __name__ == "__main__":
    run_all_tests()
    
