#!/bin/bash
echo "====================================================="
echo "Initiating Project Cornucopia Validation Pipeline..."
echo "====================================================="

# Ensure data directory exists
mkdir -p data/resonator_raw_logs

# Step 1: Run Simulation
echo "--> STEP 1: Running FDTD M^4 Brane Simulation..."
cd analysis
python meep_cornucopia_sim.py

# Step 2: Run Analysis
echo "--> STEP 2: Calculating Geometric Energy Accumulation..."
python delta_E_calc.py

echo "====================================================="
echo "Pipeline Complete. Check /analysis for results."
echo "====================================================="
