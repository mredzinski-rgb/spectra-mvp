import streamlit as st

def send_notification(subject, body):
    # Na MVP: Wyświetlamy sukces i logujemy do konsoli.
    # Docelowo tutaj wstawisz kod SMTP (Gmail/Outlook).
    st.success("Twoje zgłoszenie zostało wysłane do FX Dealera. Oddzwonimy w ciągu 15 minut.")
    print(f"POWIADOMIENIE: {subject}\nTreść: {body}")

def counterparty_form():
    st.subheader("🕵️ Sprawdź Kontrahenta")
    st.info("Zlec badanie wiarygodności swojego partnera biznesowego przed transakcją.")
    with st.form("kyc_request"):
        name = st.text_input("Nazwa firmy")
        nip = st.text_input("NIP / KRS")
        details = st.text_area("Dodatkowe informacje (np. kraj rejestracji)")
        if st.form_submit_button("Wyślij zapytanie o wycenę"):
            send_notification(f"ZLECENIE KYC: {name}", f"NIP: {nip}\nSzczegóły: {details}")

def dealer_contact_button():
    if st.sidebar.button("📞 KONTAKT Z FX DEALEREM"):
        send_notification("PROŚBA O KONTAKT", "Klient prosi o pilny kontakt telefoniczny.")