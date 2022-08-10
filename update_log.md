1. 20220810 05:-- 
   1. Codes with ability to perform timer triggered interrupt event which perform power estimation are pushed to the repo.
   2. Codes are not tested with ESP32 yet.
   3. This project source is build with vscode platformio arduino framework instead of arduino or ESP32 IDF since it is currently the only method to work programming wise (not tested with ESP32). Following are steps are how to create new project.
      1. Open vscode, platformio homepage.
      2. Give it a name, select "uPesy ESP32 Wroom DevKit" board, select "Arduino" framework. (proved to be working, can try "Expressif IoT Development Framework" for framework.)
      3. Finished baudrate settings.
         1. In file "platformio.ini", add "monitor_speed = 921600".
         2. In file "main.cpp", add "Serial.begin(921600)" in setup function.
      4. (Noe necessary) Copy all the files to desired destination.
2. 20220811 12:44
   1. Full program was tested with ESP32, and found few bugs which are tagged as "bugged".
   2. Majority of the bugs are related to variable operations, and therefore I think declaring with the right embedded variable type should solve the problems.
   3. Another problem beside programing bugges is the high frequency interrupt operation. The experiment proofs that it's currently impossible to operate anything when the frequency is set too high (probably > 1000 Hz).
   4. If any bugs are found when executing, ESP32 returns a set of exception code, it can be decoded with external method. [This video](https://www.youtube.com/watch?v=323CS87h6WU&list=PL8UUpsd7hljNe75Xk2zzHRcwvmWGTSttQ) explains how to debug with encoded exception code. But to do it in vscode, it's not possible for now. Following are steps:
      1. Copy codes to Arduino IDE.
      2. Delete "ARDUINO_ISR_ATTR" in line 110 in declaration of function "onTime".
      3. Build the codes.
      4. Copy the exception codes and paste them into Arduino IDE/tools/ESP Exception Decoder
      5. Use the error line number and check codes back in vscode and try to solve it.