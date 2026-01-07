import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# --- 1. SET UP THE WEBPAGE ---
st.set_page_config(page_title="Stock Anomaly Detector", layout="wide")
st.title("📈 Real-Time Stock Anomaly Detector")

# --- 2. SIDEBAR (User Controls) ---
st.sidebar.header("Settings")
ticker = st.sidebar.text_input("Enter Stock Ticker", value="AAPL")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2024-01-01"))

# --- 3. GET DATA ---
@st.cache_data
def get_data(ticker_symbol, start):
    try:
        df = yf.download(ticker_symbol, start=start)
        # Fix for column names
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        return df
    except:
        return None

df = get_data(ticker, start_date)

if df is not None and not df.empty:
    # --- 4. THE MATH (DSA + Stats) ---
    window = 20
    df['Moving_Avg'] = df['Close'].rolling(window=window).mean()
    df['Std_Dev'] = df['Close'].rolling(window=window).std()
    df['Z_Score'] = (df['Close'] - df['Moving_Avg']) / df['Std_Dev']
    
    # Define Anomaly: If Z-Score is > 3 or < -3
    df['Anomaly'] = df['Z_Score'].apply(lambda x: abs(x) > 3)
    
    # Filter just the anomalies to show them
    anomalies = df[df['Anomaly'] == True]

    # --- 5. VISUALIZATION (The Graph) ---
    st.subheader(f"Price Chart for {ticker}")
    
    # Draw the main Blue Line
    fig = px.line(df, x=df.index, y='Close', title=f"{ticker} Stock Price")
    
    # Add Red Dots for Anomalies
    if not anomalies.empty:
        fig.add_scatter(x=anomalies.index, y=anomalies['Close'], 
                        mode='markers', marker=dict(color='red', size=10), 
                        name='Anomaly')
    
    st.plotly_chart(fig, use_container_width=True)

    # --- 6. DATA TABLE ---
    st.subheader("Detected Anomalies (Unusual Events)")
    if not anomalies.empty:
        st.write(anomalies[['Close', 'Z_Score']])
    else:
        st.write("No anomalies found in this period.")

else:
    st.error("Could not fetch data. Please check the Ticker symbol.")