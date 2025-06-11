import numpy as np
import matplotlib.pyplot as plt
from math import floor
from typing import Optional
from approximator import find_periods, interpolate

class PeriodicSignal:
    def __init__(self, x, y, detect='all', margin=6):
        self.x = x
        self.y = y
        
        self.peaks = []
        self.cycles = []
        
        if detect == 'all':
            self.find_cycles(margin=margin)
        elif detect == 'segment':
            self.find_cycles_by_segment(margin=margin)
        else:
            raise ValueError("Incorrect detection mode.")

        self.yf = []

        for cycle in self.cycles:
            for yf in cycle.yf:
                self.yf.append(yf)

    def find_cycles(self, margin=0):
        self.peaks = find_periods(self.y)

        last_peak = 0
        
        for peak in self.peaks:
            start = max(0, last_peak - margin)
            end = min(len(self.x), peak + margin)
            
            if end - start <= 2:
                continue
            
            self.cycles.append(Cycle(self.x[start:end], self.y[start:end], margin, peak - last_peak + 1))
            last_peak = peak+1
            
        if last_peak < len(self.x) - 1:
            self.cycles.append(Cycle(self.x[last_peak:], self.y[last_peak:], margin, len(self.x) - last_peak))
            
    def find_cycles_by_segment(self, margin=0):
        seg_start = 0

        while seg_start < len(self.x) - 1:
            local_y = self.y[seg_start:]
            peaks = find_periods(local_y)
            
            if len(peaks) < 1:
                break

            if len(peaks) >= 5:
                seg_end = seg_start + peaks[4]
            else:
                seg_end = seg_start + peaks[-1]

            seg_end = min(seg_end + 1, len(self.x))

            segment_y = self.y[seg_start:seg_end]
            segment_peaks = find_periods(segment_y)
            
            last_peak = seg_start
            for peak in segment_peaks:
                absolute_peak = seg_start + peak
                start = max(0, last_peak - margin)
                end = min(len(self.x), absolute_peak + margin)
                
                self.cycles.append(
                    Cycle(self.x[start:end], self.y[start:end], margin, absolute_peak - last_peak + 1)
                )
                
                last_peak = absolute_peak
                self.peaks.append(absolute_peak)

            seg_start = seg_end

    def plot_signal(self):
        plt.figure(figsize=(10,4))
        plt.plot(self.x, self.y)
        plt.plot(self.x[:len(self.yf)], self.yf, color='red')

        for peak in self.peaks:
            plt.axvline(self.x[peak], linestyle='--', color='black')

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
        
class Cycle:
    def __init__(self, x: list, y: list, margin, length):
        self.yf = interpolate(x, y)
        self.yf = self.yf[margin:length + margin]
        self.x = x[margin:length + margin]
        self.y = y[margin:length + margin]
        self.len = len(self.x)