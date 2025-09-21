import yfinance as yf
import pandas as pd
import ta
import numpy as np

# ========== CONFIG ==========
STOCK = "ICICIBANK.NS"
PERIOD = "6mo"
INTERVAL = "1d"

# Enable/Disable Tools
TOOLS = {
    "RSI": True,
    "MACD": True,
    "EMA": True,
    "Bollinger": True,
    "ATR": True,
    "ML_Predictor": False  # Turn on later if needed
}

# ========== FETCH DATA ==========
def fetch_data(stock, period, interval):
    df = yf.download(stock, period=period, interval=interval)
    df.dropna(inplace=True)
    return df

# ========== STRATEGY TOOLS ==========
def apply_indicators(df):
    if TOOLS["RSI"]:
        df["RSI"] = ta.momentum.RSIIndicator(df["Close"]).rsi()

    if TOOLS["MACD"]:
        macd = ta.trend.MACD(df["Close"])
        df["MACD"] = macd.macd()
        df["MACD_Signal"] = macd.macd_signal()

    if TOOLS["EMA"]:
        df["EMA20"] = ta.trend.EMAIndicator(df["Close"], window=20).ema_indicator()
        df["EMA50"] = ta.trend.EMAIndicator(df["Close"], window=50).ema_indicator()

    if TOOLS["Bollinger"]:
        bb = ta.volatility.BollingerBands(df["Close"])
        df["BB_High"] = bb.bollinger_hband()
        df["BB_Low"] = bb.bollinger_lband()

    if TOOLS["ATR"]:
        df["ATR"] = ta.volatility.AverageTrueRange(df["High"], df["Low"], df["Close"]).average_true_range()

    return df

# ========== SIGNAL GENERATOR ==========
def generate_signals(df):
    df["Signal"] = ""

    for i in range(1, len(df)):
        buy = False
        sell = False

        # RSI
        if TOOLS["RSI"]:
            if df["RSI"].iloc[i] < 30:
                buy = True
            elif df["RSI"].iloc[i] > 70:
                sell = True

        # MACD
        if TOOLS["MACD"]:
            if df["MACD"].iloc[i] > df["MACD_Signal"].iloc[i]:
                buy = True
            elif df["MACD"].iloc[i] < df["MACD_Signal"].iloc[i]:
                sell = True

        # EMA
        if TOOLS["EMA"]:
            if df["EMA20"].iloc[i] > df["EMA50"].iloc[i]:
                buy = True
            elif df["EMA20"].iloc[i] < df["EMA50"].iloc[i]:
                sell = True

        if buy:
            df.loc[df.index[i], "Signal"] = "BUY"
        elif sell:
            df.loc[df.index[i], "Signal"] = "SELL"
        else:
            df.loc[df.index[i], "Signal"] = "HOLD"

    return df

# ========== RUN APP ==========
if __name__ == "__main__":
    print(f"Fetching data for {STOCK}...")
    data = fetch_data(STOCK, PERIOD, INTERVAL)
    data = apply_indicators(data)
    data = generate_signals(data)

    print(data[["Close", "RSI", "MACD", "MACD_Signal", "EMA20", "EMA50", "Signal"]].tail(20))
