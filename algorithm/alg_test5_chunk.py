# import gpiozero
import pyaudio
import wave
import math
import array
import numpy as np
from os.path import join
from matplotlib import pyplot as plt
from time import sleep
from pixel_ring import pixel_ring
from gpiozero import LED

'''
Improvement:
1. Patameter testing.
'''

# Parameters
RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 8
RESPEAKER_WIDTH = 2
RESPEAKER_INDEX = 2  # refer to input device id # run getDeviceInfo.py to get index
chunk = 100
TOTAL_PIC = 100  # increase total recorded data length by saving them as plot in pic
POWER_CNT = 100  # how many samples to finish calculation # not used yet
alpha = 0.99
sample_downsize = 2000  # sample = sample / sample_downsize
IMG_PATH = '/home/pi/code/alg_test5/'
IMG_NAME = 'chunk.png'
PLOT_P = False  # plot power of each measurement # if TOTAL_PIC>10 it is going to take forever
PLOT_D = False  # plot decision of microphone
PLOT_T = True   # plot trend of decision

MIN = 50 # testing parameter min
MAX = 100 # testing parameter max

# LED initialize
power = LED(5)
power.on()
pixel_ring.set_brightness(10)
pixel_ring.wakeup()
# MIC initialize
p = pyaudio.PyAudio()
stream = p.open(
    rate=RESPEAKER_RATE,
    format=p.get_format_from_width(RESPEAKER_WIDTH),
    channels=RESPEAKER_CHANNELS,
    input=True,
    input_device_index=RESPEAKER_INDEX,)

pixel_ring.off()

length = len(range(MIN, MAX))
times_p = 0
param_test_result = []
for x in range(MIN, MAX):
    # Mem
    mem_p_a = []
    mem_p_b = []
    mem_p_c = []
    mem_p_d = []
    mem_p_disc = []
    chunk = x # set value to testing parameter
    times_p += 1
    times = 0
    while times < TOTAL_PIC:
        times += 1
        print('{0}/{1}'.format(times + (times_p-1) * TOTAL_PIC, length * TOTAL_PIC))
        frames_a = []
        frames_b = []
        frames_c = []
        frames_d = []

        # get data
        # prevent over flow error
        data = stream.read(chunk, exception_on_overflow=False)
        a = np.frombuffer(data, dtype=np.int16)[0::8]
        b = np.frombuffer(data, dtype=np.int16)[1::8]
        c = np.frombuffer(data, dtype=np.int16)[2::8]
        d = np.frombuffer(data, dtype=np.int16)[3::8]
        frames_a.append(a.tobytes())
        frames_b.append(b.tobytes())
        frames_c.append(c.tobytes())
        frames_d.append(d.tobytes())

        # decode data
        pcm_a = array.array('h')
        pcm_a.frombytes(b''.join(frames_a))
        pcm_b = array.array('h')
        pcm_b.frombytes(b''.join(frames_b))
        pcm_c = array.array('h')
        pcm_c.frombytes(b''.join(frames_c))
        pcm_d = array.array('h')
        pcm_d.frombytes(b''.join(frames_d))

        # power calculation v1 (without locking sample size)
        p_a = []
        p_b = []
        p_c = []
        p_d = []
        p_disc = []
        p_a.append(0)
        p_b.append(0)
        p_c.append(0)
        p_d.append(0)
        try:
            for i in range(chunk):
                p_t_a = (pcm_a[i] / sample_downsize)**2
                p_t_b = (pcm_b[i] / sample_downsize)**2
                p_t_c = (pcm_c[i] / sample_downsize)**2
                p_t_d = (pcm_d[i] / sample_downsize)**2
                p_a.append(alpha*p_t_a+(1-alpha)*(p_a[-1]**2))
                p_b.append(alpha*p_t_b+(1-alpha)*(p_b[-1]**2))
                p_c.append(alpha*p_t_c+(1-alpha)*(p_c[-1]**2))
                p_d.append(alpha*p_t_d+(1-alpha)*(p_d[-1]**2))
            p_t_disc = np.argmax([p_a[-1], p_b[-1], p_c[-1], p_d[-1]]) + 1
            p_disc.append(p_t_disc)
            if p_t_disc == 1:
                pixel_ring.open1()
            elif p_t_disc == 2:
                pixel_ring.open2()
            elif p_t_disc == 3:
                pixel_ring.open3()
            else:
                pixel_ring.open4()
        except Exception as e:
            # redo if overflow occurs
            print(e)
            times -= 1
            continue

        # store data in mem
        mem_p_a.append(p_a)
        mem_p_b.append(p_b)
        mem_p_c.append(p_c)
        mem_p_d.append(p_d)
        mem_p_disc.append(p_disc)
        
    # calculate percentage
    unique, counts = np.unique(mem_p_disc, return_counts=True)
    mic = dict(zip(unique, counts))
    try:
        n1 = int(mic[1]/TOTAL_PIC*100)
    except:
        n1 = 0
    try:
        n2 = int(mic[2]/TOTAL_PIC*100)
    except:
        n2 = 0
    try:
        n3 = int(mic[3]/TOTAL_PIC*100)
    except:
        n3 = 0
    try:
        n4 = int(mic[4]/TOTAL_PIC*100)
    except:
        n4 = 0

    plt_title = ['mic1', 'mic2', 'mic3', 'mic4', 'stacked', 'decision']
    if PLOT_P:
        for i in range(TOTAL_PIC):
            plt.figure(figsize=(16, 9))
            plt.plot(mem_p_a[i])
            plt.plot(mem_p_b[i])
            plt.plot(mem_p_c[i])
            plt.plot(mem_p_d[i])
            plt.title(plt_title[4] + ' decision: mic{0}'.format(mem_p_disc[i]))
            plt.legend(['mic1', 'mic2', 'mic3', 'mic4'])
            plt.savefig(join(IMG_PATH, 'p{0}.png'.format(i + 1)))
            plt.clf()
            print('{0}/{1}'.format(i+1, TOTAL_PIC))
    if PLOT_D:
        plt.figure(figsize=(16, 9))
        plt.hlines(mem_p_disc, range(TOTAL_PIC), range(1, TOTAL_PIC+1))
        plt.title(plt_title[5] +
                  ' mic=[{0}, {1}, {2}, {3}]%'.format(n1, n2, n3, n4))
        plt.ylim((0, 5))
        plt.savefig(join(IMG_PATH, 'p_decision_{0}.png'.format(TOTAL_PIC)))
    param_test_result.append(mem_p_disc)
    # print('* done plotting')
param_test_result = ((np.array(param_test_result)).squeeze()).tolist() # 2D to 1D
result = []
for element in param_test_result:    
    unique, counts = np.unique(element, return_counts=True)
    result.append(dict(zip(unique, counts)))
mic1 = []
mic2 = []
mic3 = []
mic4 = []
for element in result:
    mic1.append(element.get(1))
    mic2.append(element.get(2))
    mic3.append(element.get(3))
    mic4.append(element.get(4))
if PLOT_T:
    plt.figure(figsize=(16, 9))
    plt.xticks(range(length), range(MIN, MAX))
    plt.plot(mic1)
    plt.plot(mic2)
    plt.plot(mic3)
    plt.plot(mic4)
    plt.title('trend')
    plt.legend(['mic1', 'mic2', 'mic3', 'mic4'])
    # plt.show()
    plt.savefig(join(IMG_PATH, IMG_NAME))
    # plt.clf()

# LED END
pixel_ring.off()
power.off()
# MIC END
stream.stop_stream()
stream.close()
p.terminate()
