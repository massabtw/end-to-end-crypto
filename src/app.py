import requests
import streamlit as st
from datetime import datetime, timedelta

API_BASE_URL = "https://end-to-end-crypto-1.onrender.com"
CRYPTO_OPTIONS = ["bitcoin", "ethereum", "solana", "cardano", "ripple"]
TIME_FILTERS = {
    "Ultima 1 hora": (timedelta(hours=1), timedelta(hours=0)),
    "Entre 1 e 6 horas": (timedelta(hours=6), timedelta(hours=1)),
    "Entre 6 e 24 horas": (timedelta(hours=24), timedelta(hours=6)),
}


def fetch_json(endpoint: str):
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        st.error(f"Erro ao conectar com a API: {error}")
        return None


def filter_by_period(data: list[dict], period_label: str) -> list[dict]:
    start_delta, end_delta = TIME_FILTERS[period_label]
    now = datetime.now()
    start_time = now - start_delta
    end_time = now - end_delta
    fmt = "%Y-%m-%d %H:%M:%S"

    filtered = []
    for registro in data:
        timestamp = datetime.strptime(registro["timestamp"], fmt)
        if start_time <= timestamp <= end_time:
            filtered.append(registro)
    return sorted(filtered, key=lambda item: item["timestamp"], reverse=True)


def render_latest_price(crypto: str):
    data = fetch_json(f"/prices/latest?crypto={crypto}")
    if not data or data.get("msg"):
        st.warning("Sem dados recentes para essa moeda.")
        return

    st.subheader(f"{crypto.capitalize()} - preco atual")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Preco (USD)", f"${data['price - usd']:,.2f}")
    with col2:
        st.metric("Atualizado em", data["timestamp"])


def render_history(crypto: str, period_label: str):
    history = fetch_json(f"/prices?crypto={crypto}")
    if history is None:
        return

    filtered = filter_by_period(history, period_label)
    st.subheader(f"Historico - {period_label}")
    st.metric("Registros no periodo", len(filtered))

    if not filtered:
        st.info("Nao ha registros para esse intervalo de tempo.")
        return

    table_rows = []
    for item in filtered:
        timestamp = datetime.strptime(item["timestamp"], "%Y-%m-%d %H:%M:%S")
        table_rows.append(
            {
                "Data/Hora": timestamp.strftime("%d/%m %H:%M"),
                "Preco (USD)": f"${item['price - usd']:,.2f}",
            }
        )

    st.dataframe(table_rows, use_container_width=True, hide_index=True)


def main():
    st.set_page_config(page_title="Dashboard de Criptomoedas", layout="wide")
    st.title("Dashboard de Criptomoedas")
    st.caption("Visualizacao de preco atual e historico por faixa de tempo.")

    col1, col2 = st.columns([2, 2])
    with col1:
        selected_crypto = st.selectbox("Criptomoeda", CRYPTO_OPTIONS)
    with col2:
        selected_period = st.selectbox("Filtro de tempo", list(TIME_FILTERS.keys()))

    render_latest_price(selected_crypto)
    st.divider()
    render_history(selected_crypto, selected_period)


main()