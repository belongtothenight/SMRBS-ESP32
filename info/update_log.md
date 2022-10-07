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
   3. A fix for this problem is found in HinTak branch, ![link](https://github.com/HinTak/seeed-voicecard). After cloning seeed-voicecard and install it, it's successfully installed and can be used with audacity to record 6 channel audio. But currently having problem transfering mp3 file back to laptop to examinate.
9. 20221005
   1. Project progress are all inside GitHub's project tab ![link](https://github.com/users/belongtothenight/projects/1).
   2. After fresh installing OS and seeed-voicecard, menu bar disappear again, and the only option now is to find a way to trigger vnc interface by command in order to transfer file between raspberry pi and my laptop.
10. 20221006
    1. After removing "lxplug-volumepulse", menu bar re-appear and the audacity still can record. File transfer is therefore possible. ![link](https://raspberrypi.stackexchange.com/questions/122579/after-fresh-install-of-raspberry-os-the-menu-bar-is-missing-in-tightvnc-session)
    2. All necessary tests in ![link](https://wiki.seeedstudio.com/ReSpeaker_6-Mic_Circular_Array_kit_for_Raspberry_Pi/) have all being conduct except realtime sound source localization and tracking section, which is cause by cmake missing package.
11. 20221007
    1. Sucessfully recorded audio data and plot it as picture.
