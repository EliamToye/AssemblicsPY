from gpiozero import DigitalOutputDevice, DigitalInputDevice
from time import sleep
import signal
import serial
import datetime
import os
import threading
import sys
import tkinter as tk
from typing import List

# Signaal-LED's
signal_r = DigitalOutputDevice(2)   # GPIO 2
signal_g = DigitalOutputDevice(3)   # GPIO 3

# inputs
led_red_out = DigitalInputDevice(10)
led_yellow_out = DigitalInputDevice(9)
led_green2_out = DigitalInputDevice(11)
led_green1_out = DigitalInputDevice(0)
DETECT = DigitalInputDevice(18)#detectie bord

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
SERIENUMMER = "a00"
LOGBESTAND = "testlog.txt"
serienummer = 123

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
    signal_r.on()
    signal_g.on()
    mc21.off()
    mc22.off()
    mc11.off()
    mc12.off()
    rs485.off()
    print("\nGPIO netjes uitgeschakeld. Programma gestopt.")

# Functie 1: Knipper met Signal R en G
def knipper_signalen(tijd=20, interval=0.5):
    print("Knipperen met signalen...")
    eindtijd = tijd / interval / 2
    for _ in range(int(eindtijd)):
        signal_g.on()
        sleep(interval)
        signal_g.off()
        sleep(interval)
    signal_g.on()

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
    
def lees_uart(poort="/dev/ttyUSB0", baudrate=9600, timeout=1):
    global serienummer
    print("Wacht 3 seconden voor UART-start...")
    sleep(1)

    try:
        with serial.Serial(poort, baudrate=baudrate, timeout=timeout) as ser:
            print("Lezen van UART gestart...", flush=True)
            while True:
                if ser.in_waiting > 0:
                    data = ser.readline().decode('utf-8', errors='ignore').strip()
                    if data:
                        serienummer = data
                        print(f"✅ Serienummer ontvangen: {serienummer}", flush=True)
                        break  # Stop met lezen zodra we geldige data hebben
                sleep(0.1)
    except serial.SerialException as e:
        print(f"[UART FOUT] {e}", flush=True)

def log_result(status, stap_omschrijving):
    tijdstip = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if status == "fout":
        regel = f"{tijdstip} | Optie : PIM | Serienummer: {serienummergui} | Status: fout | {stap_omschrijving}"
    else:
        regel = f"{tijdstip} | Optie : PIM | Serienummer: {serienummergui} | Status: correct - {stap_omschrijving}"
    
    print(regel, flush=True)
    with open(LOGBESTAND, "a") as f:
        f.write(regel + "\n")



def vraag_led_status(vraag: str) -> bool:
    root = tk.Tk()
    root.withdraw()
    antwoord = {"result": None}

    def ja():
        antwoord["result"] = True
        popup.destroy()

    def nee():
        antwoord["result"] = False
        popup.destroy()

    popup = tk.Toplevel()
    popup.title("LED Controle")
    tk.Label(popup, text=vraag, font=("Arial", 12)).pack(padx=20, pady=10)
    tk.Button(popup, text="JA", width=10, command=ja).pack(side=tk.LEFT, padx=20, pady=10)
    tk.Button(popup, text="NEE", width=10, command=nee).pack(side=tk.RIGHT, padx=20, pady=10)

    popup.grab_set()
    root.wait_window(popup)
    root.destroy()
    return antwoord["result"]
    
   
        
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
        print("Programma onderbroken met Ctrl+C", flush=True)
    finally:
        afsluiten()


def stap_1_r24v_uart_check():
    if DETECT.value:
        print("Stap 1: Zet R_24V aan (GPIO 23 / RS485)...", flush=True)
        R_24V.on()
        sleep(1)
        print(led_green2_out.value)

        # Lees UART
        lees_uart()
        uart_data = serienummer  # Waarde moet na lees_uart() komen

        if uart_data == SERIENUMMER:
            print("✅ Stap 1: Power up device met 24VDC en controle van module is correct", flush=True)
            return True
        else:
            log_result("fout", f"Stap 1: UART komt niet overeen: ontvangen = {uart_data}, verwacht = {SERIENUMMER}")
            return False
    else:
        log_result("fout", "Stap 1: Detectie is negatief – module niet gedetecteerd")
        return False
        
        
def stap_2_rs485_check():
    print("Stap 2: Zet RS485 aan en controleer RS485A + Gele LED (via gebruiker)...", flush=True)
    rs485.on()
    sleep(0.5)

    rs485a_status = rs485a.value
    gele_led_ok = vraag_led_status("Brand de gele LED?")

    if rs485a_status and gele_led_ok:
        print("correct", "Stap 2 : RS485 ligt uit en gele led brand", flush=True)
        return True
    else:
        log_result("fout", "Stap 2 : RS485 aanleggen en controle op RS485A + bevestiging gele LED via gebruiker")
        return False
    
def stap_3_magneet_fixstuur_check():
    print("Stap 3: Zet MC1.1 en MC2.1 aan, daarna MC1.2 en controleer groene fixstuur LED...", flush=True)
    
    mc11.on()
    mc21.on()
    mc12.on()
    sleep(1)

    green_led_status = vraag_led_status("Branden beide groene LEDs?")
    

    if green_led_status:
        print("correct", "Stap 3 : Beide groene leds branden niet, alleen 1", flush=True)
        return True
    else:
        log_result("fout", "Stap 3 : beide groene LEDs branden")
        return False
    
def stap_4_groen_led1_check():
    print("Stap 4: Zet MC1.2 uit, MC2.2 aan en controleer of groene LED 1 brandt...", flush=True)
    
    mc12.off()
    mc22.on()
    sleep(0.5)

    groen_led1_status = vraag_led_status("Branden beide groene LEDs?")

    if not groen_led1_status:
        print("correct", "Stap 4 : MC2.2 staat aan en 1 groene led brand", flush=True)
        return True
    else:
        log_result("fout", "Stap 4 : MC2.2 staat aan maar beide groene leds branden")
        return False    

def stap_5_rode_led_pcb_check():
    print("Stap 5: Controleer of de rode LED op de PCB brandt...", flush=True)
    sleep(1)
    rood_led_status = vraag_led_status("Brand de rode LED?")

    if rood_led_status:
        print("correct", "Stap 5 : rode LED op de PCB brand", flush=True)
        return True
    else:
        log_result("fout", "Stap 5 : rode led brand niet")
        return False
    
def stap_6_magneet_roodled_check():
    print("Stap 6: Zet MC2.2 uit, MC1.2 aan en controleer of rode LED op PCB brandt...", flush=True)

    mc22.off()
    mc12.on()
    sleep(0.5)

    rood_led_status = vraag_led_status("Brand de rode LED?")

    if not rood_led_status:
        print("correct", "Stap 6 : rode led brandt niet", flush=True)
        return True
    else:
        log_result("fout", "Stap 6 : rode led brand")
        return False
    
def stap_7_afleggen():
    print("Stap 7: Schakel alle uitgangen uit...", flush=True)

    mc11.off()
    mc12.off()
    mc21.off()
    mc22.off()
    signal_r.on()
    signal_g.on()
    rs485.off()
    R_24V.off()

    log_result("correct", "Test is correct")
    return True

# Start het script
if __name__ == "__main__":
    main()
