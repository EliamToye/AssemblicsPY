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
DETECT = DigitalInputDevice(18)#detectie bord




# Serienummer verkrijgen
# Verkrijg het serienummer uit de commandoregelargumenten
if len(sys.argv) > 1:
    serienummergui = sys.argv[1]
    print(f"Serienummer ontvangen: {serienummergui}", flush=True)
else:
    print("Fout: Geen serienummer opgegeven.")
    sys.exit(1)
if not serienummergui.isdigit():
    print("Fout: Serienummer moet uit cijfers bestaan.", flush=True)
    sys.exit(1)

# variabelen
SERIENUMMER = serienummergui
LOGBESTAND = "/home/Assemblics/shared/AssemblicsPY/testlog.txt"
serienummer = 123

# Exit netjes bij Ctrl+C
def afsluiten():
    signal_r.on()
    signal_g.on()
    P3A.off()
    P3C.off()
    P1_1.off()
    P1_2.off()
    BUTTON_1.off()
    BUTTON_2.off()
    R_24V.off()
    RS485.off()
    print("\nGPIO netjes uitgeschakeld. Programma gestopt.", flush=True)

# Functie 1: Knipper met Signal R en G
def knipper_signalen(tijd=15, interval=0.5,poort="/dev/ttyUSB0", baudrate=9600, timeout=1, wacht_seconden=2):
    print("Knipperen met signalen...")
    eindtijd = tijd / interval / 2
    for _ in range(int(eindtijd)):
        signal_g.off()
        sleep(interval)
        signal_g.on()
        sleep(interval)
    signal_g.off()
    
    
# Functie 1b: uart  
def lees_uart(poort="/dev/ttyUSB0", baudrate=9600, timeout=1):
    global serienummer
    print("Wacht 3 seconden voor UART-start...")
    #sleep(1)

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
    

# Functie 2: Doorloop de stappen
def doorloop_stappen():
    print("Start stappen...", flush=True)

    if not stap_1():
        return

    if not stap_2():
        return

    if not stap_3():
        return
    
    #if not stap_4():
        #return
    
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
    
    print("Stappen beëindigd.", flush=True)
    

def log_result(status, stap_omschrijving):
    if status == "fout":
        tijdstip = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        regel = f"{tijdstip} | Optie : RISP EL | Serienummer: {SERIENUMMER} | Status: fout | {stap_omschrijving}"
    else:
        regel = f"{tijdstip} | Optie : RISP EL | Serienummer: {SERIENUMMER} | Status: correct - {stap_omschrijving}"
    print(regel, flush=True)
    with open(LOGBESTAND, "a") as f:
        f.write(regel + "\n")
        
        
# Functie 5: Main
def main():
    try:
        signal_g.on()
        signal_r.on()
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

def stap_1():
  if DETECT.value:
    try:
        print("Stap 1: Zet BUTTON_1 en BUTTON_2 aan, controleer R24V...", flush=True)
        # Zet BUTTON_1 en BUTTON_2 aan
        BUTTON_1.on()
        BUTTON_2.on()
        
        # Zet R24V aan
        R_24V.on()

        # Wacht even om de instellingen te laten doorvoeren (indien nodig)
        sleep(0.5)
        
        BUTTON_1.off()
        BUTTON_2.off()
        
        sleep(0.5)

        # Controleer of de outputs goed zijn ingeschakeld
        if R_24V.is_active:
            print("correct", "BUTTON_1 en BUTTON_2 zijn aan, en R24V is aan.", flush=True)
            return True
        else:
            log_result("fout", "24V is niet ingeschakeld.")
            return False
            
    except Exception as e:
        log_result("fout", f"Fout in stap 1: {str(e)}")
        return False
        
  else:
      log_result("fout","print detectie is negatief")
        


def stap_2():
    try:
        print("Stap 2: serienummer uitlezen via UART...")
        # Lees het serienummer via UART
        
        signal_r.off
        if INPUT_P2C.value and INPUT_P4C.value:
            log_result("fout", "verkeerde PCB aangesloten")
            return False
        else:
            print("correct", "Relais PCB")
            sleep(0.2)
            # Controleer of het serienummer correct is
            lees_uart()
            if serienummer[-2:] == SERIENUMMER[-2:]:  # vergelijk met verwachte serienummer
              print("correct", f"Serienummer {serienummer} komt overeen.")
              signal_r.on()
              return True
            else:
              log_result("fout", f"Fout: Serienummer is {serienummer}, maar verwacht {SERIENUMMER}.")
              signal_r.on()
              return False
        

    except Exception as e:
        log_result("fout", f"Fout in stap 2: {str(e)}")
        return False
    
  
def stap_3():
    try:
        print("Stap 3: BUTTON_2 aan, wacht op UART = S03...", flush=True)

        # Zet BUTTON_2 aan
        BUTTON_2.on()
        sleep(0.2)  # kleine vertraging
        BUTTON_2.off()
        sleep(0.2)  # kleine vertraging

        max_herhalingen = 10  # maximaal aantal pogingen om eindeloos lussen te vermijden
        pogingen = 0

        while pogingen < max_herhalingen:
            lees_uart()
            uart_data = serienummer

            if uart_data == "503":
                print("correct", "UART status is S03 na drukken van BUTTON_2/BUTTON_1.", flush=True)
                BUTTON_1.on()
                BUTTON_2.on()
                sleep(3)
                BUTTON_1.off()
                BUTTON_2.off()
                return True
            else:
                print("fout", f"UART gaf '{uart_data}' i.p.v. 'S03'. Probeer opnieuw met BUTTON_1.")
                BUTTON_1.on()
                sleep(0.2)  # wacht even voor ESP update
                BUTTON_1.off()
                pogingen += 1

        log_result("fout", "UART status werd niet 'S03' na meerdere pogingen.")
        return False

    except Exception as e:
        log_result("fout", f"Fout in stap 3: {str(e)}")
        return False
    
    
def stap_4():
    try:
        print("Stap 4: Controleer groene LED 2 en gele LED...", flush=True)

        groen_ok = LED_GREEN2_OUT.value
        geel_ok = LED_YELLOW_OUT.value
        p2c_ok = INPUT_P2C.value
        p4c_ok = INPUT_P4C.value
        p2b_ok = Input_P2B.value
        p4b_ok = INPUT_P4B.value
        signal_r.off()
        
        print(f"P2C: {p2c_ok}, P4C: {p4c_ok}, P4B: {p4b_ok}, P2B: {p2b_ok}")

        if groen_ok and geel_ok and not p2c_ok and not p4c_ok and p2b_ok and p4b_ok:
            print("correct", "Groene LED 2 en gele LED branden. Relais's zijn open.", flush=True)
            return True
        else:
            foutmelding = "Fout: "
            if not groen_ok:
                foutmelding += "Groene LED 2 brandt niet. "
            if not geel_ok:
                foutmelding += "Gele LED brandt niet."
            if p2c_ok:
                foutmelding += "Relais 1 is niet open.controle op U6"
            if not p2b_ok:
                foutmelding += "Relais 1 is niet open.controle op U6"
            if p4c_ok:
                foutmelding += "Relais 2 is niet open.controle op U5"
            if not p4b_ok:
                foutmelding += "Relais 2 is niet open.controle op U5"
            log_result("fout", foutmelding.strip())
            return False

    except Exception as e:
        log_result("fout", f"Fout in stap 4: {str(e)}")
        return False
    
    
def stap_5():
    try:
        print("Stap 5: P3A aan, controle groene LED 2...", flush=True)
        p2c_ok = INPUT_P2C.value
        p4c_ok = INPUT_P4C.value
        p2b_ok = Input_P2B.value
        p4b_ok = INPUT_P4B.value
        signal_r.off()
        sleep(0.2)
        P3A.on()
        
        #print(f"P2C: {p2c_ok}, P4C: {p4c_ok}, P4B: {p4b_ok}, P2B: {p2b_ok}")

        if LED_GREEN2_OUT.value and not p2c_ok and not p4c_ok and not p2b_ok and p4b_ok:
            print("correct", "Groene LED 2 brandt na inschakelen P3A. Relais 2 is open", flush=True)
            return True
        else:
            foutmelding = "Fout: "
            if not LED_GREEN2_OUT.value:
                foutmelding += "Groene LED 2 brandt niet. 240 ohm weerstand is niet goed aangesloten. "
            if not p2c_ok:
                foutmelding += "Relais 1 is niet open.controle op U6"
            if p2b_ok:
                foutmelding += "Relais 1 is niet open.controle op U6"
            if not p4c_ok:
                foutmelding += "Relais 2 is niet open.controle op U5"
            if not p4b_ok:
                foutmelding += "Relais 2 is niet open.controle op U5"
            log_result("fout", foutmelding.strip())
            return False

    except Exception as e:
        log_result("fout", f"Fout in stap 5: {str(e)}")
        return False
    
def stap_6():
    try:
        print("Stap 6: P3A uit, controle groene LED 2 en rode LED...", flush=True)
        P3A.off()
        sleep(0.2)  # geef de hardware tijd om te schakelen

        groen_status = LED_GREEN2_OUT.value
        rood_status = LED_RED_OUT.value
        p2c_ok = INPUT_P2C.value
        p4c_ok = INPUT_P4C.value
        p2b_ok = Input_P2B.value
        p4b_ok = INPUT_P4B.value
        
        

        if groen_status and rood_status and not p2c_ok and not p4c_ok and not p2b_ok and not p4b_ok:
            print("correct", "Groene LED 2 en rode LED branden beide.Relais 1 is open. Relais 2 is gesloten.", flush=True)
            return True
        else:
            foutmelding = "Fout: "
            if not groen_status:
                foutmelding += "Groene LED 2 brandt niet. 1k60 weerstand is niet goed aangesloten. "
            if not rood_status:
                foutmelding += "Rode LED brandt niet. 1k60 weerstand is niet goed aangesloten. "
            if p2c_ok:
                foutmelding += "Relais 1 is niet open.controle op U6"
            if p2b_ok:
                foutmelding += "Relais 1 is niet open.controle op U6"
            if not p4c_ok:
                foutmelding += "Relais 2 is open.controle op U5"
            if not p4b_ok:
                foutmelding += "Relais 2 is open.(p4b)controle op U5"
            log_result("fout", foutmelding.strip())
            return False

    except Exception as e:
        log_result("fout", f"Fout in stap 6: {str(e)}")
        return False
    
    
def stap_7():
    try:
        print("Stap 7: P3A en P3C aan, controle groene LED 2 en gele LED...", flush=True)

        P3A.on()
        P3C.on()
        sleep(0.2)  # hardware de tijd geven om te schakelen

        groen_status = LED_GREEN2_OUT.value
        geel_status = LED_YELLOW_OUT.value
        p2c_ok = INPUT_P2C.value
        p4c_ok = INPUT_P4C.value
        p2b_ok = Input_P2B.value
        p4b_ok = INPUT_P4B.value
        
        

        if groen_status and geel_status and not p2c_ok and not p4c_ok and not p2b_ok and not p4b_ok:
            print("correct", "Groene LED 2 en gele LED branden beide.Relais 1 is gesloten. Relais 2 is open.", flush=True)
            return True
        else:
            foutmelding = "Fout: "
            if not groen_status:
                foutmelding += "Groene LED 2 brandt niet. Fout bij aansluiten van 240 en 820 ohm weerstand. "
            if not geel_status:
                foutmelding += "Gele LED brandt niet. fout bij aansluiten van 240 en 820 ohm weerstand. "
            if not p2c_ok:
                foutmelding += "Relais 1 is open.controle op U6"
            if not p2b_ok:
                foutmelding += "Relais 1 is open.controle op U6"
            if p4c_ok:
                foutmelding += "Relais 2 is niet open.controle op U5"
            if p4b_ok:
                foutmelding += "Relais 2 is niet open.controle op U5"
            log_result("fout", foutmelding.strip())
            return False

    except Exception as e:
        log_result("fout", f"Fout in stap 7: {str(e)}")
        return False
    
    
def stap_8():
    try:
        print("Stap 8: P3A en P3C uit, controle op UART = 'S02'...", flush=True)

        P3A.off()
        P3C.off()
        sleep(0.2)
        signal_r.on()

        poging = 0
        while True:
            lees_uart()
            data = serienummer
            if data == "502":
                print("correct", "UART geeft 'S02' door.", flush=True)
                BUTTON_1.on()
                BUTTON_2.on()
                sleep(3)
                BUTTON_1.off()
                BUTTON_2.off()
                return True

            poging += 1
            print(f"[Stap 8] Poging {poging}: UART was '{data}', BUTTON_1 schakelen...", flush=True)

            BUTTON_1.on()
            sleep(0.2)
            BUTTON_1.off()
            sleep(0.2)
            BUTTON_1.on()
            sleep(0.2)
            BUTTON_1.off()
            sleep(0.2)
            BUTTON_1.on()
            sleep(0.2)
            BUTTON_1.off()
            sleep(0.2)

            if poging > 10:
                log_result("fout", "Maximale pogingen bereikt zonder 'S02' van UART.")
                return False

    except Exception as e:
        log_result("fout", f"Fout in stap 8: {str(e)}")
        return False
    
def stap_9():
    try:
        print("Stap 9: Controle of groene LED 2 brandt...", flush=True)
        signal_r.off()
        p4c_ok = INPUT_P4C.value
        p2b_ok = Input_P2B.value
        p4b_ok = INPUT_P4B.value
        p2c_ok = INPUT_P2C.value
        
        

        if LED_GREEN2_OUT.value and not p2c_ok and not p4c_ok and not p2b_ok and not p4b_ok:
            print("correct", "Groene LED 2 brandt. en relais's zijn gesloten.", flush=True)
            return True
        else:
            foutmelding = "Fout: "
            if not LED_GREEN2_OUT.value:
                foutmelding += "Groene LED 2 brandt niet. Controle van p1"
            if not p2c_ok:
                foutmelding += "Relais 1 is open.controle op U6"
            if not p2b_ok:
                foutmelding += "Relais 1 is open.controle op U6"
            if not p4c_ok:
                foutmelding += "Relais 2 is open.controle op U5"
            if not p4b_ok:
                foutmelding += "Relais 2 is open.controle op U5"
            log_result("fout", foutmelding.strip())
            return False

    except Exception as e:
        log_result("fout", f"Fout in stap 9: {str(e)}")
        return False
    
