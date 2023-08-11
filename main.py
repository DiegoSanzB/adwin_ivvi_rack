import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from routines import run_calibration
from adwin_utils.transformations import convert_bin_to_v, convert_v_to_bin, get_delays

calibration_path = 'calibration.txt'

run_calibration(reference_resistance=1.0009e5, save_path=calibration_path)

data = pd.read_csv(calibration_path)

voltage_bin = data['0'].to_numpy()[:-2]
voltage = convert_bin_to_v(voltage_bin.astype(int))
current = data['1'].to_numpy()[:-2]

plt.plot(voltage, current)
plt.title('Real current vs voltage meassured')
plt.xlabel('V_out [bin]')
plt.ylabel('I_out [A]')
plt.show()

## end of file ##