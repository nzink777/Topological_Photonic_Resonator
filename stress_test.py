import sys
import os

# Adds the 'src' folder to the path so Python can find your code
sys.path.append(os.path.abspath("./src")) 

# Now import your logic (Ensure 'resonator_logic' is the name of your file in src/)
from resonator_logic import calculate_bandgap

# Define your threshold for failure
THRESHOLD = 0.5 

def stress_test_lattice_noise(noise_level=0.02):
    print(f"[*] Running Defect Sensitivity Test (Noise: {noise_level*100}%)")
    
    # Call your REAL function here
    current_gap = calculate_bandgap(perturbation=noise_level)
    
    if current_gap < THRESHOLD:
        print(f"[!] FAILURE: Bandgap too small ({current_gap})")
        return False
    return True

if __name__ == "__main__":
    if not stress_test_lattice_noise():
        sys.exit(1) # This forces GitHub Actions to report a 'Fail'
    print("=== TEST PASSED ===")
  
