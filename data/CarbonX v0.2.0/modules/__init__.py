"""
Supporting modules for CarbonX solver
Contains kinetics solvers, particle models, and utility functions
"""

# Import all solver modules
try:
    from . import saturation_test
    from . import chemical_kinetics_solver
    from . import particle_temperature_solver
    from . import surface_kinetics
    from . import chemical_kinetics_species_detector
    from . import sintering_models
    from . import Results_Processor_5
    from . import Results_Processor7
    from . import hydrogen_tracker
    from . import gas_UDF
    from . import simulation_setup_loader
    
    from . import aerosol_cnt_solver
    from . import aerosol_kinetics_solver
    from . import aerosol_ratio_calculator
    from . import aerosol_visc_calculator    
    from . import build_in_temp
    
except ImportError as e:
    print(f"Warning: Some modules could not be imported: {e}")

# You can also import specific functions if you want them easily accessible
try:
    from .chemical_kinetics_solver import chemical_kinetics
    from .surface_kinetics import (
        Multilayerd_Model,
        Dual_Diss_Model_Steady,
        Surface_Kinetics_General_UDF,
    )
except ImportError:
    pass

# Define what's publicly available
__all__ = [
    'saturation_test',
    'chemical_kinetics_solver', 
    'particle_temperature_solver',
    'surface_kinetics',
    'chemical_kinetics_species_detector',
    'sintering_models',
    'Results_Processor_5',
    'Results_Processor7',
    'hydrogen_tracker',
    'gas_UDF',
    'simulation_setup_loader',
    'aerosol_cnt_solver',
    'aerosol_kinetics_solver',
    'aerosol_ratio_calculator',
    'aerosol_visc_calculator',
    'build_in_temp',
    'chemical_kinetics',  # Convenience import
]