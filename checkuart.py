import serial
import time

print("USB UART test gestart.")

# ? Pas deze poort aan op basis van `ls /dev/tty*` of `dmesg | grep tty`
PORT = "/dev/ttyUSB0"  # of bv. /dev/ttyACM0
BAUDRATE = 9600

try:
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
    time.sleep(2)  # Geef de verbinding even tijd om op te starten
    print(f"Verbonden met {PORT} op {BAUDRATE} baud.\n")

    while True:
        try:
            if ser.in_waiting > 0:
                data = ser.readline().decode(errors='ignore').strip()
                print(f"[RX] Ontvangen: {data}")
        except serial.SerialException as e:
            print("[Fout tijdens lezen]:", e)
            break
        except OSError as e:
            print("[OS Fout]:", e)
            break
except serial.SerialException as e:
    print("Fout bij openen seriele poort:", e)
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Seriele poort gesloten.")