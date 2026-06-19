import sys
import os
import matplotlib
# Force headless mode to prevent crashes on GitHub servers
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

# 1. Expand the system's "Vision" (Pathing)
# We add both 'src' and 'scripts' so the Genie can see all your modules
sys.path.append(os.path.abspath("./src"))
sys.path.append(os.path.abspath("./scripts"))

# 2. Import the Library
# If any of these fail to import, the Sentinel will stop immediately.
from resonator_logic import calculate_bandgap
import flux_calculator
import hofstadter_generator
import lattice_mapper

# 3. The Smoke Test Suite
def run_smoke_test():
    """Verifies that all modules load without errors."""
    print("[*] Running Smoke Test: Checking module integrity...")
    # Add simple sanity checks here if you have specific run functions
    print("[+] All modules loaded successfully.")
    return True

def stress_test_lattice_noise(noise_level=0.02):
    print(f"[*] Running Defect Sensitivity Test (Noise: {noise_level*100}%)")
    current_gap = calculate_bandgap(perturbation=noise_level)
    
    threshold = 0.4
    if current_gap < threshold:
        print(f"[!] FAILURE: Bandgap too small ({current_gap:.4f})")
        return False
    return True

# 4. Orchestration
def run_all_tests():
    print("=== INITIALIZING TECHNOMOUSE MASTER SUITE ===")
    
    # Check 1: Loading
    if not run_smoke_test():
        sys.exit(1)
        
    # Check 2: Physics Integrity
    if not stress_test_lattice_noise():
        sys.exit(1)
        
    print("=== SYSTEM INTEGRITY VERIFIED: ALL SYSTEMS NOMINAL ===")

if __name__ == "__main__":
    run_all_tests()
  
