import numpy as np
import wave
import struct
import matplotlib.pyplot as plt
import simpleaudio as sa
import time
import sounddevice as sd
from scipy.io.wavfile import write
import soundfile as sf
import pyaudio
from scipy.signal import chirp, find_peaks, peak_widths

# inits
frequency = 1000
num_samples = 48000
sampling_rate = 48000.0
amplitude = 16000
sine_wave = [
    np.sin(2 * np.pi * frequency * x / sampling_rate)
    for x in range(num_samples)
]
nframes = num_samples
comptype = "NONE"
compname = "not compressed"
nchannels = 1
sampwidth = 2

threshold_comp = .5


def create_wave():
    wav_file = wave.open("test.wav", 'w')
    wav_file.setparams((nchannels, sampwidth, int(sampling_rate), nframes,
                        comptype, compname))
    for s in sine_wave:
        wav_file.writeframes(struct.pack('h', int(s * amplitude)))

    plt.title("Original audio wave")
    plt.xlim(0, 1500)
    # plt.ylim(0.005, -0.005)
    plt.plot(sine_wave)
    plt.savefig("created_wave.png")
    plt.clf()


def plot_recorded():
    data, fs = sf.read("record.wav", dtype='float32')
    plt.title("Original audio wave")
    plt.plot(data)
    plt.xlim(0, 1500)
    plt.ylim(0.005, -0.005)
    plt.savefig("plotted_from_record.png")


def record_sound():

    fs = 48000
    seconds = 1
    print('wait for message')
    time.sleep(4)
    print('recording')
    myrecording = sd.rec(int(seconds * amplitude), samplerate=int(sampling_rate), channels=nchannels)
    sd.wait()
    write('recorded.wav', fs, myrecording)

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

    peak_sub = p1-p2
    width_sub = w1-w2

    # no of peaks

    lenp1 = len(p1)
    lenp2 = len(p2)

    if(lenp1>=lenp2+3 and lenp1<=lenp2-3):
        flag = 1
    else:
        flag = 0

    # difference

    peak_sub = [x<threshold_comp for x in peak_sub]
    # width_sub = [x<threshold_comp for x in width_sub]









