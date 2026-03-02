import streamlit as st
import base64
import os


def load_css():
    """Wczytuje pełną tożsamość wizualną Black Stag Spectra."""
    st.markdown("""
        <style>
        /* 1. CZCIONKI I TŁO */
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Roboto:wght@300;400;700&display=swap');

        .stApp { 
            background: radial-gradient(circle at center, #0f2027 0%, #203a43 50%, #2c5364 100%);
            color: #ffffff !important;
            font-family: 'Roboto', sans-serif; 
        }

        /* 2. UKRYWANIE ELEMENTÓW STREAMLIT */
        #MainMenu, footer, header {visibility: hidden;}
        [data-testid="collapsedControl"] { display: none !important; }

        /* 3. ANIMACJA LOGO */
        @keyframes spin { 
            from { transform: rotateY(0deg); } 
            to { transform: rotateY(360deg); } 
        }
        .rotating-logo {
            animation: spin 12s infinite linear; 
            filter: drop-shadow(0 0 20px rgba(100, 255, 218, 0.4));
            margin-bottom: 10px;
            display: block;
            margin-left: auto;
            margin-right: auto;
        }

        /* 4. TYPOGRAFIA BRANDINGOWA */
        .brand-title-text {
            font-family: 'Orbitron', sans-serif !important;
            font-weight: 900 !important; 
            color: #ffffff !important;
            text-shadow: 0 0 15px rgba(100, 255, 218, 0.8) !important;
            text-transform: uppercase !important;
            letter-spacing: 2px !important; 
            text-align: center !important;
        }

        .brand-subtitle-text {
            font-family: 'Orbitron', sans-serif !important;
            color: #64ffda !important;
            letter-spacing: 4px !important;
            text-transform: uppercase !important;
            text-align: center !important;
            font-size: 0.8rem !important;
        }

        /* 5. CZERWONY PRZYCISK KONTAKTU (Secondary) */
        /* Celujemy bezpośrednio w przycisk oznaczony jako 'secondary' w main.py */
        div.stButton > button[data-testid="baseButton-secondary"] {
            background-color: #ff4b4b !important;
            color: white !important;
            border: 2px solid #ff4b4b !important;
            font-family: 'Orbitron', sans-serif !important;
            font-weight: bold !important;
            text-transform: uppercase !important;
            box-shadow: 0 0 15px rgba(255, 75, 75, 0.4) !important;
            transition: all 0.3s ease !important;
            width: 100%;
        }

        div.stButton > button[data-testid="baseButton-secondary"]:hover {
            background-color: #ff3333 !important;
            box-shadow: 0 0 25px rgba(255, 75, 75, 0.7) !important;
            transform: scale(1.02);
            color: white !important;
        }

        /* 6. STYLE FORMULARZY I INPUTÓW */
        .stTextInput input, .stSelectbox div[data-baseweb="select"] {
            background-color: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(100, 255, 218, 0.2) !important;
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)


def get_img_as_base64(file_path):
    """Konwertuje obraz na format base64 do wyświetlenia w HTML."""
    if not os.path.exists(file_path):
        return None
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def show_branding(main_title="BLACK STAG SPECTRA", subtitle="GLOBAL INTELLIGENCE SYSTEM"):
    """Wyświetla animowane logo i stylizowane nagłówki."""
    img_path = os.path.join("assets", "logo.png")
    img_base64 = get_img_as_base64(img_path)

    if img_base64:
        logo_html = f'<img src="data:image/png;base64,{img_base64}" class="rotating-logo" style="width: 120px;">'
    else:
        # Fallback gdyby plik logo.png nie został znaleziony w assets/
        logo_html = '<div style="font-size: 80px; text-align: center; margin-bottom: 10px;">🦌</div>'

    st.markdown(f"""
        <div style="text-align: center; padding: 10px 0;">
            {logo_html}
            <div class="brand-title-text" style="font-size: 2.2rem;">{main_title}</div>
            <div class="brand-subtitle-text">{subtitle}</div>
        </div>
    """, unsafe_allow_html=True)