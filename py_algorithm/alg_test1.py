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
    frames = []
    for i in range(0, int(RESPEAKER_RATE / CHUNK * RECORD_SECONDS)):
        # prevent over flow error
        data = stream.read(CHUNK, exception_on_overflow=False)
        # extract channel 0 data from 8 channels, if you want to extract channel 1, please change to [1::8]
        a = np.frombuffer(data, dtype=np.int16)[0::8]
        frames.append(a.tobytes())
    pcm = array.array('h')
    pcm.frombytes(b''.join(frames))
    plt.plot(pcm)
    plt.title('pic' + str(times))
# plt.show()
    plt.savefig('/home/pi/code/pic/chx1/p{0}.png'.format(times))
    # prevent overlapping
    plt.clf()
# sleep(0.1)

print("* done recording")
stream.stop_stream()
stream.close()
p.terminate()
