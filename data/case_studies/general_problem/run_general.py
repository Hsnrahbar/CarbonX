from pathlib import Path
from carbonx.core.carbonx_wrapper import FCCVD_GasReactor
from carbonx.modules.simulation_setup_loader import build_kwargs
from carbonx.core.carbonx_wrapper import SCVD_GasReactor


SETUP_FILE = Path("simulation_setup.txt")
model = FCCVD_GasReactor(
    **build_kwargs(
        SETUP_FILE,
        catalsyt_element="Ni",
        kinetics_mechanism_type="FFCM2",
        collision_type="dm&dg",
        intnum= 24,
        bin_spacing=1.9,
        rtol=1e-6,
        atol= 1e-105,
        length_step = 'flex_tight',
        kernel_type="fuchs",
        wrapper_mapping_temp=None,
        temperature_history="custom",
        total_initial_concentration=1e+17,
        E_a1=0.5,
        fraction_cnt_gp=0.99,
        __xqtot=1.667e-5,
        reactor_length=0.55,
        xdtube=0.0254,
        gas_initial_composition={"C2H2": 0.0045, "H2": 0.045, "N2": 1 - 0.0045- 0.045},
        dp_initial_premade=15e-9, 
        surface_kinetics_solver_activated=True,
        carb_struct_enabled=True,
        collision_kernel_enhc=True, ##*****Note! when this kernel_enhc is activated make sure we dont define many to much bins because it reduced the speed of the code significantly 
        cnt_length_bundling_effect=1e-10,
        surface_kinetics_type = "Multilayerd_Model",#Multilayerd_Model  #Dual_Diss_Model_Steady #Surface_Kinetics_General_UDF
        sulfuration=False,
        initial_distribution="Popydisperse",
        sulfur_percentage=.09
    )) 
_, solutions = model.run()



