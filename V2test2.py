from gpiozero import DigitalOutputDevice, DigitalInputDevice
from time import sleep
import signal
import serial

# Signaal-LED's
signal_r = DigitalOutputDevice(2)   # GPIO 2
signal_g = DigitalOutputDevice(3)   # GPIO 3

# Voorbeeld inputs (kun je verder invullen als je wil)
led_red_out = DigitalInputDevice(10)
led_yellow_out = DigitalInputDevice(9)
led_green2_out = DigitalInputDevice(11)
led_green1_out = DigitalInputDevice(0)

# Magneten (outputs)
mc21 = DigitalOutputDevice(13)
mc22 = DigitalOutputDevice(19)
mc11 = DigitalOutputDevice(8)
mc12 = DigitalOutputDevice(7)

# RS485 (output + input)
rs485 = DigitalOutputDevice(23)     # RS485 sturing
rs485a = DigitalInputDevice(24)     # RS485 indicatie (input)
R_24V = DigitalOutputDevice(26)# R_24V (GPIO 26) - Output: 24V extern

# Exit netjes bij Ctrl+C
def afsluiten():
    signal_r.off()
    signal_g.off()
    mc21.off()
    mc22.off()
    mc11.off()
    mc12.off()
    rs485.off()
    print("\nGPIO netjes uitgeschakeld. Programma gestopt.")

# Functie 1: Knipper met Signal R en G
def knipper_signalen(tijd=5, interval=0.5):
    print("Knipperen met signalen...")
    eindtijd = tijd / interval / 2
    for _ in range(int(eindtijd)):
        signal_r.on()
        signal_g.off()
        sleep(interval)
        signal_r.off()
        signal_g.on()
        sleep(interval)
    signal_r.off()
    signal_g.off()

# Functie 2: Doorloop de stappen
def doorloop_stappen():
    print("Start stappen...")

    mc21.on()
    mc22.on()
    print("MC2.1 en MC2.2 ingeschakeld.")
    sleep(2)

    rs485.on()
    print("RS485 aansturing ingeschakeld.")
    sleep(1)

    knipper_signalen(4)

    mc11.on()
    mc12.on()
    print("MC1.1 en MC1.2 ingeschakeld.")
    sleep(2)

    # Lees inputs (voorbeeld)
    print("LED-statussen:")
    print("Rood:", led_red_out.value)
    print("Geel:", led_yellow_out.value)
    print("Groen 1:", led_green1_out.value)
    print("Groen 2:", led_green2_out.value)

    # Uitschakelen
    mc21.off()
    mc22.off()
    mc11.off()
    mc12.off()
    rs485.off()

    print("Stappen beëindigd.")
    
def lees_uart(poort="/dev/serial0", baudrate=9600, timeout=1):
    print("UART uitlezen vanaf ESP...")
    try:
        with serial.Serial(poort, baudrate=baudrate, timeout=timeout) as ser:
            if ser.in_waiting:
                data = ser.readline().decode('utf-8', errors='ignore').strip()
                print(f"[UART] Ontvangen: {data}")
                return data
            else:
                print("[UART] Geen data beschikbaar.")
                return None
    except serial.SerialException as e:
        print(f"[UART FOUT] {e}")
        return None

# Functie 4: Main
def main():
    try:
        doorloop_stappen()
    except KeyboardInterrupt:
        pass
    finally:
        afsluiten()

# Start het script
if __name__ == "__main__":
    main()