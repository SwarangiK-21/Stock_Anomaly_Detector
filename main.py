import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# --- 1. SET UP THE WEBPAGE ---
st.set_page_config(page_title="Stock Anomaly Detector", layout="wide")
st.title("📈 Real-Time Stock Anomaly Detector")

# --- 2. SIDEBAR ---
st.sidebar.header("Settings")
ticker = st.sidebar.text_input("Enter Stock Ticker", value="AAPL")

# --- 3. GET DATA (The "Sturdy" Version) ---
@st.cache_data
def get_data(ticker_symbol):
    try:
        # We use period="2y" because it's more stable on Cloud than specific dates
        data = yf.download(ticker_symbol, period="2y")
        
        # Check if data is empty
        if data.empty:
            st.error("⚠️ Yahoo Finance returned empty data. The ticker might be wrong.")
            return None

        # Fix for the "MultiIndex" bug (Common in 2025)
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
            
        return data

    except Exception as e:
        # This will print the EXACT error on the screen so we can fix it
        st.error(f"❌ Connection Error: {e}")
        return None

df = get_data(ticker)

# --- 4. THE LOGIC ---
if df is not None:
    # Math: Average & Standard Deviation
    window = 20
    df['Moving_Avg'] = df['Close'].rolling(window=window).mean()
    df['Std_Dev'] = df['Close'].rolling(window=window).std()
    df['Z_Score'] = (df['Close'] - df['Moving_Avg']) / df['Std_Dev']
    
    # Identify Anomalies
    df['Anomaly'] = df['Z_Score'].apply(lambda x: abs(x) > 3)
    anomalies = df[df['Anomaly'] == True]

    # --- 5. VISUALIZATION ---
    st.subheader(f"Price Analysis: {ticker}")
    
    # Graph
    fig = px.line(df, x=df.index, y='Close', title=f"{ticker} Price Trend")
    
    # Add Red Dots
    if not anomalies.empty:
        fig.add_scatter(x=anomalies.index, y=anomalies['Close'], 
                        mode='markers', marker=dict(color='red', size=10), 
                        name='Anomaly Detected')
    
    st.plotly_chart(fig, use_container_width=True)

    # Table
    if not anomalies.empty:
        st.write(f"⚠️ Found {len(anomalies)} anomalies in the last 2 years.")
        st.dataframe(anomalies[['Close', 'Z_Score']].tail(5))
    else:
        st.success("✅ Market looks normal (No anomalies found).")