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
Add number scalling to the output of power estimation.
Prefer scale up than scale down. (computational cost)
Scale = max_value / channel_value
'''

# <<parameters>>
RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 8
RESPEAKER_WIDTH = 2
RESPEAKER_INDEX = 2  # refer to input device id # run getDeviceInfo.py to get index

# <<channel scaller>>
# SIG1_SCALE = 1.476979213
# SIG2_SCALE = 1.322764609
# SIG3_SCALE = 1.240418716
# SIG4_SCALE = 1.022989161
# SIG5_SCALE = 1.0
# SIG6_SCALE = 1.558879525
SIG1_SCALE = 1.0
SIG2_SCALE = 1.0
SIG3_SCALE = 1.0
SIG4_SCALE = 1.0
SIG5_SCALE = 1.0
SIG6_SCALE = 1.0
PE11_SCALE = 1.0
PE12_SCALE = 1.0
PE13_SCALE = 1.0
PE14_SCALE = 1.0
PE15_SCALE = 1.0
PE16_SCALE = 1.0
# PE11_SCALE = 1.2363
# PE12_SCALE = 1.1541
# PE13_SCALE = 1.0
# PE14_SCALE = 1.1009
# PE15_SCALE = 1.2657
# PE16_SCALE = 1.2044

samp_dp = 20    # sample to drop at the beginning of each run
samp_ds = 2000  # sample = sample / samp_ds (sample_downsize)
chunk = 100     # number of samples to read from stream
alpha = 0.99    # power estimation coefficient

img_path = '/home/pi/code_alg/alg/'

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
    # ==============================================================================
    # PE core

    # ====================
    # PE core/setup
    def __init__(self, sampdp=samp_dp, sampds=samp_ds, chunk_=chunk, alpha_=alpha, img_path_=img_path):
        # PARAM
        self.samp_dp = sampdp
        self.samp_ds = sampds
        self.chunk = chunk_
        self.alpha = alpha_
        self.img_path = img_path_
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
        self.mem_evaluation = []
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

    # ====================
    # PE core/gather data
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
        # drop first few samples
        self.d1 = self.d1[self.samp_dp:]
        self.d2 = self.d2[self.samp_dp:]
        self.d3 = self.d3[self.samp_dp:]
        self.d4 = self.d4[self.samp_dp:]
        self.d5 = self.d5[self.samp_dp:]
        self.d6 = self.d6[self.samp_dp:]
        # downsize samples & scale
        self.d1 = [x/self.samp_ds*SIG1_SCALE for x in self.d1]
        self.d2 = [x/self.samp_ds*SIG2_SCALE for x in self.d2]
        self.d3 = [x/self.samp_ds*SIG3_SCALE for x in self.d3]
        self.d4 = [x/self.samp_ds*SIG4_SCALE for x in self.d4]
        self.d5 = [x/self.samp_ds*SIG5_SCALE for x in self.d5]
        self.d6 = [x/self.samp_ds*SIG6_SCALE for x in self.d6]
        self.d1avg = sum(self.d1) / len(self.d1)
        self.d2avg = sum(self.d2) / len(self.d2)
        self.d3avg = sum(self.d3) / len(self.d3)
        self.d4avg = sum(self.d4) / len(self.d4)
        self.d5avg = sum(self.d5) / len(self.d5)
        self.d6avg = sum(self.d6) / len(self.d6)
        # print
        if pf:
            print(self.d1)
            print(self.d2)
            print(self.d3)
            print(self.d4)
            print(self.d5)
            print(self.d6)

    def pow(self, pf=False):
        self.p1 = [x**2 for x in self.d1]
        self.p2 = [x**2 for x in self.d2]
        self.p3 = [x**2 for x in self.d3]
        self.p4 = [x**2 for x in self.d4]
        self.p5 = [x**2 for x in self.d5]
        self.p6 = [x**2 for x in self.d6]
        # average
        self.p1avg = sum(self.p1)/len(self.p1)
        self.p2avg = sum(self.p2)/len(self.p2)
        self.p3avg = sum(self.p3)/len(self.p3)
        self.p4avg = sum(self.p4)/len(self.p4)
        self.p5avg = sum(self.p5)/len(self.p5)
        self.p6avg = sum(self.p6)/len(self.p6)
        if pf:
            print(self.p1)
            print(self.p2)
            print(self.p3)
            print(self.p4)
            print(self.p5)
            print(self.p6)

    # ====================
    # PE core/algorithm
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
        # PE1
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
        # scale
        self.pe11 = [x*PE11_SCALE for x in self.pe11]
        self.pe12 = [x*PE12_SCALE for x in self.pe12]
        self.pe13 = [x*PE13_SCALE for x in self.pe13]
        self.pe14 = [x*PE14_SCALE for x in self.pe14]
        self.pe15 = [x*PE15_SCALE for x in self.pe15]
        self.pe16 = [x*PE16_SCALE for x in self.pe16]
        # average
        self.pe11avg = sum(self.pe11)/len(self.pe11)
        self.pe12avg = sum(self.pe12)/len(self.pe12)
        self.pe13avg = sum(self.pe13)/len(self.pe13)
        self.pe14avg = sum(self.pe14)/len(self.pe14)
        self.pe15avg = sum(self.pe15)/len(self.pe15)
        self.pe16avg = sum(self.pe16)/len(self.pe16)
        # force re-run if no data is received
        if int(self.pe11[-1]) == 0:
            print('no data received')
            return True
        if int(self.pe12[-1]) == 0:
            print('no data received')
            return True
        if int(self.pe13[-1]) == 0:
            print('no data received')
            return True
        if int(self.pe14[-1]) == 0:
            print('no data received')
            return True
        if int(self.pe15[-1]) == 0:
            print('no data received')
            return True
        if int(self.pe16[-1]) == 0:
            print('no data received')
            return True

    # ====================
    # PE core/process data

    def dc1(self, led=True):
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

    def store_data(self):
        '''
        store data in memory
        '''
        # signal (list)
        self.mem_d1.append(self.d1)
        self.mem_d2.append(self.d2)
        self.mem_d3.append(self.d3)
        self.mem_d4.append(self.d4)
        self.mem_d5.append(self.d5)
        self.mem_d6.append(self.d6)
        # power (list)
        self.mem_p1.append(self.p1)
        self.mem_p2.append(self.p2)
        self.mem_p3.append(self.p3)
        self.mem_p4.append(self.p4)
        self.mem_p5.append(self.p5)
        self.mem_p6.append(self.p6)
        # power estimation (list)
        self.mem_pe11.append(self.pe11)
        self.mem_pe12.append(self.pe12)
        self.mem_pe13.append(self.pe13)
        self.mem_pe14.append(self.pe14)
        self.mem_pe15.append(self.pe15)
        self.mem_pe16.append(self.pe16)
        # signal average (float)
        self.mem_d1avg.append(self.d1avg)
        self.mem_d2avg.append(self.d2avg)
        self.mem_d3avg.append(self.d3avg)
        self.mem_d4avg.append(self.d4avg)
        self.mem_d5avg.append(self.d5avg)
        self.mem_d6avg.append(self.d6avg)
        # power average (float)
        self.mem_p1avg.append(self.p1avg)
        self.mem_p2avg.append(self.p2avg)
        self.mem_p3avg.append(self.p3avg)
        self.mem_p4avg.append(self.p4avg)
        self.mem_p5avg.append(self.p5avg)
        self.mem_p6avg.append(self.p6avg)
        # power estimation average (float)
        self.mem_pe11avg.append(self.pe11avg)
        self.mem_pe12avg.append(self.pe12avg)
        self.mem_pe13avg.append(self.pe13avg)
        self.mem_pe14avg.append(self.pe14avg)
        self.mem_pe15avg.append(self.pe15avg)
        self.mem_pe16avg.append(self.pe16avg)
        # max channel (int)
        self.mem_max_ch.append(self.max_ch)

    def clear_data(self):
        '''
        clear data in memory
        '''
        # signal (list)
        self.mem_d1 = []
        self.mem_d2 = []
        self.mem_d3 = []
        self.mem_d4 = []
        self.mem_d5 = []
        self.mem_d6 = []
        # power (list)
        self.mem_p1 = []
        self.mem_p2 = []
        self.mem_p3 = []
        self.mem_p4 = []
        self.mem_p5 = []
        self.mem_p6 = []
        # power estimation (list)
        self.mem_pe11 = []
        self.mem_pe12 = []
        self.mem_pe13 = []
        self.mem_pe14 = []
        self.mem_pe15 = []
        self.mem_pe16 = []
        # signal average (float)
        self.mem_d1avg = []
        self.mem_d2avg = []
        self.mem_d3avg = []
        self.mem_d4avg = []
        self.mem_d5avg = []
        self.mem_d6avg = []
        # power average (float)
        self.mem_p1avg = []
        self.mem_p2avg = []
        self.mem_p3avg = []
        self.mem_p4avg = []
        self.mem_p5avg = []
        self.mem_p6avg = []
        # power estimation average (float)
        self.mem_pe11avg = []
        self.mem_pe12avg = []
        self.mem_pe13avg = []
        self.mem_pe14avg = []
        self.mem_pe15avg = []
        self.mem_pe16avg = []
        # max channel (int)
        self.mem_max_ch = []
        # evaluation (list)
        self.mem_evaluation = []

    def evaluate(self, show=True):
        '''
        Evaluate the performance of power estimation.
        '''
        ch_cnt = [0, 0, 0, 0, 0, 0]
        ch_pct = [0, 0, 0, 0, 0, 0]
        ch_run = len(self.mem_max_ch)
        for i in range(6):
            ch_cnt[i] = self.mem_max_ch.count(i+1)
            ch_pct[i] = ch_cnt[i] / ch_run * 100
        self.mem_evaluation.append([
            '\nResult of power estimation',
            'ch1: {0}\t\t({1:.2f}%)'.format(ch_cnt[0], ch_pct[0]),
            'ch2: {0}\t\t({1:.2f}%)'.format(ch_cnt[1], ch_pct[1]),
            'ch3: {0}\t\t({1:.2f}%)'.format(ch_cnt[2], ch_pct[2]),
            'ch4: {0}\t\t({1:.2f}%)'.format(ch_cnt[3], ch_pct[3]),
            'ch5: {0}\t\t({1:.2f}%)'.format(ch_cnt[4], ch_pct[4]),
            'ch6: {0}\t\t({1:.2f}%)'.format(ch_cnt[5], ch_pct[5]),
        ])
        if show:
            for x in self.mem_evaluation:
                for y in x:
                    print(y)
        return ch_cnt

    # ====================
    # PE core/plot data
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
        plt.legend()
        plt.show()
        plt.close()

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
        plt.legend()
        plt.show()
        plt.close()

    def plt_pe1(self, cl=False, maxch='0', fn='', fi=-1, show=False, save=True):
        # power estimation 1
        if cl:
            plt.clf()
        plt.figure(figsize=(20, 10))
        plt.title('source: ch{0}'.format(maxch))
        plt.xlabel('Sample')
        plt.ylabel('W (scaled)')
        plt.axhline(0, color='black')
        plt.axvline(0, color='black')
        l1 = plt.plot(
            self.mem_pe11[fi], label='ch1={0:.3f}'.format(self.mem_pe11[fi][-1]))
        l2 = plt.plot(
            self.mem_pe12[fi], label='ch2={0:.3f}'.format(self.mem_pe12[fi][-1]))
        l3 = plt.plot(
            self.mem_pe13[fi], label='ch3={0:.3f}'.format(self.mem_pe13[fi][-1]))
        l4 = plt.plot(
            self.mem_pe14[fi], label='ch4={0:.3f}'.format(self.mem_pe14[fi][-1]))
        l5 = plt.plot(
            self.mem_pe15[fi], label='ch5={0:.3f}'.format(self.mem_pe15[fi][-1]))
        l6 = plt.plot(
            self.mem_pe16[fi], label='ch6={0:.3f}'.format(self.mem_pe16[fi][-1]))
        plt.legend()
        if show:
            plt.show()
        if save:
            plt.savefig('{0}pe1_ch{1}.png'.format(fn, maxch))
        plt.close()

    def plt_cb11(self, cl=False):
        '''
        x: sample
        y: s+p
        '''
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
        plt.close()

    def plt_cb12(self, cl=False, fn='', fi=0, show=False, save=True):
        '''
        x: sample
        y: v+p+pe1+dc
        '''
        if cl:
            plt.clf()
        fig, axs = plt.subplots(2, 3, figsize=(20, 10))
        fig.suptitle(
            'signal + power + power estimation =>ch{0}'.format(self.mem_max_ch[fi]))
        fig.tight_layout(pad=3, h_pad=3, w_pad=3)
        # fig (0, 0)
        axs[0, 0].set_title('ch1 pe1={0:.2f}'.format(self.mem_pe11[fi][-1]))
        axs[0, 0].set_xlabel('Sample')
        axs[0, 0].set_ylabel('V/W (scaled)')
        axs[0, 0].axhline(0, color='black')
        axs[0, 0].axvline(0, color='black')
        axs[0, 0].axhline(self.mem_d1avg[-1], color='red',
                          label='savg={0:.2f}'.format(self.mem_d1avg[fi]))
        axs[0, 0].axhline(self.mem_p1avg[-1], color='purple',
                          label='pavg={0:.2f}'.format(self.mem_p1avg[fi]))
        axs[0, 0].axhline(self.mem_pe11avg[-1], color='pink',
                          label='pe1avg={0:.2f}'.format(self.mem_pe11avg[fi]))
        axs[0, 0].plot(self.mem_d1[fi], label='signal')
        axs[0, 0].plot(self.mem_p1[fi], label='power')
        axs[0, 0].plot(self.mem_pe11[fi], label='pe1')
        axs[0, 0].legend()
        # fig (0, 1)
        axs[0, 1].set_title('ch2 pe1={0:.2f}'.format(self.mem_pe12[fi][-1]))
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
        # fig (0, 2)
        axs[0, 2].set_title('ch3 pe1={0:.2f}'.format(self.mem_pe13[fi][-1]))
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
        # fig (1, 0)
        axs[1, 0].set_title('ch4 pe1={0:.2f}'.format(self.mem_pe14[fi][-1]))
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
        # fig (1, 1)
        axs[1, 1].set_title('ch5 pe1={0:.2f}'.format(self.mem_pe15[fi][-1]))
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
        # fig (1, 2)
        axs[1, 2].set_title('ch6 pe1={0:.2f}'.format(self.mem_pe16[fi][-1]))
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
            plt.savefig(join(self.img_path, fn +
                        '_{0}.png'.format(fi+1)), dpi=300)
        plt.close()

    def plt_cb13(self, xtick, cl=False, fn='', show=False, save=True):
        '''
        x: runs
        y: davg, pavg, pe1avg, pe1[-1], max_ch
        '''
        if cl:
            plt.clf()
        fig, axs = plt.subplots(2, 3, figsize=(20, 10))
        fig.suptitle('param_test: {0}, from {1} to {2}, {3} runs'.format(
            fn, xtick[0], xtick[-1], len(xtick)))
        fig.tight_layout(pad=3, h_pad=3, w_pad=3)
        # fig (0, 0)
        axs[0, 0].set_title('averaged signal')
        axs[0, 0].set_xlabel('Run with different parameters')
        axs[0, 0].set_ylabel('V (scaled)')
        axs[0, 0].axhline(0, color='black')
        axs[0, 0].axvline(0, color='black')
        axs[0, 0].plot(self.mem_d1avg, label='d1avg')
        axs[0, 0].plot(self.mem_d2avg, label='d2avg')
        axs[0, 0].plot(self.mem_d3avg, label='d3avg')
        axs[0, 0].plot(self.mem_d4avg, label='d4avg')
        axs[0, 0].plot(self.mem_d5avg, label='d5avg')
        axs[0, 0].plot(self.mem_d6avg, label='d6avg')
        axs[0, 0].legend()
        # fig (0, 1)
        axs[0, 1].set_title('averaged power')
        axs[0, 1].set_xlabel('Run with different parameters')
        axs[0, 1].set_ylabel('W (scaled)')
        axs[0, 1].axhline(0, color='black')
        axs[0, 1].axvline(0, color='black')
        axs[0, 1].plot(self.mem_p1avg, label='p1avg')
        axs[0, 1].plot(self.mem_p2avg, label='p2avg')
        axs[0, 1].plot(self.mem_p3avg, label='p3avg')
        axs[0, 1].plot(self.mem_p4avg, label='p4avg')
        axs[0, 1].plot(self.mem_p5avg, label='p5avg')
        axs[0, 1].plot(self.mem_p6avg, label='p6avg')
        axs[0, 1].legend()
        # fig (0, 2)
        axs[0, 2].set_title('averaged power estimation')
        axs[0, 2].set_xlabel('Run with different parameters')
        axs[0, 2].set_ylabel('W (scaled)')
        axs[0, 2].axhline(0, color='black')
        axs[0, 2].axvline(0, color='black')
        axs[0, 2].plot(self.mem_pe11avg, label='pe11avg')
        axs[0, 2].plot(self.mem_pe12avg, label='pe12avg')
        axs[0, 2].plot(self.mem_pe13avg, label='pe13avg')
        axs[0, 2].plot(self.mem_pe14avg, label='pe14avg')
        axs[0, 2].plot(self.mem_pe15avg, label='pe15avg')
        axs[0, 2].plot(self.mem_pe16avg, label='pe16avg')
        axs[0, 2].legend()
        # fig (1, 0)
        lpe11 = []
        lpe12 = []
        lpe13 = []
        lpe14 = []
        lpe15 = []
        lpe16 = []
        for i in range(len(self.mem_pe11)):
            lpe11.append(self.mem_pe11[i][-1])
            lpe12.append(self.mem_pe12[i][-1])
            lpe13.append(self.mem_pe13[i][-1])
            lpe14.append(self.mem_pe14[i][-1])
            lpe15.append(self.mem_pe15[i][-1])
            lpe16.append(self.mem_pe16[i][-1])
        axs[1, 0].set_title('power estimation')
        axs[1, 0].set_xlabel('Run with different parameters')
        axs[1, 0].set_ylabel('W (scaled)')
        axs[1, 0].axhline(0, color='black')
        axs[1, 0].axvline(0, color='black')
        axs[1, 0].plot(lpe11, label='pe11')
        axs[1, 0].plot(lpe12, label='pe12')
        axs[1, 0].plot(lpe13, label='pe13')
        axs[1, 0].plot(lpe14, label='pe14')
        axs[1, 0].plot(lpe15, label='pe15')
        axs[1, 0].plot(lpe16, label='pe16')
        axs[1, 0].legend()
        # fig (1, 1)
        axs[1, 1].set_title('max channel')
        axs[1, 1].set_xlabel('Run with different parameters')
        axs[1, 1].set_ylabel('Channel')
        axs[1, 1].axhline(0, color='black')
        axs[1, 1].axvline(0, color='black')
        axs[1, 1].bar([1, 2, 3, 4, 5, 6], self.evaluate(False))
        # fig (1, 2)
        axs[1, 2].set_title('power estimation in detail')
        axs[1, 2].set_xlabel('Samples')
        axs[1, 2].set_ylabel('W (scaled)')
        axs[1, 2].axhline(0, color='black')
        axs[1, 2].axvline(0, color='black')
        for i in range(len(self.mem_pe11)):
            axs[1, 2].plot(self.mem_pe11[i], label='pe11_{0}'.format(i+1))
            axs[1, 2].plot(self.mem_pe12[i], label='pe12_{0}'.format(i+1))
            axs[1, 2].plot(self.mem_pe13[i], label='pe13_{0}'.format(i+1))
            axs[1, 2].plot(self.mem_pe14[i], label='pe14_{0}'.format(i+1))
            axs[1, 2].plot(self.mem_pe15[i], label='pe15_{0}'.format(i+1))
            axs[1, 2].plot(self.mem_pe16[i], label='pe16_{0}'.format(i+1))

        # xticks
        plt.sca(axs[0, 0])
        plt.xticks(range(len(xtick)), xtick)
        plt.sca(axs[0, 1])
        plt.xticks(range(len(xtick)), xtick)
        plt.sca(axs[0, 2])
        plt.xticks(range(len(xtick)), xtick)
        plt.sca(axs[1, 0])
        plt.xticks(range(len(xtick)), xtick)
        plt.sca(axs[1, 1])
        plt.xticks(range(1, 7), ['ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6'])
        if show:
            plt.show()
        if save:
            plt.savefig(join(self.img_path, fn + '.png'), dpi=300)
        plt.close()

    # =========================================================================
    # PE extension
    def continuous_run(self, times, plot=False):
        '''
        Continuous perform power estimation with same set of parameters.
        '''
        print('start continuous run')
        # self.samp_dp =
        # self.samp_ds =
        # self.chunk =
        # self.alpha =

        for i in range(times):
            print('{0}/{1}'.format(i+1, times), end='\r')
            while True:
                # loop run to make sure getting data
                self.read_data()
                self.pow()
                if self.pe1():
                    i -= 1
                    continue
                else:
                    break
            self.dc1()
            self.store_data()
        print('\nend continuous run')
        if plot:
            print('start plotting')
            for i in range(times):
                print('{0}/{1}'.format(i+1, times), end='\r')
                self.plt_cb12(fn='conti', fi=i, save=True)
            print('\nend plotting')

    def run_forever(self):
        '''
        Run forever.
        '''
        print('start run forever')
        while True:
            self.read_data()
            self.pow()
            self.pe1()
            self.dc1()

    def param_test1(self, param, min, max, inc, plot=True):
        '''
        Do power estimation with different set of parameters.
        '''

        def runs():
            self.read_data()
            self.pow()
            self.pe1()
            self.dc1()
            self.store_data()
            pass
        self.clear_data()
        print('Start parameter test')
        test_range = np.round(np.arange(min, max, inc).tolist(), 2)
        test_length = len(test_range)
        if param == 'samp_dp':
            test_range = [int(x) for x in test_range]
            print('start testing samp_dp')
            for i in range(test_length):
                print('{0}/{1}'.format(i+1, test_length), end='\r')
                self.samp_dp = test_range[i]
                runs()
            print('\nend testing samp_dp')
        elif param == 'samp_ds':
            print('start testing samp_ds')
            for i in range(test_length):
                print('{0}/{1}'.format(i+1, test_length), end='\r')
                self.samp_ds = test_range[i]
                runs()
            print('\nend testing samp_ds')
        elif param == 'chunk':
            test_range = [int(x) for x in test_range]
            print('start testing chunk')
            for i in range(test_length):
                print('{0}/{1}'.format(i+1, test_length), end='\r')
                self.chunk = test_range[i]
                runs()
            print('\nend testing chunk')
        elif param == 'alpha':
            print('start testing alpha')
            for i in range(test_length):
                print('{0}/{1}'.format(i+1, test_length), end='\r')
                self.alpha = test_range[i]
                runs()
            print('\nend testing alpha')
        if plot:
            print('start plotting {0}'.format(param))
            self.plt_cb13(test_range, fn=param, save=True)
            print('end plotting {0}'.format(param))
        print('End parameter test')

    def param_test2(self, param, min, max, inc, plot=True):
        '''
        Do power estimation with different set of parameters.
        '''

        def runs():
            self.read_data()
            self.pow()
            self.pe1()
            self.dc1()
            self.store_data()
            pass
        self.clear_data()
        print('Start parameter test')
        test_range = np.round(np.arange(min, max, inc).tolist(), 2)
        test_length = len(test_range)
        if param == 'samp_dp':
            test_range = [int(x) for x in test_range]
            print('start testing samp_dp')
            for i in range(test_length):
                print('{0}/{1}'.format(i+1, test_length), end='\r')
                self.samp_dp = test_range[i]
                runs()
            print('\nend testing samp_dp')
        elif param == 'samp_ds':
            print('start testing samp_ds')
            for i in range(test_length):
                print('{0}/{1}'.format(i+1, test_length), end='\r')
                self.samp_ds = test_range[i]
                runs()
            print('\nend testing samp_ds')
        elif param == 'chunk':
            test_range = [int(x) for x in test_range]
            print('start testing chunk')
            for i in range(test_length):
                print('{0}/{1}'.format(i+1, test_length), end='\r')
                self.chunk = test_range[i]
                runs()
            print('\nend testing chunk')
        elif param == 'alpha':
            print('start testing alpha')
            for i in range(test_length):
                print('{0}/{1}'.format(i+1, test_length), end='\r')
                self.alpha = test_range[i]
                runs()
            print('\nend testing alpha')
        if plot:
            print('start plotting {0}'.format(param))
            self.plt_cb13(test_range, fn=param, save=True)
            print('end plotting {0}'.format(param))
        print('End parameter test')


# <<main>>


if __name__ == '__main__':
    pe = PE(chunk_=300)
    runs = int(input("How many times do you want to detect? "))
    pe.continuous_run(runs, plot=False)
    pe.evaluate()
    pe.terminate()

'''
# sample code
pe = PE(chunk_=500)
    # >>>>> testing parameters
    pe.param_test1('samp_dp', 0, 100, 5)
    pe.param_test1('samp_ds', 1500, 3500, 200)
    pe.param_test1('chunk', 20, 150, 10)
    pe.param_test1('alpha', 0.992, 0.999, 0.001)
    # >>>>> testing parameters
    pe.param_test2('samp_dp', 0, 100, 5)
    pe.param_test2('samp_ds', 1500, 3500, 200)
    pe.param_test2('chunk', 20, 150, 10)
    pe.param_test2('alpha', 0.992, 0.999, 0.001)
    # >>>>> execution
    pe.continuous_run(2, plot=False)
    pe.evaluate()
    pe.terminate()
'''
