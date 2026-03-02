import streamlit as st
import pandas as pd
import os
from datetime import datetime
from modules import market_data

def get_file_info(path):
    """Pobiera czas ostatniej modyfikacji pliku."""
    if os.path.exists(path):
        mtime = os.path.getmtime(path)
        return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
    return None

def show():
    # CSS likwidujący problem pustych marginesów i ucinania kursów do 4.2...
    st.markdown("""
        <style>
        .block-container {
            max-width: 95% !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
        div[data-testid="stMetricValue"] {
            white-space: nowrap !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # PODZIAŁ: col_news (lewa) | col_spacer (przerwa) | col_main (kursy, szeroka kolumna)
    col_news, col_spacer, col_main = st.columns([1.2, 0.4, 4.5])

    # ====================================================
    # ODRĘBNA SEKCJA: MARKET NEWS (Między Sidebarem a Kursami)
    # ====================================================
    with col_news:
        st.markdown("### 🔔 MARKET NEWS")
        # --- SEKCJA 0: KOMUNIKAT RYNKOWY (Dynamiczny) ---
        news_path = "data/news.txt"
        if os.path.exists(news_path):
            ts_news = get_file_info(news_path)
            with open(news_path, "r", encoding="utf-8") as f:
                content = f.read()
                if content:
                    # Wyświetlanie komunikatu z datą publikacji
                    st.warning(f"**Opublikowano: {ts_news}**\n\n{content}")
        else:
            st.info("Brak aktywnych komunikatów.")

    # ====================================================
    # GŁÓWNA SEKCJA: KURSY, PDF, WYKRESY (Szeroka by zapobiec ucinaniu)
    # ====================================================
    with col_main:
        # --- SEKCJA 1: LIVE MARKET FEED ---
        st.markdown("### 📡 LIVE MARKET FEED")

        with st.spinner("Pobieranie danych rynkowych..."):
            df_rates = market_data.get_live_rates()

        if df_rates.empty:
            st.error("Nie udało się pobrać danych z Yahoo Finance.")
        else:
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

        # --- SEKCJA 2: RAPORTY PDF (Z datą publikacji) ---
        st.markdown("### 📑 BLACK STAG INTELLIGENCE")

        report_path = "data/raport.pdf"

        if os.path.exists(report_path):
            ts_pdf = get_file_info(report_path)
            col_icon, col_text = st.columns([1, 5])
            with col_icon:
                st.markdown("<h1 style='text-align: center;'>📄</h1>", unsafe_allow_html=True)
            with col_text:
                st.write("**Najnowszy Raport Geopolityczny i Analiza FX**")
                # Wyświetlanie daty publikacji PDF
                st.caption(f"Opublikowano: {ts_pdf}")
                st.write("Raport przygotowany przez zespół Black Stag Intelligence.")

                with open(report_path, "rb") as f:
                    st.download_button(
                        label="POBIERZ AKTUALNY RAPORT (PDF)",
                        data=f,
                        file_name=f"Black_Stag_Report_{ts_pdf.replace(':', '-')}.pdf",
                        mime="application/pdf",
                        type="primary"
                    )
        else:
            st.info("Oczekiwanie na publikację dzisiejszego raportu geopolitycznego.")

        st.markdown("---")

        # --- SEKCJA 3: WYKRESY (CURRENCY MONITOR) ---
        st.markdown("### 📈 CURRENCY MONITOR")

        c1, c2 = st.columns(2)

        with c1:
            st.markdown("**EUR/PLN**")
            fig_eur = market_data.get_chart_of_day("EUR/PLN")
            if fig_eur:
                st.plotly_chart(fig_eur, use_container_width=True)
            else:
                st.warning("Brak danych wykresu.")

        with c2:
            st.markdown("**USD/PLN**")
            fig_usd = market_data.get_chart_of_day("USD/PLN")
            if fig_usd:
                st.plotly_chart(fig_usd, use_container_width=True)
            else:
                st.warning("Brak danych wykresu.")