import pytest
import math
import typhoon.api.hil as hil
import typhoon.test.capture as cap
import typhoon.test.signals as sig
import typhoon.test.reporting.figures as fig
from typhoon.api.schematic_editor import SchematicAPI

mdl = SchematicAPI()

fs = 100e3

@pytest.fixture(scope='function')
def load_model(request):
#Fixture setup code
    
#Model Property Changes
    print(request.param)
    mdl.load(filename='microgrid_Data generation.tse')

    #faultHandle = mdl.get_item(name='Fault infront of WT')
    #print(mdl.get_property_value(mdl.prop(faultHandle,'resistance')))
    #print(mdl.get_property_value(mdl.prop(faultHandle,'fault_type')))
    
    #mdl.set_property_value(mdl.prop(faultHandle,'resistance'), 
    #                        value=resistanceValue, 
    #                        )
                            
    #mdl.set_property_value(mdl.prop(faultHandle,'fault_type'), 
    #                        value=request.param, 
    #                        )
    #mdl.save()
    #mdl.compile()
    
    
    hil.load_model(file='microgrid_Data generation Target files\\microgrid_Data generation.cpd', 
                    vhil_device=True, 
                    )
    
    #Source Inputs
    """
    hil.set_source_sine_waveform(name='Grid1.Vsp_sin1', 
                                  rms=math.sqrt(2), 
                                  )
    hil.set_source_sine_waveform(name='Grid1.Vsp_sin2', 
                                  rms=math.sqrt(2), 
                                  )
    hil.set_source_sine_waveform(name='Grid1.Vsp_sin3', 
                                  rms=math.sqrt(2), 
                                  )                              
    """
    #Grid Inputs
    inputs_grid = {
        'Grid UI1.Connect': 1.0,
        'MGCC_ON': 1.0,
        'c_option': 0.0,
        'op_mode': 0.0,
    }
    #Battery Inputs
    inputs_battery = {
        'Battery ESS (Generic) UI1.Pref': 0.7,  
        'Battery ESS (Generic) UI1.Pref rate of change': 0.0,
        'Battery ESS (Generic) UI1.Qref': 0.0,
        'Battery ESS (Generic) UI1.Qref rate of change': 0.1,
        'Battery ESS (Generic) UI1.Converter mode': 1.0,
        'Battery ESS (Generic) UI1.Max SOC': 80.0,
        'Battery ESS (Generic) UI1.Min SOC': 20.0,
        'Battery ESS (Generic) UI1.Initial SOC': 86.0,
        'Battery ESS (Generic) UI1.Initial SOH': 90.0,
        'Battery ESS (Generic) UI1.Enable': 1.0,  
        
    }
    
    #Wind Plant Inputs
    inputs_windturbine = {
        'Wind Power Plant (Generic) UI1.Pcurtailment': 1.0,
        'Wind Power Plant (Generic) UI1.MPPT rate of change': 1.0,
        'Wind Power Plant (Generic) UI1.Pcurtailment rate of change': 1.0,
        'Wind Power Plant (Generic) UI1.Qref rate of change': 1.0,
        'Wind Power Plant (Generic) UI1.Average wind speed max (SC)': 34.0,
        'Wind Power Plant (Generic) UI1.Cut out wind speed (SC)': 28.0,
        'Wind Power Plant (Generic) UI1.P reduction wind speed (SC)': 19.0,
        'Wind Power Plant (Generic) UI1.Wind speed': 17.0,
        'Wind Power Plant (Generic) UI1.int1 wind speed max': 25.0,
        'Wind Power Plant (Generic) UI1.int2 wind speed max': 30.0,
        'Wind Power Plant (Generic) UI1.time interval (SC)': 600.0,
        'Wind Power Plant (Generic) UI1.time interval 1': 180.0,
        'Wind Power Plant (Generic) UI1.time interval 2': 15.0,
        'Wind Power Plant (Generic) UI1.Enable': 1.0,
        
    }
    #PV Plant Inputs
    inputs_pvplant = {
        'PV Power Plant (Generic) UI1.Pcurtailment': 1.0,
        'PV Power Plant (Generic) UI1.Qref': 0,
        'PV Power Plant (Generic) UI1.Pcurtailment rate of change': 1.0,
        'PV Power Plant (Generic) UI1.Qref rate of change': 1.0,
        'PV Power Plant (Generic) UI1.MPPT rate of change': 1.0,
        'PV Power Plant (Generic) UI1.Enable': 1.0,
    }
                        
    #Diesel Genset Inputs
    inputs_dieselgenset = {
        'Diesel Genset (Generic) UI1.Operation mode': 2.0,
        'Diesel Genset (Generic) UI1.Pref': 0.1,
        'Diesel Genset (Generic) UI1.Qref': 0.02,
        'Diesel Genset (Generic) UI1.Fref': 1.0,
        'Diesel Genset (Generic) UI1.Frequency droop offset': 1.0,
        'Diesel Genset (Generic) UI1.Frequency droop coeff': 7.0,
        'Diesel Genset (Generic) UI1.Voltage droop coeff': 10,
        'Diesel Genset (Generic) UI1.Pref rate of change': 0.05,
        'Diesel Genset (Generic) UI1.Qref rate of change': 1.0,
        'Diesel Genset (Generic) UI1.Vrms_ref': 1.0,
        'Diesel Genset (Generic) UI1.Vrms_ref rate of change': 1.0,
        'Diesel Genset (Generic) UI1.Qref rate of change': 1.0,
        'Diesel Genset (Generic) UI1.Enable': 1.0,
    }
    
    scadaInputs = {**inputs_grid, **inputs_battery, **inputs_windturbine,
                    **inputs_pvplant, **inputs_dieselgenset}
    
    for key, value in scadaInputs.items():
        hil.set_scada_input_value(scadaInputName=key, value=value)    
    
        #Fixture setup code
    hil.set_scada_input_value(scadaInputName='Grid UI1.Grid_Vrms_cmd', 
                               value=1.0, 
                               )
    hil.set_scada_input_value(scadaInputName='Grid UI1.Grid_freq_cmd',
                                value=1.0,
                                )
                                
    faults =  ['Fault infront of WT.enable', 'Fault infront of WT1.enable', 
                'Fault infront of PV.enable', 'Fault infront of B.enable', 
                'Fault between WTE.enable', 'Fault between WT-BE.enable', 
                'Fault between WT-BI.enable']
    
    for fault in faults:
        hil.set_contactor(name=fault, 
                           swControl=True, 
                           swState=False, 
                           )
    
    hil.start_simulation()
    
    yield 
    #Fixture teardown code
    hil.stop_simulation()
                                    
