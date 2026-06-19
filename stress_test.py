import sys
import os

# Ensure Python can see the 'src' folder
sys.path.append(os.path.abspath("./src"))

# Now we import the function we just defined
from resonator_logic import calculate_bandgap

def stress_test_lattice_noise(noise_level=0.02):
    print(f"[*] Running Defect Sensitivity Test (Noise: {noise_level*100}%)")
    
    # Call the logic defined in resonator_logic.py
    current_gap = calculate_bandgap(perturbation=noise_level)
    
    # Assuming a threshold for pass/fail
    threshold = 0.4
    if current_gap < threshold:
        print(f"[!] FAILURE: Bandgap too small ({current_gap:.4f})")
        return False
    return True

def run_all_tests():
    print("=== INITIALIZING TECHNOMOUSE STRESS TEST ===")
    if not stress_test_lattice_noise():
        sys.exit(1)
    print("=== SYSTEM INTEGRITY VERIFIED ===")

if __name__ == "__main__":
    run_all_tests()
    
