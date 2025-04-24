from gpiozero import DigitalInputDevice
from time import sleep
from datetime import datetime

# Veelgebruikte GPIO-pinnen (BCM-nummering)
gpio_pins = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
             12, 13, 14, 15, 16, 17, 18, 19,
             20, 21, 22, 23, 24, 25, 26, 27]

def print_gpio_status():
    print(f"\n[ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ] GPIO status (via gpiozero):")
    print("-" * 40)
    for pin in gpio_pins:
        try:
            device = DigitalInputDevice(pin)
            status = "HOOG (1)" if device.value else "LAAG (0)"
            print(f"GPIO {pin:>2}: {status}")
        except Exception as e:
            print(f"GPIO {pin:>2}: Niet beschikbaar ({e})")

# Herhaal dit elke 5 minuten
try:
    while True:
        print_gpio_status()
        print("Volgende update over 5 minuten...\n")
        sleep(5 * 60)  # 5 minuten wachten

except KeyboardInterrupt:
    print("\nScript handmatig gestopt met Ctrl+C.")
