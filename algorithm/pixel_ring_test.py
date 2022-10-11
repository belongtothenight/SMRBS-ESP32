from pixel_ring import pixel_ring
from gpiozero import LED
from time import sleep

power = LED(5)
power.on()

pixel_ring.set_brightness(10)

while True:
    pixel_ring.open1()
    pixel_ring.open2()
    pixel_ring.open3()
    pixel_ring.open4()
    

