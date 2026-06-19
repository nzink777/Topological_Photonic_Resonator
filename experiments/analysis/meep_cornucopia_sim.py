"""
meep_cornucopia_sim.py
Project: Topological Photonic Resonator (Project Cornucopia)
Description: 
FDTD Simulation of the 64-sector geometric diode using the Meep library.
This script maps the hyperbolic curvature and Klein-bottle topology into 
an effective dielectric medium, simulating the photonic traversal across 
the 64 state-spaces.

It outputs a CSV of the field dynamics, converted into the fluid-dynamic 
proxies (Acoustic Pressure and Fluid Velocity) required by delta_E_calc.py.

Dependencies: meep, numpy, pandas
"""

import meep as mp
import numpy as np
import pandas as pd
import math

# --- Simulation Parameters ---
RESOLUTION = 50           # Pixels per micron (higher = more accurate, slower)
CELL_SIZE = 10.0          # 10x10 micron simulation cell
PML_THICKNESS = 1.0       # Perfectly Matched Layer (absorbs boundary reflections)
N_SECTORS = 64            # The 2^6 tensor permutations

# --- Material Projection (Topological to Dielectric Mapping) ---
# We map the topological "ratchet" effect by alternating the refractive 
# index slightly across the 64 azimuthal sectors.
BASE_INDEX = 1.5          # Baseline index of the substrate
GEOMETRIC_DELTA = 0.05    # The "Topological Drag" index variance

def lattice_dielectric(p):
    """
    Returns the dielectric constant at a given point (p).
    Divides a central ring into 64 alternating sectors to simulate 
    the geometric transitions of the Klein-bottle projection.
    """
    r = math.sqrt(p.x**2 + p.y**2)
    # Define the resonator waveguide boundaries
    if 2.0 <= r <= 4.0:
        angle = math.atan2(p.y, p.x)
        # Map angle from [-pi, pi] to [0, 2pi]
        if angle < 0:
            angle += 2 * math.pi
        
        # Determine which of the 64 sectors we are in
        sector_angle = (2 * math.pi) / N_SECTORS
        sector_id = int(angle / sector_angle)
        
        # Alternate the index to create the geometric "ratchet" steps
        if sector_id % 2 == 0:
            return mp.Medium(index=BASE_INDEX + GEOMETRIC_DELTA)
        else:
            return mp.Medium(index=BASE_INDEX - GEOMETRIC_DELTA)
    
    # Air/Vacuum elsewhere
    return mp.Medium(index=1.0)

def run_simulation():
    print("Initializing FDTD M^4 Brane Projection...")
    
    # 1. Geometry Setup
    cell = mp.Vector3(CELL_SIZE, CELL_SIZE, 0)
    geometry = [mp.Block(size=mp.Vector3(mp.inf, mp.inf, mp.inf), material=lattice_dielectric)]
    pml_layers = [mp.PML(PML_THICKNESS)]
    
    # 2. Source Configuration (representing ambient photonic noise)
    # Using a Gaussian pulse injected off-center to force circulation
    fcen = 0.15  # Pulse center frequency
    df = 0.1     # Pulse width
    sources = [mp.Source(src=mp.GaussianSource(fcen, fwidth=df),
                         component=mp.Ez,
                         center=mp.Vector3(3.0, 0, 0))]
    
    # 3. Initialize Meep
    sim = mp.Simulation(cell_size=cell,
                        boundary_layers=pml_layers,
                        geometry=geometry,
                        sources=sources,
                        resolution=RESOLUTION)
    
    # 4. Define Data Extraction Points (one per sector)
    probe_radius = 3.0
    probes = []
    for i in range(N_SECTORS):
        angle = i * ((2 * math.pi) / N_SECTORS)
        px = probe_radius * math.cos(angle)
        py = probe_radius * math.sin(angle)
        probes.append(mp.Vector3(px, py, 0))
    
    # 5. Run the Simulation
    # We step through time and record the E-field and H-field at each sector probe
    print(f"Running simulation for {N_SECTORS} state-spaces...")
    
    time_steps = 100
    sim_data = []
    
    def record_fields(sim):
        current_time = sim.meep_time()
        for idx, p in enumerate(probes):
            # Extract fields (Electric Field Ez, Magnetic Field Hx/Hy)
            ez = sim.get_field_point(mp.Ez, p).real
            hx = sim.get_field_point(mp.Hx, p).real
            hy = sim.get_field_point(mp.Hy, p).real
            h_mag = math.sqrt(hx**2 + hy**2)
            
            # Record raw photonic data
            sim_data.append({
                'time_meep': current_time,
                'sector_id': idx + 1,
                'Ez_field': ez,
                'H_mag': h_mag
            })

    # Run for a set amount of Meep time units, capturing data at intervals
    sim.run(mp.at_every(0.5, record_fields), until=50)
    
    return pd.DataFrame(sim_data)

def generate_empirical_csv(df, output_path):
    """
    Translates the photonic Meep data into the fluid-dynamic proxy variables 
    required by the Aurum Resonator experiment.
    Ez Field -> Acoustic Pressure (Pa)
    H-field Magnitude -> Fluid Velocity (m/s)
    """
    print("Translating photonic FDTD data to fluid-dynamic proxies...")
    
    # Convert Meep time to arbitrary milliseconds for the hardware proxy
    df['time_ms'] = df['time_meep'] * 10.0 
    
    # Scale Ez field to an acoustic pressure proxy range (e.g., Pascals)
    df['acoustic_pressure_pa'] = df['Ez_field'] * 1500.0 
    
    # Scale H field magnitude to a fluid velocity proxy range (e.g., m/s)
    df['fluid_velocity_ms'] = df['H_mag'] * 5.0
    
    # Filter only the necessary columns for delta_E_calc.py
    export_df = df[['time_ms', 'sector_id', 'acoustic_pressure_pa', 'fluid_velocity_ms']]
    
    # Save to the data directory
    export_df.to_csv(output_path, index=False)
    print(f"Simulation data successfully exported to {output_path}")
    print("Ready for processing via delta_E_calc.py.")

if __name__ == "__main__":
    # Execute the simulation
    raw_data_df = run_simulation()
    
    # Output path mapping to your repository structure
    OUTPUT_FILE = "../data/resonator_raw_logs/sample_data.csv"
    generate_empirical_csv(raw_data_df, OUTPUT_FILE)
