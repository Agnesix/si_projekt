import numpy as np
from scipy.signal import find_peaks
from scipy.interpolate import UnivariateSpline

def polynomial_fit(x, y, degree):
    coeffs = np.polyfit(x, y, degree)
    y_fit = np.polyval(coeffs, x)
    return y_fit, coeffs

def find_periods(y, distance=10, height=0):
    mean_y = y - np.mean(y)

    corr = np.correlate(mean_y, mean_y, mode='full')
    corr = corr[len(corr)//2:]

    peaks, _ = find_peaks(corr[1:], distance=distance, height=height)

    return peaks