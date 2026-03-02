import streamlit as st
import pandas as pd
from modules import market_data  # Importujemy Twój nowy moduł


def show():
    st.markdown("### 📡 LIVE MARKET FEED")

    # 1. POBIERANIE DANYCH (Używamy Twojej funkcji get_live_rates)
    with st.spinner("Pobieranie danych rynkowych..."):
        df_rates = market_data.get_live_rates()

    # Jeśli dane się nie pobrały, wyświetl komunikat, ale nie wywalaj apki
    if df_rates.empty:
        st.error("Nie udało się pobrać danych z Yahoo Finance.")
        return

    # 2. WYŚWIETLANIE KAFELKÓW (METRICS)
    # Musimy "rozpakować" DataFrame do kolumn.
    # Zakładam kolejność: EUR/PLN, USD/PLN, CHF/PLN, EUR/USD, GBP/PLN

    cols = st.columns(5)
    desired_order = ["EUR/PLN", "USD/PLN", "CHF/PLN", "EUR/USD", "GBP/PLN"]

    for i, pair_name in enumerate(desired_order):
        # Znajdź wiersz w DataFrame dla danej pary
        row = df_rates[df_rates['Para'] == pair_name]

        with cols[i]:
            if not row.empty:
                price = row.iloc[0]['Kurs']
                change = row.iloc[0]['Zmiana']
                st.metric(
                    label=pair_name,
                    value=f"{price:.4f}",
                    delta=f"{change:.2f}%"
                )
            else:
                st.metric(label=pair_name, value="--", delta=None)

    st.markdown("---")

    # 3. WYKRESY (CURRENCY MONITOR)
    st.markdown("### 📈 CURRENCY MONITOR")

    c1, c2 = st.columns(2)

    # Wykres 1: EUR/PLN
    with c1:
        st.markdown("**EUR/PLN - GŁÓWNA PARA**")
        fig_eur = market_data.get_chart_of_day("EUR/PLN")  # Twoja funkcja
        if fig_eur:
            st.plotly_chart(fig_eur, use_container_width=True)
        else:
            st.warning("Brak danych wykresu.")
        st.caption("Analiza: Trend boczny. Wsparcie na 4.2800 silne.")

    # Wykres 2: USD/PLN
    with c2:
        st.markdown("**USD/PLN - DOLAR AMERYKAŃSKI**")
        fig_usd = market_data.get_chart_of_day("USD/PLN")  # Twoja funkcja
        if fig_usd:
            st.plotly_chart(fig_usd, use_container_width=True)
        else:
            st.warning("Brak danych wykresu.")
        st.caption("Analiza: Zależność od danych z USA (Non-Farm Payrolls).")

    # 4. POWIADOMIENIE NA DOLE
    st.info("💡 Black Stag Insight: Zalecamy zwiększenie hedge na EUR do 65% w związku z planowanym posiedzeniem RPP.")