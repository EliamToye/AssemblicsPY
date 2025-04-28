from gpiozero import LED
from time import sleep

# Set up the LED on GPIO 2
led = LED(2)

while True:
    led.on()  # Turn on the LED
    sleep(10)  # Wait for 10 seconds
    led.off()  # Turn off the LED
    sleep(10)  # Wait for another 10 seconds