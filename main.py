import streamlit as st
import os
from modules import ui, market_data, mailer
from views import dashboard, admin_panel

# 1. KONFIGURACJA WIZUALNA
ui.load_css()

if "auth" not in st.session_state:
    st.session_state.auth = False
    st.session_state.role = None
    st.session_state.user_id = None

# =================================================
#               EKRAN PUBLICZNY (Auth & KYC)
# =================================================
if not st.session_state.auth:
    ui.show_branding()

    tab_login, tab_reg = st.tabs(["Logowanie", "Rejestracja Nowego Klienta (KYC)"])

    with tab_login:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### PANEL DOSTĘPU")
            user_input = st.text_input("Operator ID")
            pw_input = st.text_input("Access Code", type="password")

            if st.button("AUTHORIZE"):
                try:
                    admin_pass = st.secrets["passwords"]["admin"]
                    klient_pass = st.secrets["passwords"]["klient"]
                except:
                    admin_pass, klient_pass = "BlackStag2026!", "SpectraStart"

                if user_input == "admin" and pw_input == admin_pass:
                    st.session_state.auth = True
                    st.session_state.role = "admin"
                    st.session_state.user_id = user_input
                    st.rerun()
                elif user_input == "klient" and pw_input == klient_pass:
                    st.session_state.auth = True
                    st.session_state.role = "client"
                    st.session_state.user_id = user_input
                    st.rerun()
                else:
                    st.error("Access Denied: Błędny Operator ID lub Access Code")

    with tab_reg:
        st.subheader("Formularz Onboardingowy KYC")
        st.info("Wypełnij dane, aby uzyskać dostęp do subskrypcji Spectra.")

        with st.form("reg_form"):
            c1, c2 = st.columns(2)
            with c1:
                comp_name = st.text_input("Pełna nazwa firmy")
                nip_val = st.text_input("NIP")
                email_val = st.text_input("Email służbowy")
            with c2:
                turnover = st.selectbox("Roczny obrót FX",
                                        ["< 100k EUR", "100k - 1mln EUR", "1-5 mln EUR", "> 5 mln EUR"])
                person = st.text_input("Osoba kontaktowa (Imię i Nazwisko)")
                interest = st.multiselect("Zainteresowanie", ["Black Stag Spectra", "Platforma Keewe", "Audyt FX"])

            agree = st.checkbox("Wyrażam zgodę na weryfikację KYC i przetwarzanie danych zgodnie z RODO.")

            if st.form_submit_button("Prześlij wniosek"):
                if agree and comp_name and email_val:
                    kyc_body = f"Nowe zgłoszenie KYC:\nFirma: {comp_name}\nNIP: {nip_val}\nKontakt: {person} ({email_val})\nObrót: {turnover}\nZainteresowania: {interest}"
                    if mailer.send_notification("NOWY WNIOSEK KYC", kyc_body):
                        st.success("Wniosek został wysłany! Skontaktujemy się wkrótce.")
                    else:
                        st.error("Błąd wysyłki powiadomienia. Spróbuj ponownie później.")
                else:
                    st.error("Proszę wypełnić wymagane pola i zaakceptować zgodę RODO.")

# =================================================
#               EKRAN OPERACYJNY (Zalogowany)
# =================================================
else:
    with st.sidebar:
        ui.show_branding("SPECTRA", "LIVE")

        st.markdown("---")

        client_phone = st.text_input("Twój numer telefonu (dla Dealera)", placeholder="+48 ...")

        if st.button("📞 KONTAKT Z FX DEALEREM", type="secondary"):
            client_id = st.session_state.get('user_id', st.session_state.role)

            contact_msg = f"""
                PILNA PROŚBA O KONTAKT (SPECTRA):
                ---------------------------------
                Operator ID: {client_id}
                Numer telefonu: {client_phone if client_phone else 'Nie podano'}
                Rola w systemie: {st.session_state.role}
                ---------------------------------
                Wysłano z: Spectra Operations Center
                """

            if mailer.send_notification(f"PROŚBA O KONTAKT: {client_id}", contact_msg):
                st.toast("Powiadomienie wysłane do Dealera!")
                st.success(f"Zgłoszenie wysłane. Oddzwonimy na podany numer.")
            else:
                st.error("Błąd połączenia z serwerem pocztowym.")

        st.markdown("---")
        menu = ["DASHBOARD", "WERYFIKACJA KONTRAHENTA"]
        if st.session_state.role == "admin":
            menu.append("ADMIN PANEL")

        choice = st.radio("NAWIGACJA CENTRUM:", menu)

        st.markdown("---")
        if st.button("TERMINATE SESSION"):
            st.session_state.auth = False
            st.session_state.role = None
            st.session_state.user_id = None
            st.rerun()

    # --- ROUTING WIDOKÓW ---

    # ZMIANA: Usunięto stary blok `if choice == "DASHBOARD":` czytający `news.txt`
    if choice == "DASHBOARD":
        dashboard.show()

    elif choice == "WERYFIKACJA KONTRAHENTA":
        st.header("Weryfikacja Kontrahenta / Zgłoszenie Dłużnika")
        with st.form("kyc_check"):
            target_name = st.text_input("Pełna Nazwa Firmy")
            target_id = st.text_input("Numer ID (NIP / KRS / REGON)")
            target_country = st.selectbox("Kraj rejestracji", ["Polska", "Niemcy", "UK", "Chiny", "USA", "Inne"])
            target_reason = st.text_area("Cel badania / zgłoszenie dłużnika - opis sprawy")

            user_contact_info = st.text_input("Twój email lub telefon do przesłania wyceny",
                                              placeholder="np. jan.kowalski@firma.pl")

            if st.form_submit_button("Wyślij zapytanie"):
                if target_name and target_id:
                    client_id = st.session_state.get('user_id', 'Nieznany')

                    audit_body = f"""
                    ZLECENIE AUDYTU KONTRAHENTA:
                    ----------------------------
                    Zleceniodawca (ID): {client_id}
                    Kontakt zwrotny: {user_contact_info if user_contact_info else 'Nie podano'}

                    DANE KONTRAHENTA:
                    Nazwa: {target_name}
                    ID: {target_id}
                    Kraj: {target_country}
                    Cel: {target_reason}
                    ----------------------------
                    """
                    if mailer.send_notification(f"AUDYT: {target_name}", audit_body):
                        st.success("Zgłoszenie przyjęte. FX Dealer przygotuje wycenę badania.")
                    else:
                        st.error("Błąd wysyłki zgłoszenia.")
                else:
                    st.error("Podaj nazwę i NIP kontrahenta.")

    elif choice == "ADMIN PANEL":
        admin_panel.show()