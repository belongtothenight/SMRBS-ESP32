from cProfile import label
import pyaudio
import wave
import math
import array
import numpy as np
from os import system
from os.path import join
from matplotlib import pyplot as plt
from time import sleep
from pixel_ring import pixel_ring
from gpiozero import LED

# <<parameters>>
RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 8
RESPEAKER_WIDTH = 2
RESPEAKER_INDEX = 2  # refer to input device id # run getDeviceInfo.py to get index

rep_cnt = 100   # repeat count of same setting while gathering data
samp_dp = 20    # sample to drop at the beginning of each run
samp_ds = 2000  # sample = sample / samp_ds (sample_downsize)
chunk = 100     # number of samples to read from stream
alpha = 0.99    # power estimation coefficient

IMG_PATH = '/home/pi/code/alg_test5/'
IMG_NAME = 'alpha.png'

PLOT_P = False  # plot power of each measurement # if TOTAL_PIC>10 it is going to take forever
PLOT_D = False  # plot decision of microphone
PLOT_T = True   # plot trend of decision

MIN = 0.9  # testing parameter minimum
MAX = 0.99  # testing parameter maximum
INC = 0.01  # testing parameter increment
testing_range = np.round(np.arange(MIN, MAX, INC).tolist(), 2)
testing_length = len(testing_range)

# <<module>>


