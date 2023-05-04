import numpy as np

from adwin_utils import adw
from adwin_utils.transformations import convert_bin_to_v, convert_v_to_bin, get_delays

# Measurements settings
AVERAGE_POINTS = 20000
SCANRATE_HZ = 90000
INTEGRATION_TIME_MS = 1
SETTLING_TIME_MS = 50
ADWIN_CLOCK_FREQUENCY_HZ = 40.0e6


# Range settings
V_START = -2.5
V_END = 2.5

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

    adw.Load_Process('ADbasic_scripts\i_measure_log_calibration.T96')

    adw.Set_Processdelay(6, int(process_delay))
    
    # adw.SetData_Float(10, )
    adw.SetData_Long(bin_array, 11, 1, len(bin_array))

    adw.Set_Par(7, int(start_bin))
    adw.Set_Par(8, int(set_bin))
    adw.Set_Par(9, int(end_bin-start_bin))
    adw.Set_Par(55, int(loops_average))
    adw.Set_Par(56, int(loops_waiting))
    adw.Set_Par(59, 1)

    adw.Start_Process(6)

    while adw.Get_Par(59) == 1:
        current_bin = adw.Get_Par(12)
        current_v = adw.Get_Par(8)
        print(f"I'm working Bias = {convert_bin_to_v(current_v)} V measuring bin {current_bin}")

    if adw.Get_Par(59) == 2:
        adw.Stop_Process(6)
        log_amplifier_bin = adw.GetData_Float(13, 1, len(bin_array))
        print("I'm done!")


    if save_path is not None:
        # Saves data to save_path
        out = np.zeros((2, len(voltage_array)))
        out[0,:] = np.array(log_amplifier_bin)
        out[1,:] = np.array(voltage_array)/reference_resistance
        np.savetxt(save_path, out, delimiter=',')

if __name__ == '__main__':
    run_calibration(reference_resistance=1.0009e3, save_path='test.txt')
