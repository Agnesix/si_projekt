import matplotlib.pyplot as plt

def plot_raw_signal(x, y, title, label, color='blue'):
    plt.figure(figsize=(10, 5))
    plt.plot(x, y, label=label, color=color)
    plt.title(title)
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_comparison(x, y_raw, y_fit, title, raw_label='Raw data', fit_label='Fitted curve', color='red'):
    plt.figure(figsize=(10, 5))
    plt.plot(x, y_raw, label=raw_label, alpha=0.6)
    plt.plot(x, y_fit, label=fit_label, color=color)
    plt.title(title)
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.legend()
    plt.show()
