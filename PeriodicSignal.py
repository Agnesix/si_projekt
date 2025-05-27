from math import floor

import numpy as np
from matplotlib import pyplot as plt

from approximator import find_periods, polynomial_fit

class PeriodicSignal:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.cycles = []
        self.find_cycles()

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

        self.cycles.append(Cycle(self.x[last_peak:], self.y[last_peak:]))

    def plot_signal(self):
        plt.plot(self.x, self.y)
        plt.plot(self.x, self.yf, color='red')

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

class Cycle:
    def __init__(self, x: [], y: [], deg = 5):
        self.len = len(x)
        self.x = x
        self.y = y

        self.max_id = int(np.argmax(y))

        left_min_id = int(np.argmin(y[:self.max_id])) if self.max_id > 0 else 0
        right_min_id = int(np.argmin(y[self.max_id:]) + self.max_id) if self.max_id < len(y) else self.max_id

        self.min_id = [left_min_id, right_min_id]

        self.yf, _ = polynomial_fit(self.x, self.y, deg)

    def get_indices(self, extra_indices = 0) -> None or []:
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
