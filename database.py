import json
from datetime import datetime,timedelta

def salvar_dado(novos_dados):
    try:
            with open('database.json', "r") as f:
               data = json.load(f)
    except FileNotFoundError:
          data = []
    
    nova_lista = []
    agora = datetime.now()

    for registro in data:
         timestamp_str = registro["timestamp"]
         timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
         diferença = agora - timestamp

         if diferença <= timedelta(hours = 24):
              nova_lista.append(registro)
              
    nova_lista.extend(novos_dados)

    with open('database.json', 'w') as f:
         json.dump(nova_lista, f, indent=2)





