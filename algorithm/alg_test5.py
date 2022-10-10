# import gpiozero
import pyaudio
import wave
import math
import numpy as np
from matplotlib import pyplot as plt
from time import sleep
import array

'''
Improvement:
1. Auto skip if skipped too many times.
'''

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

p = pyaudio.PyAudio()
stream = p.open(
    rate=RESPEAKER_RATE,
    format=p.get_format_from_width(RESPEAKER_WIDTH),
    channels=RESPEAKER_CHANNELS,
    input=True,
    input_device_index=RESPEAKER_INDEX,)
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
    sk_a = 0
    sk_b = 0
    sk_c = 0
    sk_d = 0
    for i in range(CHUNK):
        s_a = pcm_a[i] / SAMPLE_DOWNSIZE
        s_b = pcm_b[i] / SAMPLE_DOWNSIZE
        s_c = pcm_c[i] / SAMPLE_DOWNSIZE
        s_d = pcm_d[i] / SAMPLE_DOWNSIZE
        p_t_a = s_a**2
        p_t_b = s_b**2
        p_t_c = s_c**2
        p_t_d = s_d**2
        p_t_disc = np.argmin([p_t_a, p_t_b, p_t_c, p_t_d])
        try:
            p_a.append(ALPHA*p_t_a+(1-ALPHA)*(p_a[-1]**2))
            p_b.append(ALPHA*p_t_b+(1-ALPHA)*(p_b[-1]**2))
            p_c.append(ALPHA*p_t_c+(1-ALPHA)*(p_c[-1]**2))
            p_d.append(ALPHA*p_t_d+(1-ALPHA)*(p_d[-1]**2))
            p_disc.append(p_t_disc)
        except:
            # skip if overflow
            sk_a += 1
            sk_b += 1
            sk_c += 1
            sk_d += 1

    # plot
    plt_title = ['mic1', 'mic2', 'mic3', 'mic4', 'stacked', 'decision']
    fig, axs = plt.subplots(2, 3, figsize=(16, 12))
    fig.suptitle('pic' + str(times))
    axs[0, 0].plot(p_a)
    axs[0, 1].plot(p_b)
    axs[1, 0].plot(p_c)
    axs[1, 1].plot(p_d)
    axs[2, 0].plot(p_a)
    axs[2, 0].plot(p_b)
    axs[2, 0].plot(p_c)
    axs[2, 0].plot(p_d)
    axs[2, 1].plot(p_disc)

# version 1
    axs[0, 0].set_title(plt_title[0] + ' skipped ' +
                        str(sk_a) + '/' + str(CHUNK))
    axs[0, 1].set_title(plt_title[1] + ' skipped ' +
                        str(sk_b) + '/' + str(CHUNK))
    axs[1, 0].set_title(plt_title[2] + ' skipped ' +
                        str(sk_c) + '/' + str(CHUNK))
    axs[1, 1].set_title(plt_title[3] + ' skipped ' +
                        str(sk_d) + '/' + str(CHUNK))
    axs[2, 0].set_title(plt_title[4])
    axs[2, 0].legend(['mic1', 'mic2', 'mic3', 'mic4'])
    axs[2, 1].set_title(plt_title[5])
# version 2
    # p1 = axs[0, 0].set_title(plt_title[0] + ' skipped ' +
    #                          str(sk_a) + '/' + str(CHUNK))
    # p2 = axs[0, 1].set_title(plt_title[1] + ' skipped ' +
    #                          str(sk_b) + '/' + str(CHUNK))
    # p3 = axs[1, 0].set_title(plt_title[2] + ' skipped ' +
    #                          str(sk_c) + '/' + str(CHUNK))
    # p4 = axs[1, 1].set_title(plt_title[3] + ' skipped ' +
    #                          str(sk_d) + '/' + str(CHUNK))
    # axs[2, 0].set_title(plt_title[4])
    # axs[2, 0].legend([p1, p2, p3, p4], ['mic1', 'mic2', 'mic3', 'mic4'])
    # axs[2, 1].set_title(plt_title[5])

    plt.savefig('/home/pi/code/alg_test3_chx4/p{0}.png'.format(times))
    plt.clf()

print("* done recording")
stream.stop_stream()
stream.close()
p.terminate()
