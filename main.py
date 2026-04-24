import requests
from datetime import datetime
import time
from database  import salvar_dado


cryptos = ["bitcoin", "ethereum", "solana", "cardano", "ripple"]
ids = ",".join(cryptos)
url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"
currency = ("usd")

while True:
    try:
        print("<------------------------>")
        response = requests.get(url, timeout=10)
        if response.status_code == 429:
            print("Rate Limit API atingido")
            time.sleep(60)
            continue   
        data = response.json()
        novos_dados = []

        for crypto, info in data.items():
            price = info.get("usd")
            if not isinstance(price, (float, int)):
                continue 
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            novo_dado = {
                "crypto": crypto,
                "price - usd": price,
                "currency": currency,
                "timestamp": timestamp
            }
            print(f"{crypto}: {price} USD - {timestamp}")
            novos_dados.append(novo_dado)
        salvar_dado(novos_dados)  
        time.sleep(600)
    except Exception as error:
        print(error )
    time.sleep(45)

    



