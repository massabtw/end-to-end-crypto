import json
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "database.json"

def salvar_dado(novos_dados):
    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    nova_lista = []
    agora = datetime.now()

    for registro in data:
        timestamp_str = registro["timestamp"]
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        diferenca = agora - timestamp

        if diferenca <= timedelta(hours=24):
            nova_lista.append(registro)

    nova_lista.extend(novos_dados)

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DB_PATH, 'w', encoding="utf-8") as f:
        json.dump(nova_lista, f, indent=2)





