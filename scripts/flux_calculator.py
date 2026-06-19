import numpy as np

def calculate_net_flux(source_flux_data, drain_flux_data):
    """
    Calculates the net Poynting vector flux (Phi) as defined in the 
    Topological Photonic Resonator protocol.
    
    Formula: Phi = Integral(S_drain) - Integral(S_source)
    Success Metric: Phi > 0 indicates net energy gain.
    """
    # Assuming input data are arrays representing integrated flux at specific time steps or frequencies
    source_integral = np.sum(source_flux_data)
    drain_integral = np.sum(drain_flux_data)
    
    net_flux = drain_integral - source_integral
    
    return net_flux

def validate_cornucopia_effect(net_flux):
    """
    Checks if the device meets the success metric for passive topological rectification.
    """
    if net_flux > 0:
        print(f"Success! Net Flux Detected: {net_flux:.4e}. The device is acting as a topological pump.")
        return True
    else:
        print(f"Net Flux: {net_flux:.4e}. No net energy gain detected.")
        return False

# Example Usage with dummy simulation data
if __name__ == "__main__":
    # Simulated Poynting flux values (e.g., from an FDTD monitor export)
    # Replace these with actual simulation data arrays
    source_S = np.random.normal(loc=1.0, scale=0.1, size=100) 
    drain_S = np.random.normal(loc=1.05, scale=0.1, size=100) 
    
    phi = calculate_net_flux(source_S, drain_S)
    validate_cornucopia_effect(phi)
  
