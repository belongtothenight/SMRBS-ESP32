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
