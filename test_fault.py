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
    
    #Grid Inputs
    inputs_grid = {
        'Grid UI1.Connect': 1,
    }
    #Battery Inputs
    inputs_battery = {
        'Battery ESS (Generic) UI1.Enable': 1,
        'Battery ESS (Generic) UI1.Pref': 0.7,
        'Battery ESS (Generic) UI1.Pref rate of change': 1,
    }
    
    #Wind Plant Inputs
    inputs_windturbine = {
        'Wind Power Plant (Generic) UI1.Enable': 1,
        'Wind Power Plant (Generic) UI1.Pcurtailment': 1,
        'Wind Power Plant (Generic) UI1.MPPT rate of change': 1,
        'Wind Power Plant (Generic) UI1.Pcurtailment rate of change': 1,
        'Wind Power Plant (Generic) UI1.Qref rate of change': 1,
        
    }
    #PV Plant Inputs
    inputs_pvplant = {
        'PV Power Plant (Generic) UI1.Enable': 1,
        'PV Power Plant (Generic) UI1.Pcurtailment': 1,
        'PV Power Plant (Generic) UI1.Qref': 0,
        'PV Power Plant (Generic) UI1.Pcurtailment rate of change': 1,
        'PV Power Plant (Generic) UI1.Qref rate of change': 1,
        'PV Power Plant (Generic) UI1.MPPT rate of change': 1,
    }
                        
    #Diesel Genset Inputs
    inputs_dieselgenset = {
        'Diesel Genset (Generic) UI1.Enable': 1,
        'Diesel Genset (Generic) UI1.Pref': 0.1,
        'Diesel Genset (Generic) UI1.Qref': 0.02,
        'Diesel Genset (Generic) UI1.Frequency droop offset': 1.0,
        'Diesel Genset (Generic) UI1.Frequency droop coeff': 7,
        'Diesel Genset (Generic) UI1.Voltage droop coeff': 10,
        'Diesel Genset (Generic) UI1.Pref rate of change': 0.05,
        'Diesel Genset (Generic) UI1.Qref rate of change': 1.0,
        'Diesel Genset (Generic) UI1.Vrms_ref rate of change': 1.0,
        'Diesel Genset (Generic) UI1.Qref rate of change': 1.0,
    }
    
    scadaInputs = {**inputs_grid, **inputs_battery, **inputs_windturbine,
                    **inputs_pvplant, **inputs_dieselgenset}
    
    for key, value in scadaInputs.items():
        hil.set_scada_input_value(scadaInputName=key, value=value)    
    
    yield 
    
    #Fixture teardown code
    hil.stop_simulation()
    
#function scope i.e running before beginning each test
@pytest.fixture()
def return_to_default(load_model):
    #Fixture setup code
    #hil.set_scada_input_value(scadaInputName='Grid UI1.Grid_Vrms_cmd', 
    #                           value=1, 
    #                           )
    faults =  ['Fault infront of WT.enable', 'Fault infront of WT1.enable', 
    'Fault infront of PV.enable', 'Fault infront of B.enable', 
    'Fault between WTE.enable', 'Fault between WT-BE.enable', 
    'Fault between WT-BI.enable']
    
    for fault in faults:
        hil.set_contactor(name=fault, 
                           swControl=True, 
                           swState=False, 
                           )

@pytest.mark.parametrize('fault', [('Fault infront of WT.enable'),('Fault infront of WT1.enable'), 
                                        ('Fault infront of PV.enable'),('Fault infront of B.enable'), 
                                        ('Fault between WTE.enable'),('Fault between WT-BE.enable'), 
                                        ('Fault between WT-BI.enable')])
def test_faults(return_to_default, fault):
    """
    test different fault locations & measures grid current and voltage
    """
    print(hil.get_scada_input_settings(scadaInputName='Grid UI1.Grid_Vrms_cmd'))
    
    cap.wait(secs=3) #wait 3 sec after starting simulation for steady cap
    
    #start capture
    cap_duration = 2
    time_before_fault = cap_duration/2
    cap.start_capture(duration=cap_duration, 
                       rate=fs, 
                       signals=[
                            'Grid1.Vc', 'Grid1.Vb', 'Grid1.Va', 
                            'Grid1.Ic', 'Grid1.Ib', 'Grid1.Ia',
                            'PCC_monitor.Va', 'PCC_monitor.Vb', 'PCC_monitor.Vc',
                            'PCC_monitor.VA', 'PCC_monitor.VB', 'PCC_monitor.VC',
                            'Grid UI1.Vrms_meas_kV', 'Grid UI1.Qmeas_kVAr', 'Grid UI1.Pmeas_kW',
                            'Wind Power Plant (Generic) UI1.Pmeas_kW', 'PV Power Plant (Generic) UI1.Pmeas_kW',
                            'Battery ESS (Generic) UI1.Pmeas_kW', 'Diesel Genset (Generic) UI1.Pmeas_kW',
                            #'Wind Power Plant (Generic) UI1.wind_speed_m_per_s',
                            'Wind Power Plant (Generic) UI1.MCB_status', 'PV Power Plant (Generic) UI1.MCB_status',
                            'Diesel Genset (Generic) UI1.MCB_status', 'Battery ESS (Generic) UI1.MCB_status',
                       ],)
    
    #Fault Section (halfway after cap starts)                  
    cap.wait(secs=time_before_fault)
    hil.set_scada_input_value(scadaInputName='Grid UI1.Grid_Vrms_cmd', 
                               value=0.5, 
                               )
   
   
                               
    #line faults
    hil.set_contactor(name=fault, 
                       swControl=True, 
                       swState=True, 
                       )
    
    #Fault reperation
    #cap.wait(secs=0.5)
    
    #hil.set_scada_input_value(scadaInputName='Grid UI1.Grid_Vrms_cmd', 
    #                           value=1, 
    #                           )
    
    df = cap.get_capture_results(wait_capture=True)
                       