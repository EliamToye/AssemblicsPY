from gpiozero import LED, Button, InputDevice, OutputDevice
import serial
import time

# Outputs
Signal_R = LED(2)
Signal_G = LED(3)
P3A = LED(17)
P3C = LED(27)
P1_2 = LED(22)
LED_RED_OUT = LED(10)
LED_YELLOW_OUT = LED(9)
LED_GREEN2_OUT = LED(11)
LED_GREEN1_OUT = LED(0)   # GPIO0
R_24V = LED(26)
RS485 = OutputDevice(23, active_high=True, initial_value=False)
RS485A = OutputDevice(24, active_high=True, initial_value=False)
P1_1 = LED(25)

# Inputs
Input_P2B = InputDevice(4, pull_up=False)
Button2 = Button(5, pull_up=False)
Button1 = Button(6, pull_up=False)
Input_P2C = InputDevice(1, pull_up=False)  # GPIO1
Input_P4B = InputDevice(12, pull_up=False)
Input_P4C = InputDevice(16, pull_up=False)

# UART
try:
    uart = serial.Serial(
        port='/dev/serial0',  # automatisch gekoppeld aan GPIO14 (TX) en GPIO15 (RX)
        baudrate=9600,
        timeout=1
    )
    print("UART verbinding geopend.")
except serial.SerialException as e:
    print(f"Fout bij openen UART: {e}")
    uart = None

def lees_inputs():
    inputs = {
        "Input_P2B": Input_P2B.value,
        "Button2": Button2.is_pressed,
        "Button1": Button1.is_pressed,
        "Input_P2C": Input_P2C.value,
        "Input_P4B": Input_P4B.value,
        "Input_P4C": Input_P4C.value,
    }
    return inputs

def toon_inputs(inputs):
    print("\n--- Inputstatus ---")
    for naam, waarde in inputs.items():
        print(f"{naam}: {'ACTIEF' if waarde else 'niet actief'}")
    print("--------------------")

def lees_uart():
    if uart and uart.in_waiting > 0:
        data = uart.readline().decode('utf-8').strip()
        if data:
            print(f"Ontvangen via UART: {data}")

def main_loop():
    try:
        while True:
            inputs = lees_inputs()
            toon_inputs(inputs)

            lees_uart()

            time.sleep(1)  # elke seconde updaten
    except KeyboardInterrupt:
        print("Programma gestopt.")

if __name__ == "__main__":
    main_loop()