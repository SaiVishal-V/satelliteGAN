# SatelliteGAN — Wind Field Reconstruction with DINCAE

[![Python 3.6+](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/)
[![TensorFlow 2.x](https://img.shields.io/badge/TensorFlow-2.x-orange.svg)](https://www.tensorflow.org/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-green.svg)](LICENSE.md)

A deep-learning pipeline for **reconstructing missing satellite wind speed observations** over the Indian Ocean using **DINCAE** (Data-Interpolating Convolutional Auto-Encoder).

This repository contains a **TensorFlow 2.x–compatible** fork of the original [DINCAE](https://github.com/gher-ulg/DINCAE) framework, extended with:

- **Checkpoint resumption** — seamlessly resume training from the latest or best checkpoint.
- **Early stopping** — halt training when validation RMS stops improving to prevent over-fitting.
- **Best-model tracking** — automatically save the model and reconstruction with the lowest validation error.
- **Date-stamped outputs** — embed per-timestep date labels directly in output NetCDF files.

---

## Overview

Satellite scatterometers (e.g., ASCAT / Oceansat-3) provide near-surface ocean wind speed measurements, but their narrow swath geometry leaves large spatial gaps in daily composites. DINCAE fills these gaps by learning the spatiotemporal structure of the wind field through a **U-Net style convolutional auto-encoder** trained on the available observations themselves—no external reanalysis data is required.

### Architecture

```
Input (obs + mask + coords + time)
  │
  ├─ Encoder: Conv2D → AvgPool  ×4 layers
  │
  ├─ Dense bottleneck (with dropout)
  │
  └─ Decoder: Upsample → Conv2D  ×4 layers (with skip connections)
        │
        └─ Output: mean_rec (reconstructed field) + sigma_rec (uncertainty)
```

---

## Repository Structure

```
.
├── DINCAE/              # Core DINCAE Python package (TF2-compatible)
│   └── __init__.py      # Model definition, training loop, data I/O
├── run_DINCAE.py        # Example training script with tuned hyperparameters
├── setup.py             # pip-installable package configuration
├── setup.txt            # Original setup configuration (TF 1.15 reference)
├── LICENSE.md           # GNU GPLv3 license
└── README.md            # This file
```

---

## Installation

### Prerequisites

- Python ≥ 3.6
- CUDA-capable GPU (recommended)

### Install from source

```bash
git clone https://github.com/SaiVishal-V/satelliteGAN.git
cd satelliteGAN
pip install -e .
```

This installs the `DINCAE` package along with its dependencies:

| Package    | Minimum Version |
|------------|----------------|
| numpy      | ≥ 1.16.0       |
| netCDF4    | ≥ 1.4.2        |
| TensorFlow | ≥ 2.13.0       |

---

## Input Data Format

Input must be a NetCDF file with the following variables:

| Variable       | Dimensions        | Description                              |
|----------------|-------------------|------------------------------------------|
| `lon`          | `(lon,)`          | Longitude in degrees East                |
| `lat`          | `(lat,)`          | Latitude in degrees North                |
| `time`         | `(time,)`         | Days since 1900-01-01 (with `units` attr)|
| `mask`         | `(lat, lon)`      | Boolean land/sea mask (1 = valid)        |
| `wind_speed`   | `(time, lat, lon)` | Wind speed with `_FillValue` for gaps    |

---

## Usage

1. **Edit `run_DINCAE.py`** to point to your input NetCDF file and desired output directory:

```python
filename = r"path/to/your_wind_data.nc"
varname  = "wind_speed"
outdir   = r"path/to/output"
```

2. **Run the reconstruction:**

```bash
python run_DINCAE.py
```

### Key Hyperparameters

| Parameter                    | Default   | Description                                      |
|------------------------------|-----------|--------------------------------------------------|
| `epochs`                     | 600       | Maximum training epochs                          |
| `batch_size`                 | 30        | Mini-batch size                                  |
| `learning_rate`              | 2e-5      | Initial Adam learning rate                       |
| `ntime_win`                  | 5         | Temporal context window (must be odd)            |
| `dropout_rate_train`         | 0.08      | Dropout probability during training              |
| `early_stopping_patience`   | 40        | Stop after N validations without improvement     |
| `save_model_each`            | 100       | Checkpoint frequency (epochs)                    |

---

## Output

Output NetCDF files contain:

- **`meandata`** — Temporal mean of the input field (used for anomaly computation).
- **`mean_rec`** — Reconstructed wind speed field (mean of predicted distribution).
- **`sigma_rec`** — Reconstruction uncertainty (standard deviation).
- **`date_stamp`** — Per-timestep date string (DD-MM-YYYY).

---

## Acknowledgements

This work is based on the original **DINCAE** framework by [Alexander Barth](https://github.com/gher-ulg/DINCAE), described in:

> Barth, A., Alvera-Azcárate, A., Licer, M., & Beckers, J.-M. (2020).  
> *DINCAE 1.0: a convolutional neural network with error estimates to reconstruct sea surface temperature satellite observations.*  
> Geoscientific Model Development, 13, 1609–1622.  
> [https://doi.org/10.5194/gmd-13-1609-2020](https://doi.org/10.5194/gmd-13-1609-2020)

---

## License

This project is licensed under the **GNU General Public License v3.0** — see [LICENSE.md](LICENSE.md) for details.
