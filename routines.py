import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from adwin_utils import adw
from adwin_utils.transformations import convert_bin_to_v, convert_v_to_bin, get_delays

# Measurements settings
AVERAGE_POINTS = 20
SCANRATE_HZ = 100000
INTEGRATION_TIME_MS = 1
SETTLING_TIME_MS = 0
ADWIN_CLOCK_FREQUENCY_HZ = 40e6

# Range settings
V_START = -2
V_END = 2

def run_calibration(reference_resistance, save_path = None):

    start_bin, start_voltage = convert_v_to_bin(V_START)
    end_bin, end_voltage = convert_v_to_bin(V_END)
    set_bin, set_voltage = start_bin, start_voltage

    bin_array = [bin for bin in np.arange(start_bin, end_bin+1, 1)]
    voltage_array = convert_bin_to_v(bin_array)
    # timing settings for adwin clock cycles
    loops_average, process_delay, loops_waiting = get_delays(SCANRATE_HZ, 
                                                        INTEGRATION_TIME_MS, 
                                                        SETTLING_TIME_MS, 
                                                        ADWIN_CLOCK_FREQUENCY_HZ)

    print(f'Loops average: {loops_average}\tProcess delay: {process_delay}\tLoops waiting: {loops_waiting}')

    time.sleep(3)

    adw.Load_Process('ADbasic_scripts\i_measure_calibration.T96')

    adw.Set_Processdelay(6, int(process_delay))
    
    # adw.SetData_Float(10, )
    adw.SetData_Long(bin_array, 11, 1, len(bin_array))

    adw.Set_Par(7, int(start_bin))
    adw.Set_Par(8, int(set_bin))
    adw.Set_Par(9, int(end_bin-start_bin))
    adw.Set_Par(55, int(loops_average))
    adw.Set_Par(56, int(loops_waiting))
    adw.Set_Par(59, 1)

    start_time = time.time()
    adw.Start_Process(6)
    
    while adw.Get_Par(59) == 1:
        current_bin = adw.Get_Par(12)
        current_v = adw.Get_Par(8)
        print(f"Current voltage = {convert_bin_to_v(current_v): .3f} V measuring bin {current_bin}")
        

    if adw.Get_Par(59) == 2:
        adw.Stop_Process(6)
        end_time = time.time()
        log_amplifier_bin = adw.GetData_Float(13, 1, len(bin_array))
        print(f"Done! Time taken {end_time - start_time: .3f} seconds")


    if save_path is not None:
        # Saves data to save_path
        out = np.zeros((2, len(voltage_array)))
        out[0,:] = np.array(log_amplifier_bin)
        out[1,:] = np.array(voltage_array)/reference_resistance
        # np.savetxt(save_path, out)
        pd.DataFrame(out.T).to_csv(save_path)

def current_measure(scanrate_hz, measure_time_s, save_path = None):
    loops_average, process_delay, loops_waiting = get_delays(scanrate_hz, 
                                                    INTEGRATION_TIME_MS, 
                                                    SETTLING_TIME_MS, 
                                                    ADWIN_CLOCK_FREQUENCY_HZ)
    
    loops_measure = int(measure_time_s * scanrate_hz / loops_average)

    print(f'Loops average: {loops_average}\tProcess delay: {process_delay}\tLoops waiting: {loops_waiting}')

    # time.sleep(3)
    
    adw.Load_Process('ADbasic_scripts\i_measure.T97')

    adw.Set_Processdelay(7, int(process_delay))
    
    # adw.SetData_Float(10, )
    # adw.SetData_Long(bin_array, 11, 1, len(bin_array))

    # adw.Set_Par(7, int(start_bin))
    # adw.Set_Par(8, int(set_bin))
    # adw.Set_Par(9, int(end_bin-start_bin))
    adw.Set_Par(50, loops_measure)
    adw.Set_Par(55, int(loops_average))
    adw.Set_Par(56, int(loops_waiting))
    adw.Set_Par(59, 1)

    start_time = time.time()
    adw.Start_Process(7)

    while adw.Get_Par(59) == 1:
        current_bin = adw.Get_Par(12)
        print(f"Measured voltage = {convert_bin_to_v(current_bin): .3f} V\tBin {current_bin}", end='\r')

    if adw.Get_Par(59) == 2:
        adw.Stop_Process(7)
        end_time = time.time()
        current_data = adw.GetData_Float(50, 1, loops_measure)
        voltage_data = adw.GetData_Long(51, 1, loops_measure)
        print()
        print(f"Done! Time taken {end_time - start_time: .3f} seconds")

    if save_path is not None:
        # Saves data to save_path
        out = np.zeros((loops_measure, 2))
        out[:, 0] = np.array(voltage_data)
        out[:, 1] = np.array(current_data)
        # np.savetxt(save_path, out)
        pd.DataFrame(out).to_csv(save_path)

    return end_time - start_time

if __name__ == '__main__':
    # run_calibration(reference_resistance=1.0009e3, save_path='calibration.txt')
    scanrate = 100000
    time_s = 10
    measured_time = current_measure(scanrate, time_s, 'test2.txt')
    
    data = pd.read_csv('test2.txt')

    voltage = data['0'].to_numpy()[:-2]
    current = data['1'].to_numpy()[:-2]

    print(len(voltage))

    plt.plot(np.linspace(0, measured_time, len(current)), convert_bin_to_v(current.astype(int)))
    plt.title('Voltage in vs current meassured')
    plt.xlabel('tiempo [s]')
    plt.ylabel('I_out [A]')
    plt.show()

## end of file ##