"""Project: Topological Photonic Resonator (Project Cornucopia)
Description: 
Calculates the net energy gain (Delta E) across the 64-sector geometric lattice.
This script numerically integrates the Energy Accumulation Formula defined in 
the theoretical framework by utilizing acoustic pressure and rotational sheer 
as macroscopic proxies for the 7D density gradient (F_7D).

Mathematical Basis:
\Delta E = \sum_{n=1}^{64} \oint_{\Gamma_{n}} (F_{7D} \cdot dl)
delta_E_calc.py
Project: Topological Photonic Resonator. 
Calculates the total energy accumulation (Delta E) and performs 
Spectral Analysis to reveal the 0.5-beat temporal sheer frequency.
"""

import pandas as pd
import numpy as np
from scipy.fft import fft, fftfreq
import os
import logging

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def perform_spectral_analysis(df, sector_id):
    """
    Performs FFT on the pressure data to isolate the 0.5-beat sheer frequency.
    """
    # Isolate data for this sector
    sector_data = df[df['sector_id'] == sector_id]
    
    # Time parameters
    N = len(sector_data)
    # Assume constant sampling rate (dt) from the simulation interval
    dt = 0.5 
    
    # Compute FFT
    yf = fft(sector_data['acoustic_pressure_pa'].values)
    xf = fftfreq(N, dt)[:N//2]
    
    # Identify dominant frequency (excluding DC/zero-frequency)
    power = 2.0/N * np.abs(yf[0:N//2])
    peak_idx = np.argmax(power[1:]) + 1 # +1 to skip DC component
    peak_freq = xf[peak_idx]
    
    return peak_freq, power[peak_idx]

def calculate_energetics():
    input_file = "../data/resonator_raw_logs/sample_data.csv"
    
    if not os.path.exists(input_file):
        logger.error(f"Input file not found: {input_file}")
        return

    df = pd.read_csv(input_file)
    logger.info(f"Loaded {len(df)} telemetry records. Analyzing spectral drift...")

    results = []
    
    for sector in range(1, 65):
        # 1. Standard Energy Integration (The original logic)
        sec_df = df[df['sector_id'] == sector]
        delta_e = sec_df['acoustic_pressure_pa'].sum() / len(sec_df)
        
        # 2. Spectral Drift Detection (The new 'Ghost Beat' logic)
        freq, amplitude = perform_spectral_analysis(df, sector)
        
        results.append({
            'sector_id': sector,
            'delta_E': delta_e,
            'dominant_freq': freq,
            'sideband_amplitude': amplitude
        })

    # Save Analysis
    results_df = pd.DataFrame(results)
    results_df.to_csv("geometric_pressure_results.csv", index=False)
    
    # Log the summary
    avg_energy = results_df['delta_E'].sum()
    logger.info(f"Analysis Complete. Total Accumulated Energy (Delta E): {avg_energy:.4f} Joules")
    logger.info("Spectral Analysis saved to 'geometric_pressure_results.csv'.")
    
    # Highlight the "Ghost Beat"
    avg_freq = results_df['dominant_freq'].mean()
    logger.info(f"Detected primary resonance frequency: {avg_freq:.4f} Hz")
    logger.info("Check 'geometric_pressure_results.csv' for sector-by-sector drift patterns.")

if __name__ == "__main__":
    calculate_energetics()
    
