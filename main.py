import numpy as np
import matplotlib.pyplot as plt
import time
import sys
from scipy.signal import find_peaks, peak_widths
from scipy.io.wavfile import write
import random
import sounddevice as sd
import soundfile as sf
import datetime

fs = 44100  # frequency
chno = 2  # no of channels
duration = 2
f = 440.0  # sine freq


def rem_empty(wave):
    temp = []
    for a in wave:
        if np.sum(a) != 0.0 or np.sum(a) != -0.0:
            temp.append(a)
    # print(temp[0])
    return np.array(temp)


def rem_empty_2(wave):
    return np.array([x for x in wave if x != 0.0])


# p = [[-0., -0.], [-0., -0.], [-0., -0.], [-0.00051845, -0.00051845],
#      [-0.00040478, -0.00040478], [-0.00033682, -0.00033682]]

# print(rem_empty(p))


def gen_wave(test=0):
    if test == 1:
        new_f = f + 22 % 10
    if test == 2:
        new_f = f + 23 % 10
    else:
        now = datetime.datetime.now()
        new_f = f + now.hour % 10
    created_wave = (np.sin(2 * np.pi * np.arange(fs * 1) * new_f / fs)).astype(
        np.float32)
    write('gen.wav', fs, created_wave)
    return created_wave


def open_wav():
    data, fs = sf.read("gen.wav", dtype='float32')
    return rem_empty(data)


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


def wave_peaker(data, fn):
    print(data)
    plt.plot(data)
    plt.xlim(0, 1500)
    # plt.ylim(0.005, -0.005)
    plt.savefig("{}.png".format(fn))


# Using a difference threshold and counting q of peaks
def comparison_fast(data1, data2):
    len1 = len(data1)
    comp = rem_empty_2(data1) - rem_empty_2(data2)

    comp = np.array([int(x) for x in comp])
    print(comp)
    comp = np.array([x for x in comp if x == 0])
    print("error within the range of {} frames".format(len1 - len(comp)))


def main_without_record_gen():
    data1 = open_wav()
    print("[INFO] opened wave")
    data2 = gen_wave(2)
    print("[INFO] generated wave")
    wave_peaker(data1, "open_peak")
    print("[INFO] Wave 1 peak")
    wave_peaker(data2, "gen_peak")
    print("[INFO] Wave 2 peak")
    comparison_fast(data1, data2)
    print("[INFO] Comparison done")

main_without_record_gen()
