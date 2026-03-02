import streamlit as st
import base64
import os


def load_css():
    st.markdown("""
        <style>
        /* Twoje istniejące style... */

        /* CZERWONY PRZYCISK KONTAKTU */
        div.stButton > button:first-child[data-testid="baseButton-secondary"] {
            background-color: #ff4b4b !important;
            color: white !important;
            border: 2px solid #ff4b4b !important;
            font-weight: bold !important;
            box-shadow: 0 0 15px rgba(255, 75, 75, 0.4);
        }
        div.stButton > button:first-child[data-testid="baseButton-secondary"]:hover {
            background-color: #ff3333 !important;
            box-shadow: 0 0 25px rgba(255, 75, 75, 0.6);
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)


def get_img_as_base64(file_path):
    if not os.path.exists(file_path): return None
    with open(file_path, "rb") as f: data = f.read()
    return base64.b64encode(data).decode()


def show_branding(main_title="BLACK STAG SPECTRA", subtitle="OPERATIONS CENTER"):
    img_path = os.path.join("assets", "logo.png")
    img_base64 = get_img_as_base64(img_path)

    if img_base64:
        logo_html = f'<img src="data:image/png;base64,{img_base64}" class="rotating-logo" style="width: 120px;">'
    else:
        logo_html = '<div style="font-size: 80px; text-align: center;">🦌</div>'

    st.markdown(f"""
        <div style="text-align: center; padding: 20px 0;">
            {logo_html}
            <div class="brand-title-text" style="font-size: 2.2rem; margin-top: 10px;">{main_title}</div>
            <div style="color: #64ffda; letter-spacing: 5px; font-family: 'Orbitron'; font-size: 0.8rem;">{subtitle}</div>
        </div>
    """, unsafe_allow_html=True)