import pandas as pd
import numpy as np

def load_breathing_data(filepath):
    df = pd.read_csv(filepath)
    time = df['seconds'].values
    amplitude = df['data'].values
    return time, amplitude

def load_heartbeat_data():
    data = []
    with open("data/ECG5000.txt") as f:
        for line in f:
            data.extend([np.float64(x) for x in line.split()])
    return np.arange(len(data)), np.array(data)
