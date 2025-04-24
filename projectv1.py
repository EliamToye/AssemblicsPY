from gpiozero import DigitalInputDevice, DigitalOutputDevice
import serial
from time import sleep

# GPIO-nummers voor input, output en UART
input_pins = [4, 10, 9, 11, 0, 18, 24, 1, 12, 16]
output_pins = [2, 3, 17, 27, 22, 5, 6, 13, 19, 26, 23, 25, 8, 7]
uart_pins = [14, 15]

# Stel de input pinnen in als DigitalInputDevice
input_devices = {pin: DigitalInputDevice(pin) for pin in input_pins}

# Stel de output pinnen in als DigitalOutputDevice
output_devices = {pin: DigitalOutputDevice(pin) for pin in output_pins}

# Stel de UART poorten in
uart = serial.Serial('/dev/serial0', 9600)  # Hier gebruik je de juiste seriële poort en baudrate

# Functie om de status van de input pins te lezen
def check_input_status():
    print("Input Pin Status:")
    for pin, device in input_devices.items():
        status = "HOOG" if device.is_active else "LAAG"
        print(f"GPIO {pin}: {status}")

# Functie om de output pins in te schakelen
def toggle_output_pins():
    for pin, device in output_devices.items():
        device.on()  # Zet de pin hoog
        sleep(0.5)  # Wacht een halve seconde
        device.off()  # Zet de pin laag
        sleep(0.5)  # Wacht een halve seconde

# Functie voor UART communicatie
def uart_communicate():
    if uart.in_waiting > 0:
        data = uart.read(100)  # Lees 100 bytes
        print("Ontvangen via UART:", data)

try:
    while True:
        check_input_status()  # Toon de status van de input pinnen
        toggle_output_pins()   # Zet de output pinnen aan en uit
        uart_communicate()     # Communiceer via UART
        sleep(1)  # Wacht 1 seconde voor de volgende update

except KeyboardInterrupt:
    print("\nProgramma gestopt.")
    uart.close()  # Sluit de UART verbinding netjes af