class PE():
    def __init__(self, repcnt=rep_cnt, sampdp=samp_dp, sampds=samp_ds, chunk_=chunk, alpha_=alpha):
        # PARAM
        self.rep_cnt = repcnt
        self.samp_dp = sampdp
        self.samp_ds = sampds
        self.chunk = chunk_
        self.alpha = alpha_
        # LED
        self.power = LED(5)
        self.power.on()
        pixel_ring.set_brightness(10)
        pixel_ring.wakeup()
        # MIC
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            rate=RESPEAKER_RATE,
            format=self.p.get_format_from_width(RESPEAKER_WIDTH),
            channels=RESPEAKER_CHANNELS,
            input=True,
            input_device_index=RESPEAKER_INDEX,)
        pixel_ring.off()
        print('PE initialized')

    def read_6ch_data(self, pf=False):
        # pf: print flag
        data = self.stream.read(self.chunk, exception_on_overflow=True)
        # byte to list
        t = np.frombuffer(data, dtype=np.int16)[0::8]
        self.d1 = array.array('h')
        self.d1.frombytes(b''.join(t))
        self.d1 = list(self.d1)
        t = np.frombuffer(data, dtype=np.int16)[1::8]
        self.d2 = array.array('h')
        self.d2.frombytes(b''.join(t))
        self.d2 = list(self.d2)
        t = np.frombuffer(data, dtype=np.int16)[2::8]
        self.d3 = array.array('h')
        self.d3.frombytes(b''.join(t))
        self.d3 = list(self.d3)
        t = np.frombuffer(data, dtype=np.int16)[3::8]
        self.d4 = array.array('h')
        self.d4.frombytes(b''.join(t))
        self.d4 = list(self.d4)
        t = np.frombuffer(data, dtype=np.int16)[4::8]
        self.d5 = array.array('h')
        self.d5.frombytes(b''.join(t))
        self.d5 = list(self.d5)
        t = np.frombuffer(data, dtype=np.int16)[5::8]
        self.d6 = array.array('h')
        self.d6.frombytes(b''.join(t))
        self.d6 = list(self.d6)
        t = np.frombuffer(data, dtype=np.int16)[6::8]
        self.d7 = array.array('h')
        self.d7.frombytes(b''.join(t))
        self.d7 = list(self.d7)
        t = np.frombuffer(data, dtype=np.int16)[7::8]
        self.d8 = array.array('h')
        self.d8.frombytes(b''.join(t))
        self.d8 = list(self.d8)
        # drop first few samples
        self.d1 = self.d1[self.samp_dp:]
        self.d2 = self.d2[self.samp_dp:]
        self.d3 = self.d3[self.samp_dp:]
        self.d4 = self.d4[self.samp_dp:]
        self.d5 = self.d5[self.samp_dp:]
        self.d6 = self.d6[self.samp_dp:]
        self.d7 = self.d7[self.samp_dp:]
        self.d8 = self.d8[self.samp_dp:]
        # downsize samples
        self.d1 = [x/self.samp_ds for x in self.d1]
        self.d2 = [x/self.samp_ds for x in self.d2]
        self.d3 = [x/self.samp_ds for x in self.d3]
        self.d4 = [x/self.samp_ds for x in self.d4]
        self.d5 = [x/self.samp_ds for x in self.d5]
        self.d6 = [x/self.samp_ds for x in self.d6]
        self.d7 = [x/self.samp_ds for x in self.d7]
        self.d8 = [x/self.samp_ds for x in self.d8]
        # print
        if pf:
            print(self.d1)
            print(self.d2)
            print(self.d3)
            print(self.d4)
            print(self.d5)
            print(self.d6)
            print(self.d7)
            print(self.d8)

    def cal_pow(self, pf=False):
        self.p1 = [x**2 for x in self.d1]
        self.p2 = [x**2 for x in self.d2]
        self.p3 = [x**2 for x in self.d3]
        self.p4 = [x**2 for x in self.d4]
        self.p5 = [x**2 for x in self.d5]
        self.p6 = [x**2 for x in self.d6]
        self.p7 = [x**2 for x in self.d7]
        self.p8 = [x**2 for x in self.d8]
        if pf:
            print(self.p1)
            print(self.p2)
            print(self.p3)
            print(self.p4)
            print(self.p5)
            print(self.p6)
            print(self.p7)
            print(self.p8)

    def pe1(self, pf=False):
        pass

    def cal_st(self):
        # calculate statatistics
        pass

    def plt_s(self, cl=False):
        # signal
        if cl:
            plt.clf()
        plt.title('signal')
        plt.xlabel('Sample')
        plt.ylabel('V (scaled)')
        plt.axhline(0, color='black')
        plt.axvline(0, color='black')
        l1 = plt.plot(self.d1, label='ch1')
        l2 = plt.plot(self.d2, label='ch2')
        l3 = plt.plot(self.d3, label='ch3')
        l4 = plt.plot(self.d4, label='ch4')
        l5 = plt.plot(self.d5, label='ch5')
        l6 = plt.plot(self.d6, label='ch6')
        l7 = plt.plot(self.d7, label='ch7')
        l8 = plt.plot(self.d8, label='ch8')
        plt.legend()
        plt.show()

    def plt_p(self, cl=False):
        # power
        if cl:
            plt.clf()
        plt.title('power')
        plt.xlabel('Sample')
        plt.ylabel('V (scaled)')
        plt.axhline(0, color='black')
        plt.axvline(0, color='black')
        l1 = plt.plot(self.p1, label='ch1')
        l2 = plt.plot(self.p2, label='ch2')
        l3 = plt.plot(self.p3, label='ch3')
        l4 = plt.plot(self.p4, label='ch4')
        l5 = plt.plot(self.p5, label='ch5')
        l6 = plt.plot(self.p6, label='ch6')
        l7 = plt.plot(self.p7, label='ch7')
        l8 = plt.plot(self.p8, label='ch8')
        plt.legend()
        plt.show()

    def plt_dc(self, cl=False):
        # decision
        pass

    def plt_cb1(self, cl=False):
        # combined: s+p
        if cl:
            plt.clf()
        plt.title('signal + power')
        plt.xlabel('Sample')
        plt.ylabel('V/W (scaled)')
        plt.axhline(0, color='black')
        plt.axvline(0, color='black')
        l1 = plt.plot(self.d1, label='signal')
        l2 = plt.plot(self.p1, label='power')
        plt.legend()
        plt.show()

    def plt_cb2(self, cl=False):
        # combined: v+p+pe1+dc
        pass


# <<main>>
if __name__ == '__main__':
    pe = PE(chunk_=500)
    pe.read_6ch_data()
    pe.cal_pow()
    pe.plt_cb1()
