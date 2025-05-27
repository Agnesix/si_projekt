from pandas.core.interchange.from_dataframe import primitive_column_to_ndarray

from PeriodicSignal import PeriodicSignal
from loader import *
from approximator import *
from plotter import *

if __name__ == "__main__":
    # Paths to the data
    slow_path = 'data/acc_slow.csv'
    normal_path = 'data/acc_normal.csv'
    hyper_path = 'data/acc_hyper.csv'

    # Extract time and amplitude from datasets
    x, y = load_breathing_data(normal_path)

    signal = PeriodicSignal(x[:len(x)//2], y[:len(x)//2])
    signal.plot_signal()
    signal.plot_cycles_raw()
    signal.plot_cycles_approx()
