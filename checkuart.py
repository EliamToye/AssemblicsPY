import serial

# Pas aan indien nodig, kan bv. /dev/ttyUSB1 zijn
PORT = '/dev/ttyUSB0'
BAUDRATE = 115200

try:
    with serial.Serial(PORT, BAUDRATE, timeout=1) as ser:
        print(f"Luisteren naar {PORT} @ {BAUDRATE} baud")
        while True:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                print(f"[UART] {line}")
except serial.SerialException as e:
    print(f"Fout bij openen van seriële poort: {e}")