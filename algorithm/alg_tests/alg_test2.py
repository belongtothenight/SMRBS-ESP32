# import gpiozero
import pyaudio
import wave
import numpy as np
from matplotlib import pyplot as plt
from time import sleep
import array

RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 8
RESPEAKER_WIDTH = 2
# run getDeviceInfo.py to get index
RESPEAKER_INDEX = 2  # refer to input device id
CHUNK = 1024
RECORD_SECONDS = 0.1
TOTAL_PIC = 10  # increase total recorded data length by saving them as plot in pic

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
    pcm_a = array.array('h')
    pcm_a.frombytes(b''.join(frames_a))
    pcm_b = array.array('h')
    pcm_b.frombytes(b''.join(frames_b))
    pcm_c = array.array('h')
    pcm_c.frombytes(b''.join(frames_c))
    pcm_d = array.array('h')
    pcm_d.frombytes(b''.join(frames_d))

    plt_title = ['mic1', 'mic2', 'mic3', 'mic4']
    fig, axs = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('pic' + str(times))
    axs[0, 0].plot(pcm_a)
    axs[0, 1].plot(pcm_b)
    axs[1, 0].plot(pcm_c)
    axs[1, 1].plot(pcm_d)
    axs[0, 0].set_title(plt_title[0])
    axs[0, 1].set_title(plt_title[1])
    axs[1, 0].set_title(plt_title[2])
    axs[1, 1].set_title(plt_title[3])
    plt.savefig('/home/pi/code/alg_test2_chx4/p{0}.png'.format(times))
    plt.clf()

print("* done recording")
stream.stop_stream()
stream.close()
p.terminate()
