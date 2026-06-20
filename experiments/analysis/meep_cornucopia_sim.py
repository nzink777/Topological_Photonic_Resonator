"""
meep_cornucopia_sim.py
Project: Topological Photonic Resonator (Project Cornucopia)
Description: 
FDTD Simulation of the 64-sector geometric diode using the Meep library.
Updated with robust directory handling and logging for CI/CD pipelines.

Dependencies: meep, numpy, pandas
"""

import meep as mp
import numpy as np
import pandas as pd
import math
import os
import logging
import sys

# --- Setup Logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Simulation Parameters ---
RESOLUTION = 50           # Pixels per micron
CELL_SIZE = 10.0          # 10x10 micron simulation cell
PML_THICKNESS = 1.0       
N_SECTORS = 64            # The 2^6 tensor permutations

# --- Material Projection ---
BASE_INDEX = 1.5          
GEOMETRIC_DELTA = 0.05    

def lattice_dielectric(p):
    """
    Returns the dielectric constant at a given point (p).
    Divides a central ring into 64 alternating sectors.
    """
    r = math.sqrt(p.x**2 + p.y**2)
    if 2.0 <= r <= 4.0:
        angle = math.atan2(p.y, p.x)
        if angle < 0:
            angle += 2 * math.pi
        
        sector_angle = (2 * math.pi) / N_SECTORS
        sector_id = int(angle / sector_angle)
        
        if sector_id % 2 == 0:
            return mp.Medium(index=BASE_INDEX + GEOMETRIC_DELTA)
        else:
            return mp.Medium(index=BASE_INDEX - GEOMETRIC_DELTA)
    
    return mp.Medium(index=1.0)

def run_simulation():
    logger.info("Initializing FDTD M^4 Brane Projection...")
    
    # 1. Geometry Setup
    cell = mp.Vector3(CELL_SIZE, CELL_SIZE, 0)
    geometry = [mp.Block(size=mp.Vector3(mp.inf, mp.inf, mp.inf), material=lattice_dielectric)]
    pml_layers = [mp.PML(PML_THICKNESS)]
    
    # 2. Source Configuration
    fcen = 0.15
    df = 0.1
    sources = [mp.Source(src=mp.GaussianSource(fcen, fwidth=df),
                         component=mp.Ez,
                         center=mp.Vector3(3.0, 0, 0))]
    
    # 3. Initialize Meep
    sim = mp.Simulation(cell_size=cell,
                        boundary_layers=pml_layers,
                        geometry=geometry,
                        sources=sources,
                        resolution=RESOLUTION)
    
    # 4. Define Data Extraction Points
    probe_radius = 3.0
    probes = [mp.Vector3(probe_radius * math.cos(i * (2 * math.pi) / N_SECTORS), 
                         probe_radius * math.sin(i * (2 * math.pi) / N_SECTORS), 0) 
              for i in range(N_SECTORS)]
    
    # 5. Run Simulation
    logger.info(f"Running simulation for {N_SECTORS} state-spaces...")
    
    sim_data = []
    
    def record_fields(sim):
        current_time = sim.meep_time()
        for idx, p in enumerate(probes):
            ez = sim.get_field_point(mp.Ez, p).real
            hx = sim.get_field_point(mp.Hx, p).real
            hy = sim.get_field_point(mp.Hy, p).real
            h_mag = math.sqrt(hx**2 + hy**2)
            
            sim_data.append({
                'time_meep': current_time,
                'sector_id': idx + 1,
                'Ez_field': ez,
                'H_mag': h_mag
            })

    sim.run(mp.at_every(0.5, record_fields), until=50)
    return pd.DataFrame(sim_data)

def generate_empirical_csv(df, output_path):
    """
    Translates photonic FDTD data to fluid-dynamic proxies and saves to CSV.
    Includes robust directory creation.
    """
    logger.info("Translating photonic FDTD data to fluid-dynamic proxies...")
    
    # --- ADDED: Ensure output directory exists ---
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        logger.info(f"Creating missing directory: {output_dir}")
        try:
            os.makedirs(output_dir, exist_ok=True)
        except OSError as e:
            logger.error(f"Failed to create directory {output_dir}: {e}")
            sys.exit(1)
    
    # Data transformation
    df['time_ms'] = df['time_meep'] * 10.0 
    df['acoustic_pressure_pa'] = df['Ez_field'] * 1500.0 
    df['fluid_velocity_ms'] = df['H_mag'] * 5.0
    
    export_df = df[['time_ms', 'sector_id', 'acoustic_pressure_pa', 'fluid_velocity_ms']]
    
    try:
        export_df.to_csv(output_path, index=False)
        logger.info(f"Simulation data successfully exported to {output_path}")
    except Exception as e:
        logger.error(f"Failed to save CSV file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # --- Execute Pipeline ---
    try:
        raw_data_df = run_simulation()
        OUTPUT_FILE = "../data/resonator_raw_logs/sample_data.csv"
        generate_empirical_csv(raw_data_df, OUTPUT_FILE)
        logger.info("Pipeline complete. Ready for processing via delta_E_calc.py.")
    except Exception as e:
        logger.critical(f"Critical simulation failure: {e}")
        sys.exit(1)
        
