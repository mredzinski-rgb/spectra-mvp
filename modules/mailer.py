import smtplib
import ssl
import certifi  # Biblioteka z certyfikatami
from email.message import EmailMessage
import streamlit as st


def send_notification(subject, body):
    try:
        login_user = st.secrets["email"]["user"]
        app_password = st.secrets["email"]["password"]
        from_alias = st.secrets["email"]["alias"]
        to_admin = st.secrets["email"]["receiver"]

        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = f"SPECTRA SYSTEM: {subject}"
        msg['From'] = from_alias
        msg['To'] = to_admin

        # POPRAWKA SSL: Używamy certifi, aby wskazać Pythonowi gdzie są certyfikaty
        context = ssl.create_default_context(cafile=certifi.where())

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(login_user, app_password)
            server.send_message(msg)
        return True
    except Exception as e:
        st.error(f"Błąd wysyłki: {e}")
        return False