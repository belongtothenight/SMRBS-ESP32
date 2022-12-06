import pyaudio
import time
import wave
import array
import numpy as np

# <<parameters>>
RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 8
RESPEAKER_WIDTH = 2
RESPEAKER_INDEX = 2  # refer to input device id # run getDeviceInfo.py to get index
AUDIO_JACK_INDEX = 0

samp_dp = 20    # sample to drop at the beginning of each run
samp_ds = 2000  # sample = sample / samp_ds (sample_downsize)
chunk = 100     # number of samples to read from stream

# https://people.csail.mit.edu/hubert/pyaudio/#examples
# https://raspberrypi.stackexchange.com/questions/38756/real-time-audio-input-output-in-python-with-pyaudio


class main1():
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.p.terminate()  # prevent channel occupation
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            rate=RESPEAKER_RATE,
            format=self.p.get_format_from_width(RESPEAKER_WIDTH),
            channels=RESPEAKER_CHANNELS,
            input=True,
            input_device_index=RESPEAKER_INDEX,
            output=True,
            stream_callback=main1.callback,
            output_device_index=AUDIO_JACK_INDEX,)

    def callback(in_data, frame_count, time_info, status):
        print(type(in_data))
        return (in_data, pyaudio.paContinue)

    def run(self):
        self.stream.start_stream()
        while self.stream.is_active():
            time.sleep(0.1)

    def terminate(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()


class main2():
    def __init__(self, sampdp=samp_dp, sampds=samp_ds, chunk_=chunk):
        self.samp_dp = sampdp
        self.samp_ds = sampds
        self.chunk = chunk_
        self.select_ch = 1
        self.p = pyaudio.PyAudio()
        self.p.terminate()  # prevent channel occupation
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            rate=RESPEAKER_RATE,
            format=self.p.get_format_from_width(RESPEAKER_WIDTH),
            channels=RESPEAKER_CHANNELS,
            input=True,
            input_device_index=RESPEAKER_INDEX,)

    def read_data(self, pf=False):
        # pf: print flag
        data = self.stream.read(self.chunk, exception_on_overflow=False)
        print(data)
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
        # print
        if pf:
            print(self.d1)
            print(self.d2)
            print(self.d3)
            print(self.d4)
            print(self.d5)
            print(self.d6)

    def select_channel(self):
        if self.select_ch == 1:
            self.d = self.d1
        elif self.select_ch == 2:
            self.d = self.d2
        elif self.select_ch == 3:
            self.d = self.d3
        elif self.select_ch == 4:
            self.d = self.d4
        elif self.select_ch == 5:
            self.d = self.d5
        elif self.select_ch == 6:
            self.d = self.d6

    def write_data(self):
        self.select_channel()
        self.d = np.array(self.d, dtype='<u2')
        # self.d = self.d.tobytes()
        self.d = self.d.astype(np.float32).tostring()
        print(self.d)
        self.stream.write(self.d, self.chunk)


if __name__ == '__main__':
    # m = main1()
    # print('initialized')
    # m.run()
    # print('executed')
    # m.terminate()

    m = main2()
    print('initialized')
    while True:
        m.read_data()
        m.select_channel()
        m.write_data()
