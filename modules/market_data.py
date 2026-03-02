import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import ssl
import certifi

# NAPRAWA SSL DLA MACOS - Bez tego yfinance zwraca puste dane na Macu
ssl_context = ssl.create_default_context(cafile=certifi.where())


def get_live_rates():
    # Poprawiono ticker GBPPLN=X (usunięto nadmiarowe 'P')
    pairs = {
        "EURPLN=X": "EUR/PLN",
        "USDPLN=X": "USD/PLN",
        "CHFPLN=X": "CHF/PLN",
        "EURUSD=X": "EUR/USD",
        "GBPPLN=X": "GBP/PLN"
    }
    results = []

    for ticker, name in pairs.items():
        try:
            # Pobieramy dane 1mo/1d dla stabilności wskaźników zmiany
            data = yf.download(ticker, period="1mo", interval="1d", progress=False)

            if not data.empty:
                # Obsługa Multi-Index dla nowych wersji yfinance
                if isinstance(data.columns, pd.MultiIndex):
                    data.columns = data.columns.get_level_values(0)

                last = data['Close'].iloc[-1]
                prev = data['Close'].iloc[-2]
                change = ((last - prev) / prev) * 100
                results.append({"Para": name, "Kurs": float(last), "Zmiana": float(change)})
        except Exception as e:
            print(f"Błąd dla {ticker}: {e}")
            continue

    return pd.DataFrame(results)


def get_chart_of_day(pair_name):
    ticker_map = {
        "EUR/PLN": "EURPLN=X",
        "USD/PLN": "USDPLN=X",
        "GBP/PLN": "GBPPLN=X",
        "CHF/PLN": "CHFPLN=X"
    }
    ticker = ticker_map.get(pair_name, "EURPLN=X")

    # Zmieniamy na 7 dni i interwał 1h - najbardziej stabilny dla par z PLN
    df = yf.download(ticker, period="7d", interval="1h", progress=False)

    if df.empty:
        return None

    # Obsługa Multi-Index (ważne, by candlestick widział kolumny)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        increasing_line_color='#64ffda',  # Kolorystyka Black Stag
        decreasing_line_color='#ff4b4b'
    )])

    fig.update_layout(
        template="plotly_dark",
        height=350,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis_rangeslider_visible=False,
        paper_bgcolor='rgba(0,0,0,0)',  # Przezroczyste tło dla lepszego wtopienia w UI
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig