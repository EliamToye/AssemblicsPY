from gpiozero import LED
from time import sleep
import time
import threading
import os
import sys
import signal
import serial
from datetime import datetime
from gpiozero import Button

#pinnen
Signal_R = LED(2)# Signal_R (GPIO 2) - Output: Rood Led fixstuur
Signal_G = LED(3)# Signal_G (GPIO 3) - Output: Groen Led fixstuur
Input_P2B = Button(4)# Input_P2B (GPIO 4) - Input: Relais 1 (for detecting state of relay)
P3A = LED(17)# P3A (GPIO 17) - Output: Eerste kortsluiting (820)
P3C = LED(27)# P3C (GPIO 27) - Output: Tweede kortsluiting (240)
P1_2 = LED(22)# P1.2 (GPIO 22) - Output: Bridge wire
LED_RED_OUT = Button(10)# LED_RED_OUT (GPIO 10) - Input: Rood led pcb
LED_YELLOW_OUT = Button(9)# LED_YELLOW_OUT (GPIO 9) - Input: Led geel pcb
LED_GREEN2_OUT = Button(11)# LED_GREEN2_OUT (GPIO 11) - Input: Led groen2 pcb
LED_GREEN1_OUT = Button(0)# LED_GREEN1_OUT (GPIO 0) - Input: Led groen1 pcb
BUTTON_2 = LED(5)# BUTTON 2 (GPIO 5) - Output: Knop 2
BUTTON_1 = LED(6)# BUTTON 1 (GPIO 6) - Output: Knop 1
R_24V = LED(26)# R_24V (GPIO 26) - Output: 24V extern
RS485 = LED(23)# RS485 (GPIO 23) - Output: Aansturing
RS485A = Button(24)# RS485A (GPIO 24) - Input: Indicatie Aansturing
P1_1 = LED(25)# P1.1 (GPIO 25) - Output: Bridge wire
INPUT_P2C = Button(1)# INPUT_P2C (GPIO 1) - Input: Relais 1
INPUT_P4B = Button(12)# INPUT_P4B (GPIO 12) - Input: Relais 2
INPUT_P4C = Button(16)# INPUT_P4C (GPIO 16) - Input: Relais 2

#functies
# Variabele om het knipperen te stoppen
knipperen = True

# Verwacht serienummer voor test
verwacht_serienummer = "153"

def knipper_leds():
    """Functie die de LEDs laat knipperen zolang 'knipperen' True is."""
    while knipperen:
        Signal_R.on()
        Signal_G.off()
        sleep(1)   # sneller knipperen voor visuele feedback
        Signal_R.off()
        Signal_G.on()
        sleep(1)
    # Als knipperen False wordt:
    Signal_R.off()
    Signal_G.off()
    print("Knipperen gestopt.")

def lees_serienummer():
    try:
        with serial.Serial("/dev/serial0", baudrate=9600, timeout=5) as ser:
            print("Wachten op serienummer via UART...")
            lijn = ser.readline().decode("utf-8").strip()
            print(f"Ontvangen serienummer: {lijn}")
            return lijn
    except Exception as e:
        print(f"FOUT bij UART lezen: {e}")
        return None