def stap_10():
    try:
        print("Stap 10: Beide bridgewires aan, controle op groene LED 2 en rode LED...", flush=True)

        P1_1.on()
        P1_2.on()
        sleep(0.2)  # even wachten voor stabilisatie

        groen = LED_GREEN2_OUT.value
        rood = LED_RED_OUT.value
        p2c_ok = INPUT_P2C.value
        p4c_ok = INPUT_P4C.value
        p2b_ok = Input_P2B.value
        p4b_ok = INPUT_P4B.value
        
        print(f"P2C: {p2c_ok}, P4C: {p4c_ok}, P4B: {p4b_ok}, P2B: {p2b_ok}")

        if groen and rood and not p2c_ok and not p4c_ok and not p2b_ok and not p4b_ok:
            print("correct", "Bridgewires aan: groene LED 2 en rode LED branden.Relais 1 is open. Relais 2 is gesloten.", flush=True)
            return True
        else:
            foutmelding = "Bridgewires actief, maar status klopt niet:"
            if not groen:
                foutmelding += " groene LED 2 uit.Controle van p1"
            if not rood:
                foutmelding += " rode LED uit.Controle van p1"
            if p2c_ok:
                foutmelding += "Relais 1 is niet open.controle op U6"
            if p2b_ok:
                foutmelding += "Relais 1 is niet open.controle op U6"
            if not p4c_ok:
                foutmelding += "Relais 2 is open.controle op U5"
            if not p4b_ok:
                foutmelding += "Relais 2 is open.controle op U5"
            log_result("fout", foutmelding)
            return False

    except Exception as e:
        log_result("fout", f"Fout in stap 10: {str(e)}")
        return False
    
def stap_11():
    try:
        print("Stap 11: Bridgewires uit, controle op UART = 'S03'...", flush=True)

        P1_1.off()
        P1_2.off()
        sleep(0.2)

        poging = 0
        while True:
            lees_uart()
            data = serienummer
            if data == "503":
                print("correct", "UART geeft 'S03' door.", flush=True)
                BUTTON_1.on()
                BUTTON_2.on()
                sleep(3)
                BUTTON_1.off()
                BUTTON_2.off()
                return True

            poging += 1
            print(f"[Stap 11] Poging {poging}: UART was '{data}', BUTTON_1 schakelen...", flush=True)

            BUTTON_1.on()
            sleep(0.2)
            BUTTON_1.off()
            sleep(0.2)  # wacht voor volgende poging

            if poging > 10:
                log_result("fout", "Maximale pogingen bereikt zonder 'S03' van UART.")
                return False

    except Exception as e:
        log_result("fout", f"Fout in stap 11: {str(e)}")
        return False
    
def stap_12():
    try:
        print("Stap 12: Controle of groene LED 2 brandt...", flush=True)

        if LED_GREEN2_OUT.value:
            print("correct", "Groene LED 2 brandt.", flush=True)
            return True
        else:
            log_result("fout", "Groene LED 2 brandt niet.Software goed ingeladen? connectie problemen?")
            return False

    except Exception as e:
        log_result("fout", f"Fout in stap 12: {str(e)}")
        return False
    
def stap_13():
    try:
        print("Stap 13: Zet alle uitgangen op 0 voor veiligheid...", flush=True)

        # Zet alle relevante GPIO-uitgangen uit
        P1_1.off()
        P1_2.off()
        P3A.off()
        P3C.off()
        BUTTON_1.off()
        BUTTON_2.off()
        R_24V.off()
        RS485.off()
        sleep(0.2)

        print("Alle uitgangen zijn uitgeschakeld.", flush=True)
        print("correct", "Alle uitgangen zijn op 0 gezet voor veiligheid.", flush=True)
        return True

    except Exception as e:
        log_result("fout", f"Fout in stap 13: {str(e)}")
        return False    

def stap_14():
    try:
        print("Stap 14: Loggen van succesbericht voor de PCB...", flush=True)

        # Als alle stappen correct zijn uitgevoerd, log dan dit succesbericht
        succesbericht = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Optie : RISP EL | Serienummer: {SERIENUMMER} | Status: correct - PCB"

        # Schrijf het succesbericht naar het logbestand
        with open(LOGBESTAND, "a") as f:
            f.write(succesbericht + "\n")

        print(succesbericht)
        signal_g.off()
        return True

    except Exception as e:
        log_result("fout", f"Fout in stap 14: {str(e)}")
        return False

# Start het script
if __name__ == "__main__":
    main()
