import time
import random
from datetime import datetime
import sys
sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
from gpiozero import DigitalInputDevice
gpio_pinsI = [4, 10, 9, 11, 0, 18, 24, 1, 12, 16]
gpio_inputs = {pin: DigitalInputDevice(pin) for pin in gpio_pinsI}

# Functie om de log naar een bestand te schrijven met alleen serienummer, tijd/datum, testuitkomst en stapbeschrijving
def log_to_file(serienummer, status, description, failed_step=None):
    log_file = "test_log.txt"
    if status == "fout" and failed_step:
        log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Serienummer: {serienummer} | Status: {status} | Fout op stap {failed_step} - {description}\n"
    else:
        log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Serienummer: {serienummer} | Status: {status} - {description}\n"
    with open(log_file, "a") as file:
        file.write(log_entry)

# Functie om de stap te loggen en de status in de terminal te tonen
def log_step(serienummer, step_number, description, status="correct"):
    print(f"\n➡️ Stap {step_number}: {description}")
    sys.stdout.flush()
    print(f"Status: {status.capitalize()}")
    sys.stdout.flush()
    time.sleep(2)  # Simuleert de uitvoeringstijd van de stap
    return status

def main():
    # Begin tijd voor het testen
    start_time = time.time()
    print("\n🔧 Testprocedure gestart...\n")
    sys.stdout.flush()

    # Willekeurig serienummer genereren
    serienummer = random.randint(100, 199)  # Willekeurig serienummer
    print(f"Gegenereerd serienummer: {serienummer}")
    sys.stdout.flush()

    # Foutteller bijhouden
    fout_count = 0  # Aantal fouten bijhouden
    failed_step = None  # Variabele voor de foutstap
    error_probability = 0.005  # Kans op fout (0,5%)

    # Stap 1: Power up en stroomverbruik
    stroomverbruik = random.uniform(20, 52)  # Willekeurig stroomverbruik tussen 20mA en 60mA
    print(f"Gecontroleerd stroomverbruik: {stroomverbruik:.2f} mA")  # Extra log voor het stroomverbruik
    sys.stdout.flush()
    if stroomverbruik > 50:  # Fout als stroomverbruik > 50mA of willekeurig falen
        description = "Power up device met 24VDC en controleer POWER LED en stroomverbruik (< 50mA, typisch 30mA)"
        status = log_step(serienummer, 1, description, status="fout")
        fout_count += 1
        failed_step = 1
        log_to_file(serienummer, "fout", description, failed_step)
        return  # Stop de test onmiddellijk bij fout

    description = "Power up device met 24VDC en controleer POWER LED en stroomverbruik (< 50mA, typisch 30mA)"
    status = log_step(serienummer, 1, description, status="correct")

    # Stap 2: Programmeer PIC16F688 met aangepast EEPROM serienummer
    if random.random() < error_probability:  # Krijgt een fout met een kans van 1%
        description = "Setup programmer en programmeer PIC16F688 met aangepast EEPROM serienummer"
        status = log_step(serienummer, 2, description, status="fout")
        fout_count += 1
        failed_step = 2
        log_to_file(serienummer, "fout", description, failed_step)
        return

    description = "Setup programmer en programmeer PIC16F688 met aangepast EEPROM serienummer"
    status = log_step(serienummer, 2, description, status="correct")

    # Stap 3: Power up SIM Control Module
    if random.random() < error_probability:
        description = "Power up SIM Control Module en verbind met SIM Field Module"
        status = log_step(serienummer, 3, description, status="fout")
        fout_count += 1
        failed_step = 3
        log_to_file(serienummer, "fout", description, failed_step)
        return

    description = "Power up SIM Control Module en verbind met SIM Field Module"
    status = log_step(serienummer, 3, description, status="correct")

    # Stap 4: Willekeurige modus
    modus = random.choice(["S00", "S01", "S02", "S03", "S04", "S05"])  # Willekeurige modus kiezen
    print(f"Verkregen Modus: {modus}")
    sys.stdout.flush()
    description = f"Verkregen Modus is '{modus}'"
    status = log_step(serienummer, 4, description, status="correct")

    # Stap 5: Wijzig modus naar S03
    if modus == "S03":
        # Als de modus al S03 is, geef dit aan zonder wijziging
        description = f"Modus is al '{modus}', geen wijziging nodig."
        status = log_step(serienummer, 5, description, status="correct")
    else:
        # Als de modus niet S03 is, wijzig deze naar S03 met een vertraging
        delay = random.uniform(1.12, 6.59)
        time.sleep(delay)  # Vertraging toevoegen om de wijziging te simuleren
        modus = "S03"
        description = f"Wijzig modus naar '{modus}', configuratie opgeslagen"
    
        if random.random() < error_probability:  # Fout kans
            status = log_step(serienummer, 5, description, status="fout")
            fout_count += 1
            failed_step = 5
            log_to_file(serienummer, "fout", description, failed_step)
            return  # Stop de test als er een fout optreedt
        status = log_step(serienummer, 5, description, status="correct")


    # LED-status simuleren
    led_status = random.choice(["Groen", "Geel", "Rood"])  # Willekeurige LED status
    if random.random() < error_probability:
        description = f"Controleer LED status op Field Module: {led_status}"
        status = log_step(serienummer, 6, description, status="fout")
        fout_count += 1
        failed_step = 6
        log_to_file(serienummer, "fout", description, failed_step)
        return

    description = f"Controleer LED status op Field Module: {led_status}"
    status = log_step(serienummer, 6, description, status="correct")

    # Test weerstanden simuleren
    resistor_820R = random.choice(["gesloten", "open"])  # Willekeurige toestand van de 820R weerstand
    if random.random() < error_probability:
        description = "Sluit testconnector aan, kort 820R weerstand en controleer relaisstatus"
        status = log_step(serienummer, 7, description, status="fout")
        fout_count += 1
        failed_step = 7
        log_to_file(serienummer, "fout", description, failed_step)
        return

    description = "Sluit testconnector aan, kort 820R weerstand en controleer relaisstatus"
    status = log_step(serienummer, 7, description, status="correct")

    # Alarm conditie simuleren
    alarm_conditie = random.choice(["Alarm", "Normaal"])  # Willekeurige alarmconditie
    if random.random() < error_probability:
        description = "Open 820R weerstand om alarm te simuleren"
        status = log_step(serienummer, 8, description, status="fout")
        fout_count += 1
        failed_step = 8
        log_to_file(serienummer, "fout", description, failed_step)
        return

    description = "Open 820R weerstand om alarm te simuleren"
    status = log_step(serienummer, 8, description, status="correct")

    # Draadkortsluiting simuleren
    short_circuit = random.choice(["kortgesloten", "normaal"])  # Willekeurige kortsluitconditie
    if random.random() < error_probability:
        description = "Kort beide weerstanden om draadkortsluiting te testen"
        status = log_step(serienummer, 9, description, status="fout")
        fout_count += 1
        failed_step = 9
        log_to_file(serienummer, "fout", description, failed_step)
        return

    description = "Kort beide weerstanden om draadkortsluiting te testen"
    status = log_step(serienummer, 9, description, status="correct")

    # Stap 10: Wijzig de modus naar S02
    modus = "S02"
    if random.random() < error_probability:
        description = f"Wijzig de modus naar '{modus}' en sla de configuratie op"
        status = log_step(serienummer, 10, description, status="fout")
        fout_count += 1
        failed_step = 10
        log_to_file(serienummer, "fout", description, failed_step)
        return

    description = f"Wijzig de modus naar '{modus}' en sla de configuratie op"
    status = log_step(serienummer, 10, description, status="correct")

    # Stap 11: Test communicatie met het veld
    if random.random() > 0.99:  # 5% kans op fout (0.95 betekent 95% kans op "Ok")
        communicatie_status = "Fout"
    else:
        communicatie_status = "Ok"
    
    if communicatie_status == "Fout":
        description = "Test communicatie met het veld"
        status = log_step(serienummer, 11, description, status="fout")
        fout_count += 1
        failed_step = 11
        log_to_file(serienummer, "fout", description, failed_step)
        return

    description = "Test communicatie met het veld"
    status = log_step(serienummer, 11, description, status="correct")

    # Stap 12: Test de display output
    if random.random() < error_probability:
        description = "Test de display output"
        status = log_step(serienummer, 12, description, status="fout")
        fout_count += 1
        failed_step = 12
        log_to_file(serienummer, "fout", description, failed_step)
        return

    description = "Test de display output"
    status = log_step(serienummer, 12, description, status="correct")

    # Stap 13: Test sensor uitlezing
    if random.random() > 0.95:  # 5% kans op fout (0.95 betekent 95% kans op "Ok")
        sensor_status = "Fout"
    else:
        sensor_status = "Ok"
    
    if sensor_status == "Fout":
        description = "Test sensor uitlezing"
        status = log_step(serienummer, 13, description, status="fout")
        fout_count += 1
        failed_step = 13
        log_to_file(serienummer, "fout", description, failed_step)
        return

    description = "Test sensor uitlezing"
    status = log_step(serienummer, 13, description, status="correct")

    # Stap 14: Test relaisactivering
    if random.random() < error_probability:
        description = "Test relaisactivering"
        status = log_step(serienummer, 14, description, status="fout")
        fout_count += 1
        failed_step = 14
        log_to_file(serienummer, "fout", description, failed_step)
        return

    description = "Test relaisactivering"
    status = log_step(serienummer, 14, description, status="correct")

    # Stap 15: Einde van de test en bevestig de status
    description = "Einde van de test en bevestig de status"
    status = log_step(serienummer, 15, description, status="correct")

    # Einde tijd voor het testen
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\n🔧 Testprocedure voltooid. Tijdsduur: {elapsed_time:.2f} seconden")
    sys.stdout.flush()

    # Resultaten loggen
    if fout_count == 0:
        print("\n✅ Alle stappen waren succesvol!")
        sys.stdout.flush()
        log_to_file(serienummer, "correct", "Alle stappen waren succesvol")
    else:
        print(f"\n⚠️ Er zijn {fout_count} fout(en) opgetreden.")
        sys.stdout.flush()

if __name__ == "__main__":
    main()