@pytest.mark.parametrize('resistanceValue', [#(0.1),
                                            #(0.5),
                                            (1.0),
                                            #(5.0),
                                            #(10.0),
                                            #(50.0),
                                            #(100.0),
                                            ], indirect=True)
@pytest.mark.parametrize('faultType',  [('A-GND'),
                                        #('B-GND'),
                                        #('C-GND'),
                                        #('A-B'),
                                        #('A-C'),
                                        #('B-C'),
                                        #('A-B-GND'),
                                        #('A-C-GND'),
                                        #('B-C-GND'),
                                        #('A-B-C'),
                                        #('A-B-C-GND'), 
                                       ], indirect=True)
#"""comment whichever faults you do NOT want included in the test"""
@pytest.mark.parametrize('fault', [ ('Fault infront of WT'),
                                    #('Fault infront of WT1'), 
                                    #('Fault infront of PV'),
                                    #('Fault infront of B'), 
                                    #('Fault between WTE'),
                                    #('Fault between WT-BE'),
                                    #('Fault between WT-BI'), 
                                    #('gridfault'),
                                    ], indirect=True)
def test_faults(load_model, resistanceValue, faultType, fault):
    """test different fault locations & measures grid current and voltage"""
    
    print('FAULT SETTINGS')
    print(hil.get_contactor_settings(name='Fault infront of WT.enable'))
    print(hil.get_contactor_settings(name='Fault infront of WT1.enable'))
    print(hil.get_contactor_settings(name='Fault infront of PV.enable'))
    print(hil.get_contactor_settings(name='Fault infront of B.enable'))
    print(hil.get_contactor_settings(name='Fault between WTE.enable'))
    print(hil.get_contactor_settings(name='Fault between WT-BE.enable'))
    print(hil.get_contactor_settings(name='Fault between WT-BI.enable'))
    
    print('BREAKER SETTINGS')
    print(hil.get_contactor_settings(name='PCC_monitor.S1'))
    print(hil.get_contactor_settings(name='Battery ESS (Generic)1.Grid Converter1.Contactor.S1'))
    print(hil.get_contactor_settings(name='Wind Power Plant (Generic)1.Grid Converter1.Contactor.S1'))
    print(hil.get_contactor_settings(name='PV Power Plant (Generic)1.Grid Converter1.Contactor.S1'))
    print(hil.get_contactor_settings(name='Grid1.Contactor.S1'))
    print(hil.get_contactor_settings(name='Diesel Genset (Generic)1.Diesel genset1.S1'))
    
    print('SOURCE SETTINGS')
    print(hil.get_source_settings(name='Grid1.Vsp_sin1'))
    print(hil.get_source_settings(name='Grid1.Vsp_sin2'))
    print(hil.get_source_settings(name='Grid1.Vsp_sin3'))
    print(hil.get_scada_input_settings(scadaInputName='Grid UI1.Grid_Vrms_cmd'))
    
    print(mdl.get_property_value(mdl.prop(faultHandle,'fault_type')))
    
    faultHandle = mdl.get_item(name='Fault infront of WT')
    print(mdl.get_property_value(mdl.prop(faultHandle,'resistance')))
    print(mdl.get_property_value(mdl.prop(faultHandle,'fault_type')))
    
    #mdl.set_property_value(mdl.prop(faultHandle,'resistance'), 
    #                        value=resistanceValue, 
    #                        )
                            
    #mdl.set_property_value(mdl.prop(faultHandle,'fault_type'), 
    #                        value=request.param, 
    #                        )
    
    cap.wait(secs=2)
    
