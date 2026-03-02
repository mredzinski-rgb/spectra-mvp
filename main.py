import streamlit as st
import os
from modules import ui, market_data
from views import dashboard, admin_panel

# 1. KONFIGURACJA WIZUALNA
ui.load_css()  # Wczytuje Twoje niestandardowe style CSS i animacje

if "auth" not in st.session_state:
    st.session_state.auth = False
    st.session_state.role = None

# =================================================
#               EKRAN PUBLICZNY (Auth & KYC)
# =================================================
if not st.session_state.auth:
    ui.show_branding()  # Wyświetla obracające się logo

    # Punkt 2: Zakładka logowania i rozbudowana rejestracja
    tab_login, tab_reg = st.tabs(["Logowanie", "Rejestracja Nowego Klienta (KYC)"])

    with tab_login:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### PANEL DOSTĘPU")
            user = st.text_input("Operator ID")
            pw = st.text_input("Access Code", type="password")

            if st.button("AUTHORIZE"):
                # Punkt 1: Naprawa logowania - ujednolicenie haseł
                # Sprawdza hasła z secrets.toml lub używa fallbacku
                try:
                    admin_pass = st.secrets["passwords"]["admin"]
                    klient_pass = st.secrets["passwords"]["klient"]
                except:
                    admin_pass, klient_pass = "BlackStag2026!", "SpectraStart"

                if user == "admin" and pw == admin_pass:
                    st.session_state.auth, st.session_state.role = True, "admin"
                    st.rerun()
                elif user == "klient" and pw == klient_pass:
                    st.session_state.auth, st.session_state.role = True, "client"
                    st.rerun()
                else:
                    st.error("Access Denied: Błędny Operator ID lub Access Code")

    with tab_reg:
        # Punkt 2: Rozbudowany formularz Onboardingowy zgodny ze screenem
        st.subheader("Formularz Onboardingowy KYC")
        st.info("Wypełnij dane, aby uzyskać dostęp do subskrypcji Spectra i preferencyjnych stawek Keewe.")

        with st.form("reg_form"):
            c1, c2 = st.columns(2)
            with c1:
                st.text_input("Pełna nazwa firmy")
                st.text_input("NIP")
                st.text_input("Email służbowy")
            with c2:
                st.selectbox("Roczny obrót FX", ["< 100k EUR", "100k - 1mln EUR", "1-5 mln EUR", "> 5 mln EUR"])
                st.text_input("Osoba kontaktowa (Imię i Nazwisko)")
                st.multiselect("Zainteresowanie", ["Black Stag Spectra", "Platforma Keewe", "Audyt FX"])

            agree = st.checkbox("Wyrażam zgodę na weryfikację KYC i przetwarzanie danych zgodnie z RODO.")

            if st.form_submit_button("Prześlij wniosek"):
                if agree:
                    st.success("Wniosek został wysłany do weryfikacji. Skontaktujemy się wkrótce!")
                else:
                    st.error("Proszę zaakceptować zgodę RODO.")

# =================================================
#               EKRAN OPERACYJNY (Zalogowany)
# =================================================
else:
    with st.sidebar:
        ui.show_branding("SPECTRA", "LIVE")

        # Punkt 7: Przycisk Kontaktu - zawsze widoczny w sidebarze
        st.markdown("---")
        if st.button("📞 KONTAKT Z FX DEALEREM"):
            st.toast("Powiadomienie wysłane do Dealera. Oddzwonimy w ciągu 15 min!")
            st.info("Status: Oczekiwanie na połączenie z Dealerem...")

        st.markdown("---")
        menu = ["DASHBOARD", "WERYFIKACJA KONTRAHENTA"]
        if st.session_state.role == "admin":
            menu.append("ADMIN PANEL")

        choice = st.radio("NAWIGACJA CENTRUM:", menu)

        st.markdown("---")
        if st.button("TERMINATE SESSION"):
            st.session_state.auth = False
            st.rerun()

    # Routing Widoków
    if choice == "DASHBOARD":
        # Sprawdzenie istnienia newsa przed wyświetleniem (naprawa FileNotFoundError)
        news_path = "data/news.txt"
        if os.path.exists(news_path):
            with open(news_path, "r", encoding="utf-8") as f:
                content = f.read()
                if content:
                    st.warning(f"🔔 **KOMUNIKAT RYNKOWY:** {content}")
        dashboard.show()  # Wywołuje Twój moduł wykresów i kafli

    elif choice == "WERYFIKACJA KONTRAHENTA":
        st.header("🕵️ Weryfikacja Kontrahenta")
        # Punkt 3: Rozdzielenie linii na Nazwę i ID
        with st.form("kyc_check"):
            st.text_input("Pełna Nazwa Firmy")
            st.text_input("Numer ID (NIP / KRS / REGON)")
            st.selectbox("Kraj rejestracji", ["Polska", "Niemcy", "Wielka Brytania", "Chiny", "USA", "Inne"])
            st.text_area("Cel badania (np. nawiązanie współpracy, audyt płatności)")

            if st.form_submit_button("Wyślij zapytanie o audyt"):
                st.success("Zgłoszenie przyjęte. FX Dealer przygotuje wycenę badania.")

    elif choice == "ADMIN PANEL":
        admin_panel.show()  # Umożliwia wgranie raportu PDF i edycję newsa