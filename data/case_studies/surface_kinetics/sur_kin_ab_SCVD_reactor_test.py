from pathlib import Path
from carbonx.core.carbonx_wrapper import FCCVD_GasReactor
from carbonx.modules.simulation_setup_loader import build_kwargs
from carbonx.core.carbonx_wrapper import SCVD_GasReactor


SETUP_FILE = Path("simulation_setup.txt")
model = FCCVD_GasReactor(
    **build_kwargs(
        SETUP_FILE,
        # --- gas chemistry ---
        kinetics_mechanism_type="FFCM2",
        gas_initial_composition={"C2H2": 0.02, "H2": 0.966, "N2": 1 - 0.02 - 0.966},
        feedstock_gas_name_dominant_current="C2H2",
        carrier_species="N2",
        total_pressure=101325,
        # --- reactor geometry (a 1 m tube; CNT/substrate zone from 0.40 m to 0.60 m) ---
        reactor_length=1.0,
        cnt_zone_start=0.40,
        cnt_zone_end=0.60,
        substrate_bin_number=100,
        xdtube=0.0254,
        gas_NP_time_considered=False,
        # --- flow ---
        __xqtot=2.01e-5,
        flow_temperature_reference=293.0,
        # --- catalyst / substrate loading ---
        dp_initial_premade=15e-9,
        rho_part_m2=1e15,
        substrate_accessible_surface_factor=0.99,
        fraction_cnt_gp=0.999,
        # --- surface kinetics options ---
        surface_kinetics_solver_activated=True,
        carb_struct_enabled=True,
        deactivation_enabled=True,
        surface_kinetics_type = "Multilayerd_Model",     #Multilayerd_Model  #Surface_Kinetics_General_UDF
        gamma="UDF",
        # --- run control ---
        total_sim_time=500.0,
        verbose=True,
    )
)
_, solutions = model.run()