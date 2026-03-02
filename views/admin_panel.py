import streamlit as st
import os
from datetime import datetime


def get_file_info(path):
    """Pobiera czas ostatniej modyfikacji pliku."""
    if os.path.exists(path):
        mtime = os.path.getmtime(path)
        return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
    return None


def show():
    st.header("🛠️ PANEL ADMINISTRATORA")

    # 1. Zabezpieczenie struktury folderów
    if not os.path.exists("data"):
        os.makedirs("data")

    # --- SEKCJA NEWSÓW ---
    with st.expander("Zarządzaj Komunikatem Rynkowym", expanded=True):
        news_path = "data/news.txt"
        current_news = ""

        # Pobieranie daty publikacji newsa
        news_ts = get_file_info(news_path)
        if news_ts:
            st.info(f"Ostatnia aktualizacja komunikatu: {news_ts}")
            with open(news_path, "r", encoding="utf-8") as f:
                current_news = f.read()
        else:
            st.write("Aktualnie brak opublikowanego komunikatu.")

        msg = st.text_area("Treść nowego ogłoszenia:", value=current_news)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Publikuj News"):
                if msg:
                    with open(news_path, "w", encoding="utf-8") as f:
                        f.write(msg)
                    st.success("Komunikat opublikowany!")
                    st.rerun()
                else:
                    st.warning("Nie możesz opublikować pustego komunikatu.")

        with col2:
            if os.path.exists(news_path):
                # Przycisk czerwony (secondary) do usuwania
                if st.button("❌ USUŃ AKTUALNY NEWS", type="secondary"):
                    os.remove(news_path)
                    st.success("Komunikat został usunięty.")
                    st.rerun()

    # --- SEKCJA RAPORTÓW PDF ---
    with st.expander("Zarządzaj Raportami PDF"):
        pdf_path = "data/daily_report.pdf"

        # Pobieranie daty publikacji raportu
        pdf_ts = get_file_info(pdf_path)
        if pdf_ts:
            st.info(f"Ostatnia publikacja raportu: {pdf_ts}")
        else:
            st.write("Aktualnie brak wgranego raportu PDF.")

        st.markdown("---")
        pdf = st.file_uploader("Wgraj nowy raport geopolityczny / audyt", type="pdf")

        col3, col4 = st.columns(2)
        with col3:
            if st.button("Zapisz i Opublikuj PDF"):
                if pdf:
                    with open(pdf_path, "wb") as f:
                        f.write(pdf.getbuffer())
                    st.success(f"Raport '{pdf.name}' został opublikowany!")
                    st.rerun()
                else:
                    st.error("Najpierw wybierz plik PDF z dysku.")

        with col4:
            if os.path.exists(pdf_path):
                # Przycisk czerwony (secondary) do usuwania
                if st.button("❌ USUŃ AKTUALNY RAPORT", type="secondary"):
                    os.remove(pdf_path)
                    st.success("Raport został usunięty z portalu.")
                    st.rerun()