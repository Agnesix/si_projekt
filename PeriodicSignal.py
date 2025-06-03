import numpy as np
import matplotlib.pyplot as plt
from math import floor
from typing import Optional
from approximator import find_periods, polynomial_fit

class PeriodicSignal:
    def __init__(self, x, y, detect='all', seg_length=300):
        self.x = x
        self.y = y

        self.cycles = []
        
        if detect == 'all':
            self.find_cycles()
        elif detect == 'segment':
            self.find_cycles_by_segment(seg_length)
        else:
            raise ValueError("Incorrect detection mode.")

        for cycle in self.cycles:
            print(cycle.len)

        self.yf = []

        for cycle in self.cycles:
            for yf in cycle.yf:
                self.yf.append(yf)

    def find_cycles(self):
        peaks = find_periods(self.y)
        last_peak = 0

        for peak in peaks:
            self.cycles.append(Cycle(self.x[last_peak:peak + 1], self.y[last_peak:peak + 1]))
            last_peak = peak + 1

        if last_peak < len(self.x) and len:
            self.cycles.append(Cycle(self.x[last_peak:], self.y[last_peak:]))
            
    def find_cycles_by_segment(self, seg_length=300):
        start = 0

        while start < len(self.y) - 1:
            segment = self.y[start:start + seg_length]
            peaks = find_periods(segment)

            if len(peaks) == 0:
                start += seg_length // 2
                continue

            last_peak = 0
            for peak in peaks:
                end = start + peak + 1
                self.cycles.append(Cycle(self.x[start + last_peak:end], self.y[start + last_peak:end]))
                last_peak = peak + 1

            start += last_peak
        

    def plot_signal(self):
        plt.plot(self.x, self.y)
        plt.plot(self.x[:len(self.yf)], self.yf, color='red')

        # for cycle in self.cycles:
        #     plt.axvline(cycle.x[0], linestyle='--', color='black')

        plt.title("Sygnał z nałożonymi okresami")
        plt.xlabel("Czas [s]")
        plt.ylabel("Amplituda")
        plt.grid(True)
        plt.show()

    def plot_cycles_raw(self):
        for cycle in self.cycles:
            x = range(cycle.len)
            plt.plot(x, cycle.y, marker='o', label=f'Cycle len={cycle.len}')

        max_len = max(cycle.len for cycle in self.cycles)
        medians = []
        means = []

        for i in range(max_len):
            values_at_i = [cycle.y[i] for cycle in self.cycles if cycle.len > i]
            medians.append(np.median(values_at_i))
            means.append(np.mean(values_at_i))

        plt.plot(range(len(medians)), medians, color='red', linewidth=3, linestyle='--', label='Mediana')
        plt.plot(range(len(means)), means, color='blue', linewidth=3, linestyle='--', label='Średnia')

        plt.title("Nakładające się surowe cykle")
        plt.xlabel("Indeks w cyklu")
        plt.ylabel("Wartość")
        plt.grid(True)
        plt.legend()
        plt.show()

    def plot_cycles_approx(self):
        for cycle in self.cycles:
            x = range(cycle.len)
            plt.plot(x, cycle.yf, marker='o', label=f'Cycle len={cycle.len}')

        max_len = max(cycle.len for cycle in self.cycles)
        medians = []
        means = []

        for i in range(max_len):
            values_at_i = [cycle.yf[i] for cycle in self.cycles if cycle.len > i]
            medians.append(np.median(values_at_i))
            means.append(np.mean(values_at_i))

        plt.plot(range(len(medians)), medians, color='red', linewidth=6, linestyle='--', label='Mediana')
        plt.plot(range(len(means)), means, color='blue', linewidth=6, linestyle='--', label='Średnia')

        plt.title("Nakładające się cykle aproksymowane")
        plt.xlabel("Indeks w cyklu")
        plt.ylabel("Wartość")
        plt.grid(True)
        plt.legend()
        plt.show()

    def find_approx_cycle(self):
        max_len = self.cycles[0].len

        for i in self.cycles:
            max_len = max(max_len, i.len)

        median = []
        mean = []

        for i in range(max_len):
            vals = []

            for j in range(len(self.cycles)):
                if len(self.cycles.x) > i:
                    vals.append(self.cycles[j].y[i])

            median.append(np.median(vals))
            mean.append(np.mean(vals))

        return [Cycle(range(max_len), median), Cycle(range(max_len), mean)]
    
    def extend(self, signal: 'PeriodicSignal'):
        self.x = np.concatenate((self.x, signal.x))
        self.y = np.concatenate((self.y, signal.y))
        self.yf = np.concatenate((self.yf, signal.yf))
        self.cycles.extend(signal.cycles)
        
        
class Cycle:
    def __init__(self, x: list, y: list, deg = 5):
        self.len = len(x)
        self.x = x
        self.y = y
        
        self.max_id = np.argmax(y)

        left_min_id = np.argmin(y[:self.max_id]) if self.max_id > 0 else 0
        right_min_id = np.argmin(y[self.max_id:]) + self.max_id if self.max_id < len(y) else self.max_id

        self.min_id = [left_min_id, right_min_id]

        self.yf, _ = polynomial_fit(self.x, self.y, 4)

    def get_indices(self, extra_indices = 0) -> Optional[list]:
        if extra_indices < 0:
            return None

        jump = (self.max_id - self.min_id[0]) / ((extra_indices / 2) + 2)
        left_indices = (i for i in range(self.min_id[0], self.max_id, int(floor(jump))))
        left_indices = left_indices[1:len(left_indices) - 1]

        jump = (self.min_id[1] - self.max_id) / ((extra_indices / 2) + 2)
        right_indices = (i for i in range(self.max_id, self.min_id[1], int(floor(jump))))
        right_indices = right_indices[1:len(right_indices) - 1]

        indices = [self.min_id[0]]
        for i in left_indices:
            indices.append(i)
        indices.append(self.max_id)
        for i in right_indices:
            indices.append(i)
        indices.append(self.min_id[1])

        return indices
