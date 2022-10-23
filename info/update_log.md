# Update Log

1. 20220810 05:?? Read ADC with loop
   1. Codes with ability to perform timer triggered interrupt event which perform power estimation are pushed to the repo.
   2. Codes are not tested with ESP32 yet.
   3. This project source is build with vscode platformio arduino framework instead of arduino or ESP32 IDF since it is currently the only method to work programming wise (not tested with ESP32). Following are steps are how to create new project.
      1. Open vscode, platformio homepage.
      2. Give it a name, select "uPesy ESP32 Wroom DevKit" board, select "Arduino" framework. (proved to be working, can try "Expressif IoT Development Framework" for framework.)
      3. Finished baudrate settings.
         1. In file "platformio.ini", add "monitor_speed = 921600".
         2. In file "main.cpp", add "Serial.begin(921600)" in setup function.
      4. (Noe necessary) Copy all the files to desired destination.
2. 20220811 00:44 Interrupt Reading ADC
   1. Full program was tested with ESP32, and found few bugs which are tagged as "bugged".
   2. Majority of the bugs are related to variable operations, and therefore I think declaring with the right embedded variable type should solve the problems.
   3. Another problem beside programing bugges is the high frequency interrupt operation. The experiment proofs that it's currently impossible to operate anything when the frequency is set too high (probably > 1000 Hz).
   4. If any bugs are found when executing, ESP32 returns a set of exception code, it can be decoded with external method. [This video](https://www.youtube.com/watch?v=323CS87h6WU&list=PL8UUpsd7hljNe75Xk2zzHRcwvmWGTSttQ) explains how to debug with encoded exception code. But to do it in vscode, it's not possible for now. Following are steps:
      1. Copy codes to Arduino IDE.
      2. Delete "ARDUINO_ISR_ATTR" in line 110 in declaration of function "onTime".
      3. Build the codes.
      4. Copy the exception codes and paste them into Arduino IDE/tools/ESP Exception Decoder
      5. Use the error line number and check codes back in vscode and try to solve it.
   5. Following steps:
      1. Try [ESP32-Audio Sampling Example](https://www.toptal.com/embedded/esp32-audio-sampling).
      2. Try find examples of high frequency timer interrupt.
      3. Try "Expressif IoT Development Framework"
3. 20220818 21:49 Dual Core Burst Read
   1. This version of code is tested on "./MS Phase6/MCU/ESP32_Platformio_1/src/main.cpp", and moved to "./MS Phase6/MCU/SMRBS-ESP32/lib/dual_core_adc_burst_read.cpp".
   2. It utilize one of the core to burst read adc values and store it inside SRAM, the other core to perform other functionality such as printing out values.
   3. Based on the test result, no bug was found, except the burst read is not confind to sampling rate, but the highest possible rate.
   4. Needs to find a way to trigger "analogRead" or "analogReadMilliVolts" by accurate sampling rate.
4. 20220913 20:57 Try ESP-IDF adc_continuous example from GitHub
   1. After some digging, the only available example code with multiple channel I2S DMA ADC example is in [esp-idf](https://github.com/espressif/esp-idf/tree/master/examples/peripherals/adc/continuous_read), so I instead use "ESP-IDF" trying to run this example. Using extension in VSCode encounters a lot of bugs, so I use ESP-IDF 4.4 CMD instead to select target, build, flash, monitor, only use VSCode to program.
   2. When building the example, the include statement doesn't work, no similiar issue was found in the internet, so I fired a [post](https://github.com/espressif/esp-idf/issues/9776) of issue on GitHub and hope this will be solved.
   3. The directory of example is "C:\Users\dachu\esp\esp-idf\examples\peripherals\adc\continuous_read_test".
   4. A list of procedures for programming using ESP-IDF. Path: "C:\Users\dachu\esp\button trigger.txt". [Go to list](https://github.com/belongtothenight/SMRBS-ESP32/blob/main/info/button%20trigger.txt)
5. 20220914 18:37 Change from Platformio to ESP-IDF.
   1. Successfully flashed and monitored sample code from GitHub after reinstalling ESP-IDF release v5.0.
   2. After testing, due to path issue cpp files can't be properly included in repo folders, so futher experiment will be done in "C:\Users\dachu\esp\test\dma_read".
6. 20220915 20:15
   1. After reinstalling esp-idf v5.0 and recloning esp-idf from github, the default sample code "continuous_read" works perfectly.
   2. Modified and obtained purified version of sample code with target limited to "ESP32".
   3. Steps to build a project from ESP-IDF 5.0 CMD
      1. Copy the folder containing all the project files like CMake.txt, **.cpp, etc.
      2. Copy the folder ".vscode_sample" into the project folder including the file "c_cpp_properties.json".
      3. Save vscode workplace in the project folder.
      4. Follow [this file](https://github.com/belongtothenight/SMRBS-ESP32/blob/main/info/button%20trigger.txt) to use ESP-IDF 5.0 CMD to build, flash, and monitor.
7. 20220920 ~ 20221003
   1. Start to test algorithm with raspberri pi 4 by setting up the environment.
   2. Environment can't be setup, VGA output no signal. Using raspberry pi official image flasher can't fix this bug, alterating the "config.txt" file or manually activating SSH functionality doesn't work as well. No way to successfully connect to raspberri pi with ethernet or even with network adaptor. Tried multiple times repeatly flashing images of operating system and it still doesn't work.
   3. Use SD Card Formatter and balenaEtcher to flash official image into SD card.
   4. On 20221003, finally after connecting to VGA output and power, it successfully boot up for the first time. Later the day, all initial setup including SSH, VNC are setup and nothing seems wrong this time.
   5. Tried to install drivers of seeed 6-channel microphone array by official documentation but failed due to unknown reason.
8. 20221004
   1. Cannot successfully install seeed driver, later cannot perform update and upgrade, somehow internet interface is gone. OS reinstall is needed.
   2. Perform OS reflash fixed this problem. Re-installed seeed-voicecard, still doesn't work. It's because the master branch of this repo is deprecated and no longer being updated.
   3. A fix for this problem is found in HinTak branch, [link](https://github.com/HinTak/seeed-voicecard). After cloning seeed-voicecard and install it, it's successfully installed and can be used with audacity to record 6 channel audio. But currently having problem transfering mp3 file back to laptop to examinate.
9. 20221005
   1. Project progress are all inside GitHub's project tab [link](https://github.com/users/belongtothenight/projects/1).
   2. After fresh installing OS and seeed-voicecard, menu bar disappear again, and the only option now is to find a way to trigger vnc interface by command in order to transfer file between raspberry pi and my laptop.
10. 20221006
    1. After removing "lxplug-volumepulse", menu bar re-appear and the audacity still can record. File transfer is therefore possible. [link](https://raspberrypi.stackexchange.com/questions/122579/after-fresh-install-of-raspberry-os-the-menu-bar-is-missing-in-tightvnc-session)
    2. All necessary tests in [link](https://wiki.seeedstudio.com/ReSpeaker_6-Mic_Circular_Array_kit_for_Raspberry_Pi/) have all being conduct except realtime sound source localization and tracking section, which is cause by cmake missing package.
11. 20221007
    1. Finished recording audio data and plot it as picture. [alg_test1](https://github.com/belongtothenight/SMRBS-ESP32/blob/main/algorithm/alg_tests/alg_test1.py)
    2. Finished recording audio data from 4 channels simultaniously and plot it as picture. [alg_test2](https://github.com/belongtothenight/SMRBS-ESP32/blob/main/algorithm/alg_tests/alg_test2.py)
    3. Implemented the power estimation algorithm previously realized in HT32F52352. The calculation currently implemented is really slow, vectorization might help accelerate this. [alg_test3.py](https://github.com/belongtothenight/SMRBS-ESP32/blob/main/algorithm/alg_tests/alg_test3.py)
       1. This algorithm relys on "SAMPLE_DOWNSIZE" parameter to downsize original sample value to prevent overflow.
       2. If overflow error occurs, this algorithm is going to automatically skip the sample.
       3. If the parameter "SAMPLE_DOWNSIZE" is not adjusted properly, algorithm is going to keep skipping samples.
       4. The approach of using pre-defined parameter to downsize sample is going to perform poorly when the input signal is either too big/loud or too small/soft.
       5. In every sample process routine, automatic "SAMPLE_DOWNSIZE" adjustment can be helpful.
       6. If some routine skipped too many samples or perform too poorly, the algorithm should be able to automatically abandon that group of samples.
    4. What next?
       1. Change "CHUNK" to smaller numbers around 128 to decrease calculation time and interval.
       2. Try to get a stable curve of power instead of lots of spikes.
       3. Implement 11.3.5 + 11.3.6
12. 20221011
    1. Sucessfully understand and added additional functions to pixel_ring model. All files are zipped to "pixel_ring_mod.7z" in "./algorithm/pixel_ring_mod.7z". Test file is [pixel_ring_test.py](https://github.com/belongtothenight/SMRBS-ESP32/blob/main/algorithm/pixel_ring_test.py)
    2. To install this
       1. unzip.
       2. "cd" to the root folder of unzipped "pixel_ring_mod.7z".
       3. "pip install -U -e .".
    3. Re-examine previously finished [alg_test4.py](https://github.com/belongtothenight/SMRBS-ESP32/blob/main/algorithm/alg_tests/alg_test4.py) and altered how the result are presented and fix some bugs.
    4. Tested parameters "chunk", "alpha", "sample_downsize" individually with ["alg_test5_chunk.py"](https://github.com/belongtothenight/SMRBS-ESP32/blob/main/algorithm/alg_tests/alg_test5_chunk.py), ["alg_test5_alpha.py"](https://github.com/belongtothenight/SMRBS-ESP32/blob/main/algorithm/alg_tests/alg_test5_alpha.py), ["alg_test5_sampledownsize.py"](https://github.com/belongtothenight/SMRBS-ESP32/blob/main/algorithm/alg_tests/alg_test5_sampledownsize.py).
13. 20221016
    1. Finished ["alg_test6.py"](https://github.com/belongtothenight/SMRBS-ESP32/blob/main/algorithm/alg_tests/alg_test6.py).
       1. The output files is written mostly in model.
       2. Plots are correctly labeled, with legends provided.
       3. Samples are downsized with 2k, no pyoverflow error ever occur(probably once?).
       4. The start section of samples are dumped to prevent spike at the begining.
       5. Results are stored in ["alg_test6"](https://github.com/belongtothenight/SMRBS-ESP32/blob/main/algorithm/alg_tests/alg_test6).
14. 20221018
    1. Add [README.md](https://github.com/belongtothenight/SMRBS-ESP32/tree/main/algorithm/README.md) of algorithm.
15. 20221021
    1. Finished pixel_ring control test on ["alg_test7_working.py"](https://github.com/belongtothenight/SMRBS-ESP32/blob/main/algorithm/alg_tests/alg_test7_working.py).
16. 20221022
    1. Finished ["alg_test7.py"](https://github.com/belongtothenight/SMRBS-ESP32/blob/main/algorithm/alg_tests/alg_test7.py).
    2. Steps to change [pixel_ring](https://github.com/respeaker/pixel_ring) library.
       1. In "pixel_ring.py", add function definition.
       2. In "apa102_pixel_ring.py", add function definition with pattern function.
       3. In "pattern.py", add details about LEDs, like their RGB values.
       4. Open terminal, go to directory "pixel_ring", with "cd pixel_ring".
       5. Install library with "pip install -U -e ."
    3. Finished ["alg_test8.py"](https://github.com/belongtothenight/SMRBS-ESP32/blob/main/algorithm/alg_tests/alg_test8.py).
    4. Finished ["alg1.py"](https://github.com/belongtothenight/SMRBS-ESP32/blob/main/algorithm/alg1.py).
17. 20221023
    1. Creates new issues to work on. [[Issues#14] Abrupt start to audio](https://github.com/belongtothenight/SMRBS-ESP32/issues/14).
    2. Working on fair comparison.
       1. Based on [experiment_withfig.txt](https://github.com/belongtothenight/SMRBS-ESP32/blob/main/algorithm/alg_tests/alg_test7/experiment_withfig.txt), the received signal from each microphone/channel after processed with power estimation is not the same, it is possible that different channel have different gain.
       2. Specs on [official wiki](https://wiki.seeedstudio.com/ReSpeaker_6-Mic_Circular_Array_kit_for_Raspberry_Pi/) provided the possible options for gain adjustments on both AC101 and AC108 chips ([details](https://github.com/belongtothenight/SMRBS-ESP32/issues/10)).
       3. Found a [post](https://forum.seeedstudio.com/t/respeaker-6-mic-circular-array-microphone-gain-what-gain-is-set-up-in-ac108-adc/261690/1) on seeed studio forum, no answer to the question and no reply to the post.
       4. In respeaker/seeed-voicecard, found Programmable Gain Amplifier (PGA) settings in [ac108.c](https://github.com/respeaker/seeed-voicecard/blob/master/ac108.c) by searching "PGA". Nothing seems out of place.
       5. Trying to do consistancy test on different microphone channels.
