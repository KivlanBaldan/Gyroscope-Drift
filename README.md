# Gyroscope-Drift
Tools and models for simulating, analyzing, and compensating for gyroscope drift in IMU sensors. Features stochastic error modeling, Allan variance insights, and filtering techniques.
# Gyroscope Drift Analysis & Simulation

A specialized toolkit for analyzing, modeling, and compensating for **gyroscope drift** in Inertial Measurement Units (IMUs). Gyroscopes inherently suffer from accumulating errors over time due to various internal and environmental noise factors. This repository provides the mathematical frameworks and Python scripts to quantify these errors and test compensation algorithms.

---

## 📐 Understanding Gyroscope Drift

Gyroscope measurements contain systematic and stochastic errors that integrate over time, causing an escalating error in calculated orientation (attitude integration drift). This repository models the primary components of this drift:

1. **Constant Bias (Fixed Offset):** A constant deterministic error that causes a linear error growth when integrated into angles.
2. **Angle Random Walk (ARW):** High-frequency white noise on the angular rate that translates to a brownian motion random walk in the integrated angle ($\propto \sqrt{t}$).
3. **Bias Instability (Flicker Noise):** Low-frequency $1/f$ noise causing the bias to wander slowly over time.
4. **Thermal Drift:** Variations in the bias baseline induced by ambient temperature fluctuations.

---

## 🚀 Core Features

- **Stochastic Noise Simulation:** Generates synthetic gyroscope data with configurable White Noise (ARW) and Pink Noise (Bias Instability) to benchmark dead-reckoning algorithms.
- **Drift Quantization:** Integrates with Allan Deviation (ADEV) to isolate and mathematically extract specific noise coefficients from raw sensor logs.
- **Compensation Filters:** Implements tracking and mitigation scripts (such as high-pass filters or zero-velocity updates) to minimize orientation divergence.

---

## 📁 Repository Directory Structure

```text
├── data/                  # Sample static IMU logs showing long-term drift
├── src/                   # Python source code
│   ├── drift_simulator.py # Script to inject synthetic drift models into data
│   ├── drift_analysis.py  # Calculates error accumulation rates over time
│   └── filters.py         # Baseline tracking or bias compensation algorithms
├── requirements.txt       # Software dependencies
└── README.md              # Project documentation
