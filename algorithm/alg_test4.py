# import gpiozero
import pyaudio
import wave
import math
import numpy as np
from matplotlib import pyplot as plt
from time import sleep
import array
from pixel_ring import pixel_ring
from gpiozero import LED

'''
Improvement:
1. Change chunk to 128
2. Generate plot with output decision result using power estimation result.
3. Add LED (ring_pixel) indicating which direction is decided.
4. Store data temperary and plot all data after execution is completed. *(data isn't inspected yet)
'''

# Parameters
RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 8
RESPEAKER_WIDTH = 2
# run getDeviceInfo.py to get index
RESPEAKER_INDEX = 2  # refer to input device id
CHUNK = 128
RECORD_SECONDS = 0.1
TOTAL_PIC = 10  # increase total recorded data length by saving them as plot in pic
POWER_CNT = 100  # how many samples to finish calculation
ALPHA = 0.99
SAMPLE_DOWNSIZE = 2000  # sample = sample / SAMPLE_DOWNSIZE

# Mem
mem_p_a = []
mem_p_b = []
mem_p_c = []
mem_p_d = []
mem_p_disc = []
mem_sk = []
mem_n1 = []
mem_n2 = []
mem_n3 = []
mem_n4 = []

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
print("* recording")

times = 0
while times < TOTAL_PIC:
    times += 1
    print('{0}/{1}'.format(times, TOTAL_PIC))
    frames_a = []
    frames_b = []
    frames_c = []
    frames_d = []

    # get data
    for i in range(0, int(RESPEAKER_RATE / CHUNK * RECORD_SECONDS)):
        # prevent over flow error
        data = stream.read(CHUNK, exception_on_overflow=False)
        # extract channel 0 data from 8 channels, if you want to extract channel 1, please change to [1::8]
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
    sk = 0
    for i in range(CHUNK):
        s_a = pcm_a[i] / SAMPLE_DOWNSIZE
        s_b = pcm_b[i] / SAMPLE_DOWNSIZE
        s_c = pcm_c[i] / SAMPLE_DOWNSIZE
        s_d = pcm_d[i] / SAMPLE_DOWNSIZE
        p_t_a = s_a**2
        p_t_b = s_b**2
        p_t_c = s_c**2
        p_t_d = s_d**2
        p_t_disc = np.argmax([p_t_a, p_t_b, p_t_c, p_t_d]) + 1
        if p_t_disc == 1:
            pixel_ring.open1()
        elif p_t_disc == 2:
            pixel_ring.open2()
        elif p_t_disc == 3:
            pixel_ring.open3()
        else:
            pixel_ring.open4()
        try:
            p_a.append(ALPHA*p_t_a+(1-ALPHA)*(p_a[-1]**2))
            p_b.append(ALPHA*p_t_b+(1-ALPHA)*(p_b[-1]**2))
            p_c.append(ALPHA*p_t_c+(1-ALPHA)*(p_c[-1]**2))
            p_d.append(ALPHA*p_t_d+(1-ALPHA)*(p_d[-1]**2))
            p_disc.append(p_t_disc)
        except:
            # skip if overflow
            sk += 1

    # skip if skipping too much
    if sk > CHUNK * 0.3:
        times -= 1
        continue

    # calculate percentage
    unique, counts = np.unique(p_disc, return_counts=True)
    mic = dict(zip(unique, counts))
    try:
        n1 = int(mic[1]/CHUNK*100)
    except:
        n1 = 0
    try:
        n2 = int(mic[2]/CHUNK*100)
    except:
        n2 = 0
    try:
        n3 = int(mic[3]/CHUNK*100)
    except:
        n3 = 0
    try:
        n4 = int(mic[4]/CHUNK*100)
    except:
        n4 = 0

    # store data in mem
    mem_p_a.append(p_a)
    mem_p_b.append(p_b)
    mem_p_c.append(p_c)
    mem_p_d.append(p_d)
    mem_p_disc.append(p_disc)
    mem_sk.append(sk)
    mem_n1.append(n1)
    mem_n2.append(n2)
    mem_n3.append(n3)
    mem_n4.append(n4)

print("* done recording")
print('start plotting')
# plot
plt_title = ['mic1', 'mic2', 'mic3', 'mic4', 'stacked', 'decision']
for i in range(TOTAL_PIC):
    fig, axs = plt.subplots(2, 3, figsize=(24, 12))
    fig.suptitle('pic' + str(i + 1))
    axs[0, 0].plot(mem_p_a[i])
    axs[0, 1].plot(mem_p_b[i])
    axs[1, 0].plot(mem_p_c[i])
    axs[1, 1].plot(mem_p_d[i])
    axs[0, 2].plot(mem_p_a[i])
    axs[0, 2].plot(mem_p_b[i])
    axs[0, 2].plot(mem_p_c[i])
    axs[0, 2].plot(mem_p_d[i])
    axs[1, 2].step(range(len(mem_p_disc[i])), mem_p_disc[i])
    axs[1, 2].set_ylim([1, 4])
    axs[0, 0].set_title(plt_title[0])
    axs[0, 1].set_title(plt_title[1])
    axs[1, 0].set_title(plt_title[2])
    axs[1, 1].set_title(plt_title[3])
    axs[0, 2].set_title(plt_title[4] + ' skipped ' +
                        str(mem_sk[i]) + '/' + str(CHUNK))
    axs[0, 2].legend(['mic1', 'mic2', 'mic3', 'mic4'])
    axs[1, 2].set_title(plt_title[5] + ' mic=[{0}, {1}, {2}, {3}]%'.format(mem_n1[i], mem_n2[i], mem_n3[i], mem_n4[i]))

    plt.savefig('/home/pi/code/alg_test4/p{0}.png'.format(i + 1))
    plt.clf()
    print('{0}/{1}'.format(i+1, TOTAL_PIC))
print('* done plotting')

# LED END
pixel_ring.off()
power.off()
# MIC END
stream.stop_stream()
stream.close()
p.terminate()
