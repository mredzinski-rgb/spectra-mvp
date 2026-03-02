import streamlit as st
import os
from modules import ui, market_data
from views import dashboard, admin_panel

ui.load_css()

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    ui.show_branding()
    # Punkt 2: Dodanie zakładki rejestracji
    tab_login, tab_reg = st.tabs(["Logowanie", "Rejestracja Nowego Klienta (KYC)"])

    with tab_login:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            user = st.text_input("Operator ID")
            pw = st.text_input("Access Code", type="password")
            if st.button("AUTHORIZE"):
                if user == "admin" and pw == "admin":  # Uproszczone dla testu
                    st.session_state.auth, st.session_state.role = True, "admin"
                    st.rerun()
                elif user == "klient" and pw == "start":
                    st.session_state.auth, st.session_state.role = True, "client"
                    st.rerun()
                else:
                    st.error("Access Denied")

    with tab_reg:
        # Kod Twojego formularza KYC (uproszczony)
        st.subheader("Formularz Onboardingowy KYC")
        with st.form("reg_form"):
            st.text_input("Pełna nazwa firmy")
            st.text_input("Email służbowy")
            if st.form_submit_button("Prześlij wniosek"):
                st.success("Wniosek wysłany!")

else:
    with st.sidebar:
        ui.show_branding("SPECTRA", "LIVE")

        # Punkt 7: Przycisk Kontaktu
        if st.button("📞 KONTAKT Z FX DEALEREM"):
            st.info("Powiadomienie wysłane do Dealera. Oddzwonimy!")

        menu = ["DASHBOARD", "WERYFIKACJA KONTRAHENTA"]
        if st.session_state.role == "admin": menu.append("ADMIN PANEL")
        choice = st.radio("NAWIGACJA", menu)

        if st.button("TERMINATE SESSION"):
            st.session_state.auth = False
            st.rerun()

    if choice == "DASHBOARD":
        if os.path.exists("data/news.txt"):
            with open("data/news.txt", "r", encoding="utf-8") as f:
                st.warning(f"💡 {f.read()}")
        dashboard.show()

    elif choice == "WERYFIKACJA KONTRAHENTA":
        st.header("🕵️ Weryfikacja Kontrahenta")
        # Punkt 3: Rozdzielenie linii
        with st.form("kyc"):
            st.text_input("Nazwa Firmy")
            st.text_input("Numer ID (NIP / KRS / REGON)")
            st.selectbox("Kraj rejestracji", ["Polska", "Niemcy", "Inne"])
            if st.form_submit_button("Wyślij zapytanie o audyt"):
                st.success("Zgłoszenie przyjęte.")

    elif choice == "ADMIN PANEL":
        admin_panel.show()