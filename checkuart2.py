# -*- coding: utf-8 -*-
import serial
import time

def main():
    # Pas dit aan naar jouw UART device
    uart_port = '/dev/serial0'  # alias voor GPIO UART op Pi
    baud_rate = 9600  # Pas aan aan je zender

    try:
        ser = serial.Serial(uart_port, baud_rate, timeout=1)
        print(f"Verbonden met UART op {uart_port} ({baud_rate} baud)")
        time.sleep(2)  # Wacht even tot verbinding stabiel is

        while True:
            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8', errors='replace').strip()
                print(f"Ontvangen: {data}")

    except serial.SerialException as e:
        print(f"Fout met seriële poort: {e}")

    except KeyboardInterrupt:
        print("\nAfsluiten...")

    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()

if __name__ == "__main__":
    main()
