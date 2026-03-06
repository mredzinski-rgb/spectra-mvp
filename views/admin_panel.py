import streamlit as st
import os
import json
from datetime import datetime


def get_file_info(path):
    if os.path.exists(path):
        mtime = os.path.getmtime(path)
        return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
    return None


def show():
    st.header("🛠️ PANEL ADMINISTRATORA")

    os.makedirs("data", exist_ok=True)
    news_file = "data/news.json"
    radar_file = "data/risk_radar.json"

    # Wczytywanie danych radaru, aby móc nimi zarządzać
    if os.path.exists(radar_file):
        with open(radar_file, "r", encoding="utf-8") as f:
            radar_data = json.load(f)
    else:
        radar_data = {"date": "", "status": "⚫ NEUTRALNIE", "bullets": [], "hotspots": []}

    # ==========================================
    # SEKCJA: ZARZĄDZANIE RISK RADAR & MAPA
    # ==========================================
    with st.expander("📡 Zarządzaj Spectra Risk Radar", expanded=True):

        tab_wskaźnik, tab_mapa = st.tabs(["Wskaźnik i Briefing", "Ogniska Zapalne (Mapa)"])

        with tab_wskaźnik:
            st.markdown("#### 1. Poziom Ryzyka (Zegar)")
            status_options = [
                "🟢 SILNY RISK-ON",
                "🟡 UMIARKOWANY RISK-ON",
                "⚫ NEUTRALNIE",
                "🟠 UMIARKOWANY RISK-OFF",
                "🔴 SILNY RISK-OFF"
            ]

            # Ustawianie domyślnego indeksu na podstawie zapisanych danych
            try:
                curr_idx = status_options.index(radar_data.get("status", "⚫ NEUTRALNIE"))
            except ValueError:
                curr_idx = 2

            selected_status = st.selectbox("Wynik z arkusza Google Sheets:", status_options, index=curr_idx)

            st.markdown("#### 2. Poranny Briefing")
            old_bullets = radar_data.get("bullets", ["", "", ""])
            while len(old_bullets) < 3: old_bullets.append("")

            bullet_1 = st.text_input("Punkt 1:", value=old_bullets[0])
            bullet_2 = st.text_input("Punkt 2:", value=old_bullets[1])
            bullet_3 = st.text_input("Punkt 3:", value=old_bullets[2])

            if st.button("🚀 Zapisz Wskaźnik i Briefing", type="primary"):
                radar_data["date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                radar_data["status"] = selected_status
                radar_data["bullets"] = [bullet_1, bullet_2, bullet_3]

                with open(radar_file, "w", encoding="utf-8") as f:
                    json.dump(radar_data, f, indent=4)
                st.success("Wskaźnik zaktualizowany!")
                st.rerun()

        with tab_mapa:
            st.markdown("#### Aktualne ogniska na mapie:")
            hotspots = radar_data.get("hotspots", [])

            if hotspots:
                for idx, h in enumerate(hotspots):
                    col_h1, col_h2 = st.columns([4, 1])
                    col_h1.write(f"📍 **{h['name']}** - {h['desc']}")
                    if col_h2.button("Usuń", key=f"del_hotspot_{idx}", type="secondary"):
                        hotspots.pop(idx)
                        radar_data["hotspots"] = hotspots
                        with open(radar_file, "w", encoding="utf-8") as f:
                            json.dump(radar_data, f, indent=4)
                        st.rerun()
            else:
                st.info("Mapa jest czysta.")

            st.markdown("---")
            st.markdown("#### ➕ Dodaj nowe ognisko zapalne")

            # Pomocniczy słownik z koordynatami, żeby admin nie musiał szukać w Google
            PREDEFINED_LOCATIONS = {
                "Bliski Wschód (Izrael / Iran)": {"lat": 31.0, "lon": 45.0},
                "Morze Czerwone (Jemen)": {"lat": 15.0, "lon": 41.0},
                "Tajwan / Morze Południowochińskie": {"lat": 23.5, "lon": 121.0},
                "Waszyngton (USA)": {"lat": 38.9, "lon": -77.0},
                "Ukraina / Rosja": {"lat": 50.0, "lon": 35.0},
                "Frankfurt (EBC)": {"lat": 50.1, "lon": 8.6},
                "Londyn (BoE)": {"lat": 51.5, "lon": -0.1},
                "Inne (Wpisz ręcznie)": {"lat": 0.0, "lon": 0.0}
            }

            loc_choice = st.selectbox("Wybierz region (lub podaj ręcznie):", list(PREDEFINED_LOCATIONS.keys()))

            c1, c2, c3 = st.columns(3)
            with c1:
                custom_name = st.text_input("Wyświetlana nazwa:", value=loc_choice if "Inne" not in loc_choice else "")
            with c2:
                lat = st.number_input("Lat (Szerokość):", value=PREDEFINED_LOCATIONS[loc_choice]["lat"])
            with c3:
                lon = st.number_input("Lon (Długość):", value=PREDEFINED_LOCATIONS[loc_choice]["lon"])

            desc = st.text_input("Krótki opis ryzyka (np. Wzrost napięcia po oświadczeniu...)")

            if st.button("📍 Dodaj do mapy"):
                if custom_name and desc:
                    new_hotspot = {"name": custom_name, "lat": lat, "lon": lon, "desc": desc}
                    radar_data["hotspots"] = radar_data.get("hotspots", [])
                    radar_data["hotspots"].append(new_hotspot)

                    with open(radar_file, "w", encoding="utf-8") as f:
                        json.dump(radar_data, f, indent=4)
                    st.success("Ognisko dodane do mapy!")
                    st.rerun()
                else:
                    st.warning("Podaj nazwę i krótki opis.")

    # ==========================================
    # SEKCJA NEWSÓW
    # ==========================================
    if os.path.exists(news_file):
        with open(news_file, "r", encoding="utf-8") as f:
            try:
                news_list = json.load(f)
            except json.JSONDecodeError:
                news_list = []
    else:
        news_list = []

    with st.expander("📰 Zarządzaj Komunikatami Rynkowymi"):
        st.markdown("#### ➕ Dodaj nowy komunikat")
        title = st.text_input("Tytuł / Nagłówek komunikatu:")
        content = st.text_area("Treść / Analiza (rozwinięcie):")

        if st.button("Publikuj News"):
            if title and content:
                new_news = {
                    "id": datetime.now().strftime("%Y%m%d%H%M%S"),
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "title": title,
                    "content": content
                }
                news_list.insert(0, new_news)

                with open(news_file, "w", encoding="utf-8") as f:
                    json.dump(news_list, f, indent=4)
                st.success("Komunikat opublikowany!")
                st.rerun()
            else:
                st.warning("Musisz podać zarówno Tytuł, jak i Treść.")

        st.markdown("---")
        st.markdown("#### 📂 Opublikowane komunikaty")
        if news_list:
            for idx, item in enumerate(news_list):
                col1, col2 = st.columns([4, 1])
                col1.write(f"**{item['title']}** ({item['date']})")
                if col2.button("Usuń", key=f"del_news_{item['id']}", type="secondary"):
                    news_list.pop(idx)
                    with open(news_file, "w", encoding="utf-8") as f:
                        json.dump(news_list, f, indent=4)
                    st.rerun()
        else:
            st.info("Brak aktywnych komunikatów.")

    # ==========================================
    # SEKCJA RAPORTÓW PDF
    # ==========================================
    with st.expander("📄 Zarządzaj Raportami PDF"):
        pdf_path = "data/raport.pdf"
        pdf_ts = get_file_info(pdf_path)
        if pdf_ts:
            st.info(f"Ostatnia publikacja raportu: {pdf_ts}")
        else:
            st.write("Aktualnie brak wgranego raportu PDF.")

        st.markdown("---")
        pdf = st.file_uploader("Wgraj nowy raport geopolityczny / audyt", type="pdf")

        col3, col4 = st.columns(2)
        with col3:
            if st.button("Zapisz i Opublikuj PDF"):
                if pdf:
                    with open(pdf_path, "wb") as f:
                        f.write(pdf.getbuffer())
                    st.success(f"Raport '{pdf.name}' został opublikowany!")
                    st.rerun()
                else:
                    st.error("Najpierw wybierz plik PDF z dysku.")
        with col4:
            if os.path.exists(pdf_path):
                if st.button("❌ USUŃ AKTUALNY RAPORT", type="secondary"):
                    try:
                        os.remove(pdf_path)
                        st.success("Raport został usunięty z portalu.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Wystąpił błąd podczas usuwania: {e}")