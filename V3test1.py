from gpiozero import DigitalOutputDevice, DigitalInputDevice
from time import sleep
import signal
import serial
import datetime
import os
import threading

# Signaal-LED's
signal_r = DigitalOutputDevice(2)   # GPIO 2
signal_g = DigitalOutputDevice(3)   # GPIO 3

Input_P2B = DigitalInputDevice(4)# Input_P2B (GPIO 4) - Input: Relais 1 (for detecting state of relay)
P3A = DigitalOutputDevice(17)# P3A (GPIO 17) - Output: Eerste kortsluiting (820)
P3C = DigitalOutputDevice(27)# P3C (GPIO 27) - Output: Tweede kortsluiting (240)
P1_2 = DigitalOutputDevice(22)# P1.2 (GPIO 22) - Output: Bridge wire
LED_RED_OUT = DigitalInputDevice(10)# LED_RED_OUT (GPIO 10) - Input: Rood led pcb
LED_YELLOW_OUT = DigitalInputDevice(9)# LED_YELLOW_OUT (GPIO 9) - Input: Led geel pcb
LED_GREEN2_OUT = DigitalInputDevice(11)# LED_GREEN2_OUT (GPIO 11) - Input: Led groen2 pcb
LED_GREEN1_OUT = DigitalInputDevice(0)# LED_GREEN1_OUT (GPIO 0) - Input: Led groen1 pcb
BUTTON_2 = DigitalOutputDevice(5)# BUTTON 2 (GPIO 5) - Output: Knop 2
BUTTON_1 = DigitalOutputDevice(6)# BUTTON 1 (GPIO 6) - Output: Knop 1
R_24V = DigitalOutputDevice(26)# R_24V (GPIO 26) - Output: 24V extern
RS485 = DigitalOutputDevice(23)# RS485 (GPIO 23) - Output: Aansturing
RS485A = DigitalInputDevice(24)# RS485A (GPIO 24) - Input: Indicatie Aansturing
P1_1 = DigitalOutputDevice(25)# P1.1 (GPIO 25) - Output: Bridge wire
INPUT_P2C = DigitalInputDevice(1)# INPUT_P2C (GPIO 1) - Input: Relais 1
INPUT_P4B = DigitalInputDevice(12)# INPUT_P4B (GPIO 12) - Input: Relais 2
INPUT_P4C = DigitalInputDevice(16)# INPUT_P4C (GPIO 16) - Input: Relais 2

# variabelen
SERIENUMMER = "---"
LOGBESTAND = "testlog.txt"

# Exit netjes bij Ctrl+C
def afsluiten():
    signal_r.off()
    signal_g.off()
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

    if not stap_1():
        return

    if not stap_2():
        return

    if not stap_3():
        return
    
    if not stap_4():
        return
    
    if not stap_5():
        return
    
    if not stap_6():
        return
    
    if not stap_7():
        return
    
    if not stap_8():
        return
    
    if not stap_9():
        return
    
    if not stap_10():
        return
    
    if not stap_11():
        return
    
    if not stap_12():
        return
    
    if not stap_13():
        return
    
    if not stap_14():
        return
    
    if not stap_15():
        return
    
    if not stap_16():
        return
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

def log_result(status, stap_omschrijving):
    tijdstip = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if status == "fout":
        regel = f"{tijdstip} | Serienummer: {SERIENUMMER} | Status: fout | {stap_omschrijving}"
    else:
        regel = f"{tijdstip} | Serienummer: {SERIENUMMER} | Status: correct - {stap_omschrijving}"
    
    print(regel)
    with open(LOGBESTAND, "a") as f:
        f.write(regel + "\n")
        
# Functie 5: Main
def main():
    try:
        # Start knipper_signalen in aparte thread
        knipper_thread = threading.Thread(target=knipper_signalen)
        knipper_thread.daemon = True  # stopt automatisch mee bij afsluiten
        knipper_thread.start()

        # Voer stappen door op hoofdthread
        doorloop_stappen()

    except KeyboardInterrupt:
        print("Programma onderbroken met Ctrl+C")
    finally:
        afsluiten()

def stap_1():
    try:
        # Zet BUTTON_1 en BUTTON_2 aan
        BUTTON_1.on()
        BUTTON_2.on()
        
        # Zet R24V aan
        R_24V.on()

        # Wacht even om de instellingen te laten doorvoeren (indien nodig)
        sleep(1)
        
        BUTTON_1.off()
        BUTTON_2.off()

        # Controleer of de outputs goed zijn ingeschakeld
        if R_24V.is_active:
            log_result("correct", "BUTTON_1 en BUTTON_2 zijn aan, en R24V is aan.")
            return True
        else:
            log_result("fout", "Niet alle outputs zijn correct ingeschakeld in stap 1.")
            return False

    except Exception as e:
        log_result("fout", f"Fout in stap 1: {str(e)}")
        return False


def stap_2():
    try:
        # Lees het serienummer via UART
        serienummer = lees_uart()  # gebruik de bestaande lees_uart functie die je hebt

        # Controleer of het serienummer correct is
        if serienummer and serienummer == SERIENUMMER:  # vergelijk met verwachte serienummer
            log_result("correct", f"Serienummer {serienummer} komt overeen.")
            return True
        else:
            log_result("fout", f"Fout: Serienummer is {serienummer}, maar verwacht {SERIENUMMER}.")
            return False

    except Exception as e:
        log_result("fout", f"Fout in stap 2: {str(e)}")
        return False
    
    
def stap_3():
    try:
        print("Stap 3: BUTTON_2 aan, wacht op UART = S03...")

        # Zet BUTTON_2 aan
        BUTTON_2.on()
        sleep(0.5)  # kleine vertraging

        max_herhalingen = 10  # maximaal aantal pogingen om eindeloos lussen te vermijden
        pogingen = 0

        while pogingen < max_herhalingen:
            uart_data = lees_uart()

            if uart_data == "S03":
                log_result("correct", "UART status is S03 na drukken van BUTTON_2/BUTTON_1.")
                return True
            else:
                log_result("fout", f"UART gaf '{uart_data}' i.p.v. 'S03'. Probeer opnieuw met BUTTON_1.")
                BUTTON_1.on()
                sleep(1)  # wacht even voor ESP update
                BUTTON_1.off()
                pogingen += 1

        log_result("fout", "UART status werd niet 'S03' na meerdere pogingen.")
        return False

    except Exception as e:
        log_result("fout", f"Fout in stap 3: {str(e)}")
        return False
    
    
def stap_4():
    try:
        print("Stap 4: Controleer groene LED 2 en gele LED...")

        groen_ok = LED_GREEN2_OUT.value
        geel_ok = LED_YELLOW_OUT.value

        if groen_ok and geel_ok:
            log_result("correct", "Groene LED 2 en gele LED branden.")
            return True
        else:
            foutmelding = "Fout: "
            if not groen_ok:
                foutmelding += "Groene LED 2 brandt niet. "
            if not geel_ok:
                foutmelding += "Gele LED brandt niet."
            log_result("fout", foutmelding.strip())
            return False

    except Exception as e:
        log_result("fout", f"Fout in stap 4: {str(e)}")
        return False
    
    

# Start het script
if __name__ == "__main__":
    main()