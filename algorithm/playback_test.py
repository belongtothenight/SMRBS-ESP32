import pyaudio
import time
import wave

# <<parameters>>
RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 8
RESPEAKER_WIDTH = 2
RESPEAKER_INDEX = 2  # refer to input device id # run getDeviceInfo.py to get index
AUDIO_JACK_INDEX = 0

# https://people.csail.mit.edu/hubert/pyaudio/#examples
# https://raspberrypi.stackexchange.com/questions/38756/real-time-audio-input-output-in-python-with-pyaudio


class main():
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
            stream_callback=main.callback,
            output_device_index=AUDIO_JACK_INDEX,)

    def callback(in_data, frame_count, time_info, status):
        return (in_data, pyaudio.paContinue)

    def run(self):
        self.stream.start_stream()
        while self.stream.is_active():
            time.sleep(0.1)

    def terminate(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()


if __name__ == '__main__':
    m = main()
    m.run()
    m.terminate()
