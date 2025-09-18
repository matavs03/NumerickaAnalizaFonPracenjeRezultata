import requests
from bs4 import BeautifulSoup
import time

TELEGRAM_TOKEN = "" #token vaseg telegram bota
CHAT_ID = "" #id vaseg chata
TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

url = "https://math.fon.bg.ac.rs/vesti/numericka-analiza/"
stari_linkovi = set()
brojac = 0

def posalji_telegram_poruku(poruka):
    payload = {
        'chat_id': CHAT_ID,
        'text': poruka
    }
    try:
        requests.post(TELEGRAM_URL, data=payload)
    except Exception as e:
        print("Greska pri slanju poruke:", e)

def proveri_rezultate():
    global stari_linkovi, brojac
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    novi_linkovi = {a['href'] for a in soup.find_all('a', href=True)}

    novi_rezultati = novi_linkovi - stari_linkovi
    if novi_rezultati:
        brojac += 1
        poruka = "OBJAVLJENI REZULTATI !!!"
        if brojac==2:
            posalji_telegram_poruku(poruka)
            return True
    else:
        print("Nista novo")

    stari_linkovi = novi_linkovi
    return False

if __name__ == "__main__":
    while True:
        nadjeno = proveri_rezultate()
        if nadjeno:
            break
        time.sleep(30)
#%%

#%%
