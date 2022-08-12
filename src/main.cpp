#include <Arduino.h>
#include "driver/gpio.h"

#define BTN_STOP_ALARM 0

hw_timer_t *timer = NULL;
volatile SemaphoreHandle_t timerSemaphore;
portMUX_TYPE timerMux = portMUX_INITIALIZER_UNLOCKED;

volatile uint32_t isrCounter = 0;
volatile uint32_t lastIsrAt = 0;

// Serial port for debugging
int baud_rate = 921600;

// ADC frequency setting
int frequency = 20000;            // Hz
int period = 1000000 / frequency; // microseconds

// ADC variables
const char adc_channel[4] = {'A', 'B', 'C', 'D'};
const int adc_pin[4] = {36, 39, 34, 35}; // Audio Channel Input Signal Pin Num
const int adc_max_add_one = 4096;        // ADC Max Value + 1
int adc_value[4] = {adc_max_add_one, adc_max_add_one, adc_max_add_one, adc_max_add_one};

// GPIO variables
const char gpio_channel[4] = {'A', 'B', 'C', 'D'};
const int gpio_pin[4] = {32, 33, 25, 26}; // Audio Channel Control Pin Num

// Power Estimation variables
float alpha = 0.99;
int v[4];
float Pn[4];
float Pn_1[4];

// Channel Control
int tolerance = 100; // need experiment

// Sort function
void sort_array(float array[], int size)
{
  for (int i = 0; i < size; i++)
  {
    if (array[i] > array[i + 1])
    {
      int temp = array[i];
      // array[i] = array[i + 1]; // bugged
      // array[i + 1] = temp; // bugged
    }
  }
}

// GPIO setup
void setup_gpio()
{
  pinMode(gpio_pin[0], OUTPUT);
  pinMode(gpio_pin[1], OUTPUT);
  pinMode(gpio_pin[2], OUTPUT);
  pinMode(gpio_pin[3], OUTPUT);
}

// ADC setup
void setup_adc()
{
  adc_value[0] = analogRead(adc_pin[0]);
  adc_value[1] = analogRead(adc_pin[1]);
  adc_value[2] = analogRead(adc_pin[2]);
  adc_value[3] = analogRead(adc_pin[3]);
  Serial.printf("ADC_value: %d, %d, %d, %d\n", adc_value[0], adc_value[1], adc_value[2], adc_value[3]);
  // need to add checks for adc_value[i] < adc_max_add_one
}

// Power Estimation
void power_estimation()
{
  for (int i = 0; i < 4; i++)
  {
    v[i] = analogReadMilliVolts(adc_pin[i]);
    // Pn_1[i] = Pn[i] * alpha + (1 - alpha) * v[i] * v[i]; // error
    Pn[i] = Pn_1[i];
  }
}

// Handles external audio channel control switch
void channel_control()
{
  sort_array(Pn, 4);
  if (Pn[0] > tolerance)
  {
    for (int i = 0; i < 4; i++)
    {
      if (Pn[0] == Pn_1[i])
      {
        // turn the channel on
        // if the power is higher than the threshold
        // if it's the highest power of all channels
        // digitalWrite(gpio_pin[i], HIGH); // bugged
      }
      else
      {
        // turn the channel off
        // if the power is lower than the threshold
        // if it isn't the highest power of all channels
        // digitalWrite(gpio_pin[i], LOW); // bugged
      }
    }
  }
}

// Function executed after each timer interrupt
void ARDUINO_ISR_ATTR onTimer()
{
  // Increment the counter and set the time of ISR
  portENTER_CRITICAL_ISR(&timerMux);
  isrCounter++;
  lastIsrAt = millis();
  portEXIT_CRITICAL_ISR(&timerMux);
  // Give a semaphore that we can check in the loop
  xSemaphoreGiveFromISR(timerSemaphore, NULL);
  // It is safe to use digitalRead/Write here if you want to toggle an output
  // power_estimation(); // currently can't cope with fast interrupts (bugged)
}

// Setting up timer interrupt
void setup_timer()
{
  // Set BTN_STOP_ALARM to input mode
  pinMode(BTN_STOP_ALARM, INPUT);

  // Create semaphore to inform us when the timer has fired
  timerSemaphore = xSemaphoreCreateBinary();

  // Use 1st timer of 4 (counted from zero).
  // Set 80 divider for prescaler (see ESP32 Technical Reference Manual for more
  // info).
  // Prescaler devider ranges from 2 to 65536. When timer is clocked at 80MHz.
  timer = timerBegin(0, 80, true);

  // Attach onTimer function to our timer.
  timerAttachInterrupt(timer, &onTimer, true);

  // Set alarm to call onTimer function every second (value in microseconds).
  // Repeat the alarm (third parameter)
  timerAlarmWrite(timer, period, true);

  // Start an alarm
  timerAlarmEnable(timer);
}

void setup()
{
  Serial.begin(baud_rate);
  setup_gpio(); // seems to not setting up pins correctly
  setup_adc();
  setup_timer();

  pinMode(36, OUTPUT);
  digitalWrite(36, LOW);
}

void loop()
{
  // If Timer has fired
  if (xSemaphoreTake(timerSemaphore, 0) == pdTRUE)
  {
    uint32_t isrCount = 0, isrTime = 0;
    // Read the interrupt count and time
    portENTER_CRITICAL(&timerMux);
    isrCount = isrCounter;
    isrTime = lastIsrAt;
    portEXIT_CRITICAL(&timerMux);
    // Print it
    Serial.print("onTimer no. ");
    Serial.print(isrCount);
    Serial.print(" at ");
    Serial.print(isrTime);
    Serial.println(" ms");
    // Control the audio channel
    // channel_control(); // only need to execute several times per second
  }
  // If button is pressed
  if (digitalRead(BTN_STOP_ALARM) == LOW)
  {
    // If timer is still running
    if (timer)
    {
      // Stop and free timer
      timerEnd(timer);
      timer = NULL;
    }
  }
}