from gpiozero import OutputDevice, InputDevice
from time import sleep
import serial

# === GPIO Outputs ===
signal_r = OutputDevice(2)       # Rood Fixstuur LED
signal_g = OutputDevice(3)       # Groen Fixstuur LED
mc21 = OutputDevice(13)          # Magneetcontact 2.1
mc22 = OutputDevice(19)          # Magneetcontact 2.2
rs485 = OutputDevice(23)         # RS485 aansturing
mc11 = OutputDevice(8)           # Magneetcontact 1.1
mc12 = OutputDevice(7)           # Magneetcontact 1.2

# === GPIO Inputs ===
led_red_out = InputDevice(10)    # Rood LED PCB
led_yellow_out = InputDevice(9)  # Geel LED PCB
led_green2_out = InputDevice(11) # Groen2 LED PCB
led_green1_out = InputDevice(0)  # Groen LED PCB
rs485a = InputDevice(24)         # RS485 aansturing indicatie

# === UART Setup (GPIO14=TX, GPIO15=RX) ===
uart = serial.Serial(
    port='/dev/serial0',  # Dit is een alias voor GPIO14/15 op Raspberry Pi
    baudrate=9600,
    timeout=1
)

print("GPIO-script met UART gestart. Druk op Ctrl+C om te stoppen.\n")

try:
    while True:
        # === UART communicatie voorbeeld ===
        uart.write(b"Hallo vanaf Raspberry Pi!\n")

        if uart.in_waiting > 0:
            received = uart.readline().decode('utf-8').strip()
            print(f"Ontvangen via UART: {received}")

        # === Ingangen lezen ===
        print("--- Ingangen ---")
        print(f"LED Rood PCB       : {'AAN' if led_red_out.value else 'UIT'}")
        print(f"LED Geel PCB       : {'AAN' if led_yellow_out.value else 'UIT'}")
        print(f"LED Groen2 PCB     : {'AAN' if led_green2_out.value else 'UIT'}")
        print(f"LED Groen1 PCB     : {'AAN' if led_green1_out.value else 'UIT'}")
        print(f"RS485 Indicatie    : {'AAN' if rs485a.value else 'UIT'}")

        # === Uitgangen instellen (voorbeeldwaarden) ===
        signal_r.on()
        signal_g.off()
        mc21.on()
        mc22.off()
        rs485.on()
        mc11.off()
        mc12.on()

        print("Wacht 2 seconden...\n")
        sleep(2)

except KeyboardInterrupt:
    print("Script gestopt door gebruiker.")
    uart.close()