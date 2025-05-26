from loader import *
from approximator import *
from plotter import *

# Paths to the data
slow_path = 'data/acc_slow.csv'
normal_path = 'data/acc_normal.csv'
hyper_path = 'data/acc_hyper.csv'

# Extract time and amplitude from datasets
x, y = load_breathing_data(slow_path)

x = x[:len(x)//2]
y = y[:len(y)//2]

peaks = find_periods(y)
y_fit = []
last_peak = 0

for peak in peaks:
    yf, _ = polynomial_fit(x[last_peak:peak+1], y[last_peak:peak+1], 5)
    y_fit.extend(yf)
    last_peak = peak+1
    plt.axvline(x[peak], color='black', linestyle='--')
    
yf, _ = polynomial_fit(x[last_peak:], y[last_peak:], 5)
y_fit.extend(yf)

# Oryginalny sygnał
plt.plot(x, y)
plt.plot(x, y_fit, color='red')
plt.title("Sygnał z nałożonymi okresami")
plt.xlabel("Czas [s]")
plt.ylabel("Amplituda")
plt.grid(True)
plt.show()

# Degree of polynomial
# degree = 100

# --- Slow breathing ---
# amplitude_slow_fit, _ = polynomial_fit(time_slow, amplitude_slow, degree)
# plot_raw_signal(time_slow, amplitude_slow, 'Slow Breathing – Raw Data', 'Raw slow breathing', color='blue')
# plot_comparison(time_slow, amplitude_slow, amplitude_slow_fit, f'Slow Breathing – Polynomial Approximation (deg {degree})')

# --- Normal breathing ---
# amplitude_normal_fit, _ = polynomial_fit(time_normal, amplitude_normal, degree)
# plot_raw_signal(time_normal, amplitude_normal, 'Normal Breathing – Raw Data', 'Raw normal breathing', color='green')
# plot_comparison(time_normal, amplitude_normal, amplitude_normal_fit, f'Normal Breathing – Polynomial Approximation (deg {degree})')

# --- Hyperventilation breathing ---
# amplitude_hyper_fit, _ = polynomial_fit(time_hyper, amplitude_hyper, degree)
# plot_raw_signal(time_hyper, amplitude_hyper, 'Hyperventilation – Raw Data', 'Raw hyperventilation', color='purple')
# plot_comparison(time_hyper, amplitude_hyper, amplitude_hyper_fit, f'Hyperventilation – Polynomial Approximation (deg {degree})')
