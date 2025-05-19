from loader import load_breathing_data
from approximator import polynomial_fit
from plotter import plot_raw_signal, plot_comparison

# Paths to the data
slow_path = 'data/acc_slow.csv'
normal_path = 'data/acc_normal.csv'
hyper_path = 'data/acc_hyper.csv'

# Extract time and amplitude from datasets
time_slow, amplitude_slow = load_breathing_data(slow_path)
time_normal, amplitude_normal = load_breathing_data(normal_path)
time_hyper, amplitude_hyper = load_breathing_data(hyper_path)

# Degree of polynomial
degree = 5

# --- Slow breathing ---
amplitude_slow_fit, _ = polynomial_fit(time_slow, amplitude_slow, degree)
plot_raw_signal(time_slow, amplitude_slow, 'Slow Breathing – Raw Data', 'Raw slow breathing', color='blue')
plot_comparison(time_slow, amplitude_slow, amplitude_slow_fit, f'Slow Breathing – Polynomial Approximation (deg {degree})')

# --- Normal breathing ---
amplitude_normal_fit, _ = polynomial_fit(time_normal, amplitude_normal, degree)
plot_raw_signal(time_normal, amplitude_normal, 'Normal Breathing – Raw Data', 'Raw normal breathing', color='green')
plot_comparison(time_normal, amplitude_normal, amplitude_normal_fit, f'Normal Breathing – Polynomial Approximation (deg {degree})')

# --- Hyperventilation breathing ---
amplitude_hyper_fit, _ = polynomial_fit(time_hyper, amplitude_hyper, degree)
plot_raw_signal(time_hyper, amplitude_hyper, 'Hyperventilation – Raw Data', 'Raw hyperventilation', color='purple')
plot_comparison(time_hyper, amplitude_hyper, amplitude_hyper_fit, f'Hyperventilation – Polynomial Approximation (deg {degree})')
