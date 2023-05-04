import numpy as np

def convert_bin_to_v(n_bin, v_range=10, resolution=16):
    '''
    Converts bins to voltage values
    '''
    step = 2*v_range/(2**resolution)
    voltage_arange = np.arange(-v_range, v_range, step)
    try:
        n = len(n_bin)
        voltage = np.zeros(n)
        for i in range(0, n):
            voltage[i] = voltage_arange[n_bin[i]]
    
    except:
        voltage = voltage_arange[int(n_bin)]

    return voltage


def convert_v_to_bin(voltage, v_range=10, resolution=16):
    '''
    Converts voltages to bin values, also returns the closest discrete voltage from the input
    '''
    step = 2*v_range/(2**resolution)
    voltage_arange = np.arange(-v_range, v_range, step)
    try:
        n = len(voltage)
        n_bin = np.zeros(n)
        for i in range(0, n):
            diff = abs(voltage_arange - voltage[i])
            n_bin[i] = diff.argmin()
    
    except:
        diff = abs(voltage_arange - voltage)
        n_bin = diff.argmin()
    
    return n_bin, convert_bin_to_v(n_bin, v_range=v_range, resolution=resolution)

def get_delays(scanrate_hz, integration_time_ms, settling_time_ms, clockfrequency_hz):
    '''
    Converts scanrate (Hz), integrsation time (ms), settling_time (ms), and ADwin clockfrequency (Hz) to ADwin clock cycles
    ''' 
    loops_av = integration_time_ms / 1000.0 * scanrate_hz
    process_delay = clockfrequency_hz / scanrate_hz
    loops_waiting = ( settling_time_ms / 1000.0) / (process_delay * 1/clockfrequency_hz )
    return loops_av, process_delay, loops_waiting