def stap_uitvoeren(stap_nummer):
    print(f"Stap {stap_nummer}: uitvoering...")
    try:
        if stap_nummer == 1:
            BUTTON_1.on()
            BUTTON_2.on()
            sleep(3)
            R_24V.on()
            sleep(1)
            BUTTON_1.off()
            BUTTON_2.off()

        elif stap_nummer == 2:
            serienummer = lees_serienummer()
            if serienummer != verwacht_serienummer:
                raise ValueError(f"Serienummer mismatch! Verwacht '{verwacht_serienummer}', kreeg '{serienummer}'")
        
        elif stap_nummer == 3:
            starttijd = time.time()
            gevonden = False
            while time.time() - starttijd < 10:
                BUTTON_1.on()
                sleep(1)
                BUTTON_1.off()
                mode = lees_serienummer()
                if mode == "S03":
                    gevonden = True
                    break
                BUTTON_2.on()
                sleep(1)
                BUTTON_2.off()
                mode = lees_serienummer()
                if mode == "S03":
                    gevonden = True
                    break
                if not gevonden:
                    raise TimeoutError("Timeout: 'S03' niet gevonden binnen 10 seconden.")

        elif stap_nummer == 4:
            if LED_GREEN1_OUT.is_pressed and LED_YELLOW_OUT.is_pressed:
                print("Stap 4: Groene en gele LED zijn aan, verder met volgende stap.")
            else:
                raise ValueError("Stap 4 Fout: Groene of gele LED is niet aan.")

        elif stap_nummer == 5:
            print("Stap 5: Zet P3A aan.")
            P3A.on()
            sleep(0.5)  # Wacht even voor stabiliteit
            if LED_GREEN1_OUT.is_pressed:
                print("Stap 5: Groene LED is aan na activeren P3A.")
            else:
                raise ValueError("Stap 5 Fout: Groene LED is niet aan na activeren P3A.")   
        elif stap_nummer == 6:
            print("Stap 6: Zet P3A uit.")
            P3A.off()
            sleep(0.5)
            if LED_RED_OUT.is_pressed and LED_GREEN2_OUT.is_pressed:
                print("Stap 6: Rood en tweede groene LED zijn aan.")
            else:
                raise ValueError("Stap 6 Fout: Rood of tweede groene LED is niet aan.")
        
        elif stap_nummer == 7:
            print("Stap 7: Zet P3A en P3C aan.")
            P3A.on()
            P3C.on()
            sleep(0.5)
            if LED_YELLOW_OUT.is_pressed:
                print("Stap 7: Gele LED is aan.")
            else:
                raise ValueError("Stap 7 Fout: Gele LED is niet aan.")

        elif stap_nummer == 8:
            print("Stap 8: Zet P3A en P3C uit.")
            P3A.off()
            P3C.off()
            sleep(0.5)
            print("Stap 8: Wachten op UART 'S02', indien niet: Button 1 pulsen.")
            timeout = 10
            start_time = time()
            while time() - start_time < timeout:
                uart_value = lees_serienummer()
                if uart_value == "S02":
                    print("Stap 8: Correcte UART-waarde 'S02' ontvangen.")
                    break
                else:
                    BUTTON_1.on()
                    sleep(0.5)
                    BUTTON_1.off()
                    sleep(0.5)
            else:
                raise ValueError("Stap 8 Fout: 'S02' niet ontvangen binnen tijdslimiet.")

        elif stap_nummer == 9:
            print("Stap 9: Controleer of groene LED 1 aan ligt.")
            if not LED_GREEN1_OUT.is_active:
                 raise ValueError("Stap 9 Fout: Groene LED 1 is niet actief.")
            print("Stap 9: Groene LED 1 is actief.")
        
        elif stap_nummer == 10:
            print("Stap 10: Zet beide bridge wires aan (P1_1 en P1_2).")
            P1_1.on()
            P1_2.on()
            sleep(0.5)
            print("Stap 10: Controleer LED groen2 en rood.")
            if not LED_GREEN2_OUT.is_active:
                raise ValueError("Stap 10 Fout: Groene LED 2 is niet actief.")
            if not LED_RED_OUT.is_active:
                raise ValueError("Stap 10 Fout: Rode LED is niet actief.")
            print("Stap 10: Beide LEDs zijn actief.")

        elif stap_nummer == 11:
            print("Stap 11: Controleer of UART terug op S03 staat.")
            start_time = time()
            serienummer = lees_serienummer()
            while time() - start_time < 10:
                serienummer = lees_serienummer()
                if serienummer == "S03":
                    break
                else:
                    raise TimeoutError("Stap 11 Fout: Timeout bij wachten op S03 via UART.")
            print(f"Stap 11: Serienummer is {serienummer}, druk BUTTON_1 in en probeer opnieuw.")
            BUTTON_1.on()
            sleep(0.5)
            BUTTON_1.off()
            sleep(0.5)
            serienummer = lees_serienummer()
            print("Stap 11: Correcte serienummer S03 ontvangen.")

        elif stap_nummer == 12:
            print("Stap 12: Controleer of groene LED 1 actief is.")
            if not LED_GREEN1_OUT.is_active:
                raise ValueError("Stap 12 Fout: Groene LED 1 is niet actief.")
            print("Stap 12: Groene LED 1 is correct actief.")
            
        elif stap_nummer == 13:
            print("Stap 13: Zet bridge wires (P1_1 en P1_2) en R_24V uit.")
            P1_1.off()
            P1_2.off()
            R_24V.off()
            sleep(0.5)
            print("Stap 13: Bridge wires en R_24V zijn uitgeschakeld.")

        elif stap_nummer == 14:
            print("Stap 14: Loggen van de resultaten.")
            # Verkrijg het huidige serienummer
            serienummer = 153
            # Bepaal de status van de stappen
            status = "correct"  # Hier zou je later de status kunnen uitbreiden als dat nodig is
            # Verkrijg de huidige tijd en datum
            huidige_tijd = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Loggen naar bestand
            with open("/home/pi/testlog.txt", "a") as log_file:
                log_file.write(f"{huidige_tijd} | Serienummer: {serienummer} | Status: {status} - Alle stappen waren succesvol\n")
            print(f"Stap 14: Loggen succesvol. Logbestand bijgewerkt.")
    except Exception as e:
        print(f"!!! FOUT bij stap {stap_nummer}: {e}")
        sys.exit(1)

def main():
    print("Programma gestart. LED-statusindicatie...")

    # Start knipper-thread
    global knipperen
    knipper_thread = threading.Thread(target=knipper_leds)
    knipper_thread.start()

    try:
        for stap in range(1, 15):  # Voer alle 14 stappen uit
            stap_uitvoeren(stap)

        print("Alle stappen succesvol doorlopen.")

    except Exception as e:
        print(f"FOUT tijdens testsequentie: {e}")

    finally:
        knipperen = False
        knipper_thread.join()
        print("Programma beëindigd.")

if __name__ == "__main__":
    main()