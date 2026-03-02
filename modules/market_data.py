import yfinance as yf
import pandas as pd
import plotly.graph_objects as go


def get_live_rates():
    # Używamy tickerów z końcówką =X dla Yahoo Finance
    pairs = {"EURPLN=X": "EUR/PLN", "USDPLN=X": "USD/PLN", "CHFPLN=X": "CHF/PLN", "EURUSD=X": "EUR/USD",
             "GBPPPLN=X": "GBP/PLN"}
    results = []
    for ticker, name in pairs.items():
        try:
            # Pobieramy dane z ostatniego miesiąca, żeby mieć pewność ciągłości
            data = yf.download(ticker, period="1mo", interval="1d", progress=False)
            if not data.empty:
                last = data['Close'].iloc[-1]
                prev = data['Close'].iloc[-2]
                change = ((last - prev) / prev) * 100
                results.append({"Para": name, "Kurs": float(last), "Zmiana": float(change)})
        except:
            continue
    return pd.DataFrame(results)


def get_chart_of_day(pair_name):
    # Mapowanie nazw na tickery
    ticker_map = {"EUR/PLN": "EURPLN=X", "USD/PLN": "USDPLN=X"}
    ticker = ticker_map.get(pair_name, "EURPLN=X")

    # Pobieramy dane 1-godzinne z ostatnich 7 dni (bardziej stabilne niż 15m)
    df = yf.download(ticker, period="7d", interval="1h", progress=False)
    if df.empty: return None

    fig = go.Figure(
        data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
    fig.update_layout(template="plotly_dark", height=350, margin=dict(l=0, r=0, t=0, b=0),
                      xaxis_rangeslider_visible=False)
    return fig