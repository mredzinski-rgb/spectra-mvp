import streamlit as st
import os


def show():
    st.header("🛠️ PANEL ADMINISTRATORA")

    # 1. Zabezpieczenie struktury folderów
    if not os.path.exists("data"):
        os.makedirs("data")

    # --- SEKCJA NEWSÓW ---
    with st.expander("Edytuj Komunikat Rynkowy", expanded=True):
        # Wczytanie aktualnego newsa, żeby admin widział co jest opublikowane
        current_news = ""
        if os.path.exists("data/news.txt"):
            with open("data/news.txt", "r", encoding="utf-8") as f:
                current_news = f.read()

        msg = st.text_area("Treść ogłoszenia (widoczna na Dashboardzie):", value=current_news)

        if st.button("Publikuj News"):
            if msg:
                with open("data/news.txt", "w", encoding="utf-8") as f:
                    f.write(msg)
                st.success("Komunikat opublikowany!")
                st.rerun()
            else:
                st.warning("Nie możesz opublikować pustego komunikatu.")

    # --- SEKCJA RAPORTÓW PDF ---
    with st.expander("Zarządzaj Raportami PDF"):
        st.info("Wgranie nowego pliku nadpisze poprzedni raport dzienny.")

        pdf = st.file_uploader("Wgraj raport geopolityczny / audyt", type="pdf")

        # Przycisk zapisu
        if st.button("Zapisz i Opublikuj PDF"):
            if pdf:
                # Używamy stałej nazwy pliku, aby Dashboard zawsze wiedział co pobrać
                file_path = "data/daily_report.pdf"

                with open(file_path, "wb") as f:
                    f.write(pdf.getbuffer())

                st.success(f"Raport '{pdf.name}' jest już widoczny dla klientów!")
            else:
                st.error("Najpierw wybierz plik PDF z dysku.")

        # Opcja usunięcia aktualnego raportu
        if os.path.exists("data/daily_report.pdf"):
            st.markdown("---")
            if st.button("❌ USUŃ AKTUALNY RAPORT"):
                os.remove("data/daily_report.pdf")
                st.success("Raport został usunięty z portalu.")
                st.rerun()