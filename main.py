from PeriodicSignal import PeriodicSignal
from loader import *
from approximator import *
from plotter import *

if __name__ == "__main__":
    slow = 'data/acc_slow.csv'
    normal = 'data/acc_normal.csv'
    hyper = 'data/acc_hyper.csv'

    x, y = load_breathing_data(slow)
    # x, y = load_heartbeat_data()

    signal = PeriodicSignal(x, y, detect='segment')
    
    signal.plot_signal()
    # signal.plot_cycles_raw()
    # signal.plot_cycles_approx()
