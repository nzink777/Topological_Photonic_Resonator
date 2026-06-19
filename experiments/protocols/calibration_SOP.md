# Protocol: System Calibration & Baseline State Verification
**Document ID:** EXP-PRO-02
**Related Theory:** Project Cornucopia (Topological Photonic Resonator)
**Objective:** Establish the "Baseline State" and calibrate mechanical rotation and acoustic harmonics to induce the 2^6 (64-sector) geometric lattice prior to the t=4 phase-inversion test.
## 1. Definition of the "Baseline State"
The Baseline State represents the system at absolute rest, stripped of external topological drag and electromagnetic interference, ready to act as a passive geometric diode.
 1. **Fluid Medium:** Fill the quartz basin with 1000 mL of double-distilled, deionized water. The absence of particulates is necessary to ensure any observed laser scattering is due strictly to structural turbulence, not physical impurities.
 2. **Thermal Equilibrium:** Allow the fluid to rest for 15 minutes to reach room temperature (20^\circ\text{C} to 22^\circ\text{C}).
 3. **Noise Floor Verification:** With the acoustic transducers and motor powered off, verify via the digital oscilloscope that the Ferrum/Aurum substrate is successfully shielding the internal basin from ambient electromagnetic frequencies. The readouts should show a flatline 0.00\text{V} AC fluctuation.
## 2. Rotational Calibration (RPM)
The mechanical rotation acts as the baseline curvature for the fluid, mirroring the hyperbolic geometry of the M^4 brane. The goal is to create a stable central vortex (the "throat" of the Klein-bottle manifold).
 1. **Initiate Spin:** Engage the brushless DC motor and slowly ramp up the speed in increments of 10 RPM.
 2. **Target Geometry:** Increase RPM until a stable, central vortex forms down to the base of the quartz basin, exposing the Aurum boundary at the very center.
 3. **Symmetry Check:** Observe the vortex from the top-down perspective. The walls of the vortex must be perfectly symmetrical. Any mechanical oscillation or "wobble" indicates topological drag and requires re-seating the basin.
 4. **Lock RPM:** Once a stable, symmetrical vortex is achieved (typically between 120–180 RPM depending on fluid viscosity), lock the motor controller and record the precise RPM value in the experimental log.
## 3. Harmonic Ratio Calibration (The 7:5:3 Handshake)
With the fluid acting as a rotating manifold, we must now apply acoustic pressure to subdivide the surface into the 64-sector geometric lattice necessary for energy accumulation.
 1. **Initialize Transducers:** Power on the 4-channel audio interface.
 2. **Apply Base Frequencies:** Input the predetermined frequencies into Channels 1, 2, and 3, ensuring they strictly adhere to the prime 7:5:3 ratio (e.g., 700\text{Hz}, 500\text{Hz}, 300\text{Hz}).
 3. **Oscilloscope Alignment:** Monitor all four channels on the digital oscilloscope. Ensure the waveforms are continuous and initially in-phase.
 4. **Visual Lattice Verification:** Look at the surface of the rotating fluid. The interference of the 7:5:3 acoustic pressure against the centrifugal force should cause standing waves to form. Adjust the master amplitude (volume) until exactly **64 distinct nodes** (ripples/peaks) lock into place around the vortex.
   * *Note: This 64-node array is the physical manifestation of the 2^6 permutations required for the geometric ratchet to function.*
## 4. The t=4 Pre-Condition State
Before the measurement phase begins, the system must hold the following state flawlessly for at least 60 seconds:
 * **Stable RPM:** The central vortex is holding steady over the N52 axial magnet.
 * **Stable Lattice:** The 64 acoustic nodes are visible and geometrically locked (not drifting).
 * **Chaotic Optical Scattering:** The 6-point red laser array is powered on. Because the fluid is currently turbulent (pre-inversion), the laser beams should heavily scatter and refract throughout the basin. This verifies that the fluid has *not* yet achieved topological coherence.
**Once all conditions are verified, the system is calibrated. The operator may proceed to trigger the 4-second countdown and execute the 180^\circ phase inversion at t=4.**
