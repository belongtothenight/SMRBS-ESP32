#include <Arduino.h>

const char adc_channel[4] = {'A', 'B', 'C', 'D'};
const int adc_pin[4] = {36, 39, 34, 35}; // Audio Channel Pin Num
const int adc_max_add_one = 4096;        // ADC Max Value + 1
const int adc_channel_num = sizeof(adc_channel);

int adc_value[4] = {adc_max_add_one, adc_max_add_one, adc_max_add_one, adc_max_add_one};

const int adc_buffer_num = 2;
const int adc_buffer_size = 1024;
int adc_buffer[adc_buffer_num][adc_channel_num][adc_buffer_size] = {0};
int adc_buffer_write_flag = 0; // 0: write to buffer 1: write to buffer 2

void adc_setup(int value[])
{
    value[0] = analogRead(adc_pin[0]);
    value[1] = analogRead(adc_pin[1]);
    value[2] = analogRead(adc_pin[2]);
    value[3] = analogRead(adc_pin[3]);
    Serial.println("ADC_value: ");
    Serial.println(adc_value[0]);
    Serial.println("/");
    Serial.println(adc_value[1]);
    Serial.println("/");
    Serial.println(adc_value[2]);
    Serial.println("/");
    Serial.println(adc_value[3]);
    // Serial.println("\n");
}

//===============================================================

TaskHandle_t Task1, Task2;
SemaphoreHandle_t baton1, baton2;

void codeForTask1(void *parameter)
{

    for (;;)
    {
        for (int i = 0; i < adc_buffer_num; i++)
        { // Storing ADC Value in two different buffer seperately
            adc_buffer_write_flag = i;
            if (i == 0)
            { // prevent read write conflict (SemaphoreHandle_t)
                xSemaphoreTake(baton1, portMAX_DELAY);
            }
            else
            {
                xSemaphoreTake(baton2, portMAX_DELAY);
            }
            for (int j = 0; j < adc_buffer_size; j++)
            { // Storing ADC Value in every element of buffer
                for (int k = 0; k < adc_channel_num; k++)
                { // storing ADC Values of every channel
                    // adc_buffer[i][k][j] = analogRead(adc_pin[k]);
                    adc_buffer[i][k][j] = analogReadMilliVolts(adc_pin[k]);
                }
            }
            if (i == 0)
            {
                xSemaphoreGive(baton1);
            }
            else
            {
                xSemaphoreGive(baton2);
            }
        }

        delay(10);
    }
}

void codeForTask2(void *parameter)
{
    for (;;)
    {
        if (xSemaphoreTake(baton1, (TickType_t)10) == pdTRUE)
        {
            Serial.print("Task1: ");
            Serial.println(adc_buffer[0][0][0]);
            xSemaphoreGive(baton1);
        }
        if (xSemaphoreTake(baton2, (TickType_t)10) == pdTRUE)
        {
            Serial.print("Task2: ");
            Serial.println(adc_buffer[1][0][0]);
            xSemaphoreGive(baton2);
        }
        delay(10);
    }
}

// the setup function runs once when you press reset or power the board
void setup()
{
    Serial.begin(115200);

    // Initialize xSemaphore
    baton1 = xSemaphoreCreateMutex();
    baton2 = xSemaphoreCreateMutex();

    // Initialize Core 1
    xTaskCreatePinnedToCore(
        codeForTask1,
        "led1Task",
        1000,
        NULL,
        1,
        &Task1,
        1);

    delay(500); // needed to start-up task1

    // Initialize Core 2
    xTaskCreatePinnedToCore(
        codeForTask2,
        "led2Task",
        1000,
        NULL,
        1,
        &Task2,
        0);
}

void loop()
{
    delay(10);
}