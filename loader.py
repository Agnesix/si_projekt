import pandas as pd

def load_breathing_data(filepath):
    df = pd.read_csv(filepath)
    time = df['seconds'].values
    amplitude = df['data'].values
    return time, amplitude
