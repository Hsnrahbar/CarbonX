<img src="./data/logo/logo_Cx2.png" alt="CarbonX logo" width="120px">

# CarbonX

**CarbonX** is an object-oriented Python package for simulating gas-phase synthesis of single- and multi-walled carbon nanotubes (CNTs) and metallic nanoparticles (Fe, Ni, Co) in floating-catalyst chemical vapor deposition (FCCVD) reactors. Its modular, extensible architecture couples four fully-integrated submodules: chemical kinetics, surface kinetics, particle dynamics, and CNT dynamics — along with a built-in machine learning classification module for parametric map analysis.

> 📄 Full documentation and case studies are available at https://github.com/Hsnrahbar/CarbonX/tree/main/docs.

---

## Table of Contents

1. [Introduction](#introduction)
2. [What Can Be Simulated?](#what-can-be-simulated)
3. [Installation](#installation)
4. [Quickstart Guide](#quickstart-guide)
5. [Input & Parameters](#input--parameters)
6. [Outputs & Post-Processing](#outputs--post-processing)
7. [License](#license)
8. [How to Cite](#how-to-cite)

---

## Introduction

Carbon nanotubes exhibit exceptional electrical, optical, and mechanical properties, making them critical candidates for applications in energy storage, sensing, and advanced composites. While CVD offers advantages in scalability and cost-effectiveness, controlling CNT morphology in FCCVD reactors remains challenging due to complex interactions between chemical kinetics, catalyst nanoparticle evolution, and carbon deposition mechanisms.

**CarbonX** addresses this challenge through a modular simulation framework integrating four fully coupled submodules:

- **Chemical kinetics** — gas-phase reaction modelling via [Cantera](https://cantera.org/), supporting mechanisms such as FFCM-2, Caltech, ABF, or user-defined YAML files.
- **Surface kinetics** — catalyst activation, deactivation, carburization, and hydrogenation (multilayered and dual-dissociation models, plus user-defined kinetics).
- **Particle dynamics** — nanoparticle evolution (inception, surface growth, coagulation, sintering) via sectional population balance models.
- **CNT dynamics** — prediction of nanotube length, diameter, wall number, and graphene layer area.

A defining feature of CarbonX is its **extensible design**: users can plug in custom surface or gas kinetics modules without modifying the core simulation engine.

---

## What Can Be Simulated?

The current version of CarbonX includes a solver for **1D plug-flow reactors** and supports:

**Physical phenomena:**
- Agglomeration, surface growth, and sintering of metallic (Ni, Fe, Co) nanoparticles
- Inception of Fe from iron pentacarbonyl (Fe(CO)₅)
- Pyrolysis of hydrocarbon feedstocks (C₂H₂, C₂H₄, CH₄, etc.)
- Surface kinetics for C₂H₂ on Fe nanoparticles (adsorption, dissociation, desorption, carburization, deactivation)
- Custom hydrocarbon–nanoparticle surface kinetics via user-defined YAML mechanisms
- Formation of graphene layers on nanoparticle surfaces
- Formation of SWCNTs and MWCNTs

**Post-processing outputs:**
- Elemental mass balance profiles
- Size distribution profiles (nanoparticles and CNTs)
- Non-dimensionalized self-preserving size distributions
- 2D parametric maps of CNT diameter, length, and wall number
- Process parameters exported to `.csv` (density, viscosity, species concentration, carbon impurity)

---

## Installation

CarbonX is available on [PyPI](https://pypi.org/project/CarbonX). Install it with:

```bash
pip install carbonx
```

All required dependencies (including Cantera) are resolved automatically. Users working in an IDE can also install it through the built-in package manager.

---

## Quickstart Guide

### Single Reactor Simulation

Use the `GasReactor` class for a single set of reactor conditions:

```python
from pathlib import Path
from carbonx import GasReactor
from carbonx.modules.simulation_setup_loader import build_kwargs

SETUP_FILE = Path("simulation_setup.txt")



model = GasReactor(
    **build_kwargs(
        SETUP_FILE,
        catalsyt_element="Ni",
        intnum= 37,
        bin_spacing=1.9,
        rtol=1e-12,
        atol= 1e-38,
        length_step = 'flex_loose',
        kernel_type="fuchs",
        wrapper_mapping_temp=None,
        temperature_history="custom",
        total_initial_concentration=1e+11,
        E_a1=0.9,
        __xqtot=2.01e-5,
        reactor_length=0.6,
        xdtube=0.0254,
        gas_initial_composition={"C2H2": 0.0045, "H2": 0.045, "N2": 1 - 0.0045- 0.045},
        dp_initial_premade=15e-9, 
        surface_kinetics_solver_activated=True,
        carb_struct_enabled=True,
        surface_kinetics_type="Multilayerd_Model",
    )
)  
_, solutions = model.run()

```

### Parametric Map Generation

Use `MappingWrapper` to sweep over multiple reactor conditions and generate 2D parametric maps:

```python
from pathlib import Path
from carbonx import MappingWrapper
from carbonx.modules.simulation_setup_loader import build_kwargs

SETUP_FILE = Path("simulation_setup.txt")

model = MappingWrapper (map_requested="P&T",
                          grid_total =1025,
                          P_range_min =0.001 ,
                          P_range_max =0.01 ,
                          P_iso =0.01 ,
                          T_range_min =800 ,
                          T_range_max =1200 ,
                          T_iso =873 ,
                          xdp_range_min =10e-9 ,
                          xdp_range_max =50e-9 ,
                          xdp_const =15e-9 ,
                          L_reactor_range_min =0.1 ,
                          L_reactor_range_max =1 ,
                          L_reactor =0.6 ,
                          xN_range_min =1e17 ,
                          xN_range_max =10e17 ,
                          xN_const =1e11 ,
                          scale_min =10e-8 ,
                          scale_max =7e-6 ,
                          ml_method = " mean " ,
                          ml_lambda_ =0.001 ,
                          ml_iterations =10000 ,
                          ml_alpha =1.5 ,
                          surface_kinetics_type = " multilayered_model " ,# "multilayered_model"
                          ml_post_cond = True) 
 
_, solutions = model.run()


results = model.run_parametric_study()
model.parametricstudyvisualizer()

```

The built-in ML classification module will automatically identify SWCNT and MWCNT formation regions across the generated map.

---

## Input & Parameters

CarbonX is configured via a `simulation_setup.txt` file. Key parameter categories include:

| Category | Example Parameters |
|---|---|
| Reactor geometry | `reactor_length`, `xdtube`, `temperature_history` |
| Gas chemistry | `gas_initial_composition`, `gas_mechanism` |
| Particle dynamics | `bin_spacing`, `kernel_type`, `dp_initial_premade` |
| Surface kinetics | `surface_kinetics_type`, `E_a1`, `carb_struct_enabled` |
| Parametric mapping | `map_param`, `T_range_min/max`, `P_range_min/max` |
| ML classification | `ml_lambda_`, `ml_iterations`, `ml_alpha`, `ml_post_cond` |

Refer to the [User Manual](https://github.com/Hsnrahbar/CarbonX_Package) for a complete parameter reference.

---

## Outputs & Post-Processing

After running a simulation, the `model` instance provides full access to all simulation data. Key output attributes include:

- `AA12` — gas composition, viscosity, density, and dominant hydrocarbon species
- `dp_saved` — primary particle diameter at each length step
- `D_cnt_saved` — CNT mobility diameter across bins and steps
- `wall_number_section_saved` — CNT wall number across bins and steps
- `carbon_data_saved` — full carbon population data at each step
- `y` — nanoparticle state vector (N, V, A, carbon, precursor concentration)

### Built-in Post-Processing

```python
from carbonx import Results_Processor 
AA=Results_Processor.ResultsPostProcessor(model)
AA.plot_psi_eta_diagram([.0001, .0005, .4],add_experimental=True,regime_type='fmr')

# ψ–η diagram with experimental comparison
AA=Results_Processor.ResultsPostProcessor(model) 
fig, ax, sigma_g_g, sigma_g_m, sigma_g_v=AA.plot_geometric_standard_deviations(plot_until=5000, figsize=(10, 6))

# Carbon mass balance
fig, axes, data = AA.mass_balance_check()

# Relative error
fig, ax, data = AA.plot_relative_error()
```

---

## License

CarbonX is licensed under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)** license. See the `LICENSE` file for details.

---

## How to Cite

If you use CarbonX in your research, please cite the associated publication (details in the repository). Case studies and validation examples benchmarked against experimental measurements are available at:

🔗 [https://github.com/Hsnrahbar/CarbonX_Package](https://github.com/Hsnrahbar/CarbonX_Package)

---

*Developed by Hossein Rahbar.*
