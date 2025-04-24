import requests
from bs4 import BeautifulSoup

def get_raspberry_pi_info():
    url = "https://en.wikipedia.org/wiki/Raspberry_Pi#Raspberry_Pi_5"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Zoek de eerste paragraaf die Raspberry Pi 5 beschrijft
            paragraph = soup.find("span", id="Raspberry_Pi_5").find_next("p")
            
            if paragraph:
                print("Raspberry Pi 5 Informatie van Wikipedia:")
                print(paragraph.get_text(strip=True))
            else:
                print("Geen informatie gevonden over Raspberry Pi 5.")
        else:
            print(f"Fout bij ophalen van de pagina: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Fout bij het ophalen van de gegevens: {e}")

# Roep de functie aan
get_raspberry_pi_info()