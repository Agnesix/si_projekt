import numpy as np

def polynomial_fit(x, y, degree):
    coeffs = np.polyfit(x, y, degree)
    y_fit = np.polyval(coeffs, x)
    return y_fit, coeffs
