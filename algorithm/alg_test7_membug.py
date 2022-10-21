from cProfile import label
from importlib.resources import path
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

'''
1. Parameter testing.
2. Testing code based on "alg_test5_alpha.py".
3. Add LED control.
'''
'''
1. test store_data()
2. test param_test()
'''

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

IMG_PATH = '/home/pi/code/alg_test7/'

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
    '''------PE core------'''

    def __init__(self, repcnt=rep_cnt, sampdp=samp_dp, sampds=samp_ds, chunk_=chunk, alpha_=alpha):
        # PARAM
        self.rep_cnt = repcnt
        self.samp_dp = sampdp
        self.samp_ds = sampds
        self.chunk = chunk_
        self.alpha = alpha_
        # MEM
        self.mem_d1 = []
        self.mem_d2 = []
        self.mem_d3 = []
        self.mem_d4 = []
        self.mem_d5 = []
        self.mem_d6 = []
        self.mem_p1 = []
        self.mem_p2 = []
        self.mem_p3 = []
        self.mem_p4 = []
        self.mem_p5 = []
        self.mem_p6 = []
        self.mem_pe11 = []
        self.mem_pe12 = []
        self.mem_pe13 = []
        self.mem_pe14 = []
        self.mem_pe15 = []
        self.mem_pe16 = []
        self.mem_d1avg = []
        self.mem_d2avg = []
        self.mem_d3avg = []
        self.mem_d4avg = []
        self.mem_d5avg = []
        self.mem_d6avg = []
        self.mem_p1avg = []
        self.mem_p2avg = []
        self.mem_p3avg = []
        self.mem_p4avg = []
        self.mem_p5avg = []
        self.mem_p6avg = []
        self.mem_pe11avg = []
        self.mem_pe12avg = []
        self.mem_pe13avg = []
        self.mem_pe14avg = []
        self.mem_pe15avg = []
        self.mem_pe16avg = []
        self.mem_max_ch = []
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

    def terminate(self):
        # LED
        pixel_ring.off()
        self.power.off()
        # MIC
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        print('PE terminated')

    def read_data(self, pf=False):
        # pf: print flag
        data = self.stream.read(self.chunk, exception_on_overflow=False)
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
        self.d1avg = sum(self.d1) / len(self.d1)
        self.d2avg = sum(self.d2) / len(self.d2)
        self.d3avg = sum(self.d3) / len(self.d3)
        self.d4avg = sum(self.d4) / len(self.d4)
        self.d5avg = sum(self.d5) / len(self.d5)
        self.d6avg = sum(self.d6) / len(self.d6)
        self.d7avg = sum(self.d7) / len(self.d7)
        self.d8avg = sum(self.d8) / len(self.d8)
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

    def pow(self, pf=False):
        self.p1 = [x**2 for x in self.d1]
        self.p2 = [x**2 for x in self.d2]
        self.p3 = [x**2 for x in self.d3]
        self.p4 = [x**2 for x in self.d4]
        self.p5 = [x**2 for x in self.d5]
        self.p6 = [x**2 for x in self.d6]
        self.p7 = [x**2 for x in self.d7]
        self.p8 = [x**2 for x in self.d8]
        self.p1avg = sum(self.p1)/len(self.p1)
        self.p2avg = sum(self.p2)/len(self.p2)
        self.p3avg = sum(self.p3)/len(self.p3)
        self.p4avg = sum(self.p4)/len(self.p4)
        self.p5avg = sum(self.p5)/len(self.p5)
        self.p6avg = sum(self.p6)/len(self.p6)
        self.p7avg = sum(self.p7)/len(self.p7)
        self.p8avg = sum(self.p8)/len(self.p8)
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
        self.pe11 = []
        self.pe11.append(0)
        self.pe12 = []
        self.pe12.append(0)
        self.pe13 = []
        self.pe13.append(0)
        self.pe14 = []
        self.pe14.append(0)
        self.pe15 = []
        self.pe15.append(0)
        self.pe16 = []
        self.pe16.append(0)
        self.pe17 = []
        self.pe17.append(0)
        self.pe18 = []
        self.pe18.append(0)
        for i in range(self.chunk - self.samp_dp):
            self.pe11.append(
                self.alpha*self.pe11[i] + (1-self.alpha)*self.p1[i])
            self.pe12.append(
                self.alpha*self.pe12[i] + (1-self.alpha)*self.p2[i])
            self.pe13.append(
                self.alpha*self.pe13[i] + (1-self.alpha)*self.p3[i])
            self.pe14.append(
                self.alpha*self.pe14[i] + (1-self.alpha)*self.p4[i])
            self.pe15.append(
                self.alpha*self.pe15[i] + (1-self.alpha)*self.p5[i])
            self.pe16.append(
                self.alpha*self.pe16[i] + (1-self.alpha)*self.p6[i])
            self.pe17.append(
                self.alpha*self.pe17[i] + (1-self.alpha)*self.p7[i])
            self.pe18.append(
                self.alpha*self.pe18[i] + (1-self.alpha)*self.p8[i])
        self.pe11avg = sum(self.pe11)/len(self.pe11)
        self.pe12avg = sum(self.pe12)/len(self.pe12)
        self.pe13avg = sum(self.pe13)/len(self.pe13)
        self.pe14avg = sum(self.pe14)/len(self.pe14)
        self.pe15avg = sum(self.pe15)/len(self.pe15)
        self.pe16avg = sum(self.pe16)/len(self.pe16)
        self.pe17avg = sum(self.pe17)/len(self.pe17)
        self.pe18avg = sum(self.pe18)/len(self.pe18)

    def dc1(self, led=False):
        index_max = np.argmax([self.pe11[-1], self.pe12[-1], self.pe13[-1],
                              self.pe14[-1], self.pe15[-1], self.pe16[-1]])
        self.max_ch = index_max + 1
        if led:
            if self.max_ch == 1:
                pixel_ring.open1()
            elif self.max_ch == 2:
                pixel_ring.open2()
            elif self.max_ch == 3:
                pixel_ring.open3()
            elif self.max_ch == 4:
                pixel_ring.open4()
            elif self.max_ch == 5:
                pixel_ring.open5()
            else:
                pixel_ring.open6()

    def cal_st(self):
        # calculate statatistics
        pass

    def store_data(self):
        # store data in memory
        self.mem_d1.append(self.d1)
        self.mem_d2.append(self.d2)
        self.mem_d3.append(self.d3)
        self.mem_d4.append(self.d4)
        self.mem_d5.append(self.d5)
        self.mem_d6.append(self.d6)
        self.mem_p1.append(self.p1)
        self.mem_p2.append(self.p2)
        self.mem_p3.append(self.p3)
        self.mem_p4.append(self.p4)
        self.mem_p5.append(self.p5)
        self.mem_p6.append(self.p6)
        self.mem_pe11.append(self.pe11)
        self.mem_pe12.append(self.pe12)
        self.mem_pe13.append(self.pe13)
        self.mem_pe14.append(self.pe14)
        self.mem_pe15.append(self.pe15)
        self.mem_pe16.append(self.pe16)
        self.mem_d1avg.append(self.d1avg)
        self.mem_d2avg.append(self.d2avg)
        self.mem_d3avg.append(self.d3avg)
        self.mem_d4avg.append(self.d4avg)
        self.mem_d5avg.append(self.d5avg)
        self.mem_d6avg.append(self.d6avg)
        self.mem_p1avg.append(self.p1avg)
        self.mem_p2avg.append(self.p2avg)
        self.mem_p3avg.append(self.p3avg)
        self.mem_p4avg.append(self.p4avg)
        self.mem_p5avg.append(self.p5avg)
        self.mem_p6avg.append(self.p6avg)
        self.mem_pe11avg.append(self.pe11avg)
        self.mem_pe12avg.append(self.pe12avg)
        self.mem_pe13avg.append(self.pe13avg)
        self.mem_pe14avg.append(self.pe14avg)
        self.mem_pe15avg.append(self.pe15avg)
        self.mem_pe16avg.append(self.pe16avg)
        self.mem_max_ch.append(self.max_ch)

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
        # l7 = plt.plot(self.d7, label='ch7')
        # l8 = plt.plot(self.d8, label='ch8')
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
        # l7 = plt.plot(self.p7, label='ch7')
        # l8 = plt.plot(self.p8, label='ch8')
        plt.legend()
        plt.show()

    def plt_pe1(self, cl=False):
        # power estimation 1
        if cl:
            plt.clf()
        plt.title('power')
        plt.xlabel('Sample')
        plt.ylabel('V (scaled)')
        plt.axhline(0, color='black')
        plt.axvline(0, color='black')
        l1 = plt.plot(self.pe11, label='ch1')
        l2 = plt.plot(self.pe12, label='ch2')
        l3 = plt.plot(self.pe13, label='ch3')
        l4 = plt.plot(self.pe14, label='ch4')
        l5 = plt.plot(self.pe15, label='ch5')
        l6 = plt.plot(self.pe16, label='ch6')
        # l7 = plt.plot(self.pe17, label='ch7')
        # l8 = plt.plot(self.pe18, label='ch8')
        plt.legend()
        plt.show()

    def plt_cb11(self, cl=False):
        # combined: s+p
        if cl:
            plt.clf()
        fig, axs = plt.subplots(2, 3, figsize=(10, 4))
        fig.suptitle('signal + power')
        fig.tight_layout(pad=0.3)
        axs[0, 0].set_title('ch1')
        axs[0, 0].set_xlabel('Sample')
        axs[0, 0].set_ylabel('V/W (scaled)')
        axs[0, 0].axhline(0, color='black')
        axs[0, 0].axvline(0, color='black')
        axs[0, 0].axhline(self.p1avg, color='red',
                          label='savg={0:.2f}'.format(self.d1avg))
        axs[0, 0].axhline(self.p1avg, color='purple',
                          label='pavg={0:.2f}'.format(self.p1avg))
        axs[0, 0].plot(self.d1, label='signal')
        axs[0, 0].plot(self.p1, label='power')
        axs[0, 0].legend()
        axs[0, 1].set_title('ch2')
        axs[0, 1].set_xlabel('Sample')
        axs[0, 1].set_ylabel('V/W (scaled)')
        axs[0, 1].axhline(0, color='black')
        axs[0, 1].axvline(0, color='black')
        axs[0, 1].axhline(self.p1avg, color='red',
                          label='savg={0:.2f}'.format(self.d2avg))
        axs[0, 1].axhline(self.p1avg, color='purple',
                          label='pavg={0:.2f}'.format(self.p2avg))
        axs[0, 1].plot(self.d2, label='signal')
        axs[0, 1].plot(self.p2, label='power')
        axs[0, 1].legend()
        axs[0, 2].set_title('ch3')
        axs[0, 2].set_xlabel('Sample')
        axs[0, 2].set_ylabel('V/W (scaled)')
        axs[0, 2].axhline(0, color='black')
        axs[0, 2].axvline(0, color='black')
        axs[0, 2].axhline(self.p1avg, color='red',
                          label='savg={0:.2f}'.format(self.d3avg))
        axs[0, 2].axhline(self.p1avg, color='purple',
                          label='pavg={0:.2f}'.format(self.p3avg))
        axs[0, 2].plot(self.d3, label='signal')
        axs[0, 2].plot(self.p3, label='power')
        axs[0, 2].legend()
        axs[1, 0].set_title('ch4')
        axs[1, 0].set_xlabel('Sample')
        axs[1, 0].set_ylabel('V/W (scaled)')
        axs[1, 0].axhline(0, color='black')
        axs[1, 0].axvline(0, color='black')
        axs[1, 0].axhline(self.p1avg, color='red',
                          label='savg={0:.2f}'.format(self.d4avg))
        axs[1, 0].axhline(self.p1avg, color='purple',
                          label='pavg={0:.2f}'.format(self.p4avg))
        axs[1, 0].plot(self.d4, label='signal')
        axs[1, 0].plot(self.p4, label='power')
        axs[1, 0].legend()
        axs[1, 1].set_title('ch5')
        axs[1, 1].set_xlabel('Sample')
        axs[1, 1].set_ylabel('V/W (scaled)')
        axs[1, 1].axhline(0, color='black')
        axs[1, 1].axvline(0, color='black')
        axs[1, 1].axhline(self.p1avg, color='red',
                          label='savg={0:.2f}'.format(self.d5avg))
        axs[1, 1].axhline(self.p1avg, color='purple',
                          label='pavg={0:.2f}'.format(self.p5avg))
        axs[1, 1].plot(self.d5, label='signal')
        axs[1, 1].plot(self.p5, label='power')
        axs[1, 1].legend()
        axs[1, 2].set_title('ch6')
        axs[1, 2].set_xlabel('Sample')
        axs[1, 2].set_ylabel('V/W (scaled)')
        axs[1, 2].axhline(0, color='black')
        axs[1, 2].axvline(0, color='black')
        axs[1, 2].axhline(self.p1avg, color='red',
                          label='savg={0:.2f}'.format(self.d6avg))
        axs[1, 2].axhline(self.p1avg, color='purple',
                          label='pavg={0:.2f}'.format(self.p6avg))
        axs[1, 2].plot(self.d6, label='signal')
        axs[1, 2].plot(self.p6, label='power')
        axs[1, 2].legend()
        plt.show()

    def plt_cb12(self, cl=False, fn='', fi=0, show=False, save=True):
        # combined: v+p+pe1+dc
        if cl:
            plt.clf()
        fig, axs = plt.subplots(2, 3, figsize=(20, 10))
        fig.suptitle(
            'signal + power + power estimation =>ch{0}'.format(self.mem_max_ch[fi]))
        fig.tight_layout(pad=3, h_pad=3, w_pad=3)
        axs[0, 0].set_title('ch1 pe1={0:.2f}'.format(self.mem_pe11[-1]))
        axs[0, 0].set_xlabel('Sample')
        axs[0, 0].set_ylabel('V/W (scaled)')
        axs[0, 0].axhline(0, color='black')
        axs[0, 0].axvline(0, color='black')
        axs[0, 0].axhline(self.mem_d1avg[fi], color='red',
                          label='savg={0:.2f}'.format(self.mem_d1avg[fi]))
        axs[0, 0].axhline(self.mem_p1avg[fi], color='purple',
                          label='pavg={0:.2f}'.format(self.mem_p1avg[fi]))
        axs[0, 0].axhline(self.mem_pe11avg[fi], color='pink',
                          label='pe1avg={0:.2f}'.format(self.mem_pe11avg[fi]))
        axs[0, 0].plot(self.mem_d1[fi], label='signal')
        axs[0, 0].plot(self.mem_p1[fi], label='power')
        axs[0, 0].plot(self.mem_pe11[fi], label='pe1')
        axs[0, 0].legend()
        axs[0, 1].set_title('ch2 pe1={0:.2f}'.format(self.mem_pe12[-1]))
        axs[0, 1].set_xlabel('Sample')
        axs[0, 1].set_ylabel('V/W (scaled)')
        axs[0, 1].axhline(0, color='black')
        axs[0, 1].axvline(0, color='black')
        axs[0, 1].axhline(self.mem_d2avg[fi], color='red',
                          label='savg={0:.2f}'.format(self.mem_d2avg[fi]))
        axs[0, 1].axhline(self.mem_p2avg[fi], color='purple',
                          label='pavg={0:.2f}'.format(self.mem_p2avg[fi]))
        axs[0, 1].axhline(self.mem_pe12avg[fi], color='pink',
                          label='pe1avg={0:.2f}'.format(self.mem_pe12avg[fi]))
        axs[0, 1].plot(self.mem_d2[fi], label='signal')
        axs[0, 1].plot(self.mem_p2[fi], label='power')
        axs[0, 1].plot(self.mem_pe12[fi], label='pe1')
        axs[0, 1].legend()
        axs[0, 2].set_title('ch3 pe1={0:.2f}'.format(self.mem_pe13[-1]))
        axs[0, 2].set_xlabel('Sample')
        axs[0, 2].set_ylabel('V/W (scaled)')
        axs[0, 2].axhline(0, color='black')
        axs[0, 2].axvline(0, color='black')
        axs[0, 2].axhline(self.mem_d3avg[fi], color='red',
                          label='savg={0:.2f}'.format(self.mem_d3avg[fi]))
        axs[0, 2].axhline(self.mem_p3avg[fi], color='purple',
                          label='pavg={0:.2f}'.format(self.mem_p3avg[fi]))
        axs[0, 2].axhline(self.mem_pe13avg[fi], color='pink',
                          label='pe1avg={0:.2f}'.format(self.mem_pe13avg[fi]))
        axs[0, 2].plot(self.mem_d3[fi], label='signal')
        axs[0, 2].plot(self.mem_p3[fi], label='power')
        axs[0, 2].plot(self.mem_pe13[fi], label='pe1')
        axs[0, 2].legend()
        axs[1, 0].set_title('ch4 pe1={0:.2f}'.format(self.mem_pe14[-1]))
        axs[1, 0].set_xlabel('Sample')
        axs[1, 0].set_ylabel('V/W (scaled)')
        axs[1, 0].axhline(0, color='black')
        axs[1, 0].axvline(0, color='black')
        axs[1, 0].axhline(self.mem_d4avg[fi], color='red',
                          label='savg={0:.2f}'.format(self.mem_d4avg[fi]))
        axs[1, 0].axhline(self.mem_p4avg[fi], color='purple',
                          label='pavg={0:.2f}'.format(self.mem_p4avg[fi]))
        axs[1, 0].axhline(self.mem_pe14avg[fi], color='pink',
                          label='pe1avg={0:.2f}'.format(self.mem_pe14avg[fi]))
        axs[1, 0].plot(self.mem_d4[fi], label='signal')
        axs[1, 0].plot(self.mem_p4[fi], label='power')
        axs[1, 0].plot(self.mem_pe14[fi], label='pe1')
        axs[1, 0].legend()
        axs[1, 1].set_title('ch5 pe1={0:.2f}'.format(self.mem_pe15[-1]))
        axs[1, 1].set_xlabel('Sample')
        axs[1, 1].set_ylabel('V/W (scaled)')
        axs[1, 1].axhline(0, color='black')
        axs[1, 1].axvline(0, color='black')
        axs[1, 1].axhline(self.mem_d5avg[fi], color='red',
                          label='savg={0:.2f}'.format(self.mem_d5avg[fi]))
        axs[1, 1].axhline(self.mem_p5avg[fi], color='purple',
                          label='pavg={0:.2f}'.format(self.mem_p5avg[fi]))
        axs[1, 1].axhline(self.mem_pe15avg[fi], color='pink',
                          label='pe1avg={0:.2f}'.format(self.mem_pe15avg[fi]))
        axs[1, 1].plot(self.mem_d5[fi], label='signal')
        axs[1, 1].plot(self.mem_p5[fi], label='power')
        axs[1, 1].plot(self.mem_pe15[fi], label='pe1')
        axs[1, 1].legend()
        axs[1, 2].set_title('ch6 pe1={0:.2f}'.format(self.mem_pe16[-1]))
        axs[1, 2].set_xlabel('Sample')
        axs[1, 2].set_ylabel('V/W (scaled)')
        axs[1, 2].axhline(0, color='black')
        axs[1, 2].axvline(0, color='black')
        axs[1, 2].axhline(self.mem_d6avg[fi], color='red',
                          label='savg={0:.2f}'.format(self.mem_d6avg[fi]))
        axs[1, 2].axhline(self.mem_p6avg[fi], color='purple',
                          label='pavg={0:.2f}'.format(self.mem_p6avg[fi]))
        axs[1, 2].axhline(self.mem_pe16avg[fi], color='pink',
                          label='pe1avg={0:.2f}'.format(self.mem_pe16avg[fi]))
        axs[1, 2].plot(self.mem_d6[fi], label='signal')
        axs[1, 2].plot(self.mem_p6[fi], label='power')
        axs[1, 2].plot(self.mem_pe16[fi], label='pe1')
        axs[1, 2].legend()
        if show:
            plt.show()
        if save:
            plt.savefig(join(IMG_PATH, fn + '_{0}.png'.format(fi)), dpi=300)

    '''------PE extension------'''

    def param_test(self, param, min, max, inc):
        test_range = np.round(np.arange(min, max, inc).tolist(), 2)
        test_length = len(test_range)
        if param == 'rep_cnt':
            # getting averaged data (skip for now)
            test_range = [int(x) for x in test_range]
            for i in range(test_length):
                print('{0}/{1}'.format(i+1, test_length), end='\r')
                self.rep_cnt = test_range[i]
                self.read_data()
                self.pow()
                self.pe1()
                self.dc1(led=False)
                self.store_data()
            for i in range(test_length):
                self.plt_cb12(fn=param, fi=i+1, save=True)
        elif param == 'samp_dp':
            test_range = [int(x) for x in test_range]
            for i in range(test_length):
                print('{0}/{1}'.format(i+1, test_length), end='\r')
                self.samp_dp = test_range[i]
                self.read_data()
                self.pow()
                self.pe1()
                self.dc1(led=False)
                self.store_data()
            for i in range(test_length):
                self.plt_cb12(fn=param, fi=i+1, save=True)
        elif param == 'samp_ds':
            pass
        elif param == 'chunk':
            test_range = [int(x) for x in test_range]
            pass
        elif param == 'alpha':
            pass
        print(self.mem_max_ch)


# <<main>>


if __name__ == '__main__':
    pe = PE(chunk_=500)
    pe.param_test('samp_dp', 0, 200, 100)
    # pe.read_data()
    # pe.pow()
    # pe.pe1()
    # pe.dc1()

    # pe.plt_s()
    # pe.plt_p()
    # pe.plt_pe1()
    # pe.plt_cb11()
    # pe.plt_cb12()

    pe.terminate()
