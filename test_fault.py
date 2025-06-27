import pytest
import typhoon.api.hil as hil
import typhoon.test.capture as cap

fs = 100e3

#module scope i.e. running only once at the start before beginning the first test
@pytest.fixture(scope="module", )
def load_model():
#Fixture setup code
    hil.load_model(file='microgrid_Data generation Target files\\microgrid_Data generation.cpd', 
                    vhil_device=True, 
                    )
    hil.start_simulation()
    
    #enable grid components
    grid_components = [
        #connect grid
        'Grid UI1.Connect',
        #grid enables
        'Battery ESS (Generic) UI1.Enable',
        'Diesel Genset (Generic) UI1.Enable',
        'PV Power Plant (Generic) UI1.Enable',
        'Wind Power Plant (Generic) UI1.Enable',
        ]
    for component in grid_components:
        hil.set_scada_input_value(scadaInputName=component,
                                    value=1,
                                    )
    #Battery Inputs
    hil.set_scada_input_value(scadaInputName='Battery ESS (Generic) UI1.Pref', 
                               value=0.7, 
                               )
    hil.set_scada_input_value(scadaInputName='Battery ESS (Generic) UI1.Pref rate of change', 
                               value=0.1, 
                               )
    yield 
    
    #Fixture teardown code
    hil.stop_simulation()
    
#function scope i.e running before beginning each test
@pytest.fixture()
def return_to_default(load_model):
    #Fixture setup code
    hil.set_scada_input_value(scadaInputName='Grid UI1.Grid_Vrms_cmd', 
                               value=1, 
                               )
                               
    hil.set_contactor(name='Fault infront of WT.enable', 
                       swControl=True, 
                       swState=False, 
                       )

def test_faults(return_to_default):
    """
    test different fault locations & measures grid current and voltage
    """
    
    cap.wait(secs=0) #wait 5 sec after starting simulation for steady cap
    
    #start capture
    cap_duration = 6
    time_before_fault = cap_duration/2
    cap.start_capture(duration=cap_duration, 
                       rate=fs, 
                       signals=[
                            #'Grid1.Vc', 'Grid1.Vb', 'Grid1.Va', 
                            #'Grid1.Ic', 'Grid1.Ib', 'Grid1.Ia',
                            #'PCC_monitor.Va', 'PCC_monitor.Vb', 'PCC_monitor.Vc',
                            #'PCC_monitor.VA', 'PCC_monitor.VB', 'PCC_monitor.VC',
                            #'Grid UI1.Vrms_meas_kV', 'Grid UI1.Qmeas_kVAr', 'Grid UI1.Pmeas_kW',
                            #'Wind Power Plant (Generic) UI1.Pmeas_kW', 'PV Power Plant (Generic) UI1.Pmeas_kW',
                            'Battery ESS (Generic) UI1.Pmeas_kW', #'Diesel Genset (Generic) UI1.Pmeas_kW',
                            #'Wind Power Plant (Generic) UI1.wind_speed_m_per_s',
                       ],)
    
                       
    #Fault Section (halfway after cap starts)                  
    #cap.wait(secs=time_before_fault)
    
    #hil.set_scada_input_value(scadaInputName='Grid UI1.Grid_Vrms_cmd', 
    #                           value=1, 
    #                           )
                               
    #hil.set_contactor(name='Fault infront of WT.enable', 
    #                   swControl=True, 
    #                   swState=True, 
    #                   )
    
    #Fault reperation
    #cap.wait(secs=0.5)
    
    #hil.set_scada_input_value(scadaInputName='Grid UI1.Grid_Vrms_cmd', 
    #                           value=1, 
    #                           )
    
    df = cap.get_capture_results(wait_capture=True)
                       