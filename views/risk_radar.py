import streamlit as st
import json
import os
import plotly.graph_objects as go


def show():
    st.markdown("### SPECTRA RISK RADAR")

    # Wczytywanie danych
    data_path = "data/risk_radar.json"
    if os.path.exists(data_path):
        with open(data_path, "r", encoding="utf-8") as f:
            radar_data = json.load(f)
    else:
        radar_data = {
            "date": "Brak danych",
            "status": "⚫ NEUTRALNIE",
            "bullets": ["Oczekiwanie na aktualizację z centrum analitycznego Black Stag FX."],
            "hotspots": []
        }

    status = radar_data.get("status", "⚫ NEUTRALNIE")

    # -----------------------------------------------------------
    # 1. ZEGAR RYZYKA (PLOTLY GAUGE)
    # -----------------------------------------------------------
    # Mapowanie statusu na wartość liczbową do zegara
    status_values = {
        "🟢 SILNY RISK-ON": 1,
        "🟡 UMIARKOWANY RISK-ON": 2,
        "⚫ NEUTRALNIE": 3,
        "🟠 UMIARKOWANY RISK-OFF": 4,
        "🔴 SILNY RISK-OFF": 5
    }
    gauge_val = status_values.get(status, 3)

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge",
        value=gauge_val,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "POZIOM AWERSJI DO RYZYKA", 'font': {'size': 16, 'color': 'white'}},
        gauge={
            'axis': {'range': [0.5, 5.5], 'tickwidth': 1, 'tickcolor': "white",
                     'tickvals': [1, 2, 3, 4, 5],
                     'ticktext': ['Silny<br>Risk-On', 'Umiark.<br>Risk-On', 'Neutralnie', 'Umiark.<br>Risk-Off',
                                  'Silny<br>Risk-Off']},
            'bar': {'color': "rgba(255,255,255,0.8)", 'thickness': 0.15},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0.5, 1.5], 'color': "#00cc66"},  # Zielony
                {'range': [1.5, 2.5], 'color': "#99ff33"},  # Jasnozielony
                {'range': [2.5, 3.5], 'color': "#808080"},  # Szary
                {'range': [3.5, 4.5], 'color': "#ff9933"},  # Pomarańczowy
                {'range': [4.5, 5.5], 'color': "#ff3300"}  # Czerwony
            ],
        }
    ))
    fig_gauge.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font={'color': "white"},
        height=250,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    st.plotly_chart(fig_gauge, use_container_width=True)

    # -----------------------------------------------------------
    # 2. PORANNY BRIEFING
    # -----------------------------------------------------------
    st.markdown("#### PORANNY BRIEFING (Kluczowe wektory)")
    st.caption(f"Ostatnia aktualizacja: {radar_data.get('date', 'Brak')}")

    bullets = radar_data.get("bullets", [])
    for b in bullets:
        if b.strip():
            st.markdown(f"- {b}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Zmieniony tekst przycisku
    if st.button("📞 KONTAKT Z OPIEKUNEM KLIENTA", type="primary", use_container_width=True):
        st.toast("Aby połączyć się z opiekunem, użyj zakładki bocznej i podaj swój numer.")

    st.markdown("---")

    # -----------------------------------------------------------
    # 3. INTERAKTYWNA MAPA ŚWIATA (GEOPOLITYKA)
    # -----------------------------------------------------------
    st.markdown("#### RADAR GEOPOLITYCZNY (Aktywne ogniska)")
    hotspots = radar_data.get("hotspots", [])

    if hotspots:
        lats = [h["lat"] for h in hotspots]
        lons = [h["lon"] for h in hotspots]
        texts = [f"{h['name']}<br>{h['desc']}" for h in hotspots]

        fig_map = go.Figure(go.Scattergeo(
            lon=lons,
            lat=lats,
            text=texts,
            hoverinfo='text',
            mode='markers+text',
            marker=dict(size=14, color='rgba(255, 50, 50, 0.9)', symbol='circle',
                        line=dict(width=2, color='white')),
            textfont=dict(color="white", size=11),
            textposition="bottom center"
        ))

        fig_map.update_layout(
            geo=dict(
                showland=True,
                landcolor="rgb(20, 35, 45)",  # Ciemny, holograficzny granat
                showocean=True,
                oceancolor="rgba(0,0,0,0)",
                showcountries=True,
                countrycolor="rgb(60, 90, 110)",
                bgcolor="rgba(0,0,0,0)",
                projection_type="natural earth"
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=0, b=0),
            height=350
        )
        st.plotly_chart(fig_map, use_container_width=True)

        # Wypisanie tekstowe pod mapą
        for h in hotspots:
            st.info(f"📍 **{h['name']}**: {h['desc']}")
    else:
        st.info("Brak aktywnych ognisk zapalnych na radarze.")

    st.markdown("---")

    # -----------------------------------------------------------
    # 4. GUSTOWNY DISCLAIMER PRAWNY (Zaktualizowany)
    # -----------------------------------------------------------
    disclaimer_html = """
    <div style="font-size: 0.75em; color: #888; text-align: justify; margin-top: 40px; border-top: 1px solid #444; padding-top: 15px; line-height: 1.4;">
        <strong>Nota Prawna / Wyłączenie odpowiedzialności:</strong> Informacje i komunikaty prezentowane na platformie Spectra są dostarczane wyłącznie w celach informacyjnych i edukacyjnych. Nie są one przeznaczone do celów handlowych, nie stanowią wiążącej oferty ani nie mają charakteru doradztwa inwestycyjnego, podatkowego lub prawnego w rozumieniu obowiązujących przepisów KNF i UE. Prezentowany poziom ryzyka jest subiektywną oceną analityczną Black Stag FX opartą na autorskich modelach. Użytkownik podejmuje wszelkie decyzje finansowe na własne ryzyko. Black Stag FX nie ponosi odpowiedzialności za decyzje podjęte na podstawie niniejszego opracowania.
    </div>
    """
    st.markdown(disclaimer_html, unsafe_allow_html=True)