import numpy as np
from scipy.signal import find_peaks

def polynomial_fit(x, y, degree):
    coeffs = np.polyfit(x, y, degree)
    y_fit = np.polyval(coeffs, x)
    return y_fit, coeffs

def estimate_period_fft(y, fs=1.0):
    freqs = np.fft.rfftfreq(len(y), d=1/fs)
    spectrum = np.abs(np.fft.rfft(y))
    peak_idx = np.argmax(spectrum[1:]) + 1
    peak_freq = freqs[peak_idx]
    return 1 / peak_freq if peak_freq > 0 else None

def estimate_period_autocorr(corr):
    derivative = np.diff(corr)
    for i in range(1, len(derivative)):
        if derivative[i] > 0:
            return i
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
    
    peaks, _ = find_peaks(corr[1:], distance=distance)
    return peaks