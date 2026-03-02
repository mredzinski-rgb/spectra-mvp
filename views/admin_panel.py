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

    # 1. Zabezpieczenie struktury folderów
    os.makedirs("data", exist_ok=True)
    news_file = "data/news.json"

    # Wczytywanie istniejących komunikatów z pliku JSON
    if os.path.exists(news_file):
        with open(news_file, "r", encoding="utf-8") as f:
            try:
                news_list = json.load(f)
            except json.JSONDecodeError:
                news_list = []
    else:
        news_list = []

    # --- SEKCJA NEWSÓW ---
    with st.expander("Zarządzaj Komunikatami Rynkowymi", expanded=True):
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
                # Dodajemy najnowszy komunikat na samą górę listy
                news_list.insert(0, new_news)

                with open(news_file, "w", encoding="utf-8") as f:
                    json.dump(news_list, f, indent=4)

                st.success("Komunikat opublikowany!")
                st.rerun()
            else:
                st.warning("Musisz podać zarówno Tytuł, jak i Treść.")

        st.markdown("---")
        st.markdown("#### 📂 Opublikowane komunikaty")

        # Zarządzanie dodanymi newsami (Lista z opcją usuwania)
        if news_list:
            for idx, item in enumerate(news_list):
                col1, col2 = st.columns([4, 1])
                col1.write(f"**{item['title']}** ({item['date']})")

                # Przycisk czerwony (secondary) do usuwania
                if col2.button("Usuń", key=f"del_{item['id']}", type="secondary"):
                    news_list.pop(idx)
                    with open(news_file, "w", encoding="utf-8") as f:
                        json.dump(news_list, f, indent=4)
                    st.rerun()
        else:
            st.info("Brak aktywnych komunikatów.")

    # --- SEKCJA RAPORTÓW PDF ---
    with st.expander("Zarządzaj Raportami PDF"):
        # UJEDNOLICONA ŚCIEŻKA - musi być raport.pdf
        pdf_path = "data/raport.pdf"

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
            # Teraz funkcja celuje w poprawny plik raport.pdf
            if os.path.exists(pdf_path):
                # Przycisk czerwony (secondary) do usuwania
                if st.button("❌ USUŃ AKTUALNY RAPORT", type="secondary"):
                    try:
                        os.remove(pdf_path)
                        st.success("Raport został usunięty z portalu.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Wystąpił błąd podczas usuwania: {e}")