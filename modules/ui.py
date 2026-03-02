import streamlit as st
import base64
import os


def load_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Roboto:wght@300;400;700&display=swap');
        .stApp { background: radial-gradient(circle at center, #0f2027 0%, #203a43 50%, #2c5364 100%); color: #ffffff !important; font-family: 'Roboto', sans-serif; }

        /* Animacja obrotowa */
        @keyframes spin { from { transform: rotateY(0deg); } to { transform: rotateY(360deg); } }
        .rotating-logo { 
            animation: spin 12s infinite linear; 
            filter: drop-shadow(0 0 20px rgba(100, 255, 218, 0.4));
            display: block; margin-left: auto; margin-right: auto;
        }

        .brand-title-text { font-family: 'Orbitron', sans-serif !important; text-shadow: 0 0 15px rgba(100, 255, 218, 0.8) !important; text-align: center !important; text-transform: uppercase; }
        .stButton>button { border: 2px solid #64ffda !important; font-family: 'Orbitron', sans-serif; background: rgba(255, 255, 255, 0.05) !important; color: #64ffda !important; width: 100%; }
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