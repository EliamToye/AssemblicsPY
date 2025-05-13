from gpiozero import DigitalOutputDevice, DigitalInputDevice
from time import sleep
import signal
import serial
import datetime
import os
import threading
import sys

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

# Stel serienummer globaal in (mag later dynamisch gemaakt worden)
SERIENUMMER = "---"
LOGBESTAND = "testlog.txt"

# Serienummer verkrijgen
# Verkrijg het serienummer uit de commandoregelargumenten
if len(sys.argv) > 1:
    serienummergui = sys.argv[1]
    print(f"Serienummer ontvangen: {serienummergui}")
else:
    print("Fout: Geen serienummer opgegeven.")
    sys.exit(1)
if not serienummergui.isdigit():
    print("Fout: Serienummer moet uit cijfers bestaan.")
    sys.exit(1)


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

    if not stap_1_r24v_uart_check():
        return

    if not stap_2_rs485_check():
        return

    if not stap_3_magneet_fixstuur_check():
        return
    
    if not stap_4_groen_led1_check():
        return
    
    if not stap_5_rode_led_pcb_check():
        return
    
    if not stap_6_magneet_roodled_check():
        return
    
    if not stap_7_afleggen():
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
        regel = f"{tijdstip} | Optie : PIM | Serienummer: {serienummergui} | Status: fout | {stap_omschrijving}"
    else:
        regel = f"{tijdstip} | Optie : PIM | Serienummer: {serienummergui} | Status: correct - {stap_omschrijving}"
    
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


def stap_1_r24v_uart_check():
    print("Stap 1: Zet R_24V aan (GPIO 23 / RS485)...")
    R_24V.on()
    sleep(0.5)

    # Lees UART
    uart_data = lees_uart()
    if uart_data == SERIENUMMER:
        print("correct", "Stap 1 : Power up device met 24VDC en controle van module")
        return True
    else:
        log_result("fout", "Stap 1 : Power up device met 24VDC en controle van module")
        return False

def stap_2_rs485_check():
    print("Stap 2: Zet RS485 aan en controleer RS485A + Gele LED...")
    rs485.on()
    sleep(0.5)

    rs485a_status = rs485a.value
    yellow_led_status = led_yellow_out.value

    if rs485a_status == 1 and yellow_led_status == 1:
        print("correct", "Stap 2 : RS485 aanleggen en controle op RS485A + controle of gele LED aan ligt")
        return True
    else:
        log_result("fout", "Stap 2 : RS485 aanleggen en controle op RS485A + controle of gele LED aan ligt")
        return False
    
def stap_3_magneet_fixstuur_check():
    print("Stap 3: Zet MC1.1 en MC2.1 aan, daarna MC1.2 en controleer groene fixstuur LED...")
    
    mc11.on()
    mc21.on()
    sleep(0.5)
    mc12.on()
    sleep(0.5)

    green_led_status = led_green1_out.value

    if green_led_status == 0:
        print("correct", "Stap 3 : Magneetcontacten schakelen en controle of groene fixstuur LED brandt")
        return True
    else:
        log_result("fout", "Stap 3 : Magneetcontacten schakelen en controle of groene fixstuur LED brandt")
        return False
    
def stap_4_groen_led1_check():
    print("Stap 4: Zet MC1.2 uit, MC2.2 aan en controleer of groene LED 1 brandt...")
    
    mc12.off()
    mc22.on()
    sleep(0.5)

    groen_led1_status = led_green1_out.value

    if groen_led1_status == 1:
        print("correct", "Stap 4 : MC1.2 uitschakelen, MC2.2 inschakelen en controle op groene LED 1")
        return True
    else:
        log_result("fout", "Stap 4 : MC1.2 uitschakelen, MC2.2 inschakelen en controle op groene LED 1")
        return False    

def stap_5_rode_led_pcb_check():
    print("Stap 5: Controleer of de rode LED op de PCB brandt...")

    rood_led_status = led_red_out.value

    if rood_led_status == 1:
        print("correct", "Stap 5 : Controle of de rode LED op de PCB brandt")
        return True
    else:
        log_result("fout", "Stap 5 : Controle of de rode LED op de PCB brandt")
        return False
    
def stap_6_magneet_roodled_check():
    print("Stap 6: Zet MC2.2 uit, MC1.2 aan en controleer of rode LED op PCB brandt...")

    mc22.off()
    mc12.on()
    sleep(0.5)

    rood_led_status = led_red_out.value

    if rood_led_status == 1:
        print("correct", "Stap 6 : MC2.2 uitschakelen, MC1.2 inschakelen en controle op rode LED PCB")
        return True
    else:
        log_result("fout", "Stap 6 : MC2.2 uitschakelen, MC1.2 inschakelen en controle op rode LED PCB")
        return False
    
def stap_7_afleggen():
    print("Stap 7: Schakel alle uitgangen uit...")

    mc11.off()
    mc12.off()
    mc21.off()
    mc22.off()
    signal_r.off()
    signal_g.off()
    rs485.off()
    R_24V.off()

    print("correct", "Stap 7 : Alle uitgangen uitgeschakeld")
    return True

# Start het script
if __name__ == "__main__":
    main()