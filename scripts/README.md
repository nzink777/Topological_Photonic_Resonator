This directory contains the computational toolset developed for the validation and analysis of the Topological Photonic Resonator. These scripts are designed to bridge the gap between the theoretical framework and numerical verification.  
Script Catalog
hofstadter_generator.py: This script generates the Hofstadter Butterfly spectrum for the 64-state lattice configuration. It provides the numerical validation that your lattice structure exhibits the necessary quantized energy gaps for the geometric ratchet effect.  
lattice_mapper.py: This utility visualizes the 64-sector waveguide discretization. It allows researchers to inspect the structural layout of the 2^6 I-Ching tensor matrix mapping used in the device design.  
flux_calculator.py: This is the primary verification tool for the experimental protocol. It processes FDTD simulation data to calculate the net Poynting vector flux (\Phi), serving as the automated success metric to determine if the device is operating as a passive topological pump.  
Usage & Requirements
These scripts are built using standard numerical and visualization libraries.
Dependencies:
numpy
matplotlib
To run the validation suite, ensure your environment has the required dependencies installed:
bash
pip install numpy matplotlib

