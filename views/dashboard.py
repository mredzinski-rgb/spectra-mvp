import streamlit as st
import pandas as pd
import os  # Dodano import do sprawdzania plików
from modules import market_data


def show():
    # --- SEKCJA 1: LIVE MARKET FEED ---
    st.markdown("### 📡 LIVE MARKET FEED")

    with st.spinner("Pobieranie danych rynkowych..."):
        df_rates = market_data.get_live_rates()

    if df_rates.empty:
        st.error("Nie udało się pobrać danych z Yahoo Finance.")
        return

    cols = st.columns(5)
    desired_order = ["EUR/PLN", "USD/PLN", "CHF/PLN", "EUR/USD", "GBP/PLN"]

    for i, pair_name in enumerate(desired_order):
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

    # --- SEKCJA 2: RAPORTY PDF (Nowa sekcja) ---
    # Ta część odpowiada za to, aby PDF wgrany przez Admina był widoczny dla klienta
    st.markdown("### 📑 BLACK STAG INTELLIGENCE")

    report_path = "data/raport.pdf"  # Musi być zgodne z nazwą w admin_panel.py

    if os.path.exists(report_path):
        # Wyświetlamy stylowy boks z informacją o raporcie
        col_icon, col_text = st.columns([1, 5])
        with col_icon:
            st.markdown("<h1 style='text-align: center;'>📄</h1>", unsafe_allow_html=True)
        with col_text:
            st.write("**Najnowszy Raport Geopolityczny i Analiza FX**")
            st.write("Raport przygotowany przez zespół Black Stag Intelligence.")

            with open(report_path, "rb") as f:
                st.download_button(
                    label="POBIERZ AKTUALNY RAPORT (PDF)",
                    data=f,
                    file_name="Black_Stag_Spectra_Report.pdf",
                    mime="application/pdf",
                    type="primary"  # Wyróżniony przycisk
                )
    else:
        st.info("Oczekiwanie na publikację dzisiejszego raportu geopolitycznego.")

    st.markdown("---")

    # --- SEKCJA 3: WYKRESY (CURRENCY MONITOR) ---
    st.markdown("### 📈 CURRENCY MONITOR")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("**EUR/PLN - GŁÓWNA PARA**")
        fig_eur = market_data.get_chart_of_day("EUR/PLN")
        if fig_eur:
            st.plotly_chart(fig_eur, use_container_width=True)
        else:
            st.warning("Brak danych wykresu.")
        st.caption("Analiza: Trend boczny. Wsparcie na 4.2800 silne.")

    with c2:
        st.markdown("**USD/PLN - DOLAR AMERYKAŃSKI**")
        fig_usd = market_data.get_chart_of_day("USD/PLN")
        if fig_usd:
            st.plotly_chart(fig_usd, use_container_width=True)
        else:
            st.warning("Brak danych wykresu.")
        st.caption("Analiza: Zależność od danych z USA (Non-Farm Payrolls).")

    # --- SEKCJA 4: POWIADOMIENIE NA DOLE ---
    st.info("💡 Black Stag Insight: Zalecamy zwiększenie hedge na EUR do 65% w związku z planowanym posiedzeniem RPP.")