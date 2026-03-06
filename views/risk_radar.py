import streamlit as st
import json
import os


def show():
    st.markdown("### 📡 SPECTRA RISK RADAR")

    # Zabezpieczenie na wypadek braku pliku
    data_path = "data/risk_radar.json"
    if os.path.exists(data_path):
        with open(data_path, "r", encoding="utf-8") as f:
            radar_data = json.load(f)
    else:
        # Domyślne dane, jeśli admin jeszcze nic nie ustawił
        radar_data = {
            "date": "Brak danych",
            "status": "⚫ NEUTRALNIE",
            "bullets": ["Oczekiwanie na aktualizację z centrum analitycznego Black Stag FX.", "", ""]
        }

    # 1. BAROMETR NASTROJÓW (Hero Element)
    st.markdown("#### 📍 GLOBALNY BAROMETR NASTROJÓW")
    st.caption(f"Ostatnia aktualizacja: {radar_data.get('date', 'Brak')}")

    # Wyświetlanie statusu z dużym wizualnym naciskiem
    status = radar_data.get("status", "⚫ NEUTRALNIE")

    # Używamy st.info/warning/error dla estetycznego tła w zależności od ryzyka
    if "RISK-ON" in status:
        st.success(f"**STATUS RYNKOWY:** {status}")
    elif "NEUTRALNIE" in status:
        st.info(f"**STATUS RYNKOWY:** {status}")
    else:
        st.error(f"**STATUS RYNKOWY:** {status}")

    st.markdown("---")

    # 2. PORANNY BRIEFING (Zasada 3 punktów)
    st.markdown("#### 📋 PORANNY BRIEFING (Kluczowe wektory)")
    bullets = radar_data.get("bullets", [])
    for b in bullets:
        if b.strip():  # Pokaż tylko jeśli nie jest puste
            st.markdown(f"- {b}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Przycisk Call To Action do Dealera
    if st.button("📞 SKONSULTUJ POZYCJE Z FX DEALEREM", type="primary", use_container_width=True):
        st.toast("Aby połączyć się z dealerem, użyj zakładki bocznej i podaj swój numer.")

    st.markdown("---")

    # 3. RADAR GEOPOLITYCZNY (Placeholder na mapę w przyszłości)
    st.markdown("#### 🗺️ AKTYWNE OGNISKA ZAPALNE")
    st.info("Trwa ładowanie koordynatów satelitarnych... (Moduł mapy interaktywnej w przygotowaniu)")

    st.markdown("---")

    # 4. GUSTOWNY DISCLAIMER PRAWNY
    disclaimer_html = """
    <div style="font-size: 0.8em; color: #888; text-align: justify; margin-top: 50px; border-top: 1px solid #444; padding-top: 10px;">
        <strong>Nota Prawna / Wyłączenie odpowiedzialności:</strong> Notowania giełdowe i wskaźniki ryzyka nie obejmują wszystkich rynków i mogą być opóźnione maksymalnie o 20 minut. Informacje są dostarczane w niezmienionej formie, wyłącznie w celach informacyjnych. Nie są one przeznaczone do celów handlowych ani nie mają charakteru doradczego. Prezentowany poziom ryzyka jest subiektywną oceną analityczną Black Stag FX i nie stanowi rekomendacji inwestycyjnej w rozumieniu przepisów prawa.
    </div>
    """
    st.markdown(disclaimer_html, unsafe_allow_html=True)