from gpiozero import LED
from time import sleep

# Signal_R (GPIO 2) - Output: Rood Led fixstuur
Signal_R = LED(2)

# Signal_G (GPIO 3) - Output: Groen Led fixstuur
Signal_G = LED(3)

# Input_P2B (GPIO 4) - Input: Relais 1 (for detecting state of relay)
# Not used for output, but if you want to read its state:
from gpiozero import Button
Input_P2B = Button(4)

# P3A (GPIO 17) - Output: Eerste kortsluiting (820)
P3A = LED(17)

# P3C (GPIO 27) - Output: Tweede kortsluiting (240)
P3C = LED(27)

# P1.2 (GPIO 22) - Output: Bridge wire
P1_2 = LED(22)

# LED_RED_OUT (GPIO 10) - Input: Rood led pcb
# If you want to read the state, use Button or InputDevice
from gpiozero import Button
LED_RED_OUT = Button(10)

# LED_YELLOW_OUT (GPIO 9) - Input: Led geel pcb
LED_YELLOW_OUT = Button(9)

# LED_GREEN2_OUT (GPIO 11) - Input: Led groen2 pcb
LED_GREEN2_OUT = Button(11)

# LED_GREEN1_OUT (GPIO 0) - Input: Led groen1 pcb
LED_GREEN1_OUT = Button(0)

# BUTTON 2 (GPIO 5) - Output: Knop 2
BUTTON_2 = LED(5)

# BUTTON 1 (GPIO 6) - Output: Knop 1
BUTTON_1 = LED(6)

# R_24V (GPIO 26) - Output: 24V extern
R_24V = LED(26)

# UART RX (GPIO 14) - UART Input: Uart RX
# Not used in this example, but you can use a library like pySerial to communicate
UART_RX = Button(14)

# UART TX (GPIO 15) - UART Output: Uart TX
UART_TX = Button(15)

# RS485 (GPIO 23) - Output: Aansturing
RS485 = LED(23)

# RS485A (GPIO 24) - Input: Indicatie Aansturing
RS485A = Button(24)

# P1.1 (GPIO 25) - Output: Bridge wire
P1_1 = LED(25)

# INPUT_P2C (GPIO 1) - Input: Relais 1
INPUT_P2C = Button(1)

# INPUT_P4B (GPIO 12) - Input: Relais 2
INPUT_P4B = Button(12)

# INPUT_P4C (GPIO 16) - Input: Relais 2
INPUT_P4C = Button(16)

# Example: Blink the red LED (Signal_R) every 10 seconds
while True:
    Signal_R.on()  # Turn on the red LED
    sleep(10)      # Wait for 10 seconds
    Signal_R.off() # Turn off the red LED
    sleep(10)      # Wait for another 10 seconds