#Capture Section    
    #start capture
    
    cap_duration = 2
    time_before_fault = cap_duration/2
    cap.start_capture(duration=cap_duration, 
                       rate=fs, 
                       signals=[

                            'Grid1.Vc', 'Grid1.Vb', 'Grid1.Va',
                            'PCC_monitor.S1_fb', 
                            'Grid1.Ic', 'Grid1.Ib', 'Grid1.Ia',
                            'PCC_monitor.Va', 'PCC_monitor.Vb', 'PCC_monitor.Vc',
                            'PCC_monitor.VA', 'PCC_monitor.VB', 'PCC_monitor.VC',
                            'Grid UI1.Vrms_meas_kV', 'Grid UI1.Qmeas_kVAr', 'Grid UI1.Pmeas_kW',
                            'Wind Power Plant (Generic) UI1.Pmeas_kW', 'PV Power Plant (Generic) UI1.Pmeas_kW',
                            'Battery ESS (Generic) UI1.Pmeas_kW', 'Diesel Genset (Generic) UI1.Pmeas_kW',
                            'PCC_monitor.Synch_check.PLLs.VABC', 'PCC_monitor.Synch_check.PLLs.Vabc'
                            #'Wind Power Plant (Generic) UI1.wind_speed_m_per_s',
                            #'Wind Power Plant (Generic) UI1.MCB_status', 'PV Power Plant (Generic) UI1.MCB_status',
                            #'Diesel Genset (Generic) UI1.MCB_status', 'Battery ESS (Generic) UI1.MCB_status',
                       ],)
                       
    print(hil.read_analog_signal(name='PCC_monitor.VA'))
    print(hil.read_analog_signal(name='PCC_monitor.Va'))
    
#Fault Section (halfway after cap starts)                  
    cap.wait(secs=time_before_fault)
 
    if  (fault == 'gridfault'):
            hil.set_scada_input_value(scadaInputName='Grid UI1.Grid_Vrms_cmd', 
                               value=0.5, 
                               )
    else:                           
        hil.set_contactor(name=f'{fault}.enable', 
                           swControl=True, 
                           swState=True, 
                           )
                       
    df = cap.get_capture_results(wait_capture=True)
    
    print('AFTER CAP')
    print(hil.get_contactor_settings(name='Fault infront of WT.enable'))
    print(hil.get_contactor_settings(name='Fault infront of WT1.enable'))
    print(hil.get_contactor_settings(name='Fault infront of PV.enable'))
    print(hil.get_contactor_settings(name='Fault infront of B.enable'))
    print(hil.get_contactor_settings(name='Fault between WTE.enable'))
    print(hil.get_contactor_settings(name='Fault between WT-BE.enable'))
    print(hil.get_contactor_settings(name='Fault between WT-BI.enable'))
    
    print('BREAKER SETTINGS')
    print(hil.get_contactor_settings(name='PCC_monitor.S1'))
    print(hil.get_contactor_settings(name='Battery ESS (Generic)1.Grid Converter1.Contactor.S1'))
    print(hil.get_contactor_settings(name='Wind Power Plant (Generic)1.Grid Converter1.Contactor.S1'))
    print(hil.get_contactor_settings(name='PV Power Plant (Generic)1.Grid Converter1.Contactor.S1'))
    print(hil.get_contactor_settings(name='Grid1.Contactor.S1'))
    print(hil.get_contactor_settings(name='Diesel Genset (Generic)1.Diesel genset1.S1'))
    
    signals = [
                ['Grid1.Ic', 'Grid1.Ib', 'Grid1.Ia'],
                ['PCC_monitor.Va', 'PCC_monitor.Vb', 'PCC_monitor.Vc'],
                ['PCC_monitor.VA', 'PCC_monitor.VB', 'PCC_monitor.VC'],
                ['Grid UI1.Pmeas_kW','Wind Power Plant (Generic) UI1.Pmeas_kW','PV Power Plant (Generic) UI1.Pmeas_kW',
                'Battery ESS (Generic) UI1.Pmeas_kW', 'Diesel Genset (Generic) UI1.Pmeas_kW'],
                ['PCC_monitor.Synch_check.PLLs.VABC','PCC_monitor.Synch_check.PLLs.Vabc'],
              ]
    plot(df, signals)
#Assert Section 

#Misc Functions
def plot(df,signals,zoom=None):
    if zoom is None:
        fig.attach_figure([df[sig] for sig in signals], 'Complete') #list comprehension
    else:
        fig.attach_figure([df[sig][zoom[0]:zoom[1]] for sig in signals], f'Zoom ({zoom[0]} to {zoom[1]})')
