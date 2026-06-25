from pathlib import Path
from carbonx.core.carbonx_wrapper import FCCVD_GasReactor
from carbonx.modules.simulation_setup_loader import build_kwargs
from carbonx.core.carbonx_wrapper import SCVD_GasReactor


SETUP_FILE = Path("simulation_setup.txt")
model = FCCVD_GasReactor(
    **build_kwargs(
        SETUP_FILE,
        catalsyt_element="Fe",
        intnum= 37,
        bin_spacing=1.55,
        rtol=1e-12,
        atol= 1e-38,
        length_step = 'flex_loose',
        kernel_type="fuchs",
        wrapper_mapping_temp=None,
        temperature_history="celnik_2008",
        total_initial_concentration=1.0749732238486255e+18,
        __xqtot=2.01e-5,
        reactor_length=0.73, #assures the equivalent residence time is ~7 sec
        xdtube=0.022,
        gas_initial_composition={"O2": 0, "Ar": 0, "C2H2": 1e-15, "H2O": 0, "N2": 1 - 1e-15},
        dp_initial_premade=5.43e-10, # 2.52 (Fe1), 3.78 (Fe2), 5.6 (Fe4), 6.81 (Fe7)
        surface_kinetics_solver_activated=False,
        carb_struct_enabled=False,
        sulfuration=False,
        sintering_blocksge_by_gp=False,
        collision_kernel_enhc=False,  
    )
)
_, solutions = model.run()
