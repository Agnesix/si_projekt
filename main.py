from PeriodicSignal import PeriodicSignal
from loader import *
from approximator import *
from plotter import *
from sklearn.metrics import mean_squared_error
import random

if __name__ == "__main__":
    slow = 'data/acc_slow.csv'
    normal = 'data/acc_normal.csv'
    hyper = 'data/acc_hyper.csv'

    # x, y = load_breathing_data(hyper)
    # x, y = load_heartbeat_data()
    # x, y = x[:2000], y[:2000]
    
    # signal = PeriodicSignal(x, y_noise, detect='all')
    # signal.plot_signal()
    # signal.plot_cycles_raw()
    # signal.plot_cycles_approx()
    
    # n = 1
    # for i in range(10):
    #     freq = np.random.uniform(0.5, 3.0)       
    #     noise_level = np.random.uniform(0.1, 1.0)
    #     phase = np.random.uniform(0, np.pi)      
    #     amp = np.random.uniform(0.5, 3.0)        

    #     x, y_noise, y_pure = generate_noisy_sine(length=1000, freq=freq, noise_level=noise_level, phase=phase, amp=amp)

    #     signal = PeriodicSignal(x, y_noise, detect='all')

    #     min_len = min(len(signal.yf), len(y_pure))
    #     mse = mean_squared_error(y_pure[:min_len], signal.yf[:min_len])

    #     print(f"mse_{n}: {mse:.4f}, len={min_len}, freq={freq:.2f}, noise={noise_level:.2f}, phase={phase:.2f}, amp={amp:.2f}")

    #     plt.figure(figsize=(10, 4))
    #     plt.title('Porównanie: zaszumiona, czysta, aproksymowana')
    #     plt.plot(x, y_noise, label='Zaszumiona', alpha=0.6)
    #     plt.plot(x, y_pure, label='Czysta', linestyle='--')
    #     plt.plot(x[:min_len], signal.yf[:min_len], label='Aproksymacja')
        
    #     for peak in signal.peaks:
    #         plt.axvline(signal.x[peak], linestyle='--', color='gray', alpha=0.4)
            
    #     plt.legend()
    #     plt.grid(True)
    #     plt.tight_layout()
    #     plt.savefig(fname=f'charts/mse_{n}')
        
    #     x, y_noise, y_pure = generate_noisy_sine(length=2000, freq=freq, noise_level=noise_level, phase=phase, amp=amp)

    #     signal = PeriodicSignal(x, y_noise, detect='all')

    #     min_len = min(len(signal.yf), len(y_pure))
    #     mse = mean_squared_error(y_pure[:min_len], signal.yf[:min_len])

    #     print(f"mse_{n+1}: {mse:.4f}, len={min_len}, freq={freq:.2f}, noise={noise_level:.2f}, phase={phase:.2f}, amp={amp:.2f}")

    #     plt.figure(figsize=(10, 4))
    #     plt.title('Porównanie: zaszumiona, czysta, aproksymowana')
    #     plt.plot(x, y_noise, label='Zaszumiona', alpha=0.6)
    #     plt.plot(x, y_pure, label='Czysta', linestyle='--')
    #     plt.plot(x[:min_len], signal.yf[:min_len], label='Aproksymacja')
        
    #     for peak in signal.peaks:
    #         plt.axvline(signal.x[peak], linestyle='--', color='gray', alpha=0.4)
            
    #     plt.legend()
    #     plt.grid(True)
    #     plt.tight_layout()
    #     plt.savefig(fname=f'charts/mse_{n+1}')
        
    #     x, y_noise, y_pure = generate_noisy_sine(length=5000, freq=freq, noise_level=noise_level, phase=phase, amp=amp)

    #     signal = PeriodicSignal(x, y_noise, detect='all')

    #     min_len = min(len(signal.yf), len(y_pure))
    #     mse = mean_squared_error(y_pure[:min_len], signal.yf[:min_len])

    #     print(f"mse_{n+2}: {mse:.4f}, len={min_len}, freq={freq:.2f}, noise={noise_level:.2f}, phase={phase:.2f}, amp={amp:.2f}")

    #     plt.figure(figsize=(10, 4))
    #     plt.title('Porównanie: zaszumiona, czysta, aproksymowana')
    #     plt.plot(x, y_noise, label='Zaszumiona', alpha=0.6)
    #     plt.plot(x, y_pure, label='Czysta', linestyle='--')
    #     plt.plot(x[:min_len], signal.yf[:min_len], label='Aproksymacja')
        
    #     for peak in signal.peaks:
    #         plt.axvline(signal.x[peak], linestyle='--', color='gray', alpha=0.4)
            
    #     plt.legend()
    #     plt.grid(True)
    #     plt.tight_layout()
    #     plt.savefig(fname=f'charts/mse_{n+2}')
        
    #     n += 3