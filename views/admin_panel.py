import streamlit as st
import os
import json
from datetime import datetime


def get_file_info(path):
    """Pobiera czas ostatniej modyfikacji pliku."""
    if os.path.exists(path):
        mtime = os.path.getmtime(path)
        return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
    return None


def show():
    st.header("🛠️ PANEL ADMINISTRATORA")

    # Zabezpieczenie struktury folderów
    os.makedirs("data", exist_ok=True)
    news_file = "data/news.json"
    radar_file = "data/risk_radar.json"  # Plik dla radaru

    # ==========================================
    # NOWA SEKCJA: ZARZĄDZANIE RISK RADAR
    # ==========================================
    with st.expander("📡 Zarządzaj Spectra Risk Radar", expanded=True):
        st.markdown("Tutaj wprowadzisz codzienne ustawienia z Twojego prywatnego algorytmu Google Sheets.")

        # Opcje statusu
        status_options = [
            "🟢 SILNY RISK-ON",
            "🟡 UMIARKOWANY RISK-ON",
            "⚫ NEUTRALNIE",
            "🟠 UMIARKOWANY RISK-OFF",
            "🔴 SILNY RISK-OFF"
        ]

        selected_status = st.selectbox("1. Poziom Ryzyka (Wynik z arkusza):", status_options, index=2)

        st.markdown("2. Poranny Briefing (3 kluczowe punkty):")
        bullet_1 = st.text_input("Punkt 1 (np. VIX rośnie...):")
        bullet_2 = st.text_input("Punkt 2 (np. Dolar umacnia...):")
        bullet_3 = st.text_input("Punkt 3 (np. Geopolityka...):")

        if st.button("🚀 Opublikuj na Radarze", type="primary"):
            radar_data = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "status": selected_status,
                "bullets": [bullet_1, bullet_2, bullet_3]
            }
            with open(radar_file, "w", encoding="utf-8") as f:
                json.dump(radar_data, f, indent=4)
            st.success("Risk Radar został zaktualizowany!")

    # ==========================================
    # SEKCJA NEWSÓW
    # ==========================================
    if os.path.exists(news_file):
        with open(news_file, "r", encoding="utf-8") as f:
            try:
                news_list = json.load(f)
            except json.JSONDecodeError:
                news_list = []
    else:
        news_list = []

    with st.expander("📰 Zarządzaj Komunikatami Rynkowymi"):
        st.markdown("#### ➕ Dodaj nowy komunikat")
        title = st.text_input("Tytuł / Nagłówek komunikatu:")
        content = st.text_area("Treść / Analiza (rozwinięcie):")

        if st.button("Publikuj News"):
            if title and content:
                new_news = {
                    "id": datetime.now().strftime("%Y%m%d%H%M%S"),
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "title": title,
                    "content": content
                }
                news_list.insert(0, new_news)

                with open(news_file, "w", encoding="utf-8") as f:
                    json.dump(news_list, f, indent=4)

                st.success("Komunikat opublikowany!")
                st.rerun()
            else:
                st.warning("Musisz podać zarówno Tytuł, jak i Treść.")

        st.markdown("---")
        st.markdown("#### 📂 Opublikowane komunikaty")
        if news_list:
            for idx, item in enumerate(news_list):
                col1, col2 = st.columns([4, 1])
                col1.write(f"**{item['title']}** ({item['date']})")

                if col2.button("Usuń", key=f"del_{item['id']}", type="secondary"):
                    news_list.pop(idx)
                    with open(news_file, "w", encoding="utf-8") as f:
                        json.dump(news_list, f, indent=4)
                    st.rerun()
        else:
            st.info("Brak aktywnych komunikatów.")

    # ==========================================
    # SEKCJA RAPORTÓW PDF
    # ==========================================
    with st.expander("📄 Zarządzaj Raportami PDF"):
        pdf_path = "data/raport.pdf"
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
                if st.button("❌ USUŃ AKTUALNY RAPORT", type="secondary"):
                    try:
                        os.remove(pdf_path)
                        st.success("Raport został usunięty z portalu.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Wystąpił błąd podczas usuwania: {e}")