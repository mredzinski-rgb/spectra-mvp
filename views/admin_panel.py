import streamlit as st
import os


def show():
    st.header("🛠️ PANEL ADMINISTRATORA")
    # Zabezpieczenie folderu
    os.makedirs("data", exist_ok=True)

    with st.expander("Edytuj Komunikat Rynkowy", expanded=True):
        msg = st.text_area("Treść ogłoszenia:")
        if st.button("Publikuj News"):
            with open("data/news.txt", "w", encoding="utf-8") as f:
                f.write(msg)
            st.success("Komunikat opublikowany!")

    # 2. Raporty
    with st.expander("Zarządzaj Raportami PDF"):
        pdf = st.file_uploader("Wgraj raport geopolityczny", type="pdf")
        if st.button("Zapisz PDF"):
            if pdf:
                with open("data/raport.pdf", "wb") as f:
                    f.write(pdf.getbuffer())
                st.success("Raport gotowy do pobrania!")