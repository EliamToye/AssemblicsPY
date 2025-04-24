from gpiozero import DigitalInputDevice
from time import sleep

# Maak een lijst van pinnen die je wil controleren, uitgezonderd GPIO2 en GPIO3
gpio_pins = [4, 17, 27, 22, 10, 9, 11, 5, 6, 13, 19, 26, 14, 15, 18, 23, 24, 25, 8, 7]

# Stel de pinnen in als inputs
pins = {}
for pin in gpio_pins:
    pins[pin] = DigitalInputDevice(pin)

# Functie om de status van de pinnen te controleren
def check_gpio_status():
    print("GPIO status overzicht (BCM):")
    print("------------------------------")
    for pin, device in pins.items():
        status = "HOOG" if device.is_active else "LAAG"
        print(f"GPIO {pin}: {status}")

try:
    while True:
        check_gpio_status()  # Check en toon de status van alle pinnen
        sleep(1)  # Wacht 1 seconde voor de volgende update

except KeyboardInterrupt:
    print("\nProgramma gestopt.")
