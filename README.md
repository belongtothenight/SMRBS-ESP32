# SMRBS-ESP32

![Repo Size](https://img.shields.io/github/repo-size/belongtothenight/SMRBS-ESP32) ![Code Size](https://img.shields.io/github/languages/code-size/belongtothenight/SMRBS-ESP32) ![Commit Per Month](https://img.shields.io/github/commit-activity/m/belongtothenight/SMRBS-ESP32)

![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=belongtothenight&repo=SMRBS-ESP32)

[Go to log](https://github.com/belongtothenight/SMRBS-ESP32/blob/main/info/update_log.md)

## Repo Structure

- algorithm (Raspberry Pi 4 + ReSpeaker 6 Microphone Array)
- info
- src (ESP32)

## Documentations

1. [ESP32-Timer](https://espressif-docs.readthedocs-hosted.com/projects/arduino-esp32/en/latest/api/timer.html?highlight=portMUX_TYPE#example-applications)
2. [ESP32-ADC](https://espressif-docs.readthedocs-hosted.com/projects/arduino-esp32/en/latest/api/adc.html?highlight=adc)
3. [ESP32-GPIO](https://espressif-docs.readthedocs-hosted.com/projects/arduino-esp32/en/latest/api/gpio.html?highlight=GPIO)
4. [ESP32-Hardware Documentation](https://www.espressif.com/sites/default/files/documentation/esp32_technical_reference_manual_en.pdf)
5. [ESP32-Audio Sampling Example](https://www.toptal.com/embedded/esp32-audio-sampling)
6. [YouTube-ESP32 SD Card Audio Recording](https://www.youtube.com/watch?v=bVru6M862HY)
7. [GitHub-esp32_SoundRecorder](https://github.com/MhageGH/esp32_SoundRecorder)
8. [GitHub-ESP32 I2S Audio](https://github.com/atomic14/esp32_audio) (Most important) esp32_audio/i2s_sampling/src/ (abandoned, since I2S DMA can't handle much adc channels)

### 20220818

1. [YouTube-Arduino fast sampling technique for high frequency signal](https://www.youtube.com/watch?v=lRmQTYLyB6E) $\large\star$
2. [YouTube-ESP32 Dual Core on Arduino IDE including Data Passing and Task Synchronization](https://www.youtube.com/watch?v=k_D_Qu0cgu8) $\large\star$
3. [GitHub-Sensorslot/ESP32-Dual-Core](https://github.com/SensorsIot/ESP32-Dual-Core)
4. [GitHub-ESPRESSIF/Arduino-ESP32](https://github.com/espressif/arduino-esp32)
5. [Programmer Think-ADC Sampling Test](https://programmer.ink/think/esp32-c3-test-i-adc-sampling.html)
6. [GitHub-ADC I2S mode with multiple channel pattern](https://github.com/espressif/esp-idf/pull/1991/commits)
7. [ESPRESSIF/Discussion Forum-Need help with ESP32 ADC DMA continuous read configuration](https://www.esp32.com/viewtopic.php?f=13&t=27603)
8. [ESPRESSIF/ESP-IDF Programming Guide/ADC](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/adc_continuous.html?highlight=adc%20sampling%20rate#adc-configurations)
9. [ESPRESSIF/ESP32 Hardware Design Guildline](https://www.espressif.com/sites/default/files/documentation/esp32_hardware_design_guidelines_en.pdf)

### 20221007

1. [ReSpeaker 6-Mic Circular Array kit for Raspberry Pi](https://wiki.seeedstudio.com/ReSpeaker_6-Mic_Circular_Array_kit_for_Raspberry_Pi/)
2. [PyAudio Documentation](https://people.csail.mit.edu/hubert/pyaudio/docs/#class-stream)
3. [GitHub pyAudio Analysis](https://github.com/tyiannak/pyAudioAnalysis)
