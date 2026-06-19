import sys
import os

# Add both 'src' and 'scripts' to the path
sys.path.append(os.path.abspath("./src"))
sys.path.append(os.path.abspath("./scripts"))

# Import your core logic
from resonator_logic import calculate_bandgap

# Import your scripts to ensure they are valid (syntax check)
import flux_calculator
import hofstadter_generator
import lattice_mapper

def stress_test_scripts():
    print("[*] Performing Smoke Test on scripts...")
    # Add specific function calls here if you want deeper testing
    # Example: flux_calculator.run_basic_check()
    print("[+] Scripts loaded successfully.")
    return True

def stress_test_lattice_noise(noise_level=0.02):
    print(f"[*] Running Defect Sensitivity Test (Noise: {noise_level*100}%)")
    current_gap = calculate_bandgap(perturbation=noise_level)
    
    threshold = 0.4
    if current_gap < threshold:
        print(f"[!] FAILURE: Bandgap too small ({current_gap:.4f})")
        return False
    return True

def run_all_tests():
    print("=== INITIALIZING TECHNOMOUSE STRESS TEST ===")
    
    # 1. Run Smoke Tests for scripts
    if not stress_test_scripts():
        sys.exit(1)
        
    # 2. Run Defect Test
    if not stress_test_lattice_noise():
        sys.exit(1)
        
    print("=== SYSTEM INTEGRITY VERIFIED ===")

if __name__ == "__main__":
    run_all_tests()
    
