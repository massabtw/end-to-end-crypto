from fastapi import FastAPI
from datetime import datetime
import json
from pathlib import Path
app = FastAPI()
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "database.json"

def buscar_dados(crypto=None):
    with open(DB_PATH, 'r', encoding="utf-8") as f:
        data = json.load(f)
        filtrados = []
        for registro in data:
            if crypto is None or registro["crypto"].lower() == crypto.lower():
                filtrados.append(registro)
        return filtrados



@app.get("/prices")
def get_prices(crypto=None):
    return buscar_dados(crypto)

@app.get("/prices/latest")
def get_latest(crypto):
    dados = buscar_dados(crypto)
    if not dados:
       return {"msg": "dados não encontrados"}
    mais_recente = dados[0]
    fmt = "%Y-%m-%d %H:%M:%S"
    for registro in dados:
        timestamp = datetime.strptime(registro["timestamp"], fmt)
        timestamp_recente = datetime.strptime(mais_recente["timestamp"], fmt)
        if timestamp > timestamp_recente:
            mais_recente = registro
    return mais_recente






        


    