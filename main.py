import numpy as np
import matplotlib.pyplot as plt
import time
import sys
from scipy.signal import find_peaks, peak_widths
from scipy.io.wavfile import write
import random
import sounddevice as sd
import datetime

fs = 44100  # frequency
chno = 2  # no of channels
duration = 2
f = 440.0 # sine freq


def rem_empty(wave):
    temp = []
    for a in wave:
        if np.sum(a) != 0.0 or np.sum(a) != -0.0:
            temp.append(a)
    # print(temp[0])
    return np.array(temp)


# p = [[-0., -0.], [-0., -0.], [-0., -0.], [-0.00051845, -0.00051845],
#      [-0.00040478, -0.00040478], [-0.00033682, -0.00033682]]

# print(rem_empty(p))


def gen_wave():
    now = datetime.datetime.now()
    new_f = f+now.hour%10
    created_wave = (np.sin(2*np.pi*np.arange(fs*1)*new_f/fs)).astype(np.float32)
    write('gen.wav', fs, created_wave)


# gen_wave()


def recorder():

    # time.sleep(.5)
    print("Play sound")

    recorded = sd.rec(int(duration * fs), samplerate=fs, channels=chno)
    time.sleep(duration)
    # with open("wave.txt", "w+") as f:
    #     f.write(str(recorded))
    # print(rem_empty(recorded))
    fin_wave = rem_empty(recorded)

    write('test.wav', fs, fin_wave)
    return fin_wave


# recorder()


def wave_peaker(data):
    peaks, _ = find_peaks(data)
    widths_all = peak_widths(data, peaks)

    plt.plot(peaks, "x")
    plt.xlim(0, 1500)
    # plt.ylim(0.005, -0.005)
    plt.savefig("peakers.png")
    return [peaks, widths_all]


# Using a difference threshold and counting q of peaks
def comparison_fast(data1, data2):
    flag = 0
    p1, w1 = wave_peaker(data1)
    p2, w2 = wave_peaker(data2)

    for p in [p1, p2, w1, w2]:
        p = np.array(p)

    peak_sub = p1 - p2
    width_sub = w1 - w2

    # no of peaks

    lenp1 = len(p1)
    lenp2 = len(p2)

    if (lenp1 >= lenp2 + 3 and lenp1 <= lenp2 - 3):
        flag = 1
    else:
        flag = 0

    # difference

    peak_sub = [x < threshold_comp for x in peak_sub]
    # width_sub = [x<threshold_comp for x in width_sub]
