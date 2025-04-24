import time
import socket
import os
import psutil
from datetime import datetime

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # verbinding maken naar een dummy IP (wordt niet echt verstuurd)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "Geen verbinding"

def get_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = int(f.read()) / 1000
            return f"{temp:.1f}°C"
    except FileNotFoundError:
        return "Niet beschikbaar"

def print_info():
    os.system('clear')  # Maak het scherm schoon
    print("📟 Systeeminformatie Raspberry Pi 5")
    print("-" * 40)
    print(f"📶 IP-adres     : {get_ip()}")
    print(f"🌡️  CPU Temp     : {get_temp()}")
    print(f"⚙️  CPU Gebruik  : {psutil.cpu_percent()}%")
    mem = psutil.virtual_memory()
    print(f"💾 Geheugen     : {mem.used // (1024**2)}MB / {mem.total // (1024**2)}MB")
    print(f"🕓 Laatste update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 40)
    print("Volgende update over 5 minuten...\n")

def main():
    while True:
        print_info()
        time.sleep(300)  # 5 minuten

if __name__ == "__main__":
    main()
