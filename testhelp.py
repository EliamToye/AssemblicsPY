def toon_uitleg():
    uitleg = """
    =============================================
       Project: Bachelorproef Artuur & Eliam (2025)
    =============================================

    Dit Python-script is ontworpen voor een Raspberry Pi 5 en wordt gebruikt om testprocedures 
    automatisch uit te voeren aan de hand van een gescande barcode. 

    Werking:
    --------
    1️⃣ De gebruiker scant een barcode.
    2️⃣ Op basis van de barcode wordt een specifieke testprocedure gestart.
    3️⃣ Testinformatie en voortgang worden weergegeven op het scherm.
    4️⃣ De resultaten van de test worden verzameld en opgeslagen.

    Doel:
    -----
    ✅ Automatisering van testprocedures.
    ✅ Weergave van relevante testinformatie in real-time.
    ✅ Gebruiksvriendelijke interactie via een Raspberry Pi 5.

    Dit script is een essentieel onderdeel van de bachelorproef en maakt het mogelijk om tests 
    efficiënt en betrouwbaar uit te voeren.

    =============================================
    """
    print(uitleg)

# Toon de uitleg als het script wordt uitgevoerd
if __name__ == "__main__":
    toon_uitleg()