import numpy as np
from scipy.signal import find_peaks
from scipy.ndimage import gaussian_filter1d
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
import warnings

def interpolate(x, y, deg=5):
    scaler = MinMaxScaler(feature_range=(-1, 1))
    x_scaled = scaler.fit_transform(np.array(x).reshape(-1, 1)).flatten()
    coeffs = np.polyfit(x_scaled, y, deg)
    return np.polyval(coeffs, x_scaled)

def estimate_period_fft(y, fs=1.0):
    freqs = np.fft.rfftfreq(len(y), d=1/fs)
    spectrum = gaussian_filter1d(np.abs(np.fft.rfft(y)), sigma=1)
    peak_idx = np.argmax(spectrum[1:]) + 1
    peak_freq = freqs[peak_idx]
    return 1 / peak_freq if peak_freq > 0 else None

def estimate_period_autocorr(corr):
    min_idx = np.argmin(corr[:len(corr)//2])
    derivative = np.diff(corr[min_idx:])
    for i in range(1, len(derivative)):
        if derivative[i] > 0:
            return min_idx + i
    return None

def find_periods(y, distance=None):
    y = y - np.mean(y)

    corr = np.correlate(y, y, mode='full')
    corr = corr[len(corr)//2:]
    
    if distance is None:
        period_fft = estimate_period_fft(y)
        period_ac = estimate_period_autocorr(corr)

        if period_fft and period_ac:
            distance = (period_fft + period_ac) / 2
        elif period_fft:
            distance = period_fft
        elif period_ac:
            distance = period_ac
        else:
            distance = 10
            
    distance = int(round(distance))    
    peaks, _ = find_peaks(corr[1:], distance=distance)
    return peaks

def generate_noisy_sine(freq=1.0, amp=1.0, phase=0.0, noise_level=0.2, length=1000, sampling_rate=100):
    t = np.linspace(0, length / sampling_rate, length)
    pure_signal = amp * np.sin(2 * np.pi * freq * t + phase)
    noise = np.random.normal(0, noise_level, size=length)
    noisy_signal = pure_signal + noise
    return t, noisy_signal, pure_signal