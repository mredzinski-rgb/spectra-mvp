import streamlit as st
import yfinance as yf
import plotly.graph_objects as go


def show_fx_market():
    st.subheader("📊 Analiza Rynkowa Live")

    # Wybór par przez klienta
    selected_pairs = st.multiselect(
        "Wybierz pary walutowe do monitorowania:",
        ["EURPLN=X", "USDPLN=X", "CHFPLN=X", "GBPPLN=X", "EURUSD=X"],
        default=["EURPLN=X", "USDPLN=X"]
    )

    timeframe = st.selectbox("Interwał:", ["15m", "1h", "1d"], index=0)

    if selected_pairs:
        cols = st.columns(len(selected_pairs))
        for i, pair in enumerate(selected_pairs):
            with cols[i % len(cols)]:
                data = yf.download(pair, period="5d", interval=timeframe)
                fig = go.Figure(data=[go.Candlestick(
                    x=data.index, open=data['Open'], high=data['High'],
                    low=data['Low'], close=data['Close']
                )])
                fig.update_layout(title=f"Kurs {pair[:6]}", template="plotly_dark", height=350)
                st.plotly_chart(fig, use_container_width=True)