import streamlit as st
import requests

def request():
    options = st.selectbox("Selecione as criptomoedas", ["bitcoin", "ethereum", "solana", "cardano", "ripple"])
    url = f"http://127.0.0.1:8000/prices/latest?crypto={options}"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        st.title(data["crypto"].capitalize())
        st.metric(
        label=f"{data['crypto'].capitalize()} Price", 
        value=f"${data['price - usd']:,.2f}"
    )

    else:
        st.write("Erro ao buscar dados")
        raise RuntimeError(f"API Status: {response.status_code}")
